# Education Site Admin Tools

This repository contains **partial admin tools** built as an extension to a main education platform. It provides backend management capabilities for key data modules using **Django** and **PostgreSQL**.

---

## Features

- **Django Admin Panel** access for viewing and managing data
- **JSON-based import/export** for:
  - Tutors
  - Schools
  - Courses
- **Data reset erasing & formatting** tools (on-demand erase)
- **Local development server** with live reload

---

## Prerequisites

- **Python 3.8+**
- **PostgreSQL** (running locally or remotely)
- Django project with configured database

> **Note**: A running PostgreSQL instance is **required**. Update `settings.py` with your database credentials.

---

## Quick Start

1. **Clone & install dependencies**
   pip install -r requirements.txt
