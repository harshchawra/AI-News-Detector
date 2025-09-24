AI News Fact-Checking Agent
This project is a web-based AI agent that fact-checks news headlines in real-time. It uses a multi-agent system built with CrewAI to research, analyze, and deliver a verdict on the credibility of a news story, complete with sources.

✨ Features
Real-time Fact-Checking: Enter any news headline and get a detailed analysis.

Multi-Agent System: Utilizes a Researcher agent for information gathering and an Analyst agent for critical evaluation.

Source Citing: The final analysis includes the URLs of the most reliable sources used.

Web Interface: Simple and clean user interface for easy interaction.

Ready for Deployment: Includes a Dockerfile for easy containerization and deployment.

🛠️ Tech Stack
Backend: FastAPI

AI Framework: CrewAI

Language Model (LLM): Google Gemini (gemini-1.5-flash)

Search Tool: SerperDevTool

Deployment: Docker

🚀 Getting Started
Follow these instructions to get the project running on your local machine.

1. Prerequisites
Python 3.9+

An active virtual environment (recommended).

2. Installation
First, clone the repository to your local machine:

git clone https://github.com/harshchawra/AI-News-Detector.git
cd AI-News-Detector

Next, install the required Python packages:

pip install -r requirements.txt

3. Environment Variables
This project requires API keys for Google Gemini and Serper.

Create a file named .env in the root directory of the project.

Add your API keys to the .env file as follows:

# Get your key from Google AI Studio: [GEMINI API KEY](https://aistudio.google.com/app/apikey)
GOOGLE_API_KEY="your_google_api_key_here"

# Get your key from Serper: [SERPER APR KEY](https://serper.dev/)
SERPER_API_KEY="your_serper_api_key_here"

4. Running the Application
Start the local server using Uvicorn:

uvicorn main:app --reload

The application will be running and accessible at http://127.0.0.1:8000.

🐳 Deployment with Docker
This project is containerized for easy and consistent deployment.

Build the Docker image:

docker build -t fact-checker-agent .

Run the Docker container, passing the environment variables from your .env file:

docker run -p 8000:8000 --env-file .env fact-checker-agent

The application will now be running inside a Docker container, accessible at http://localhost:8000.