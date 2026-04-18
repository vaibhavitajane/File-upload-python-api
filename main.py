from fastapi import FastAPI, File, UploadFile, HTTPException
import os

app = FastAPI()
UPLOAD_DIR = "uploads"

# Create the folder if it doesn't exist
if not os.path.exists(UPLOAD_DIR):
    os.makedirs(UPLOAD_DIR)

@app.get("/")
def home():
    return {"message": "File Uploader API is running!"}

@app.post("/upload/")
async def upload_file(file: UploadFile = File(...)):
    # --- WEEK 2: SIZE VALIDATION ---
    MAX_FILE_SIZE = 5 * 1024 * 1024  # 5MB limit
    
    content = await file.read() # Read the file data
    
    if len(content) > MAX_FILE_SIZE:
        # Stop the process if file is too big
        raise HTTPException(status_code=413, detail="File too large! Maximum limit is 5MB.")

    # Reset the pointer so we can save the actual data
    await file.seek(0)

    # --- SAVE PROCESS ---
    file_path = os.path.join(UPLOAD_DIR, file.filename)
    with open(file_path, "wb") as f:
        f.write(content)

    return {"message": f"Successfully uploaded {file.filename}"}
    
