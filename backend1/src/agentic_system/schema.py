from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime


class FileUploadResponse(BaseModel):
    file_id: str
    filename: str
    file_size: int
    upload_time: datetime
    content_type: str
    message: str


class QuestionRequest(BaseModel):
    file_id: str
    question: str


class AgentResponse(BaseModel):
    file_id: str
    question: str
    answer: str
    response_time: datetime
    agent_type: str


class FileInfo(BaseModel):
    file_id: str
    filename: str
    file_size: int
    upload_time: datetime
    content_type: str


class ChatHistory(BaseModel):
    file_id: str
    conversations: List[dict]


class ChatMessage(BaseModel):
    question: str
    answer: str
    timestamp: datetime
    agent_type: str


class AgentInfo(BaseModel):
    agent_id: str
    name: str
    description: str
    capabilities: List[str]
    status: str = "active" 