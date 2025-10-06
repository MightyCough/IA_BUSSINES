from fastapi_mail import FastMail, MessageSchema, ConnectionConfig, MessageType
from pydantic import EmailStr
from typing import List 
import os
from pathlib import Path
import random 
import string 
from datetime import datetime, timedelta
import redis
import json
from app.core.config import settings


class EmailService:
    def __init__(self):
        self.conf = ConnectionConfig(
            MAIL_USERNAME=settings.MAIL_USERNAME,
            MAIL_PASSWORD=settings.MAIL_PASSWORD,
            MAIL_FROM=settings.MAIL_FROM,
            MAIL_PORT=settings.MAIL_PORT,
            MAIL_SERVER=settings.MAIL_SERVER,
            MAIL_STARTTLS=settings.MAIL_STARTTLS,
            MAIL_SSL_TLS=settings.MAIL_SSL,
            USE_CREDENTIALS=True,
            VALIDATE_CERTS=True,
            TEMPLATE_FOLDER=None  # evita error si no existe carpeta templates
        )

        self.fastmail = FastMail(self.conf)


        ##Redis para almacenar codigos temporales
        try:
            self.redis_client = redis.Redis(host='localhost',port=6379,db=0,decode_responses=True)
            self.redis_client.ping()
            self.use_redis = True
            print("Redis conectado para codigos de verificacion")
        except Exception as e:
            #Si no hay redis, usar diccionario en memoria (solo para desarrollo)
            self.verification_codes = {}
            self.use_redis = False
            print("Redis no disponible, usando memoria para codigos (solo desarrollo)", str(e))
        
    def generate_verification_code(self) ->str:
        """Generar codigo de 6 digitos"""

        return ''.join(random.choices(string.digits,k=6))
    
    async def send_verification_email(self,email:str,user_name:str)->str:
        """Enviar email de verificacion
        Retorna el codigo generado (para testing)"""

        try:
            #Genera el codigo
            code = self.generate_verification_code()
            #Guarda codigo de expiracion
            expiry = datetime.now() + timedelta(minutes=5)

            if self.use_redis:
                try:
                #Guardar en Redis con TTL
                    self.redis_client.setex(
                    f"verification_code:{email}",
                    300, #5 minutos
                    json.dumps({
                        "code":code,
                        "created_at":datetime.now().isoformat(),
                        "expires_at":expiry.isoformat()
                    })
                )
                except Exception as e:
                    print("Fallo Redis, usando memoria: ",str(e))
                    self.use_redis = False
                    self.verification_codes[email]={
                        "code":code,
                        "created_at":datetime.now(),
                        "expires_at":expiry
                    }
            else:
                #Guardar en memoria
                self.verification_codes[email]={
                    "code":code,
                    "created_at":datetime.now(),
                    "expires_at":expiry
                }

            #Crear mensaje de email
            html_content = f"""
            <!DOCTYPE html>
            <html>
            <head>
                <meta charset="UTF-8">
                <title>Verificación de Email - Asesor Empresarial IA</title>
                <style>
                    body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
                    .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
                    .header {{ background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 30px; text-align: center; border-radius: 10px 10px 0 0; }}
                    .content {{ background: #f9f9f9; padding: 30px; border-radius: 0 0 10px 10px; }}
                    .code-box {{ background: white; border: 2px dashed #667eea; padding: 20px; text-align: center; margin: 20px 0; border-radius: 8px; }}
                    .code {{ font-size: 32px; font-weight: bold; color: #667eea; letter-spacing: 8px; }}
                    .warning {{ color: #e53e3e; font-size: 14px; margin-top: 20px; }}
                    .footer {{ text-align: center; margin-top: 30px; color: #666; font-size: 12px; }}
                </style>
            </head>
            <body>
                <div class="container">
                    <div class="header">
                        <h1>🤖 Asesor Empresarial IA</h1>
                        <p>Verificación de tu cuenta</p>
                    </div>
                    <div class="content">
                        <h2>¡Hola {user_name}!</h2>
                        <p>Gracias por registrarte en nuestro Asesor Empresarial IA. Para completar tu registro, necesitamos verificar tu dirección de email.</p>
                        
                        <div class="code-box">
                            <p><strong>Tu código de verificación es:</strong></p>
                            <div class="code">{code}</div>
                        </div>
                        
                        <p>Ingresa este código en la aplicación para activar tu cuenta.</p>
                        
                        <div class="warning">
                            ⏰ <strong>Este código expira en 5 minutos.</strong><br>
                            🔒 Si no solicitaste este código, puedes ignorar este email.
                        </div>
                        
                        <p>¡Estamos emocionados de ayudarte con tu emprendimiento!</p>
                        
                        <p>Saludos,<br><strong>El equipo de Asesor Empresarial IA</strong></p>
                    </div>
                    <div class="footer">
                        <p>Este es un email automático, por favor no respondas a este mensaje.</p>
                    </div>
                </div>
            </body>
            </html>
            """

            #Enviar email
            message = MessageSchema(
                subject = "Codigo de verificacion - Asesor Empresarial IA",
                recipients = [email],
                body=html_content,
                subtype=MessageType.html
            )

            await self.fastmail.send_message(message)

            print(f"Email enviado a {email} con codigo {code}")
            return code #testing
        
        except Exception as e:
            print(f"Error enviando email : {str(e)}")
            raise Exception(f"Error enviando email de verificacion: {str(e)}")
    
    def verify_code(self, email: str, provided_code: str) -> bool:
        """Verificar código de verificación (NO limpiar aquí)"""
        try:
            if self.use_redis:
                stored_data = self.redis_client.get(f"verification_code:{email}")
                if not stored_data:
                    return False

                data = json.loads(stored_data)
                stored_code = data["code"]
                expires_at = datetime.fromisoformat(data["expires_at"])

            else:
                if email not in self.verification_codes:
                    return False

            data = self.verification_codes[email]
            stored_code = data["code"]
            expires_at = data["expires_at"]

            if datetime.now() > expires_at:
                return False  # expirado

            return provided_code == stored_code

        except Exception as e:
            print(f"Error verificando codigo: {str(e)}")
            return False

        
    def cleanup_code(self,email:str):
        """"Limpiar codigo usando o expirado"""
        try:
            if self.use_redis:
                self.redis_client.delete(f"verification_code:{email}")

            else:
                self.verification_codes.pop(email,None)
        except Exception as e:
            print(f"Error limpiendo codigo: {str(e)}")

    async def resend_verification_code(self,email:str,user_name:str) -> str:
        """"Reenviar codigo de verificacion"""
        #limpiar codigo anterior
        self.cleanup_code(email)

        #enviar nuevo codigo
        return await self.send_verification_email(email, user_name)
    
email_service = EmailService()
        







