# Leapfrog Connect — Career Readiness Engine
> Relay Hack x Leapfrog Connect Hackathon — Sprint 2: Design the Haddi

---

Problem Statement — Career Readiness Engine
1. The Core Problem
At Leapfrog Connect, mentors and admins do not have a clear way to understand how a trainee is actually progressing over time.
Students go through courses, build skills, and complete tasks, but all of this information exists in separate pieces. There is no single system that brings everything together to show a trainee’s overall growth.
Because of this, progress is seen only at specific moments, not as a continuous journey. Mentors can see what a student has done, but they cannot clearly see whether the student is improving, staying the same, or slowly falling behind.

3. Where the Problem Occurs
This issue appears throughout the entire trainee journey.
While students are learning, their skills may be improving or declining, but this change is not tracked in a meaningful way. During courses, scores are recorded, but they are not connected to long-term development.
By the time trainees reach the final stages, such as evaluation or placement, there is still no clear picture of their readiness. At that point, any gaps in learning or performance become visible, but much later than they should.

5. The Impact
The biggest consequence is that support comes too late.
Students who start struggling early are not identified in time, and they gradually lose engagement. Mentors are unable to step in when it would make the most difference. Admins are left making decisions based on final outcomes instead of continuous insight.
This also affects companies, as they receive candidates who may have completed training but are not fully prepared for real job requirements.
In the end, the system reacts after problems have already grown, instead of preventing them early.

6. Our Solution

A **Career Readiness Engine** — a backend API system that:

- Tracks each trainee's skills and courses over time
- Calculates a readiness score using a weighted formula
- Exposes a full growth journey so mentors can see progress, not just snapshots


## Part 1 — Design

### Data Backbone

```
User
 └── StudentProfile
       ├── SkillProgress (many — tracked over time with timestamps)
       └── CourseEnrollment (many)
             └── Course
```

| Table | Purpose |
|---|---|
| `users` | Auth identity — email, role (student / admin / company) |
| `student_profiles` | Core trainee record — name, readiness score |
| `skill_progress` | Each skill log entry with timestamp — tracks growth over time |
| `courses` | Available courses |
| `course_enrollments` | Tracks enrollment status and score per student per course |

**Time tracking is built in:**
- `skill_progress.recorded_at` — every skill update is a new row, not an overwrite
- `course_enrollments.enrolled_at` — when the student started the course
- `student_profiles.updated_at` — when the readiness score last changed

### API Architecture

| Method | Endpoint | Purpose |
|---|---|---|
| `POST` | `/profile/` | Create student profile with skills and courses |
| `GET` | `/profile/{id}` | Get full student profile |
| `GET` | `/profile/{id}/readiness-score` | Calculate score + trigger alert if low |
| `POST` | `/profile/{id}/skill` | Log a new skill level entry (growth tracking) |
| `GET` | `/profile/{id}/journey` | Full skill + course history over time |

### The Insight — What Decision Does This Create?

> The system alerts admins when a trainee's readiness score drops below 40/100, recommending immediate intervention.

The readiness score is calculated as:

```
Score = (avg course score × 0.4)
      + (avg skill level / 3 × 100 × 0.4)
      + (courses completed / 5 × 100 × 0.2)
```

This is not a dashboard. It is a decision trigger.

When a student's score is below 40, the API response includes:
```json
"alert": "⚠️ Low readiness score (32/100). Admin intervention recommended."
```

---

## Part 2 — Implementation

### Tech Stack

- **Python 3.13**
- **FastAPI** — API framework
- **SQLAlchemy** — ORM
- **SQLite** — Database
- **Uvicorn** — ASGI server
- **Pydantic** — Request/response validation

### Project Structure

```
leapfrog-connect/
├── main.py              # App entry point
├── database.py          # DB connection and session
├── models.py            # SQLAlchemy models (tables)
├── schemas.py           # Pydantic request/response schemas
├── requirements.txt     # Dependencies
└── routes/
    └── profile.py       # All API endpoints
```

### Setup & Run

```bash
# 1. Clone the repo
git clone 
cd leapfrog-connect

# 2. Create and activate virtual environment
python3 -m venv venv
source venv/bin/activate      # Mac/Linux
venv\Scripts\activate         # Windows

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run the server
uvicorn main:app --reload
```

Server runs at: `http://127.0.0.1:8000`

Interactive API docs: `http://127.0.0.1:8000/docs`

---


  "courses": ["Backend Fundamentals", "System Design"]
}
```



## What This System Does That Dashboards Cannot

| Weak System | Our System |
|---|---|
| Shows charts | Creates alerts |
| Snapshot of today | Tracks change over time |
| Admin manually checks | System flags automatically |
| Reacts after evaluation | Intervenes before it is too late |

---

*Built for Relay Hack x Leapfrog Connect Hackathon — Sprint 2*
