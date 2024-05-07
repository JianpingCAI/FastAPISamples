from pydantic import BaseModel


class Task(BaseModel):
    type: str
    name: str
    description: str
    shell_script: str
