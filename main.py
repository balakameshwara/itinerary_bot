import os
import urllib.parse
from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field
from dotenv import load_dotenv

# Langchain imports
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import JsonOutputParser

from dotenv import load_dotenv

env_path = os.path.join(os.path.dirname(__file__), ".env")
# load_dotenv is called in the endpoint so that changes take true effect dynamically

app = FastAPI()

# Pydantic models for API request
class RequestParams(BaseModel):
    destination: str
    budget: float
    days: int = 3

# Pydantic models for Langchain Output Parsing
class Activity(BaseModel):
    place_name: str = Field(description="Name of the tourist attraction or place")
    description: str = Field(description="Short engaging description of the activity")
    estimated_cost: float = Field(description="Estimated cost of visiting in USD")

class DayItinerary(BaseModel):
    day: int = Field(description="Day number (1, 2, 3...)")
    activities: list[Activity] = Field(description="List of activities for the day")

class Statistics(BaseModel):
    visitable_places: int = Field(description="Total number of unique places to visit.")
    estimated_total_cost: float = Field(description="Sum of estimated costs. Must be <= budget.")
    budget_surplus: float = Field(description="Remaining budget.")

class ItineraryResponse(BaseModel):
    statistics: Statistics
    itinerary: list[DayItinerary]

def get_google_maps_url(place_name: str, destination: str) -> str:
    query = f"{place_name} {destination}"
    return f"https://www.google.com/maps/search/?api=1&query={urllib.parse.quote(query)}"

@app.post("/api/generate")
async def generate_itinerary(params: RequestParams):
    load_dotenv(env_path, override=True) # Always fetch latest from .env
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key or api_key == "your_gemini_api_key_here":
        raise HTTPException(
            status_code=500, 
            detail="Gemini API key not configured. Please add GEMINI_API_KEY to your .env file in C:\\Users\\india\\.gemini\\antigravity\\scratch\\itinerary_bot and restart."
        )

    llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0.7)
    parser = JsonOutputParser(pydantic_object=ItineraryResponse)
    
    prompt = ChatPromptTemplate.from_messages([
        ("system", "You are an expert personalized travel planner. You carefully optimize itineraries based on strict budgets.\n{format_instructions}"),
        ("user", "Create an itinerary for a trip to {destination}.\nTotal Budget constraint: ${budget}\nDuration: {days} days.\nEnsure the estimated_total_cost does not exceed the budget.")
    ])
    
    chain = prompt | llm | parser

    try:
        # Generate the itinerary using LangChain
        result = chain.invoke({
            "destination": params.destination,
            "budget": params.budget,
            "days": params.days,
            "format_instructions": parser.get_format_instructions()
        })
        
        # Post-process to inject Google Maps links
        for day in result.get("itinerary", []):
            for activity in day.get("activities", []):
                activity["map_url"] = get_google_maps_url(activity["place_name"], params.destination)
                
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Mount static files for the frontend
app.mount("/", StaticFiles(directory="static", html=True), name="static")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
