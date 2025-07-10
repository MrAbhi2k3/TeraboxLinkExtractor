# 📦 TeraBox Direct Link Extractor Bot

A simple Telegram bot to extract **direct download links** from shared TeraBox URLs.

## 🚀 Features

- Supports multiple TeraBox-related domains:
  - `terabox.com`, `1024tera.com`, `terasharelink.com`, `nephobox.com`, `1024terabox.com`, `4funbox.com`, `mirrobox.com`, `momerybox.com`, `teraboxapp.com`
- Automatically parses and fetches direct links from shared file pages.
- Handles retries and errors gracefully.
- Telegram bot interface – easy to use and share.

## ⚙️ Requirements

- Python 3.7+
- Telegram bot token, API ID, and API hash
- TeraBox `ndus` Cookie

## 📦 Installation

1. **Clone this repository:**
   ```bash
   git clone https://github.com/MrAbhi2k3/TeraboxLinkExtractor.git
   cd TeraboxLinkExtractor
   ```

2. **Install dependencies:**
   ```bash
   pip install aiohttp telethon beautifulsoup4 lxml
   ```

3. **Set your environment variables or define the following values in your script:**
   ```python
   TERA_COOKIE = 'your_ndus_cookie_here'
   api_id = YOUR_TELEGRAM_API_ID
   api_hash = 'YOUR_TELEGRAM_API_HASH'
   bot_token = 'YOUR_BOT_TOKEN'
   ```

## 💡 Usage

1. **Run the bot:**
   ```bash
   python main.py
   ```

2. **In Telegram:**
   - Send `/start` to the bot
   - Paste a **TeraBox share link**, such as:
     ```
     https://terabox.com/s/1a2b3c4d5e
     ```
   - The bot will reply with a **direct download link**

## ⚠️ Limitations

- Only one file per share link is supported.
- Folders and multiple files in one link are **not supported**.
- Requires a valid TeraBox `ndus` cookie. Public links may still require authentication depending on share settings.

## 📜 Example

**Input:**
```
https://terabox.com/s/1a2b3c4d5e
```

**Output:**
```
✅ Direct download link:

https://d.terabox.com/file/abcd1234efgh5678...
```

## 🛡 Disclaimer

This tool is provided for educational and personal use only. The developer is not responsible for any misuse or violations of TeraBox's terms of service.

---
