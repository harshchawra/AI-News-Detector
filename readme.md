AI Fact-Checking Agent
This project provides a deployable AI agent that fact-checks news headlines using CrewAI and serves the results via a FastAPI web interface.

How It Works
The system uses a "crew" of two specialized AI agents:

Researcher Agent: Scours the internet using the Serper API to find multiple sources and perspectives on a given headline.

Analyst Agent: Takes the researcher's findings, analyzes them for bias and consistency, and provides a final verdict with supporting sources.

The entire application is exposed as a simple API and can be easily deployed as a Docker container.

Setup and Running Locally
1. Prerequisites
Python 3.9+

Docker (for deployment)

2. Get API Keys
You need two API keys:

LLM Provider Key: An API key for your chosen Large Language Model. The code is configured for Groq (GROQ_API_KEY), which is very fast. You can also easily switch to OpenAI (OPENAI_API_KEY) or a local model via Ollama.

Serper API Key: An API key for the Serper.dev search tool. They have a generous free tier.

3. Project Setup
Clone the repository or create the files as provided.

Create a .env file in the root directory to store your API keys:

GROQ_API_KEY="gsk_..."
SERPER_API_KEY="your_serper_api_key"

Install dependencies:

pip install -r requirements.txt

4. Run the Application
Start the FastAPI server:

uvicorn main:app --reload

Open your browser and navigate to http://127.0.0.1:8000. You will see the user interface.

Deployment
This application is ready for deployment using Docker.

Build the Docker image:

docker build -t fact-checker-agent .

Run the Docker container:

docker run -d -p 8000:8000 --env-file .env fact-checker-agent

The --env-file .env flag passes your API keys to the container.

Deploy to the Cloud:
You can deploy this container image to services like:

Hugging Face Spaces: Great for ML demos, free tier available.

Render: Easy to use PaaS for deploying web services.

Railway: Another user-friendly deployment platform.

Any cloud provider that supports Docker containers (AWS, GCP, Azure).