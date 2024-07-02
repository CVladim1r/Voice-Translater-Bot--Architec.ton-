# Whisper Telegram Bot

## ARCHITEC.ton

## Описание

Whisper Telegram Bot is a simple Telegram bot that recognizes audio files and voice messages, converting them into text. The bot is based on the whisper model from OpenAI.

## Using the bot

To use the bot, send it an audio message or an audio file. After processing, the bot will reply with the translated text.

## Message type

The bot handles messages containing:

- аудио файлы, голосовые сообщения
- видео, видео-записки

The bot cannot process files larger than 20 MB.

## Installation and Launch

### 1. Installing Dependencies

Install necessary packages and libraries, including ffmpeg and Python dependencies:

Python:

```shell
sudo apt install ffmpeg
pip3 install -r requirements.txt
```

### 2. Environment Variables

The bot uses the environment variable WHISPER_MIBOT_TOKEN, which should contain the bot token obtained from @BotFather on Telegram. You can set this variable directly in the config.py file.

### 3. Starting the Bot

Launch the bot with the command:

Python:

```shell
python3 app.py
```

### 4. Running as a Service on Linux

To run the bot as a service on Linux, create a service file /etc/systemd/system/bot_translater.service with the appropriate configuration. An example configuration is provided above.
