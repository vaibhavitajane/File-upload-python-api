from fastapi import FastAPI, UploadFile, File, HTTPException
import os

app = FastAPI()

# 1. Setup folders and rules
UPLOAD_DIR = "uploads"
MAX_FILE_SIZE = 5 * 1024 * 1024  # 5MB limit
ALLOWED_TYPES = ["image/jpeg", "image/png", "application/pdf"] # Only Images & PDFs

# Create the uploads folder if it doesn't exist
if not os.path.exists(UPLOAD_DIR):
    os.makedirs(UPLOAD_DIR)

@app.post("/upload/")
async def upload_file(file: UploadFile = File(...)):
    # 2. SECURITY CHECK: Check File Size
    content = await file.read()
    if len(content) > MAX_FILE_SIZE:
        raise HTTPException(status_code=413, detail="File too large! Maximum limit is 5MB.")

    # 3. SECURITY CHECK: Check File Type (MIME Type)
    if file.content_type not in ALLOWED_TYPES:
        raise HTTPException(status_code=400, detail="Invalid file type! Only JPG, PNG, and PDF are allowed.")

    # 4. SAVE THE FILE: If it passes all checks
    file_path = os.path.join(UPLOAD_DIR, file.filename)
    with open(file_path, "wb") as f:
        f.write(content)

    return {"message": f"Successfully uploaded {file.filename}", "type": file.content_type}

# 5. NEW FOR WEEK 3: List all files
@app.get("/files/")
async def list_files():
    files = os.listdir(UPLOAD_DIR)
    return {"uploaded_files": files}
    
    
