from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes.math_routes import router as math_router
from services.dspy_module import init_dspy_optimizer
import os
app = FastAPI(title="Math Routing Agent")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# Initialize DSPy optimizer with Groq API key
GROQ_API_KEY = "YOUR-API-KEY"
init_dspy_optimizer(GROQ_API_KEY)

app.include_router(math_router, prefix="/api")

@app.get("/")
def read_root():
    return {"message": "Math Routing Agent API"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
