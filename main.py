from fastapi import FastAPI, Request
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import sys
import os
import subprocess
from io import StringIO

app = FastAPI()

# Enable CORS so your Flutter app can talk to Render
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
            # We use a clean dictionary for local_vars so users don't clash
            local_vars = {} 
            exec(request.user_code, {"__builtins__": __builtins__}, local_vars)
            result = redirected_output.getvalue()
        except Exception as e:
            result = f"PYTHON ERROR: {str(e)}"
        finally:
            sys.stdout = old_stdout # Reset stdout correctly
            
        return {"output": result.strip() if result else "Success (No output)"}

    # --- DART EXECUTION ENGINE ---
    elif lang == "dart":
        # Create a temporary file for the user's Dart code
        temp_file = "bridge_temp.dart"
        with open(temp_file, "w") as f:
            f.write(request.user_code)
        
        try:
            # We call the dart binary we downloaded in build.sh
            # 'dart run' handles the compilation and execution in one go
            process = subprocess.run(
                ["dart", "run", temp_file],
                capture_output=True,
                text=True,
                timeout=10 # Prevents infinite loops from crashing your server
            )
            
            # Combine stdout (print statements) and stderr (errors)
            output = process.stdout if process.returncode == 0 else process.stderr
            result = output.strip()
        except subprocess.TimeoutExpired:
            result = "DART ERROR: Execution timed out (Possible infinite loop)"
        except Exception as e:
            result = f"DART SYSTEM ERROR: {str(e)}"
        finally:
            # Always clean up the temp file
            if os.path.exists(temp_file):
                os.remove(temp_file)
                
        return {"output": result if result else "Success (No output)"}

    return {"output": "ERROR: Unsupported Language"}

@app.post("/reset")
async def reset_memory():
    return {"output": "SYSTEM REBOOTED: Neural Bridge Refreshed."}
