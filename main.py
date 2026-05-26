from fastapi import FastAPI, UploadFile, File, HTTPException, Depends
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
import os
import uuid
from werkzeug.utils import secure_filename
from sqlalchemy.orm import Session
from database import get_db, engine
import models

# Initialize Database tables
models.Base.metadata.create_all(bind=engine)

app = FastAPI()

UPLOAD_DIR = "uploads"
MAX_FILE_SIZE = 5 * 1024 * 1024  # 5MB Limit
ALLOWED_TYPES = ["image/jpeg", "image/png", "application/pdf"]

if not os.path.exists(UPLOAD_DIR):
    os.makedirs(UPLOAD_DIR)

app.mount("/download", StaticFiles(directory=UPLOAD_DIR), name="download")

@app.post("/upload/")
async def upload_file(file: UploadFile = File(...), db: Session = Depends(get_db)):
    try:
        # 1. Read and Check Size
        content = await file.read()
        if len(content) > MAX_FILE_SIZE:
            raise HTTPException(status_code=413, detail="File too large! Max 5MB.")

        # 2. Type Check
        if file.content_type not in ALLOWED_TYPES:
            raise HTTPException(status_code=400, detail="Invalid file type!")

        # 3. Create SECURE Unique Filename (Week 7 Security)
        unique_id = uuid.uuid4().hex
        safe_name = secure_filename(file.filename)
        unique_filename = f"{unique_id}_{safe_name}"
        
        # 4. Save file to disk
        file_path = os.path.join(UPLOAD_DIR, unique_filename)
        with open(file_path, "wb") as f:
            f.write(content)

        # 5. Save to Database
        new_file = models.FileMetadata(filename=unique_filename)
        db.add(new_file)
        db.commit()

        return {"message": "Successfully uploaded!", "filename": unique_filename}

    except Exception as e:
        # Generic error message for security (don't leak system details)
        raise HTTPException(status_code=500, detail="Internal server error.")

@app.get("/", response_class=HTMLResponse)
async def get_index():
    with open("index.html", "r") as f:
        return f.read()