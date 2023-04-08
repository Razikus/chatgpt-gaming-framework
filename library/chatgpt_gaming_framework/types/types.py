import pydantic
from typing import List

class Conversation(pydantic.BaseModel):
    role: str
    content: str

class ConversationList(pydantic.BaseModel):
    conversations: List[Conversation]