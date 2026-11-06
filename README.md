# AI Psychological Support Telegram Bot

An AI-powered Telegram chatbot designed to provide emotional support through text and voice interactions.

## Overview

This project is a Python-based Telegram chatbot that uses large language models to generate supportive conversational responses. It was developed as an independent software project.

The bot is designed to help users express their feelings, reflect on their emotional state, and access educational resources.

## Features

- AI-powered text conversations.
- Voice message transcription using Whisper.
- Emotion-related conversation support.
- Interactive Telegram keyboard.
- Conversation history during an active session.
- Educational video recommendations.
- Safety disclaimer explaining that the bot does not replace professional psychological assistance.

## Technologies

- Python
- aiogram
- OpenAI Python Client
- OpenRouter API
- GPT-4o-mini
- Whisper
- python-dotenv
- Telegram Bot API

## Architecture

The application uses Telegram as its user interface. The Python backend processes incoming messages and communicates with language models through the OpenRouter API.

Voice messages are transcribed using Whisper before being processed by the conversational model.

## Installation

1. Clone the repository.
2. Install the dependencies:

   `pip install -r requirements.txt`

3. Create a `.env` file based on `.env.example`.
4. Add your own Telegram bot token and OpenRouter API key.
5. Run the application:

   `python bot.py`

## Environment Variables

- `BOT_TOKEN` — Telegram Bot API token.
- `OPENAI_API_KEY` — API key used for OpenRouter access.

Never commit your `.env` file or expose API credentials.

## Limitations

- Conversation history is stored in memory and is not persistent across restarts.
- The chatbot is not a substitute for a licensed mental health professional.
- AI-generated responses may be inaccurate and should not be treated as medical advice.

## Developer

Sofiya Zavialova

Independent Developer
