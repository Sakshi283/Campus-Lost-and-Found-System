# Campus Lost & Found Management System

A beginner-friendly individual project using Python, MongoDB, PyMongo, and Streamlit.

## Requirements
- Python 3.10 or newer
- MongoDB Server running locally on port 27017
- Python packages listed in `requirements.txt`

## Setup
1. Open a terminal in this folder.
2. Install dependencies:
   ```bash
   python -m pip install -r requirements.txt
   ```
3. Ensure the MongoDB Server service is running.
4. Start the application:
   ```bash
   python -m streamlit run app.py
   ```
5. Streamlit will display a local address (usually http://localhost:8501) to open in your browser.

## Database
The app uses database `campus_lost_found` and collection `items`. MongoDB creates the database and collection automatically when the first report is inserted.

## Features
- Create lost/found reports
- View and search reports
- Update status, location, and description
- Delete reports with confirmation
- Input validation
- MongoDB aggregation reports by type, category, status, and location

## Notes
- The default connection URI is `mongodb://localhost:27017/`.
- Use fictional names and contact details for demonstrations.
- The app expects MongoDB to be running locally.
