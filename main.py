from fastapi import FastAPI, Request
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import sys
import os
import subprocess
import uuid
from io import StringIO

app = FastAPI()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

class CodeRequest(BaseModel):
    user_code: str
    language: str 

@app.get("/")
def health():
    return {"status": "MindShift Neural Brain is Online and Multi-Language Ready"}

@app.post("/execute")
async def execute_code(request: CodeRequest):
    lang = request.language.lower()
    
    # --- PYTHON EXECUTION ENGINE ---
    if lang == "python":
        old_stdout = sys.stdout
        redirected_output = sys.stdout = StringIO()
        try:
            # FIX: Use a single dictionary for both globals and locals.
            # This allows functions to access modules imported at the top level.
            exec_globals = {"__builtins__": __builtins__}
            exec(request.user_code, exec_globals, exec_globals)
            result = redirected_output.getvalue()
        except Exception as e:
            result = f"PYTHON ERROR: {str(e)}"
        finally:
            sys.stdout = old_stdout 
            
        return {"output": result.strip() if result else "Success (No output)"}

    # --- DART EXECUTION ENGINE ---
    elif lang == "dart":
        # FIX: Generate a unique filename using UUID to prevent collisions
        unique_id = uuid.uuid4().hex
        temp_file = f"bridge_{unique_id}.dart"
        
        with open(temp_file, "w") as f:
            f.write(request.user_code)
        
        try:
            process = subprocess.run(
                ["dart", "run", temp_file],
                capture_output=True,
                text=True,
                timeout=10 
            )
            
            # Combine stdout and stderr
            if process.returncode == 0:
                result = process.stdout
            else:
                result = f"DART ERROR:\n{process.stderr}"
                
        except subprocess.TimeoutExpired:
            result = "DART ERROR: Execution timed out (Possible infinite loop)"
        except Exception as e:
            result = f"DART SYSTEM ERROR: {str(e)}"
        finally:
            # Clean up the specific unique temp file
            if os.path.exists(temp_file):
                os.remove(temp_file)
                
        return {"output": result.strip() if result else "Success (No output)"}

    return {"output": "ERROR: Unsupported Language"}

@app.post("/reset")
async def reset_memory():
    return {"output": "SYSTEM REBOOTED: Neural Bridge Refreshed."}
