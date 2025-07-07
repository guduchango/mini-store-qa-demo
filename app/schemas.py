from pydantic import BaseModel

class Query(BaseModel):
    ask: str