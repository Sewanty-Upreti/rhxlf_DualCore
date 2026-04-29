import uuid
from datetime import datetime
from sqlalchemy import Column, String, Integer, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from database import Base

def gen_uuid():
    return str(uuid.uuid4())

class User(Base):
    __tablename__ = "users"
    id         = Column(String, primary_key=True, default=gen_uuid)
    email      = Column(String, unique=True, nullable=False)
    role       = Column(String, default="student")
    created_at = Column(DateTime, default=datetime.utcnow)
    profile    = relationship("StudentProfile", back_populates="user", uselist=False)

class StudentProfile(Base):
    __tablename__ = "student_profiles"
    id              = Column(String, primary_key=True, default=gen_uuid)
    user_id         = Column(String, ForeignKey("users.id"), nullable=False)
    name            = Column(String, nullable=False)
    readiness_score = Column(Integer, default=0)
    updated_at      = Column(DateTime, default=datetime.utcnow)
    user        = relationship("User", back_populates="profile")
    skills      = relationship("SkillProgress", back_populates="student")
    enrollments = relationship("CourseEnrollment", back_populates="student")

class SkillProgress(Base):
    __tablename__ = "skill_progress"
    id          = Column(String, primary_key=True, default=gen_uuid)
    student_id  = Column(String, ForeignKey("student_profiles.id"), nullable=False)
    skill_name  = Column(String, nullable=False)
    level       = Column(Integer, default=1)
    recorded_at = Column(DateTime, default=datetime.utcnow)
    student = relationship("StudentProfile", back_populates="skills")

class CourseEnrollment(Base):
    __tablename__ = "course_enrollments"
    id          = Column(String, primary_key=True, default=gen_uuid)
    student_id  = Column(String, ForeignKey("student_profiles.id"), nullable=False)
    course_name = Column(String, nullable=False)
    status      = Column(String, default="enrolled")
    score       = Column(Integer, default=0)
    enrolled_at = Column(DateTime, default=datetime.utcnow)
    student = relationship("StudentProfile", back_populates="enrollments")