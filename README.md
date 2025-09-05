# Koala Backend (FastAPI)

A modular FastAPI backend supporting **Koala**, a social networking and upskilling platform for blue‑collar workers.  
This backend provides REST APIs for user authentication, job posting and discovery, social feeds (posts, comments, likes, shares), referrals, upskilling videos and streaks, image uploads, profile management, and other services.  
The project is organized into routers, CRUD classes, models, and utilities for maintainable code.

## Features at a Glance

| Category | Functionality |
| --- | --- |
| **Authentication & Registration** | Login for applicants and company users; applicant and company registration validating uniqueness and hashing passwords. |
| **Company Information** | Retrieve company details by email. |
| **Health Check** | `/healthcheck` returns a status and message for monitoring. |
| **Image Uploads** | Upload applicant profile image, company user profile image, and company banner to AWS S3 and update records. |
| **User Management** | Get current user, update details, disable user, disable any user by ID, retrieve and update user bio, and create or update a full profile. |
| **Website Leads** | Capture leads from website forms for applicants and providers. |
| **Job Management & Discovery** | Create jobs, list all jobs, retrieve by ID, update, close, delete, and bookmark jobs. |
| **Job Application & User‑Job Relations** | Apply to a job, view count of applied jobs, list recent or all applied jobs, count applicants, list recent or all applicants, update applicant status, list matched jobs, fresher jobs and filter jobs by city, type, and salary. |
| **Master Data & Tags** | Fetch gig types, operational cities & areas, job categories, and social tags. |
| **Social Posts** | Create and update social posts, retrieve posts by ID or user, fetch all posts, job news, or additional feed. |
| **Social Actions** | Like/unlike posts, share posts, comment on posts, and report inappropriate posts. |
| **Comments** | Comments are handled via `/action/comment`, which accepts a post ID and comment text. |
| **Reporting** | Users can report a post for abuse or inappropriate content. |
| **Shares** | Sharing is implemented through `/action/share`. |
| **Followers & Groups** | Users can follow other users and groups can be created, listed, followed, and fetched by ID; posts can be filtered by tags or groups. |
| **Recommendation & Discovery** | Suggest users to follow based on company or social graph; filter posts by tags. |
| **Streaks & Leaderboards** | Streak features reward continuous learning and posting. Learning video actions update streaks. |
| **Upskilling & Learning** | Create/update/list learning categories and videos, record when users start and finish videos, and deliver recommendations. |
| **Referral (Lead Capture)** | Referral data captured through website leads for outreach. |

## Architecture

The backend is designed around FastAPI’s router‑based architecture with routers, models, schemas, crud, utils, and alembic migrations.

## Getting Started

```bash
git clone https://github.com/aashishgarg94/koalaBackend.git
cd koalaBackend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
alembic upgrade head
uvicorn app.main:app --reload
```

Swagger UI: [http://localhost:8000/docs](http://localhost:8000/docs)  
ReDoc: [http://localhost:8000/redoc](http://localhost:8000/redoc)

## Contribution

- Fork the repository
- Create a branch and make changes
- Commit with clear messages
- Open a Pull Request

## License

MIT License
