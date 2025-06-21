# Telegram Django API Integration

A Django REST Framework project integrated with:

- User authentication (Login, Register, Profile)
- API Key + JWT-based access control
- Telegram Bot for user interaction
- Celery + Redis for background task execution

---

## 🔧 Project Features

1. **Django Project Setup**
   - Environment-based configuration
   - Secure production-ready `settings.py`

2. **Authentication APIs**
   - `register/` and `login/` (public endpoints, API key required)
   - `profile/` (protected endpoint, JWT required)

3. **Telegram Bot Integration**
   - Collects user info on `/start` command
   - Saves Telegram data to Django database

4. **Celery Integration**
   - Redis-based worker queue
   - Email trigger task after registration (example)

---

## 🚀 Getting Started

### 1️⃣ Clone the Repository

```bash
git clone https://github.com/lalitVerma2003/Telegram_Api.git
cd Telegram_Api
