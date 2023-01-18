from pydantic import BaseModel, Field


class MessageIn(BaseModel):
    review_uuid: str
    review_text: str
