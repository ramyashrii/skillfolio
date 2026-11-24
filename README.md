# skillfolio
# ROLEQUEST

**Track 4: Education, Skills and Jobs** | wHACKiest 2026

> AI can write the code. Can you prove you understand it?

## Problem
Students finish courses and certificates, but that doesn't show they can do
real work or adapt when requirements change. Employers can't tell claimed
skills from demonstrated ones.

## Our solution
ROLEQUEST is a simulated workplace where a student works on a real Python
project, gets a changed requirement, and must adapt their own solution
with the AI mentor locked. Hidden tests score both attempts, and the results
become an evidence page of what the student can do unaided.

## How it works
1. Student opens a task at a fictional company (Nexora Tech).
2. They fix a bug in a small Python project (TASK-001: The Broken API).
3. Hidden tests check the fix.
4. A changed requirement arrives. The mentor is locked.
5. Both attempts are compared and saved to an evidence page.

## What makes it different
- Work is verified by tests, not self-checked or AI-scored.
- The changed-requirement round with the mentor locked shows who understands
  the code and who only pasted a solution.
- Evidence links every skill claim to evaluated work.

## Tech stack
React + Vite, Tailwind CSS, Monaco Editor, Python + FastAPI, SQLite, pytest.
AI mentor: prewritten hints (local model planned).

## Current status
- [x] Documentation and design
- [ ] Mission workspace with code editor (in progress)
- [ ] Test runner and evaluation (in progress)
- [ ] Changed-requirement round
- [ ] Evidence page

This is a hackathon prototype. Student code execution is not
production-hardened yet. Planned: container isolation with no network and
resource limits.

## Run locally
```
# backend
cd backend
python -m venv venv
venv\Scripts\activate
pip install fastapi uvicorn
uvicorn main:app --reload

# frontend (new terminal)
cd frontend
npm install
npm run dev
```
Open http://localhost:5173

## Limitations (honest)
- One career path (Python backend) and a small set of hand-written missions.
- Mission quality depends on people writing and reviewing missions.
- Not yet validated with real students or employers.

## Team
[Name 1], [Name 2], ... | [College name]

## Links
Docs: [link] | Demo video: [add before the 27th]
