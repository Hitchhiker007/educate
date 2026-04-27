from pydantic import BaseModel
from fastapi import FastAPI

app = FastAPI()

class CodeRequest(BaseModel):
        code_snippet: str

class CodeResponse(BaseModel):
        docs: list[str]
        summary: str
        improvements: list[str]

@app.get("/")
def read_root():
        return {"Hello": "World"}

@app.post("/educate")
def educate(code_request: CodeRequest):
        return CodeResponse(
            docs=["placeholder doc"],
            summary="placeholder summary",
            improvements=["placeholder improvement"]
        )