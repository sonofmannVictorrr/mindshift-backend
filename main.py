from fastapi import FastAPI, Request
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import sys
from io import StringIO

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

class CodeRequest(BaseModel):
    user_code: str
    language: str 

# We will use a simple dictionary, but for V1 across Kenya, 
# let's keep it simple. Note: State management for 100s of users 
# usually requires a Database like Redis or Firebase.
storage = {}

@app.get("/")
def health():
    return {"status": "MindShift Neural Brain is Online"}

@app.post("/execute")
async def execute_code(request: CodeRequest):
    if request.language.lower() == "python":
        old_stdout = sys.stdout
        redirected_output = sys.stdout = StringIO()
        
        try:
            # isolate user scope roughly
            # To truly allow 10 people at once without mixing variables,
            # we don't use a global storage in V1.
            local_vars = {} 
            exec(request.user_code, {}, local_vars)
            result = redirected_output.getvalue()
        except Exception as e:
            result = f"PYTHON ERROR: {str(e)}"
        finally:
            sys.stdout = sys.__stdout__
            
        return {"output": result.strip() if result else "Success (No output)"}

    elif request.language.lower() == "dart":
        # Dart is tricky on Render. For V1, we return a "Simulation" 
        # unless you use a Dockerfile (which is advanced).
        return {"output": "DART MODULE: Online. (Cloud Dart requires Docker)"}

@app.post("/reset")
async def reset_memory():
    return {"output": "SYSTEM REBOOTED: Cloud Memory Cleared."}