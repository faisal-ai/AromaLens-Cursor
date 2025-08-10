from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .db import init_db
from .routers import ingredients, compounds, analyses

app = FastAPI(title="Perfume Compound AI", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
def on_startup() -> None:
    init_db()

app.include_router(ingredients.router, prefix="/ingredients", tags=["ingredients"])
app.include_router(compounds.router, prefix="/compounds", tags=["compounds"])
app.include_router(analyses.router, prefix="/analyses", tags=["analyses"])