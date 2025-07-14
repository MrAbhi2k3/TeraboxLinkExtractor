import re
import aiohttp
import asyncio
from bs4 import BeautifulSoup
from telethon import TelegramClient, events, Button

api_id = 123456               # Put your actual API ID
api_hash = 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxx'  # Put with your actual API Hash
bot_token = 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxx'  # Put with your actual Bot Token

TERA_COOKIE = "xxxxxxxxxxxxxxxxxxxxxxxxxxxxx"  # Put with your actual TeraBox cookie

TERABOX_DOMAINS = [
    "terabox.com", "1024tera.com", "terasharelink.com", "nephobox.com",
    "1024terabox.com", "4funbox.com", "mirrobox.com", "momerybox.com", "teraboxapp.com"
]

class DDLException(Exception):
    pass

async def fetch(session, url):
    for _ in range(5):
        try:
            async with session.get(url) as response:
                return await response.text(), str(response.url)
        except Exception:
            await asyncio.sleep(1)
    raise DDLException(f"Failed to fetch {url}")

async def fetch_json(session, url):
    for _ in range(5):
        try:
            async with session.get(url) as response:
                return await response.json()
        except Exception:
            await asyncio.sleep(1)
    raise DDLException(f"Failed to fetch JSON from {url}")

async def terabox(url: str) -> str:
    headers = {
        "Cookie": f"ndus={TERA_COOKIE}",
        "User-Agent": "Mozilla/5.0"
    }
    async with aiohttp.ClientSession(headers=headers) as session:
        _, final_url = await fetch(session, url)
        key = final_url.split("?surl=")[-1]
        html, _ = await fetch(session, f"http://www.terabox.com/wap/share/filelist?surl={key}")
        soup = BeautifulSoup(html, "lxml")
        jsToken = next(
            (fs.string.split("%22")[1] for fs in soup.find_all("script")
             if fs.string and fs.string.startswith("try {eval(decodeURIComponent") and "%22" in fs.string),
            None
        )
        if not jsToken:
            raise DDLException("jsToken not found in page")

        result = await fetch_json(session, f"https://www.terabox.com/share/list?app_id=250528&jsToken={jsToken}&shorturl={key}&root=1")
        if result["errno"] != 0:
            raise DDLException(f"{result['errmsg']} - Check cookie")

        items = result.get("list", [])
        if len(items) != 1:
            raise DDLException("Only one file allowed, or none found")

        item = items[0]
        if item.get("isdir") != "0":
            raise DDLException("Folders are not supported")

        dlink = item.get("dlink")
        if not dlink:
            raise DDLException("Direct link not found")

        return dlink

client = TelegramClient('terabox_bot', api_id, api_hash).start(bot_token=bot_token)

domain_pattern = "|".join(re.escape(domain) for domain in TERABOX_DOMAINS)
url_pattern = re.compile(rf'https?://(?:www\.)?(?:{domain_pattern})(?:/s/\S+|/wap/share/filelist\?surl=\S+)', re.IGNORECASE)

@client.on(events.NewMessage)
async def handle_messages(event):
    matches = url_pattern.findall(event.raw_text)
    if not matches:
        return

    for url in matches:
        msg = await event.reply("🔍 Extracting direct download link...")
        try:
            link = await terabox(url)
            await msg.delete()
            await event.reply(
                f"✅ Direct download link:\n\n{link}",
                buttons=[Button.url("🌐 Source Code", "https://github.com/MrAbhi2k3/TeraboxLinkExtractor")]
            )
        except Exception as e:
            await msg.edit(f"❌ Error: {str(e)}")

@client.on(events.NewMessage(pattern='/start'))
async def start_cmd(event):
    await event.reply(
        "👋 Send a TeraBox share URL and I will extract the direct download link.",
        buttons=[
            [Button.url("📢 Channel", "https://teleroidgroup.t.me"), Button.url("🌐 Source Code", "https://github.com/MrAbhi2k3/TeraboxLinkExtractor")]
        ]
    )

print("Bot Started...")
client.run_until_disconnected()
