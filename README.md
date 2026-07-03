# AI-chatbot

AI-chatbot, is an interactive conversational agent built with Streamlit, LangGraph, and LangChain that uses Google's gemini-2.5-flash model to assist users with real-time responses. It works by managing chat conversational history through a state-driven graph topology, leveraging LangGraph's MemorySaver as an in-memory checkpointer to persist context across message turns under a unified session thread ID. 

To get started:
1) Navigate into the project folder
2) Set up a Python virtual environment
3) Install the dependencies with pip install -r requirements.txt
4) Create a .env file in the root directory containing your GOOGLE_API_KEY=your-key-here
5) Launch the web application locally by running streamlit run app.py to view it at 
