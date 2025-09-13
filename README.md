# System Design Interview Companion

🎯 A Python-based assistant to help you practice system design interviews with random question generation.

## Features

- 📚 **20+ System Design Questions**: Curated questions covering various complexity levels
- 🎲 **Random Question Generation**: Get surprised with different challenges each time
- 🔒 **Secure API Key Management**: Environment-based OpenAI API key handling (ready for future AI integration)
- 💻 **Clean CLI Interface**: Simple command-line experience

## Project Structure

```
interview-companion/
├── src/
│   └── main.py                 # Main CLI application
├── requirements.txt            # Python dependencies
├── README.md                   # This file
└── .env.example                # Example environment file
```

## Quick Start

### Prerequisites

- Python 3.7+
- OpenAI API key (for future AI features)

### Installation

1. **Clone or download this repository**

2. **Create and activate a virtual environment** (recommended):
   ```bash
   # Create virtual environment
   python3 -m venv venv
   
   # Activate it (macOS/Linux)
   source venv/bin/activate
   
   # Activate it (Windows)
   venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up your environment**:
   ```bash
   # Set your OpenAI API key for future AI features
   export OPENAI_API_KEY='your-openai-api-key-here'
   
   # Or create a .env file (recommended)
   echo "OPENAI_API_KEY=your-openai-api-key-here" > .env
   ```

### Usage

```bash
# Make sure your virtual environment is activated
source venv/bin/activate  # macOS/Linux
# or
venv\Scripts\activate     # Windows

# Run the question generator
python3 src/main.py
```

## Sample Questions

The system includes 20+ carefully selected system design questions:

- Design a URL shortener like bit.ly or TinyURL
- Design a social media feed like Twitter or Facebook  
- Design a chat system like WhatsApp or Slack
- Design a video streaming platform like YouTube or Netflix
- Design a ride-sharing service like Uber or Lyft
- And 15+ more...

---

**Happy practicing! 🚀**

*Built with ❤️ for system design interview preparation*