# Koala Backend (FastAPI)

A modular FastAPI backend supporting **Koala**, a social networking and upskilling platform for blue‑collar workers.  
This backend provides REST APIs for user authentication, job posting and discovery, social feeds (posts, comments, likes, shares), referrals, upskilling videos and streaks, image uploads, profile management, and other services.  
The project is organized into routers, CRUD classes, models, and utilities for maintainable code.

---

## Features at a Glance

| Category | Functionality |
| --- | --- |
| **Authentication & Registration** | Login for applicants and company users (`POST /login`, `POST /login/company`) returning JWT tokens; applicant and company registration (`POST /register/applicant`, `POST /register/company`) validating uniqueness and hashing passwords. |
| **Company Information** | Retrieve company details by email via `POST /company/get_details`. |
| **Health Check** | `GET /healthcheck` returns a status and message for monitoring. |
| **Image Uploads** | Upload applicant profile image, company user profile image, and company banner to AWS S3 and update records (`POST /applicant_profile_image`, `POST /company_user_profile_image`, `POST /company_banner`). |
| **User Management** | Get current user, update details, disable account, manage bios and profiles (`/user/me`, `/user/update/me`, `/user/disable/me`, `/user/disable_user_by_id`, `/user/bio`, `/user/bio/update`, `/user/create_profile`). |
| **Website Leads** | Capture leads from website forms for applicants and providers via `POST /website/applicant` and `POST /website/provider`. |
| **Job Management & Discovery** | Create, list, retrieve, update, close, soft‑delete, and bookmark jobs (`/jobs/create`, `/jobs/all`, `/jobs/all/full_detail`, `/jobs/get/{job_id}`, `/jobs/update/{job_id}`, `/jobs/close/{job_id}`, `/jobs/delete/{job_id}`, `/jobs/save/{job_id}`). |
| **Job Application & User‑Job Relations** | Apply to jobs, track applied jobs, count applicants, update applicant status, view matched/fresher/filter jobs (`/job/apply`, `/user/jobs/*`, `/job/applicant/*`, `/jobs/user_op_jobs`, `/jobs/all_matched`, `/jobs/freshers_jobs`, `/jobs/all/filter`). |
| **Master Data & Tags** | Fetch gig types, operational cities & areas, job categories, and social tags (`/gigs`, `/op_cities`, `/op_area`, `/job/job_master`, `/social/tags`). |
| **Social Posts** | Create/update posts, retrieve posts by ID or user, fetch feeds and job news (`/create_post`, `/update_post`, `/post_by_post_id`, `/post_by_user_id`, `/all_posts`, `/job_news`, `/feed`). |
| **Social Actions** | Like/unlike, share, comment, or report posts (`/action/like`, `/action/share`, `/action/comment`, `/action/report`). |
| **Followers & Groups** | Follow/unfollow users and groups, create groups, list groups, fetch by ID (`/follow_user`, `/user_following`, `/user_followed`, `/create_group`, `/get_all_groups`, `/group_by_id`, `/follow_group`). |
| **Recommendation & Discovery** | Discover posts or users via tags, company, or graph (`/post_by_tags`, `/same_company_users`, `/users_to_follow`). |
| **Streaks & Leaderboards** | Track streaks for posting and learning (`/get_streak_count`, `/video_started`, `/video_finished`). |
| **Upskilling & Learning** | Manage learning categories and videos; track user progress; recommend videos (`/create_learning_category`, `/update_learning_category`, `/all_learning_categories`, `/create_learning_video`, `/update_learning_video`, `/all_learning_videos`, `/recommended_learning_videos`). |
| **Moderation** | Disable/hide posts (`POST /disable_post_by_post_id`). |

> **Note:** Exact request/response schemas are defined in `schemas/`. Explore the interactive docs at `/docs` (Swagger UI) for the authoritative contract.

---

## Architecture

**High‑level layout**

