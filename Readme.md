## Installation
1. Clone the repository
2. (Optional) Create and activate a virtual environment:
    python -m venv envirtual
    .\envirtual\Scripts\activate
3. Install the required dependencies:
    pip install -r requirements.txt
4. Update the dependencies:
    pip install -r requirements.txt --upgrade
## Running the Application
To run the application, execute the following command:
    uvicorn main:app --reload
    if using localhost
    uvicorn main:app --reload --host 0.0.0.0 --port 8000

Run ngrok
    ngrok http http://localhost:8000