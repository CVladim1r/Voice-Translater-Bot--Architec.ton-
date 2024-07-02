import asyncio
import os
import pathlib
import logging  # Add logging module

import ffmpeg

from aiogram import Bot
from aiogram import Dispatcher
from aiogram import types
from aiogram.filters.command import Command
from aiogram import F

import torch
import whisper

from db.utils import video_decoding
from db.utils import register_message
from db.utils import send_long_message
from db.utils import get_translate
from config import Config

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)

# Paths
voice_dir = Config.dirs.get("voice") or "./voice"
audio_dir = Config.dirs.get("audio") or "./audio"
models_dir = Config.dirs.get("models") or "./models"
video_dir = Config.dirs.get("video") or "./video"

device = "cuda" if torch.cuda.is_available() else "cpu"

model = whisper.load_model(Config.model, device=device, download_root=models_dir)
logger.info(
    f"{'Multilingual ' if model.is_multilingual else 'English '}{Config.model} model loaded."
)

bot = Bot(token=Config.WHISPER_MIBOT_TOKEN)
dp = Dispatcher()


@dp.message(Command("start"))
async def command_start(message: types.Message):
    logger.info(f"Received /start command from chat id: {message.chat.id}")
    await message.answer(f"start command. Chat id: {message.chat.id}")


@dp.message(Command("id"))
@register_message
async def command_id(message: types.Message):
    logger.info(f"Received /id command from chat id: {message.chat.id}")
    await message.reply(
        f"chat id: {message.chat.id}\n" f"user_id: {message.from_user.id}"
    )


@dp.message(Command("help"))
@register_message
async def help_command(message: types.Message):
    logger.info(f"Received /help command from chat id: {message.chat.id}")
    await message.reply("Бот для получения текста из аудио")


@dp.message(F.voice)
@dp.message(F.audio)
@register_message
async def get_audio(message: types.Message):
    logger.info(f"Received audio message from chat id: {message.chat.id}")
    voice_object = message.voice or message.audio
    pathlib.Path(audio_dir).mkdir(parents=True, exist_ok=True)
    filename = os.path.join(audio_dir, f"{voice_object.file_unique_id}")

    mess = await message.reply("Downloading file...")
    try:
        await bot.download(
            voice_object,
            destination=filename,
        )
        logger.info(f"Downloaded audio file to: {filename}")
    except Exception as E:
        logger.error(f"Error downloading file: {E}")
        await message.reply(f"Error: Cannot download file.\n{E}")
        raise E
    finally:
        await mess.delete()

    mess = await message.reply("Processing audio to text...")
    try:
        text = get_translate(model, filename)
    except Exception as E:
        logger.error(f"Error processing audio to text: {E}")
        await message.reply("Error: Cannot extract text.")
        raise E
    finally:
        await mess.delete()
    await send_long_message(message, text)


@dp.message(F.video)
@dp.message(F.video_note)
@dp.message(F.document)
@register_message
async def get_video_like(message: types.Message):
    logger.info(f"Received video/document message from chat id: {message.chat.id}")
    pathlib.Path(video_dir).mkdir(parents=True, exist_ok=True)
    object = message.video or message.video_note or message.document

    filename = os.path.join(
        video_dir,
        f"{object.file_unique_id}",
    )

    mess = await message.reply("Downloading file...")
    try:
        await bot.download(
            object,
            destination=filename,
        )
        logger.info(f"Downloaded video/document file to: {filename}")
    except Exception as E:
        logger.error(f"Error downloading file: {E}")
        await message.reply(f"Error: Cannot download file.\n{E}")
        raise E
    finally:
        await mess.delete()

    output_filename = filename
    if message.document:
        mess = await message.reply("Extracting audio...")
        output_filename = os.path.join(
            video_dir,
            f"{object.file_unique_id}.ogg",
        )
        try:
            video_decoding(filename, output_filename)
            logger.info(f"Extracted audio to: {output_filename}")
        except Exception as E:
            logger.error(f"Error extracting audio: {E}")
            await message.reply(f"Error: Cannot extract audio.\n{E}")
            raise E
        finally:
            await mess.delete()

    mess = await message.reply("Processing audio to text...")
    try:
        text = get_translate(model, output_filename)
    except Exception as E:
        logger.error(f"Error processing audio to text: {E}")
        await message.reply("Error: Cannot extract text.")
        raise E
    finally:
        await mess.delete()
    await send_long_message(message, text)


async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
