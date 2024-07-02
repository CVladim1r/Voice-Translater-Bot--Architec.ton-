import os


class Config:
    WHISPER_MIBOT_TOKEN = os.environ.get("WHISPER_ARCHITEC.TON_TOKEN") or "bot_token"
    
    model = "small"

    dirs = {
        "models": "./models",
        "audio": "./tmp",
        "voice": "./tmp",
        "video": "./tmp",
    }

    MongoDB_string = os.environ.get("MONGO_STRING")
    MongoDB_db_name = "whisper_bot_architec_ton"
