import uuid
from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models import User, StudentProfile, SkillProgress, CourseEnrollment
from schemas import ProfileCreateRequest, ProfileResponse, ReadinessResponse, SkillOut, CourseOut

router = APIRouter(prefix="/profile", tags=["Profile"])


# ── POST /profile ─────────────────────────────────────────────────────────────
@router.post("/", response_model=ProfileResponse)
def create_profile(data: ProfileCreateRequest, db: Session = Depends(get_db)):

    # Check duplicate email
    if db.query(User).filter(User.email == data.email).first():
        raise HTTPException(status_code=400, detail="Email already registered")

    # Create user
    user = User(id=str(uuid.uuid4()), email=data.email, role="student")
    db.add(user)
    db.flush()

    # Create profile
    profile = StudentProfile(
        id=str(uuid.uuid4()),
        user_id=user.id,
        name=data.name,
        readiness_score=0
    )
    db.add(profile)
    db.flush()

    # Add skills
    for s in data.skills:
        db.add(SkillProgress(
            id=str(uuid.uuid4()),
            student_id=profile.id,
            skill_name=s.skill_name,
            level=s.level
        ))

    # Add courses
    for c in data.courses:
        db.add(CourseEnrollment(
            id=str(uuid.uuid4()),
            student_id=profile.id,
            course_name=c,
            status="enrolled",
            score=0
        ))

    # Calculate initial score
    profile.readiness_score = _calc_score(data.skills, [])
    db.commit()
    db.refresh(profile)

    return _build_response(profile, user)


# ── GET /profile/{id} ─────────────────────────────────────────────────────────
@router.get("/{student_id}", response_model=ProfileResponse)
def get_profile(student_id: str, db: Session = Depends(get_db)):
    profile = db.query(StudentProfile).filter(StudentProfile.id == student_id).first()
    if not profile:
        raise HTTPException(status_code=404, detail="Student not found")
    return _build_response(profile, profile.user)


# ── GET /profile/{id}/readiness-score ─────────────────────────────────────────
@router.get("/{student_id}/readiness-score", response_model=ReadinessResponse)
def get_readiness(student_id: str, db: Session = Depends(get_db)):
    profile = db.query(StudentProfile).filter(StudentProfile.id == student_id).first()
    if not profile:
        raise HTTPException(status_code=404, detail="Student not found")

    skills      = profile.skills
    enrollments = profile.enrollments
    completed   = [e for e in enrollments if e.status == "completed"]

    avg_score   = sum(e.score for e in completed) / len(completed) if completed else 0
    avg_skill   = sum(s.level for s in skills) / len(skills) if skills else 0

    score = int((avg_skill / 3) * 100 * 0.6 + avg_score * 0.4)
    score = max(0, min(100, score))

    profile.readiness_score = score
    profile.updated_at = datetime.utcnow()
    db.commit()

    alert = None
    if score < 40:
        alert = f"⚠️ Low readiness score ({score}/100). Admin intervention recommended."

    top_skills = sorted(skills, key=lambda s: s.level, reverse=True)[:3]

    return ReadinessResponse(
        student_id=profile.id,
        name=profile.name,
        readiness_score=score,
        breakdown={
            "courses_enrolled": len(enrollments),
            "courses_completed": len(completed),
            "average_course_score": round(avg_score, 1),
            "average_skill_level": round(avg_skill, 1),
            "top_skills": [s.skill_name for s in top_skills],
            "trend": "improving" if score >= 50 else "needs_attention"
        },
        alert=alert
    )


# ── Helpers ───────────────────────────────────────────────────────────────────
def _calc_score(skills, enrollments):
    if not skills:
        return 0
    avg = sum(s.level for s in skills) / len(skills)
    return int((avg / 3) * 100 * 0.6)

def _build_response(profile, user):
    return ProfileResponse(
        id=profile.id,
        name=profile.name,
        email=user.email,
        readiness_score=profile.readiness_score,
        skills=[
            SkillOut(skill_name=s.skill_name, level=s.level, recorded_at=s.recorded_at)
            for s in profile.skills
        ],
        courses=[
            CourseOut(course_name=e.course_name, status=e.status, score=e.score, enrolled_at=e.enrolled_at)
            for e in profile.enrollments
        ]
    )