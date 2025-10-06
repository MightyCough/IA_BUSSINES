import asyncio
from dotenv import load_dotenv
import os
load_dotenv()  # carga /home/mightycough/Desktop/IA_bussines/bussines-backend/.env

from app.services.email_service import email_service

async def main():
    target = os.getenv("TEST_EMAIL_TO", "tu-correo-de-prueba@dominio.com")
    code = await email_service.send_verification_email(target, "Usuario Prueba")
    print("Código enviado (solo testing):", code)
    ok = email_service.verify_code(target, code)
    print("Verificación inmediata:", ok)

if __name__ == "__main__":
    asyncio.run(main())