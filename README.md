## Perfume Compound AI (FastAPI)

### Setup
1. Create `.env` from template:
   ```bash
   cp .env.example .env
   # edit GROQ_API_KEY and GROQ_MODEL
   ```

2. Install dependencies (user site if venv unavailable):
   ```bash
   pip install -r requirements.txt --user
   ```

3. Run the server:
   ```bash
   python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
   ```

### Key endpoints
- `POST /ingredients/bulk_upsert`
- `GET /ingredients?q=`
- `POST /compounds`
- `GET /compounds/{id}`
- `PUT /compounds/{id}`
- `POST /analyses/run/{compound_id}`
- `GET /analyses/by_compound/{compound_id}`

### Example payloads
- Create compound:
  ```json
  {
    "name": "Citrus Amber Test",
    "description": "experiment",
    "items": [
      {"ingredient_name": "Bergamot Oil", "percentage": 15},
      {"ingredient_name": "Limonene", "percentage": 10},
      {"ingredient_name": "Hedione", "percentage": 25},
      {"ingredient_name": "Iso E Super", "percentage": 30},
      {"ingredient_name": "Ambroxan", "percentage": 5},
      {"ingredient_name": "Patchouli Oil", "percentage": 3}
    ]
  }
  ```

- Trigger analysis:
  ```
  POST /analyses/run/1
  ```

### Notes
- SQLite by default; switch to Postgres by setting `DATABASE_URL`.
- Analysis returns structured JSON suitable for UI rendering.
- All compliance outputs are advisory only.