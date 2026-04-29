from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class SkillInput(BaseModel):
    skill_name: str
    level: int

class ProfileCreateRequest(BaseModel):
    name: str
    email: str
    skills: List[SkillInput] = []
    courses: List[str] = []

class SkillOut(BaseModel):
    skill_name: str
    level: int
    recorded_at: datetime
    model_config = {"from_attributes": True}

class CourseOut(BaseModel):
    course_name: str
    status: str
    score: int
    enrolled_at: datetime
    model_config = {"from_attributes": True}

class ProfileResponse(BaseModel):
    id: str
    name: str
    email: str
    readiness_score: int
    skills: List[SkillOut]
    courses: List[CourseOut]

class ReadinessResponse(BaseModel):
    student_id: str
    name: str
    readiness_score: int
    breakdown: dict
    alert: Optional[str] = None