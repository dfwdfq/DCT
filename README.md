# Telegram Channel Dumper (dtc)

A command-line tool to **list and dump messages from Telegram channels**, including text, replies, and attached media.

---

## 🚀 Features

- ✅ List all channels you're part of  
- ✅ Dump full message history from a selected channel  
- ✅ Download attached photos  
- ✅ Save messages in structured JSONL format  
- ✅ Interactive CLI interface with tabular output  

---

## 📦 Requirements

- Python 3.8+
- `telethon` (Telegram API client)
- `pandas` (for table formatting)
- `tabulate` (for prettier output)

---

## ⚙️ Setup

### 1. Create Virtual Environment
```bash
# Create a virtual environment
python3 -m venv venv

# Activate the environment
source venv/bin/activate       # Unix/macOS
# OR
venv\Scripts\activate          # Windows
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

---

## 🔐 Configuration

### 1. Get Telegram API Credentials
Go to [my.telegram.org](https://my.telegram.org) → "API development tools" → Create Application

```bash
export API_ID=your_api_id_here
export API_HASH=your_api_hash_here
```

---

## 📦 Usage

### Run the Tool

```bash
python3 DTC <api_id> <api_hash>
```

Example:

```bash
python3 DTC 1234567 abcdef1234567890abcdef1234567890
```

---

## 🧪 Available Commands

### `list`  
Lists all Telegram channels you're part of:

```
>> list
```

Output:
```
+----+----------------------------+-------------+
|    | name                       | telegram id |
+====+============================+=============+
|  0 | My Favorite Channel        |   123456789 |
+----+----------------------------+-------------+
|  1 | News Channel               |   987654321 |
+----+----------------------------+-------------+
```

### `dump <index>`  
Dumps messages and media from a channel using the list index:

```
>> dump 0
```

Output:
```
Processed message 12345 (3 replies)
Downloaded photo: media/123456789_12345.jpg
Channel dump completed. Output saved to 'output.jsonl'.
```

---

## 📁 Output Structure

### JSONL File (`output.jsonl`)
Each line contains:

```json
{
  "id": 12345,
  "date": "2024-07-01 12:34:56",
  "sender_id": 1122334455,
  "text": "This is a message with photo",
  "media_path": "media/123456789_12345.jpg",
  "replies": [
    {
      "id": 12346,
      "date": "2024-07-01 12:35:01",
      "sender_id": 5544332211,
      "text": "Nice photo!",
      "media_path": null
    }
  ]
}
```

### Media Directory

Photos are saved in `media/` with naming:

```
media/{channel_id}_{msg_id}_reply_{reply_id}.jpg
```

---

## ⚠️ Notes & Best Practices

### Session Management
- Sessions are stored 
- Reuse sessions to avoid re-login and rate limits
- Delete session file to log out

### Rate Limits
- Telegram enforces **strict rate limits**
- Avoid rapid login attempts or spamming requests
- If you hit `FloodWaitError`, wait for the required time

### Security
- Never share `.session` files
- Don't commit API credentials to public repos

---

## 🛠 Example Workflow

```bash
# 0. clone repo
git clone https://github.com/dfwdfq/DCT.git

# 1. cd into directory
cd DCT

# 3. Create and activate virtual environment
python3 -m venv venv
source venv/bin/activate

# 4. Install dependencies
pip install -r dependencies.txt

# 5. get back
cd ..

# 6. Run the tool
python DCT 1234567 abcdef1234567890abcdef1234567890

# 7. In the CLI
>> list
>> dump 0
```




## 🤝 Contributing

Feel free to open issues or PRs for:
- Adding video/media support
- Improving error handling
- Adding CLI argument parsing
- Supporting config files

---

## 📬 Contact

For questions or feedback: [haskel.list@yandex.ru]