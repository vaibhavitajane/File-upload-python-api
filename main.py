from fastapi import FastAPI, UploadFile, File
import os

app = FastAPI()

# Create a folder to save uploaded files if it doesn't exist
UPLOAD_DIR = "uploads"
if not os.path.exists(UPLOAD_DIR):
    os.makedirs(UPLOAD_DIR)

@app.get("/")
def home():
    return {"message": "Welcome to the File Upload API!"}

@app.post("/upload/")
async def upload_file(file: UploadFile = File(...)):
    # Create the full path where the file will be saved
    file_path = os.path.join(UPLOAD_DIR, file.filename)
    
    # Save the file locally
    with open(file_path, "wb") as buffer:
        content = await file.read()
        buffer.write(content)
        
    return {
        "filename": file.filename,
        "content_type": file.content_type,
        "message": "File uploaded successfully!"
    }