```
app/
  main.py                # FastAPI app, router includes, middlewares
  config.py              # Settings (env vars), CORS, etc.
  database.py            # SQLAlchemy/SQLModel engine + Session
  core/                  # Core services (auth, security, etc.)
  dao/                   # Data access abstractions (optional)
  models/                # ORM models: Users, Companies, Jobs, Posts, Groups, Learning, ...
  schemas/               # Pydantic models for request/response validation
  crud/                  # DB operations per domain (users, jobs, social, learning, ...)
  routers/
    jobs_routers/        # jobs, auth, company, healthcheck, images, job_user, master, register, user, website
    learning/            # learning categories, videos, progress
    social/              # posts, actions, groups, discovery
  utils/                 # helpers: JWT, password hashing, S3 uploads, pagination, etc.
alembic/                 # migrations
tests/                   # optional tests
```

**Design principles**
- **Modular routers** isolate domains (jobs, social, learning).
- **CRUD layer** keeps business logic near the database, keeping routes thin.
- **Pydantic schemas** ensure validation and consistent API contracts.
- **Stateless JWT auth** for applicants and company users.
- **S3 uploads** for profile images and banners.

---

## Getting Started

### 1) Clone the repository
```bash
git clone https://github.com/aashishgarg94/koalaBackend.git
cd koalaBackend
```

### 2) Create & activate a virtual environment
```bash
python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
```

### 3) Configure environment variables
Copy `.env.example` → `.env` and set values:

```ini
# Database
DATABASE_URL=postgresql+psycopg2://USER:PASSWORD@HOST:PORT/DBNAME

# Auth
SECRET_KEY=replace-with-strong-secret
ACCESS_TOKEN_EXPIRE_MINUTES=60

# AWS (for S3 uploads)
AWS_ACCESS_KEY_ID=your-access-key
AWS_SECRET_ACCESS_KEY=your-secret-key
AWS_S3_BUCKET=your-bucket-name
AWS_S3_REGION=ap-south-1

# CORS
CORS_ALLOW_ORIGINS=["http://localhost:3000","https://your-frontend.app"]
```

### 4) Run database migrations
```bash
alembic upgrade head
```

### 5) Start the server
```bash
uvicorn app.main:app --reload
```
- Swagger UI: `http://localhost:8000/docs`  
- ReDoc: `http://localhost:8000/redoc`

### 6) Run tests (if present)
```bash
pytest -q
```

---

## API Overview (Selected Endpoints)

### 🔐 Auth & Users
- `POST /login` — applicant login (JWT)  
- `POST /login/company` — company user login (JWT)  
- `POST /register/applicant` — register applicant  
- `POST /register/company` — register company user  
- `GET /user/me` — current authenticated user  
- `POST /user/update/me` — update own profile  
- `GET /user/disable/me` — self‑disable account  
- `GET /user/disable_user_by_id` — admin/company disable user by ID  
- `GET /user/bio` / `POST /user/bio/update` — view/update user bio  
- `POST /user/create_profile` — create a full profile (skills, resume, etc.)  

### 🏢 Company
- `POST /company/get_details` — company details by email  

### 🩺 Health
- `GET /healthcheck` — liveness check  

### 🖼️ Image Uploads
- `POST /applicant_profile_image` — upload applicant profile image to S3  
- `POST /company_user_profile_image` — upload company user image to S3  
- `POST /company_banner` — upload company banner to S3  

### 🌐 Website Leads
- `POST /website/applicant` — capture applicant lead  
- `POST /website/provider` — capture provider lead  

### 💼 Jobs
- `POST /jobs/create` — create a job (company auth)  
- `GET /jobs/all/full_detail` — list jobs with full detail  
- `GET /jobs/all` — paginated jobs list  
- `GET /jobs/get/{job_id}` — job by ID  
- `POST /jobs/update/{job_id}` — update a job  
- `GET /jobs/close/{job_id}` — close a job  
- `POST /jobs/delete/{job_id}` — soft delete job  
- `POST /jobs/save/{job_id}` — bookmark job  

