from fastapi import FastAPI
from database import engine, Base
from routes.profile import router as profile_router

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Leapfrog Connect",
    version="1.0.0",
    description="Career Readiness Engine — Relay Hack x Leapfrog Connect Hackathon"
)

app.include_router(profile_router)

@app.get("/")
def root():
    return {
        "message": "Leapfrog Connect API is running",
        "docs": "/docs",
        "endpoints": [
            "POST /profile/",
            "GET  /profile/{student_id}",
            "GET  /profile/{student_id}/readiness-score",
            "POST /profile/{student_id}/skill",
            "GET  /profile/{student_id}/journey"
        ]
    }