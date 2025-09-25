import os
import sys  # Import sys to print to stderr
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from crewai import Agent, Task, Crew, Process
from crewai_tools import SerperDevTool

# --- Configuration ---
# Switched from Groq to Google Gemini
from langchain_google_genai import ChatGoogleGenerativeAI

# Instantiate the Gemini model with the latest compatible model name
llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash", # Corrected model name
    verbose=True,
    temperature=0.5,
    google_api_key=os.getenv("GOOGLE_API_KEY")
)


# --- FastAPI App Setup ---
app = FastAPI()

class FactCheckRequest(BaseModel):
    headline: str

# --- Task Definition ---
# Note: Agents are now passed as arguments
def create_crew_tasks(headline, researcher_agent, analyst_agent):
    # Task for the Researcher
    research_task = Task(
        description=(
            f"Investigate the news headline: '{headline}'. "
            "Gather information from at least 3-5 diverse and reputable sources. "
            "Look for official statements, reports from major news organizations, "
            "and expert analysis. Summarize your findings."
        ),
        expected_output=(
            "A detailed report summarizing the findings from multiple sources, "
            "including direct quotes or key data points and the URLs of the sources."
        ),
        agent=researcher_agent
    )

    # Task for the Analyst
    analysis_task = Task(
        description=(
            "Analyze the research report on the headline. Cross-reference the facts, "
            "check for consistency between sources, and identify any potential bias or red flags. "
            "Based on your analysis, write a final verdict."
        ),
        expected_output=(
            "A final verdict on the news headline with a clear conclusion: 'Verified', "
            "'Misleading', 'Unverifiable', or 'False'. Provide a concise justification "
            "for your verdict and list the top 3 most reliable sources you consulted."
        ),
        agent=analyst_agent
    )
    return [research_task, analysis_task]

# --- API Endpoints ---
@app.post("/fact-check")
def fact_check_endpoint(request: FactCheckRequest):
    """
    Accepts a news headline and returns a fact-checking analysis.
    """
    headline = request.headline
    
    # --- DEBUGGING LOGS ---
    # print("--- Starting Fact Check ---", file=sys.stderr)
    # print(f"Received headline: {headline}", file=sys.stderr)
    
    google_api_key = os.getenv("GOOGLE_API_KEY")
    serper_api_key = os.getenv("SERPER_API_KEY")

    # print(f"Google Key Loaded: {'Yes' if google_api_key else 'No'}", file=sys.stderr)
    # print(f"SERPER Key Loaded: {'Yes' if serper_api_key else 'No'}", file=sys.stderr)
    # --- END DEBUGGING LOGS ---
    
    if not headline:
        return {"error": "Headline cannot be empty."}

    # --- Agent and Tool Initialization moved inside the endpoint ---
    search_tool = SerperDevTool()

    researcher = Agent(
        role='Senior News Researcher',
        goal='Uncover comprehensive and unbiased information on a given news headline.',
        backstory=(
            "You are a seasoned investigative journalist with a knack for digging deep "
            "and finding the real story behind the headlines. You use a variety of "
            "online sources to find multiple perspectives, identifying primary sources "
            "and checking for corroborating evidence."
        ),
        verbose=True,
        allow_delegation=False,
        tools=[search_tool],
        llm=llm
    )

    analyst = Agent(
        role='Fact-Checking Analyst',
        goal='Critically evaluate the information gathered by the researcher to determine its veracity.',
        backstory=(
            "You are a meticulous fact-checker with a background in critical analysis and logic. "
            "You have a keen eye for misinformation, logical fallacies, and media bias. "
            "Your job is to synthesize the collected information and and provide a clear, "
            "well-reasoned conclusion on the validity of the news headline, citing all sources."
        ),
        verbose=True,
        allow_delegation=False,
        llm=llm
    )
    
    tasks = create_crew_tasks(headline, researcher, analyst)
    
    news_crew = Crew(
        agents=[researcher, analyst],
        tasks=tasks,
        process=Process.sequential,
        verbose=True
    )
    
    print("--- Kicking off Crew ---", file=sys.stderr)
    result = news_crew.kickoff()
    print("--- Crew execution finished ---", file=sys.stderr)
    
    return {"analysis": result}

# Mount a directory to serve static files (like index.html)
app.mount("/", StaticFiles(directory=".", html=True), name="static")

