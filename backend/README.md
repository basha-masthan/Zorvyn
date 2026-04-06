# Finance Data Backend (Zorvyn)

## Assignment: Finance Data Processing and Access Control Backend
This project implements a secure, role-based backend designed for a finance dashboard. It handles financial records (income/expenses), provides aggregated analytics, and enforces access control across different user levels.

---

## 🚀 Key Features

- **RBAC (Role Based Access Control)**:
  - `Admin`: Full control over users and records.
  - `Analyst`: View-only access to records and full access to dashboard insights.
  - `Viewer`: Restricted access - can only see aggregated dashboard data.
- **Financial Analytics**: Custom endpoints for real-time calculation of net balance, trends, and category-wise spending.
- **Data Integrity**: Input validation via Pydantic (e.g., positive amounts, email validation).
- **Security**: JWT-based authentication with salted Bcrypt password hashing.
- **Persistence**: SQLite database using SQLModel for a clean relational mapping.
- **Auto-Seeding**: The application automatically seeds starter accounts and sample data on its first run for immediate testing.

---

## 🛠 Tech Stack

- **FastAPI**: Modern, high-performance web framework for Python.
- **SQLModel**: A wrapper around SQLAlchemy and Pydantic for streamlined DB operations.
- **JOSE / Passlib**: For secure token management and hashing.
- **Pydantic v2**: Next-gen data validation.

---

## 📖 API Documentation

Once the server is running, you can explore the interactive documentation:
- **Swagger UI**: [http://localhost:8000/docs](http://localhost:8000/docs)
- **ReDoc**: [http://localhost:8000/redoc](http://localhost:8000/redoc)

### Core Endpoints
- `POST /api/v1/login/access-token`: Authenticate and receive a JWT.
- `GET /api/v1/dashboard/summary`: (Viewers/Analysts/Admins) - Aggregated data and trends.
- `GET /api/v1/records/`: (Analysts/Admins) - List and filter transactions.
- `POST /api/v1/records/`: (Admins) - Create new entry.
- `GET /api/v1/users/`: (Admins) - User management.

---

## 🏁 Quick Start

1. **Setup Environment**:
   ```bash
   # Recommended: Create a virtualenv
   python -m venv venv
   .\venv\Scripts\activate
   ```

2. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the Application**:
   ```bash
   python run.py
   ```
   *The database will be initialized at `backend/finance.db` automatically.*

### Sample Accounts
The seeder creates these default accounts (Password = Username):
- `admin@example.com` (Full Access)
- `analyst@example.com` (Records + Dashboard)
- `viewer@example.com` (Dashboard only)

---

## 🧠 Design Decisions & Rationales

- **SQLite for Portability**: Chosen to ensure the project runs out-of-the-box without requiring a Postgres/MySQL installation, fitting the "simplified implementation" option.
- **SQLModel Integration**: By using SQLModel, the data models double as Pydantic schemas, reducing code duplication and ensuring that the DB schema is always in sync with API validation.
- **Stateless Auth**: JWT was used instead of sessions to make the backend horizontally scalable (ideal for a real-world scenario).
- **Filtering Logic**: Implemented `start_date` and `end_date` parameters to support the "weekly/monthly trends" requirement, allowing the client to request specific windows of data.
- **Error Handling**: Custom `RequireRole` dependency provides a centralized place for permission checks, ensuring "403 Forbidden" responses are consistent and clean.

---

## 🔮 Future Improvements (If time allowed)
- **Soft Delete**: Adding a `deleted_at` field to records to prevent accidental data loss.
- **Export to CSV**: An analyst tool to download transaction reports.
- **Audit Logs**: Tracking which admin modified which record for accountability.
- **Currency Support**: Handling multi-currency entries with real-time conversion rates.
