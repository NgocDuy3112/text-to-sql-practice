from enum import Enum
from pydantic import BaseModel, Field


class MESSAGE_TYPE(Enum):
    USER = 0
    ASSISTANT = 1
    SYSTEM = 2


class ChatbotMessage(BaseModel):
    type: MESSAGE_TYPE = Field(description="Loại tin nhắn: người dùng, hệ thống, trợ lý.")
    content: str = Field(description="Nội dung tin nhắn.")
        
    @classmethod
    def from_data(cls, data: dict) -> "ChatbotMessage":
        role = data.get('role', 'user')
        content = data.get('content', '')
        
        if role == 'user':
            cls_type = MESSAGE_TYPE.USER
        elif role == 'assistant':
            cls_type = MESSAGE_TYPE.ASSISTANT
        elif role == 'system':
            cls_type = MESSAGE_TYPE.SYSTEM
        else:
            cls_type = MESSAGE_TYPE.USER
        
        return cls(type=cls_type, content=content)