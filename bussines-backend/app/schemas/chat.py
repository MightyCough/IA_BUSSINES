from pydantic import BaseModel
from typing import List,Optional,Dict,Any
from datetime import datetime
from uuid import UUID

class MessageCreate(BaseModel):
    content:str

class Message(BaseModel):
    id:UUID
    conversation_id:UUID
    role:str
    content:str
    metadata:Optional[Dict[str,Any]]={}
    created_at:datetime

class ConversationCreate(BaseModel):
    title:Optional[str] = "Nueva Conversación"

class Conversation(BaseModel):
    id:UUID
    user_id:UUID
    title:str
    is_archived:Optional[bool] = False
    created_at:datetime
    updated_at:datetime
    messages:Optional[List[Message]]=[]

class ChatResponse(BaseModel):
    conversation_id:UUID
    user_message:Message
    assistant_message:Message

