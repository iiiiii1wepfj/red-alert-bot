from pyrogram import Client
import tzevaadom

api_id = your api id
api_hash = "your api hash"
bot_token = "your bot token"

app = Client(
    "redalertbot",
    api_id=api_id,
    api_hash=api_hash,
    bot_token=bot_token,
)
chats_to_forward = []


@app.on_message(pyrogram.filters.command("start"))
def pvtmsg(c, m):
    m.reply("הבוט נוצר על ידי @itayki ופועל בערוץ https://t.me/redalertil2021")


def redalertsendfunc(alert):
    for i in alert:
        alertcityformat, alertzoneformat, alerttimeformat = (
            i["name"],
            i["zone"],
            i["time"],
        )
    a = app.send_message(
        "-1001423200544",
        f"צבע אדום ב: {alertcityformat}\n\n אזור: {alertzoneformat}\n\n זמן: {alerttimeformat}\n\nערוץ https://t.me/redalertil2021",
        disable_web_page_preview=True,
    )
    for e in chats_to_forward:
        a.forward(e)


tzevaadom.alerts_listener(redalertsendfunc)
app.run()
