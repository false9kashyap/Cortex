# CORTEX - AI Resume Intelligence Engine

CORTEX is an AI-powered resume screening system that analyzes resumes against job descriptions and ranks candidates intelligently.

## Features

- Resume PDF Parsing
- AI Role Prediction
- Semantic Resume-JD Matching
- Candidate Ranking
- Match Score Generation
- FastAPI Backend
- React Frontend


## Tech Stack

### Frontend
- React
- Tailwind CSS
- Axios

### Backend
- FastAPI
- Python
- Machine Learning
- NLP


## API Endpoints

### Analyze Single Candidate

POST /predict


### Rank Multiple Candidates

POST /rank


## Run Backend

```bash
uvicorn app.main:app --reload