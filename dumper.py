import time
import json
import random
import hashlib
from telethon.sync import TelegramClient
from telethon.tl.types import Channel
from telethon.errors import FloodWaitError, SessionPasswordNeededError
from telethon.tl.types import PeerChannel

class Dumper:
    def __init__(self, api_id: str, api_hash: str,  output_file: str = "channel_dump.jsonl"):
        self.output_file = output_file
        self.client = TelegramClient(self.get_session_name(), api_id, api_hash)
        self.client.start()

    def get_session_name(self) -> str:
        """Generate a unique session name to avoid conflicts."""
        h = hashlib.sha256()
        h.update(random.randint(0, 1000000).to_bytes(4, "big"))
        return h.hexdigest()[:8]

    def list_available_channels(self) -> list:
        """return list of dicts, containing data about all available channels you joined."""
        data = list()
        for dialog in self.client.iter_dialogs():
            if isinstance(dialog.entity, Channel):
                entry = {
                    "title":dialog.entity.title,
                    "id":dialog.entity.id
                }
                data.append(entry)
        return data
    
