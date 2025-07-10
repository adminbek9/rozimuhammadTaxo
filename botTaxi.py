import hashlib
from telethon import TelegramClient, events

api_id = 22731419
api_hash = '2e2a9ce500a5bd08bae56f6ac2cc4890'

client = TelegramClient('taxi_session', api_id, api_hash)

# Kalit so'zlar
keywords = [
    'odam bor', 'odam bor 1', 'odam bor 1ta', 'odam bor 1 ta',
    'rishtonga odam bor', 'toshkentga odam bor',
    'pochta bor', 'rishtonga pochta bor', 'rishtondan pochta bor',
    'toshkentga pochta bor', 'toshkentdan pochta bor',
    'ketadi', 'ketishadi', 'ketishi kerak', 'ketishi', 'ayol kishi ketadi',
    'mashina kerak', 'mashina kere', 'mashina kerek',
    'kampilek odam bor', 'kompilekt odam bor', 'komplek odam bor'
]

# Qayerga yuboriladi
target_chat = '@rozimuhammadTaxi'

# Yuborilgan xabarlarning hash qiymatlari
seen_messages = set()

def get_md5(text):
    return hashlib.md5(text.encode('utf-8')).hexdigest()

@client.on(events.NewMessage(incoming=True))
async def handler(event):
    try:
        if event.is_private:
            return

        text = event.raw_text
        if not text:
            return

        text_lower = text.lower()
        if not any(keyword in text_lower for keyword in keywords):
            return

        # Xabar hash ni tekshiramiz
        text_hash = get_md5(text)
        if text_hash in seen_messages:
            return  # Allaqachon yuborilgan, o‘tkazamiz
        seen_messages.add(text_hash)

        chat = await event.get_chat()

        if hasattr(chat, 'username') and chat.username:
            chat_link = f"https://t.me/{chat.username}/{event.message.id}"
            chat_name = chat.title or chat.username
            source_line = f"{chat_name} ({chat_link})"
        else:
            if hasattr(event.sender, 'username') and event.sender.username:
                source_line = f"@{event.sender.username} (Link yo‘q)"
            else:
                source_line = "Shaxsiy yoki yopiq guruh (username yo‘q)"

        message_to_send = (
            f"🚖 <b>Xabar topildi!</b>\n\n"
            f"📄 <b>Matn:</b>\n{text}\n\n"
            f"📍 <b>Qayerdan:</b>\n{source_line}\n\n"
            f"🤝 <i>Hamkorlik va do‘stlik yo‘lidamiz. Siz bilan birgamiz!</i>"
        )

        await client.send_message(target_chat, message_to_send, parse_mode='html')
        print("✅ Yuborildi:", text[:50])

    except Exception as e:
        print("❌ Xatolik:", e)

print("🚕 Taxi bot ishga tushdi...")
client.start()
client.run_until_disconnected()