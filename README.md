# LLM-PromptCraft

HW10 Technical Prototype — a 10-minute interactive lesson that teaches the
**RCTF** framework (Role / Context / Task / Format) for writing effective LLM
prompts, followed by a 4-question quiz.

## Tech Stack
- **Backend:** Flask (Python)
- **Frontend:** HTML + jQuery + Bootstrap 5
- **Data:** JSON (`data/lessons.json`) — not hard-coded into templates

## Running Locally

```bash
pip install -r requirements.txt
python app.py
```

Then open http://127.0.0.1:5000

## Routes

| Route                  | Method | Owner       | Purpose                              |
|------------------------|--------|-------------|--------------------------------------|
| `/`                    | GET    | Part 1      | Home / Welcome                       |
| `/start`               | POST   | Part 1      | Records start time, enters lesson 1  |
| `/learn/<n>`           | GET    | Part 1      | Renders lesson n (1–5)               |
| `/api/build-prompt`    | POST   | Part 1      | Stores user's Lesson 5 RCTF picks    |
| `/api/state`           | GET    | Part 1      | Debug — dumps stored user activity   |
| `/quiz`                | GET    | Part 2 stub | Quiz intro                           |
| `/quiz/<n>`            | GET    | Part 2 stub | Quiz question n (1–4)                |
| `/quiz/result`         | GET    | Part 2 stub | Quiz result                          |

Part 2 routes currently render placeholders so the prototype is click-through
complete. Vishal / Yve / Eric own the real quiz implementation.

## Project Structure

```
LLM-PromptCraft/
├── app.py                 # Flask routes + in-memory user state
├── data/
│   └── lessons.json       # All lesson copy & interactive data
├── templates/
│   ├── base.html          # Shared shell (navbar, Bootstrap, jQuery)
│   ├── home.html          # Welcome page
│   ├── learn.html         # Single data-driven lesson renderer
│   └── quiz_stub.html     # Placeholder for Part 2 pages
├── static/
│   ├── css/styles.css     # Hand-rolled styles on top of Bootstrap
│   └── js/main.js         # Lesson 5 Build-A-Prompt interactivity (jQuery)
├── requirements.txt
└── README.md
```

## HW10 Job Responsibility Mapping

| Person   | Part 1 role             | Part 2 role             |
|----------|-------------------------|-------------------------|
| Shubham  | **Implementing the UI** | Testing click-through   |
| Vishal   | Testing click-through   | Architecting the data   |
| Eric     | Architecting the data   | Implementing the UI     |
| Yve      | Testing click-through   | Implementing the UI     |

## HW10 Requirement Checklist (Part 1)

- [x] Flask backend + HTML/JS/jQuery/Bootstrap frontend
- [x] Home screen with a Start button (`POST /start`)
- [x] Backend stores user choices on every page (`USER_STATE` in `app.py`)
- [x] Lesson data lives in JSON, templates render it — nothing hard-coded
- [x] `/learn/<n>` route with variable lesson number
- [x] Every page shows data, has a CTA, advances to the next page
- [x] Single-user prototype (per requirement #8)

## Notes for Teammates

- Lesson copy is in `data/lessons.json` — edit there, no template changes
  needed.
- Part 2 stubs live in `app.py` under the big comment banner. Swap those
  routes for real quiz implementations and wire in quiz data under a new
  `data/quiz.json` (or extend `lessons.json`).
- `GET /api/state` is handy for confirming Part 2 is storing answers the
  same way Part 1 does.
