# Itinerary Bot

A full-stack web application that acts as an expert personalized travel planner. It utilizes Artificial Intelligence to carefully optimize travel itineraries based on strict personal budgets, tracking destinations using Google Maps integrations.

## Features
- **Budget Tracking**: Computes statistics on how many unique places you can visit while keeping the estimated total cost within the available budget constraints.
- **Smart Itineraries**: Generates comprehensive daily schedules including descriptions and cost estimations for each activity.
- **Google Maps Integration**: Automatically injects Google Maps search links to quickly navigate to every recommended tourist attraction.
- **AI-Powered Generation**: Leverages advanced LLMs and Langchain to intelligently curate logical, day-by-day travel suggestions.

## Technology Stack
- **Frontend**: JavaScript, HTML, CSS
- **Backend Framework**: Python, FastAPI, Uvicorn
- **AI & Integrations**: LangChain, Google Gemini API (Migrated from OpenAI API for improved quotas), Pydantic
- **Environment Management**: python-dotenv

## Getting Started

### Prerequisites
- Python 3.8+
- An API Key for Google Gemini (Generative AI)

### Installation

1. **Clone or Download the Repository**
2. **Setup Virtual Environment (Optional but recommended)**
   ```bash
   python -m venv venv
   # On Windows:
   .\venv\Scripts\activate
   # On macOS/Linux:
   source venv/bin/activate
   ```
3. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```
4. **Environment Configuration**
   Copy the `.env.example` file to create a new `.env` file in the root directory:
   ```bash
   cp .env.example .env
   ```
   Add your Gemini API Key:
   ```env
   GEMINI_API_KEY="your_gemini_api_key_here"
   ```

### Running the Application

Start the backend server using Uvicorn:

```bash
python main.py
```
*Alternatively:*
```bash
uvicorn main:app --reload
```

Then, open your web browser and navigate to `http://localhost:8000` to access the application.

## API Endpoints

- **`POST /api/generate`**: Expects destination string, total budget, and number of days. Returns a JSON structured breakdown containing `statistics` and a day-by-day `itinerary` including Google Maps URLs.
