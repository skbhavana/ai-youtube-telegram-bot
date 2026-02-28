import re
import requests
import yt_dlp
import ollama
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters,
)

# 🔴 PUT YOUR TELEGRAM BOT TOKEN HERE
BOT_TOKEN = "8612925287:AAEhk6bizKnVnru7j2io1GC_n7xFbOpnK38"

# Store transcript per user
user_sessions = {}


# ----------------------------
# Extract Video ID
# ----------------------------
def extract_video_id(url):
    pattern = r"(?:v=|\/)([0-9A-Za-z_-]{11})"
    match = re.search(pattern, url)
    return match.group(1) if match else None


# ----------------------------
# Fetch Transcript (Reliable)
# ----------------------------
def fetch_transcript(video_id):
    video_url = f"https://www.youtube.com/watch?v={video_id}"

    ydl_opts = {
        "skip_download": True,
        "quiet": True,
        "writesubtitles": True,
        "writeautomaticsub": True,
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(video_url, download=False)
            subtitles = info.get("subtitles") or info.get("automatic_captions")

            if not subtitles:
                return None

            # Prefer English
            if "en" in subtitles:
                subtitle_url = subtitles["en"][0]["url"]
            else:
                first_lang = list(subtitles.keys())[0]
                subtitle_url = subtitles[first_lang][0]["url"]

        response = requests.get(subtitle_url)
        raw_text = response.text

        clean_text = re.sub(r"<.*?>", "", raw_text)
        clean_text = re.sub(r"\d{2}:\d{2}:\d{2}\.\d+ --> .*", "", clean_text)
        clean_text = re.sub(r"\n+", " ", clean_text)

        return clean_text.strip()

    except Exception as e:
        print("Transcript Error:", e)
        return None


# ----------------------------
# Generate Structured Summary
# ----------------------------
def generate_summary(transcript, language="English"):

    prompt = f"""
You are a professional AI YouTube summarizer.

IMPORTANT:
- You MUST generate ALL sections.
- Use ONLY the transcript.
- Do NOT hallucinate.
- Respond fully in {language}.

Output EXACTLY in this format:

🎥 Video Title:
<Write title>

📌 5 Key Points:
1.
2.
3.
4.
5.

⏱ Important Timestamps:
- 00:00 -
- 00:00 -

🧠 Core Takeaway:
<Clear takeaway paragraph>

Transcript:
{transcript[:3000]}
"""

    response = ollama.chat(
        model="phi",
        messages=[{"role": "user", "content": prompt}],
    )

    return response["message"]["content"]


# ----------------------------
# Q&A Generator
# ----------------------------
def generate_answer(transcript, question, language="English"):

    prompt = f"""
Answer ONLY using the transcript below.

Rules:
- Do NOT add outside knowledge.
- If answer not found say:
  "This topic is not covered in the video."
- Respond in {language}.

Transcript:
{transcript[:4000]}

Question:
{question}
"""

    response = ollama.chat(
        model="phi",
        messages=[{"role": "user", "content": prompt}],
    )

    return response["message"]["content"]


# ----------------------------
# Start Command
# ----------------------------
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👋 Send a YouTube link.\n"
        "I will summarize and answer your questions."
    )


# ----------------------------
# Message Handler
# ----------------------------
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):

    user_id = update.message.from_user.id
    text = update.message.text.strip()

    # Q&A Mode
    if user_id in user_sessions:

        transcript = user_sessions[user_id]["transcript"]

        # Kannada summary
        if "kannada" in text.lower():
            await update.message.reply_text("🔄 Generating Kannada summary...")
            summary = generate_summary(transcript, language="Kannada")
            await update.message.reply_text(summary)
            return

        # Q&A
        await update.message.reply_text("🤔 Thinking...")
        answer = generate_answer(transcript, text)
        await update.message.reply_text(answer)
        return

    # Expect YouTube link
    video_id = extract_video_id(text)

    if not video_id:
        await update.message.reply_text("❌ Invalid YouTube URL.")
        return

    await update.message.reply_text("🔄 Fetching transcript...")

    transcript = fetch_transcript(video_id)

    if not transcript:
        await update.message.reply_text("❌ Transcript not available.")
        return

    # Store transcript
    user_sessions[user_id] = {
        "transcript": transcript
    }

    await update.message.reply_text("🧠 Generating English summary...")

    summary = generate_summary(transcript, language="English")

    if len(summary) > 4000:
        summary = summary[:4000]

    await update.message.reply_text(summary)

    await update.message.reply_text(
        "✅ You can now ask questions.\n"
        "Or type: Summarize in Kannada"
    )


# ----------------------------
# Run Bot
# ----------------------------
app = ApplicationBuilder().token(BOT_TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

print("🚀 Bot running...")
app.run_polling()