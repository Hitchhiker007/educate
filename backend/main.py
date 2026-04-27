from pydantic import BaseModel
from fastapi import FastAPI
from dotenv import load_dotenv
import os
from google import genai
import json

load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

client = genai.Client(api_key=api_key)
# this is a free tier friendly model

app = FastAPI()

INSTRUCTIONS = """ You are a coding tutor helping beginner Python students understand best practices.

The user has submitted this function:
{code}

Your job is to:
1. Identify what this function does and what libraries/patterns it uses
2. Find relevant best practices for those patterns
3. Compare the submitted code against those best practices
4. Return specific, beginner-friendly feedback with improvements

Respond ONLY in JSON. No markdown, no backticks, just raw JSON. with docs, summary, improvements
docs: list[str]
summary: str
improvements: list[str]

Example style:
# Best practice: Always handle exceptions when making HTTP requests
# This prevents your app from crashing on network failures
def fetch_user(url):
    ..."""

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
        prompt = INSTRUCTIONS.format(code=code_request.code_snippet)
        response = client.models.generate_content(
            # use flash latest to auto update whenever google release a new version and depreictaes
            # the old model
            model="gemini-flash-latest",
            contents=prompt
        )

        data = json.loads(response.text)

        return CodeResponse(docs=data["docs"], summary=data["summary"], improvements=data["improvements"])