#### Applicants & Matching
- `POST /job/apply` — apply to job  
- `GET /user/jobs/count` — count of applied jobs  
- `GET /user/jobs/recent` — recent applied jobs  
- `GET /user/jobs` — all applied jobs  
- `POST /job/applicant/count` — applicant count for a job  
- `GET /jobs/applicant/recent` — recent applicants  
- `POST /job/applicant` — list applicants  
- `POST /job/applicant/action` — update applicant status  
- `POST /jobs/user_op_jobs` — jobs for user’s operating prefs  
- `POST /jobs/all_matched` — matched jobs  
- `POST /jobs/freshers_jobs` — fresher jobs  
- `POST /jobs/all/filter` — filter by city, type, salary  

### 🧭 Master Data & Tags
- `GET /gigs` — gig types  
- `GET /op_cities` — operating cities  
- `GET /op_area` — operating areas  
- `GET /job/job_master` — job categories & master data  
- `GET /social/tags` — social tags  

### 🗣️ Social
#### Posts
- `POST /create_post` / `POST /update_post` — create/update post (text, files, tags, group)  
- `POST /post_by_post_id` — post by ID  
- `POST /post_by_user_id` — posts by user  
- `POST /all_posts` — all posts (paginated)  
- `POST /job_news` — job news feed  
- `POST /feed` — additional feed  

#### Actions
- `POST /action/like` — like/unlike  
- `POST /action/share` — share (e.g., WhatsApp; extensible)  
- `POST /action/comment` — add comment  
- `POST /action/report` — report post (abuse/inappropriate)  

#### Follows & Groups
- `POST /follow_user` — follow a user  
- `GET /user_following` — who the user follows  
- `POST /user_followed` — who follows the user  
- `POST /create_group` — create group  
- `GET /get_all_groups` — list groups  
- `POST /group_by_id` — group details  
- `POST /follow_group` — follow/unfollow group  

#### Discovery
- `POST /post_by_tags` — posts by tags  
- `POST /same_company_users` — users from same company  
- `POST /users_to_follow` — recommended users to follow  

#### Moderation
- `POST /disable_post_by_post_id` — disable/hide a post  

### 🎯 Streaks & Learning
- `POST /get_streak_count` — current streaks (posting, learning)  
- `POST /video_started` / `POST /video_finished` — track learning progress  
- `POST /create_learning_category` / `POST /update_learning_category` / `POST /all_learning_categories`  
- `POST /create_learning_video` / `POST /update_learning_video` / `POST /all_learning_videos`  
- `POST /recommended_learning_videos` — recommendations  

---

## Auth, Security & Conventions

- **JWT**: Include `Authorization: Bearer <token>` for protected endpoints.  
- **Password hashing**: Handled in utils during registration.  
- **Roles**: Applicant vs Company user; route guards enforce access.  
- **Validation**: All requests validated via Pydantic schemas.  
- **File uploads**: Multipart form‑data; S3 keys stored on user/company records.  
- **Pagination**: Where applicable, pass `page`, `limit` (or equivalent) query params.  
- **Error model**: JSON with `detail` and/or validation errors (FastAPI default).  

---

## Local Development Tips

- Use **uvicorn** with `--reload` for hot‑reloading.  
- Add sample `.env` values for local S3 (or disable upload features during dev).  
- Prefer **conventional commits** (`feat:`, `fix:`, `docs:`, `refactor:` …).  
- Consider enabling **pre‑commit** (black, isort, ruff) for consistent style.  

---

## Contribution

1. Fork the repo.  
2. Create a feature branch:  
   ```bash
   git checkout -b feature/my-new-feature
   ```
3. Commit with conventional messages.  
4. Open a Pull Request describing your changes and rationale.  
5. Add tests & update docs where relevant.

---

## License

This project is licensed under the **MIT License**.
