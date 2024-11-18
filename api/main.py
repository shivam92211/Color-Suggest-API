from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.routers import single_suggestion, couple_suggestion

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(single_suggestion.router)
app.include_router(couple_suggestion.router)
