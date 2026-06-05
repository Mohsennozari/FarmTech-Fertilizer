# Platform-v3\backend\run.py

import uvicorn

if __name__ == "__main__":
    print("=" * 50)
    print("FarmTech API Server")
    print("=" * 50)
    print("\nStarting server...")
    print("API Documentation: http://127.0.0.1:8000/docs")
    print("Swagger UI: http://127.0.0.1:8000/docs")
    print("ReDoc: http://127.0.0.1:8000/redoc")
    print("\nPress Ctrl+C to stop the server")
    print("=" * 50)
    print()
    
    uvicorn.run(
        "app.main:app",
        host="127.0.0.1",
        port=8000,
        reload=True
    )