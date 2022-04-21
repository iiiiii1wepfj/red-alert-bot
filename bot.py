from pyrogram import Client, idle, filters
import pikudhaoref

api_id: int = 0  # Put your API ID here
api_hash: str = ""  # Put your API hash here
bot_token: str = ""  # Put your bot token here


app = Client(
    "redalertbot",
    api_id=api_id,
    api_hash=api_hash,
    bot_token=bot_token,
)
chats_to_forward = []
main_channel = "-100"

client = pikudhaoref.AsyncClient(update_interval=2, loop=app.loop)


@app.on_message(filters.command("start"))
async def pvtmsg(c, m):
    await m.reply("הבוט נוצר על ידי @itayki ופועל בערוץ https://t.me/redalertil2021")


@client.event()
async def on_siren(sirens):
    for i in sirens:
        city_name = i.city.name.he
        city_countdown = i.city.countdown.he
        city_zone = i.city.zone.he or "לא ידוע"
        if not i.city.zone.he:
            city_countdown = "לא ידוע"

        a = await app.send_message(
            main_channel,
            f"🔴 <b>צבע אדום</b>\n\n<b>עיר:</b> {city_name}\n<b>אזור:</b> {city_zone}\n<b>זמן:</b> {city_countdown}\n\n<b>ערוץ https://t.me/redalertil2021</b>",
            disable_web_page_preview=True,
        )
        for e in chats_to_forward:
            await a.forward(e)


async def main():
    await app.start()
    await client.initialize()
    await idle()
    client.closed = True
    await client.http.session.close()
    await app.stop()


app.loop.run_until_complete(main())
