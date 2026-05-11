# SGP – Système de Gestion de Projets

SGP (Système de Gestion de Projets) is a comprehensive project management application built with **Python** and **PyQt6**. It features a modern, sidebar-based navigation interface and a robust Role-Based Access Control (RBAC) system.

## 🚀 Features

- **Interactive Dashboard**: Get an overview of project status and key metrics.
- **Project Management**: Create, track, and manage complex projects.
- **Task Tracking**: Assign and monitor tasks within projects.
- **Team Collaboration**: Manage team members and roles (Admin, Project Manager, Team Member, Client, Management).
- **Resource Planning**: Integrated planning and scheduling tools.
- **Document Management**: Centralized storage for project-related documents.
- **Reporting**: Generate insightful reports on project progress and performance.
- **User Profiles**: Manage personal settings and information.

## 🛠️ Technology Stack

- **Frontend**: Python 3.x, PyQt6
- **Styling**: QSS (Qt Style Sheets) for a modern UI/UX.
- **Icons**: FontAwesome integration via `qtawesome`.
- **Database**: PostgreSQL (Schema included).
- **Logging**: Integrated application logging.

## 📋 Prerequisites

- Python 3.8+
- PostgreSQL
- Required Python packages:
  - `PyQt6`
  - `qtawesome`
  - `psycopg2` (or `psycopg2-binary`)

## ⚙️ Installation & Setup

1. **Clone the repository**:
   ```bash
   git clone https://github.com/amir-ai-bot/sgp-project.git
   cd sgp-project
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```
   *(Note: Ensure you have the necessary system libraries for PyQt6 and PostgreSQL.)*

3. **Database Setup**:
   - Create a PostgreSQL database named `sgp_db`.
   - Run the provided schema script:
     ```bash
     psql -d sgp_db -f sgp_postgresql_schema.sql
     ```
   - (Optional) Seed test data:
     ```bash
     python init_db.py
     python seed_test_data.py
     ```

4. **Configuration**:
   The application uses environment variables for sensitive database credentials. Set the following variables in your environment:
   - `DB_NAME` (default: `sgp_db`)
   - `DB_USER`
   - `DB_PASSWORD`
   - `DB_HOST` (default: `localhost`)
   - `DB_PORT` (default: `5432`)

## 🚦 How to Run

Execute the main entry point:
```bash
python main.py
```

## 🔐 Security & Privacy

This repository has been sanitized to remove all critical information, such as database passwords and local log files. Always use environment variables for production secrets.

---
*Developed by Yassin DHIBI (@amir-ai-bot)*
