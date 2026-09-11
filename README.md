# Digital Legal Metrology Portal

A full-stack SIH prototype for the digital lifecycle management of weighing and measuring instruments.

## Technology

- Backend: Python, Django, Django REST Framework
- Database: PostgreSQL on Supabase
- Authentication: JWT / SimpleJWT
- Frontend: Vite, HTML, CSS, Vanilla JavaScript
- Charts: Chart.js
- QR scanning: html5-qrcode
- Icons: Lucide

## Architecture

Owner → Instrument registration → permanent UID/QR → verification application → LMO review → GATC assignment → inspection → LMO decision → certificate → public QR verification.

The instrument UID remains permanent across re-verification and certificate renewal.

## Backend setup

```powershell
cd backend
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

Copy `.env.example` to `.env` and put your Supabase PostgreSQL connection string in `DATABASE_URL`.

Then:

```powershell
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

## Supabase

Use a PostgreSQL connection string from your Supabase project. Do not commit `.env` or real passwords to Git.

Example format:

```env
DATABASE_URL=postgresql://postgres:YOUR_PASSWORD@YOUR_HOST:5432/postgres
```

If the password contains URL-special characters, URL-encode them in the connection string.

## Frontend setup

```powershell
cd frontend
npm install
npm run dev
```

The Vite application runs at:

`http://localhost:5173`

The Django API runs at:

`http://127.0.0.1:8000`

## Roles

- OWNER: register instruments and submit applications
- LMO: review, assign, approve or reject applications
- GATC: conduct assigned inspections
- ADMIN: full administrative access

Use Django admin to create LMO/GATC users for a prototype.

## Important prototype notes

- Document files use Django media storage locally. Production deployment should use an object-storage service.
- Email/SMS reminders are not implemented as fake functionality.
- QR codes point to the public frontend verification route.
- Public verification intentionally excludes sensitive owner information.
