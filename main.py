from fastapi import FastAPI, UploadFile, File, HTTPException
import os
import uuid  # NEW FOR WEEK 4: Generates unique IDs

app = FastAPI()

# Setup folders and rules
UPLOAD_DIR = "uploads"
MAX_FILE_SIZE = 5 * 1024 * 1024  # 5MB limit
ALLOWED_TYPES = ["image/jpeg", "image/png", "application/pdf"]

if not os.path.exists(UPLOAD_DIR):
    os.makedirs(UPLOAD_DIR)

@app.post("/upload/")
async def upload_file(file: UploadFile = File(...)):
    # 1. Size Check
    content = await file.read()
    if len(content) > MAX_FILE_SIZE:
        raise HTTPException(status_code=413, detail="File too large! Maximum limit is 5MB.")

    # 2. Type Check
    if file.content_type not in ALLOWED_TYPES:
        raise HTTPException(status_code=400, detail="Invalid file type! Only JPG, PNG, and PDF are allowed.")

    # 3. NEW FOR WEEK 4: Make the filename unique using UUID
    unique_id = uuid.uuid4().hex  # Generates a random unique string
    unique_filename = f"{unique_id}_{file.filename}" # Combines ID + original name
    
    # 4. Save the file with the unique name
    file_path = os.path.join(UPLOAD_DIR, unique_filename)
    with open(file_path, "wb") as f:
        f.write(content)

    return {
        "message": "Successfully uploaded!",
        "original_filename": file.filename,
        "unique_filename": unique_filename,
        "type": file.content_type
    }

@app.get("/files/")
async def list_files():
    files = os.listdir(UPLOAD_DIR)
    return {"uploaded_files": files}