# 📌 Daily Task Tracker App

A full-stack desktop task management application built using *Flet (Frontend), FastAPI (Backend), and SQLite (Database)*.

---

## 🚀 Features

- Add, edit, delete tasks
- Mark tasks as completed
- Priority-based task organization
- Due date & time tracking
- Overdue task indication
- Clean desktop UI with Flet

---

## 🏗️ Architecture

Flet (Frontend)  
↓  
FastAPI (Backend)  
↓  
SQLite (Database)

---

## 📂 Project Structure

daily-task-tracker/  
│  
├── frontend/  
├── backend/  
├── requirements.txt  
├── README.md  
└── .gitignore  

---

## ⚙️ Setup

### 1. Clone repo
git clone <repo-link>  
cd daily-task-tracker  

### 2. Create virtual environment
python -m venv venv  
venv\Scripts\activate  

### 3. Install dependencies
pip install -r requirements.txt  

---

## ▶️ Run the App

### Start backend
uvicorn backend.main:app --reload  

### Run frontend
python frontend/app.py  

---

## 🖥️ Build Windows App (Optional)

flet build windows  

---

## 📌 Tech Stack

- Python  
- Flet  
- FastAPI  
- SQLite  

---

## 🎯 Status

✔ Core features completed  
✔ UI + Backend integrated  
✔ Ready for desktop build  
