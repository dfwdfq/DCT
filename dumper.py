import time
import json
import random
import hashlib
import os

from telethon.sync import TelegramClient
from telethon.tl.types import Channel, PeerChannel
from telethon.errors import FloodWaitError, SessionPasswordNeededError

class Dumper:
    def __init__(self, api_id: str, api_hash: str, output_file: str = "channel_dump.jsonl", media_dir: str = "media"):
        self.api_id = api_id
        self.api_hash = api_hash
        self.output_file = output_file
        self.media_dir = media_dir
        os.makedirs(self.media_dir, exist_ok=True)

        self.session_name = self.get_session_name()
        self.client = TelegramClient(self.session_name, self.api_id, self.api_hash)
        self.ensure_authorized()

    def get_session_name(self) -> str:
        """Generate a unique session name to avoid conflicts."""
        h = hashlib.sha256()
        h.update(random.randint(0, 1000000).to_bytes(4, "big"))
        return h.hexdigest()[:8]

    def ensure_authorized(self):
        """Ensure the client is authorized, handle login flow interactively."""
        self.client.start()
        if not self.client.is_user_authorized():
            phone = input("Enter your phone number (e.g., +1234567890): ")
            print("Sending code request...")
            self.client.send_code_request(phone)
            try:
                code = input("Enter the code you received: ")
                self.client.sign_in(phone, code)
            except SessionPasswordNeededError:
                password = input("Two-step verification is enabled. Enter your password: ")
                self.client.sign_in(password=password)

    def list_available_channels(self) -> list:
        """Return list of dicts, containing data about all available channels you joined."""
        data = []
        for dialog in self.client.iter_dialogs():
            if isinstance(dialog.entity, Channel):
                entry = {
                    "title": dialog.entity.title,
                    "id": dialog.entity.id
                }
                data.append(entry)
        return data

    def dump_channel_by_id(self, channel_id: int) -> None:
        """Dump all messages and replies from a channel by its ID, including attached photos."""
        try:
            channel = self.client.get_entity(PeerChannel(channel_id=channel_id))
            print(f"Dumping channel: {channel.title} (ID: {channel.id})")
        except Exception as e:
            print(f"Error fetching channel by ID: {e}")
            return

        media_path_template = os.path.join(self.media_dir, f"{channel.id}_{{msg_id}}_{{ext}}")

        with open(self.output_file, 'w', encoding='utf-8') as f:
            try:
                for message in self.client.iter_messages(channel, reverse=True):  # Oldest first
                    try:
                        # Prepare message entry
                        message_entry = {
                            'id': message.id,
                            'date': str(message.date),
                            'sender_id': getattr(message, 'sender_id', None),
                            'text': message.message if message.message else '',
                            'media_path': None,
                            'replies': []
                        }

                        # Download photo if exists
                        if message.photo:
                            photo_path = media_path_template.format(msg_id=message.id, ext="jpg")
                            try:
                                message.download_media(photo_path)
                                message_entry['media_path'] = photo_path
                                print(f"Downloaded photo: {photo_path}")
                            except Exception as e:
                                print(f"Error downloading media for message {message.id}: {e}")
                                message_entry['media_path'] = "ERROR"

                        # Fetch replies
                        reply_count = 0
                        try:
                            replies = self.client.iter_messages(channel, reply_to=message.id, reverse=True)
                            for reply in replies:
                                reply_entry = {
                                    'id': reply.id,
                                    'date': str(reply.date),
                                    'sender_id': getattr(reply, 'sender_id', None),
                                    'text': reply.message if reply.message else '',
                                    'media_path': None
                                }

                                if reply.photo:
                                    reply_photo_path = media_path_template.format(msg_id=f"reply_{reply.id}", ext="jpg")
                                    try:
                                        reply.download_media(reply_photo_path)
                                        reply_entry['media_path'] = reply_photo_path
                                    except Exception as e:
                                        print(f"Error downloading reply photo {reply.id}: {e}")
                                        reply_entry['media_path'] = "ERROR"

                                message_entry['replies'].append(reply_entry)
                                reply_count += 1
                                time.sleep(0.1)  # Rate limiting
                        except Exception as e:
                            print(f"Error fetching replies for message {message.id}: {e}")

                        # Write to file
                        f.write(json.dumps(message_entry, ensure_ascii=False) + '\n')
                        f.flush()
                        print(f"Processed message {message.id} ({reply_count} replies)")
                        time.sleep(0.1)  # Rate limiting

                    except FloodWaitError as fwe:
                        print(f"FloodWaitError: Waiting for {fwe.seconds} seconds...")
                        time.sleep(fwe.seconds + 1)
                    except Exception as e:
                        print(f"Error processing message {message.id}: {e}")

            except Exception as e:
                print(f"Error during message iteration: {e}")

        print(f"Channel dump completed. Output saved to '{self.output_file}'.")
