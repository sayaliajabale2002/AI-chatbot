# AI-chatbot

AI-Chatbot is an interactive, state-driven conversational app built with Streamlit, LangGraph, and LangChain. Powered by Google's gemini-2.5-flash, the agent dynamically selects and executes tools—such as real-time web searches via Tavily and mathematical functions—to deliver accurate, up-to-date responses. It uses LangGraph's MemorySaver to manage stateful graph execution and persist conversation context seamlessly across user turns under unified session threads.

To get started:
1) Navigate into the project folder
2) Set up a Python virtual environment
3) Install the dependencies with pip install -r requirements.txt
4) Create a .env file in the root directory containing your GOOGLE_API_KEY=your-key-here and TAVILY_API_KEY=your-key-here
5) Launch the web application locally by running streamlit run app.py to view it at 
