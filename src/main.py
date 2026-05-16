# main.py
import uvicorn
from controller.controller import app  # Import the FastAPI app from controller.py

if __name__ == "__main__":
    # Run the FastAPI app using uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)