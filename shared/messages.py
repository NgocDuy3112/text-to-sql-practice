from enum import Enum
from pydantic import BaseModel, Field


class MESSAGE_TYPE(Enum):
    USER = 0
    ASSISTANT = 1
    SYSTEM = 2


class ChatbotMessage(BaseModel):
    type: MESSAGE_TYPE = Field(description="Loại tin nhắn: người dùng, hệ thống, trợ lý.")
    content: str = Field(description="Nội dung tin nhắn.")