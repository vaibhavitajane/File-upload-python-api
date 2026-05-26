# 🚀 File Upload Python API

> A robust, secure, and database-integrated File Upload API built with **FastAPI** and **Python**.

This project was developed over a 7-week structured internship, evolving from a simple API endpoint to a secure, full-stack application with database persistence and front-end integration.

---

## 🌟 Key Milestones

* **API Foundation:** Built a high-performance backend using **FastAPI** and **Uvicorn**.
* **Frontend Integration:** Served an interactive **HTML/CSS** client interface with asynchronous JavaScript uploads.
* **Persistent Storage:** Integrated **SQLite** and **SQLAlchemy** to track file metadata.
* **Security Hardening:** Implemented strict file validation, error handling, and path-traversal prevention.

---

## 📅 Project Timeline & Weekly Breakdown

### **Week 1: Project Setup and Backend Initialization**
The first week focused on establishing a clean and scalable backend architecture. 
* **Environment Configuration:** Initialized the project environment, set up an isolated Python virtual environment (`.venv`), and managed dependencies.
* **FastAPI Initialization:** Created the core `main.py` file, instantiated the FastAPI application, and configured the ASGI server using **Uvicorn** to enable live reloading during development.

### **Week 2: Core API Endpoints**
Built the engine that handles incoming data from users.
* **Route Creation:** Developed the foundational `POST /upload/` endpoint.
* **Data Parsing:** Utilized FastAPI's native `UploadFile` and `File` classes to successfully parse and accept `multipart/form-data` requests, allowing the server to temporarily hold incoming files in memory.

### **Week 3: Frontend Interface Design**
Focused on the client-side experience by building a clean user interface.
* **UI/UX Design:** Developed an intuitive `index.html` interface with clean CSS styling.
* **Form Structure:** Created a drag-and-drop style file selection area and an upload button, ensuring the interface is visually appealing and easy to navigate for end-users.

### **Week 4: Client-Server Integration**
Connected the frontend UI to the backend API without relying on bulky external frameworks.
* **Static File Mounting:** Utilized `fastapi.staticfiles` to mount an `uploads/` directory and route the root URL (`/`) to serve the HTML file natively.
* **Asynchronous JavaScript:** Wrote vanilla **JavaScript** utilizing the `Fetch API` to intercept form submissions, send the file data asynchronously to the backend, and dynamically display success or error messages without requiring a page reload.

### **Week 5: File Processing and Local Storage**
Transitioned from handling in-memory files to robust physical storage and data extraction.
* **Metadata Extraction:** Upgraded the API logic to read the incoming file bytes to calculate the exact file size, while extracting the original filename and MIME type (`content_type`).
* **Collision Prevention:** Implemented the `uuid` library to generate unique hexadecimal prefixes for incoming files. This ensures that if two users upload a file named `image.png`, the server will safely store both.
* **File System Operations:** Used the `os` module to verify directory existence and safely write binary chunks (`"wb"`) directly to the local `uploads/` folder.

### **Week 6: Database Integration (ORM)**
Added data persistence to track upload history and metadata beyond the physical files.
* **Database Configuration:** Set up a local **SQLite** database connection in `database.py` using **SQLAlchemy** (`create_engine`, `sessionmaker`, `declarative_base`).
* **Data Modeling:** Created robust database schemas in `models.py`, defining a `FileMetadata` table to store the unique filename, original name, and upload timestamps.
* **Dependency Injection:** Updated `main.py` to inject the database session (`Depends(get_db)`) directly into the upload route, ensuring a clean, thread-safe database transaction (`db.add()`, `db.commit()`) every time a file is saved.

### **Week 7: Security & System Hardening**
Secured the application against malicious intent by implementing industry-standard backend security practices.
* **Filename Sanitization:** Integrated `werkzeug.utils.secure_filename` to strip dangerous characters (e.g., `../../`) and prevent Directory Traversal/Path Injection attacks.
* **Constraint Enforcement:** * Enforced a strict **5MB** maximum file size, rejecting larger payloads with a `413 Payload Too Large` error.
  * Created a strict whitelist of allowed MIME types (**JPG, PNG, PDF**), rejecting unapproved scripts with a `400 Bad Request`.
* **Error Masking:** Wrapped the entire upload execution in robust `try-except` blocks to catch unexpected errors and return safe, generic `500 Internal Server Error` responses to the client, preventing the leakage of sensitive system architecture.

---

## 💻 Tech Stack

* **Backend:** Python 3, FastAPI, Uvicorn
* **Database:** SQLite, SQLAlchemy ORM
* **Security:** Werkzeug
* **Frontend:** HTML5, CSS3, JavaScript (Fetch API)

---

## 🚀 How to Run the Project Locally

**1. Clone the repository:**
```bash
git clone [https://github.com/vaibhavitajane/File-upload-python-api.git](https://github.com/vaibhavitajane/File-upload-python-api.git)
cd File-upload-python-api