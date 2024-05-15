from pydantic import BaseModel



class File(BaseModel):
    name: str
    full_path: str
    content: str



class Message(BaseModel):
    role: str
    content: str
    message_format: str