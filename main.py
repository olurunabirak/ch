from pyrogram import Client, filters
from pyrogram.raw.functions.messages import Report

api_id =   
api_hash = " "  
session_string = " "

app = Client("spam", api_id=api_id, api_hash=api_hash, session_string=session_string)

@app.on_message(filters.command("spam"))
async def report_spam(client, message):
    try:
        if message.reply_to_message:  
            chat = message.reply_to_message.chat
            message_id = message.reply_to_message.id

            if message.reply_to_message.forward_from_chat:
                chat = message.reply_to_message.forward_from_chat

            peer = await client.resolve_peer(chat.id)
            reason = "personal details"

            for _ in range(10):  
                await client.invoke(Report(peer=peer, id=[message_id], reason=reason, message=""))

            if chat.username:
                msg_link = f"https://t.me/{chat.username}/{message_id}"
            else:
                msg_link = f"https://t.me/c/{str(chat.id)[4:]}/{message_id}"

            await message.edit_text(f"✅ mesaj şikayet edildi: [tıkla]({msg_link}) (sebep: {reason})", disable_web_page_preview=True)

        elif len(message.command) > 1:
            target_id = message.command[1]

            if not target_id.lstrip('-').isdigit():
                await message.edit_text("❌ hata: geçersiz kanal ID!")
                return

            target_id = int(target_id)
            peer = await client.resolve_peer(target_id)
            reason = "personal details"

            for _ in range(10):  
                await client.invoke(Report(peer=peer, id=[], reason=reason, message=""))

            await message.edit_text(f"✅ {target_id} başarıyla şikayet edildi! (sebep: {reason})")

        else:
            await message.edit_text("❌ kullanım: /spam <kanal_id> veya bir mesaja yanıt verin!")

    except Exception as e:
        await message.edit_text(f"❌ hata: {str(e)}")

app.run()
