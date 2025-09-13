# System Design Interview Companion

🎯 An interactive web application and CLI tool to help you practice system design interviews with AI-powered feedback.

## Features

- 🤖 **AI-Powered Virtual Interviewer**: Senior staff engineer persona providing structured feedback
- 📝 **Structured Interview Flow**: Guided through clarifications → requirements → design → deep dive
- 💬 **Interactive Web Interface**: Modern React frontend with clean, simple design
- 🚀 **FastAPI Backend**: High-performance Python API server
- 📚 **20+ Curated Questions**: System design challenges covering various complexity levels
- 💾 **Memory & Context**: LangChain-powered conversation memory throughout sessions

## Quick Start

### Prerequisites

- Python 3.8+
- Node.js 16+
- OpenAI API key

### Installation & Setup

1. **Clone the repository and set up environment**:
   ```bash
   git clone <repository-url>
   cd interview-companion

   # Set up your OpenAI API key
   echo "OPENAI_API_KEY=your-openai-api-key-here" > .env
   ```

2. **Start Backend (FastAPI)**:
   ```bash
   cd src/backend

   # Set up environment (copy and edit .env.example)
   cp .env.example .env
   # Edit .env and add your OpenAI API key

   # Install dependencies
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt

   # Start server
   python3 main.py
   ```
   *Backend runs on http://localhost:8000*

3. **Start Frontend (React)** - in a new terminal:
   ```bash
   cd src/frontend
   npm install
   npm start
   ```
   *Frontend runs on http://localhost:3000*

4. **Open your browser** and go to http://localhost:3000

## Project Structure

```
interview-companion/
├── src/
│   ├── backend/
│   │   ├── main.py              # FastAPI server with LangChain integration
│   │   ├── interviewer.py       # AI interviewer logic & prompts
│   │   ├── questions.py         # Question database
│   │   ├── requirements.txt     # Backend dependencies
│   │   └── .env.example         # Environment variables template
│   └── frontend/
│       ├── src/                 # React TypeScript application
│       ├── package.json         # Frontend dependencies
│       └── ...                  # React configuration files
├── .env.example                 # Global environment template
└── README.md                    # This file
```

## Sample Questions

The system includes 20+ carefully selected system design questions:

- Design a URL shortener like bit.ly or TinyURL
- Design a social media feed like Twitter or Facebook
- Design a chat system like WhatsApp or Slack
- Design a video streaming platform like YouTube or Netflix
- Design a ride-sharing service like Uber or Lyft
- Design a search engine like Google
- Design an online marketplace like Amazon or eBay
- Design a notification system for mobile apps
- Design a distributed cache system like Redis
- Design a file storage service like Dropbox or Google Drive
- And 10+ more...

---

**Happy practicing! 🚀**

*Built with ❤️ for system design interview preparation*