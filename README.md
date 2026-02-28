# ai-youtube-telegram-bot

# 📌 Project Title

# 🎥 AI YouTube Research Assistant Bot (Telegram + OpenClaw Local Setup)

---

# 📖 Project Overview

This project is a smart AI-powered Telegram bot that helps users:

* Understand long YouTube videos quickly
* Extract key insights
* Ask contextual follow-up questions
* Get responses in English and Kannada

The system behaves like a **personal AI research assistant for YouTube videos**.

---

# 🚀 Features Implemented

✅ Accepts YouTube link
✅ Fetches video transcript
✅ Generates structured English summary
✅ Provides contextual Q&A
✅ Supports Kannada translation
✅ Handles invalid URLs
✅ Handles missing transcripts
✅ Manages user session context
✅ Prevents hallucination using grounded prompts

---

# 🏗️ Architecture Overview

## 🔹 High-Level Flow

User → Telegram Bot → Transcript Fetcher → Local LLM (Ollama) → Response → User

---

## 🔹 Components

### 1️⃣ Telegram Bot Layer

* Built using `python-telegram-bot`
* Handles commands and user messages
* Maintains per-user session using dictionary storage

---

### 2️⃣ Transcript Retrieval Layer

* Uses `yt-dlp` to extract subtitles
* Falls back to automatic captions
* Cleans HTML tags and timestamp formatting
* Handles transcript unavailable cases gracefully

---

### 3️⃣ AI Processing Layer (OpenClaw Local via Ollama)

* Uses local `phi` model
* No cloud API required
* Prompt-engineered for:

  * Structured summary
  * Context-grounded Q&A
  * Kannada translation

---

### 4️⃣ Session Management

* Stores transcript per user
* Allows multi-user usage simultaneously
* Supports multiple follow-up questions

---

# 🧠 Design Decisions

### Why Local LLM (Ollama)?

* No API cost
* No rate limits
* Fully offline capability
* Better control over experimentation

### Why Prompt Engineering Instead of RAG?

* Simpler architecture for assignment scope
* Transcript chunking used to avoid token overflow
* Ensures responses remain grounded

### Why Not Whisper?

* Heavy for 8GB RAM systems
* YouTube subtitle extraction sufficient for business use case

---

# ⚖️ Trade-offs

| Decision              | Trade-off                             |
| --------------------- | ------------------------------------- |
| Local LLM             | Slightly slower than cloud            |
| No embeddings         | Simpler but less scalable             |
| In-memory storage     | No persistence across restarts        |
| Transcript truncation | Very long videos partially summarized |

---

# 🛠️ Setup Instructions

## 1️⃣ Clone Repository

```bash
git clone <your-repo-link>
cd telegram-youtube-bot
```

---

## 2️⃣ Create Virtual Environment

```bash
python -m venv venv
venv\Scripts\activate
```

---

## 3️⃣ Install Dependencies

```bash
pip install python-telegram-bot==20.3
pip install yt-dlp
pip install requests
pip install ollama
pip install httpx==0.24.1
```

---

## 4️⃣ Install Ollama (Local OpenClaw Equivalent)

Download from:
[https://ollama.com](https://ollama.com)

Then pull model:

```bash
ollama pull phi
```

---

## 5️⃣ Create Telegram Bot

* Open Telegram
* Search **@BotFather**
* Create new bot
* Copy token
* Paste in `main.py`

---

## 6️⃣ Run Bot

```bash
python main.py
```

You should see:

```
🚀 Bot running...
```

---

# 👤 Core User Flow

## Step 1 — User Sends YouTube Link

Bot returns:

🎥 Video Title
📌 5 Key Points
⏱ Important Timestamps
🧠 Core Takeaway

---

## Step 2 — User Asks Question

Bot:

* Answers using transcript
* If not found →
  "This topic is not covered in the video."

---

## Step 3 — Multi-language Support

User types:

```
Summarize in Kannada
```

Bot generates full structured summary in Kannada.

---

# 🛡️ Edge Cases Handled

✅ Invalid YouTube URL
✅ Transcript not available
✅ Automatic captions fallback
✅ Very long transcript truncation
✅ Network failures
✅ Multiple user sessions
✅ Hallucination prevention

---

# 📊 Evaluation Criteria Coverage

| Category                 | Covered |
| ------------------------ | ------- |
| End-to-end functionality | ✅       |
| Summary quality          | ✅       |
| Q&A accuracy             | ✅       |
| Multi-language support   | ✅       |
| Code quality             | ✅       |
| Error handling           | ✅       |

---



---

# 🔮 Future Improvements

* Persistent database storage
* Embeddings + semantic search
* Audio transcription fallback
* Deployment on cloud server
* Web dashboard UI

---

# 🎯 Final Result

This system successfully behaves as a business-focused AI research assistant for YouTube content with multi-language capability and contextual intelligence.


# 🚀 **DEMO – OPEN THIS LINK**

👉 [Click Here to Watch the Demo](https://drive.google.com/file/d/1Ys7kO6pLL7qSjsQQB0ZKQpVVLm5U2Z5c/view?usp=drivesdk)

