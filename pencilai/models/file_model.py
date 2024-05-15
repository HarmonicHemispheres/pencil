from pydantic import BaseModel

class File(BaseModel):
    name: str
    full_file_path: str
    content: str