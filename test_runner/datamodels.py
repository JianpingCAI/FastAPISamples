from pydantic import BaseModel


class TestRunner(BaseModel):
    ip: str
    capabilities: dict
