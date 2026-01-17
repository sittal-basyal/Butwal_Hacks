Project Name: Book Thrift

Short Description
Welcome to Book Thrift — a simple, friendly web app that helps people buy, sell, or donate books near them. It uses your browser's location to show nearby listings, supports photo uploads for condition images, and converts coordinates into readable addresses so everything is easy to find.

The Problem
- Waste and deforestation 
- Limited access to affordable books 

Key Features
- Quickly list books to sell, give away, or trade.
- See books that are physically close to you using geolocation.
- Upload photos (including camera capture on supported devices) to show book condition.
- Addresses are human-friendly thanks to reverse geocoding.

Built With
- Backend: FastAPI + async SQLAlchemy
- Database: PostgreSQL
- Frontend: Plain HTML, Tailwind CSS, and vanilla JavaScript


   
1. Create and activate a virtual environment:
   - macOS / Linux:
     bash
     python -m venv venv
     source venv/bin/activate
     
   - Windows (PowerShell):
     powershell
     python -m venv venv
     .\venv\Scripts\Activate.ps1
     
2. Install dependencies:
   bash
   pip install -r requirements.txt
   

Configuration
1. Create a .env file in the project root.
2. Add your database URL and a secret key, for example:
   properties
   DATABASE_URL=postgresql+asyncpg://postgres:password@localhost/bookthrift_db
   SECRET_KEY=supersecretkey
   
   Replace postgres:password and supersecretkey with values that match your environment.

Run the app
1. Start the FastAPI server:
   bash
   uvicorn app.main:app --reload
   
2. Open the web UI at http://localhost:8000

API docs
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

Team Members
Sittal Basyal (github/sittal-basyal)
Rohit Nyaupane  (github/rohit-496)
Sandesh Aryal (github/Sandesh-91)