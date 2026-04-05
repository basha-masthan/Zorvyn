# Finance Data Processing API

A clean, role-based backend for managing financial records and dashboard summaries.

## Tech Stack
- **Framework**: FastAPI
- **Database**: SQLite (via SQLModel/SQLAlchemy)
- **Security**: JWT Authentication (python-jose + passlib[bcrypt])
- **Validation**: Pydantic v2

## Quick Start

1. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Run the server**:
   ```bash
   python run.py
   ```
   *Note: This will automatically create the database and seed it with starter users.*

## User Roles
- **Admin**: Full CRUD on users and records.
- **Analyst**: Access to dashboard summaries and record viewing.
- **Viewer**: Read-only access to records.

## Authentication
Use the `/api/v1/login/access-token` endpoint (via Swagger Docs at `/docs`) to log in and receive a JWT token. This token should be passed in the `Authorization: Bearer <token>` header for protected routes.
