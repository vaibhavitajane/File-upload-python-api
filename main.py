from fastapi import FastAPI, File, UploadFile # Make sure File and UploadFile are here
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
import os
import uuid

app = FastAPI()

UPLOAD_DIR = "uploads"
MAX_FILE_SIZE = 5 * 1024 * 1024  # 5MB limit
ALLOWED_TYPES = ["image/jpeg", "image/png", "application/pdf"]

if not os.path.exists(UPLOAD_DIR):
    os.makedirs(UPLOAD_DIR)

# NEW FOR WEEK 5: This makes the files accessible via a web browser URL
app.mount("/download", StaticFiles(directory=UPLOAD_DIR), name="download")

@app.post("/upload/")
async def upload_file(file: UploadFile = File(...)):
    # 1. Read content and check size
    content = await file.read()
    file_size = len(content)  # NEW FOR WEEK 5: Calculate file size in bytes
    
    if file_size > MAX_FILE_SIZE:
        raise HTTPException(status_code=413, detail="File too large! Maximum limit is 5MB.")

    # 2. Type Check
    if file.content_type not in ALLOWED_TYPES:
        raise HTTPException(status_code=400, detail="Invalid file type! Only JPG, PNG, and PDF are allowed.")

    # 3. Create Unique Filename
    unique_id = uuid.uuid4().hex
    unique_filename = f"{unique_id}_{file.filename}"
    
    # 4. Save the file
    file_path = os.path.join(UPLOAD_DIR, unique_filename)
    with open(file_path, "wb") as f:
        f.write(content)

    # 5. NEW FOR WEEK 5: Generate a working download URL
    download_url = f"http://127.0.0.1:8000/download/{unique_filename}"

    # Return complete File Metadata
    return {
        "message": "Successfully uploaded!",
        "metadata": {
            "original_filename": file.filename,
            "unique_filename": unique_filename,
            "file_size_bytes": file_size,
            "file_type": file.content_type,
            "download_url": download_url
        }
    }
@app.get("/", response_class=HTMLResponse)
async def get_index():
    # Make sure index.html is in the same folder as main.py
    try:
        with open("index.html", "r") as f:
            html_content = f.read()
        return HTMLResponse(content=html_content, status_code=200)
    except FileNotFoundError:
        return HTMLResponse(content="<h1>index.html not found!</h1>", status_code=404)
        

