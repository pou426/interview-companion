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
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
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
│   │   ├── main.py              # FastAPI server
│   │   └── requirements.txt     # Backend dependencies
│   ├── frontend/
│   │   ├── src/                 # React application
│   │   ├── package.json         # Frontend dependencies
│   │   └── ...                  # React configuration
│   ├── main.py                  # CLI interviewer (see below)
│   ├── interviewer.py           # AI interviewer logic & prompts
│   └── questions.py             # Question database
├── .env                         # Environment variables
└── requirements.txt             # CLI dependencies
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

## 🖥️ Exploratory CLI Program

For those who prefer command-line interfaces or want to explore the core interview logic:

### Features
- 🎯 **Interactive Interview Sessions**: Step-by-step guided interviews with AI feedback
- 🧠 **Memory & Context**: Conversation history maintained throughout the session
- 📊 **Phase-based Structure**: Clarifications → Requirements → Design → Deep Dive
- 💡 **Smart Guidance**: AI provides ratings and specific improvement suggestions

### Setup & Usage

```bash
# Create and activate virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Set up environment
echo "OPENAI_API_KEY=your-openai-api-key-here" > .env

# Run the interactive CLI interviewer
python src/main.py
```

### CLI Commands
- Type your responses to interviewer questions
- `quit` - Exit the interview session
- `help` - Show available commands

The CLI program uses the same AI interviewer logic as the web application but in a terminal interface.

---

**Happy practicing! 🚀**

*Built with ❤️ for system design interview preparation*