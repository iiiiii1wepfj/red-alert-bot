from pyrogram import Client, filters
import pikudhaoref

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
main_channel = "-100"


client = pikudhaoref.SyncClient(update_interval=2)


@app.on_message(filters.command("start"))
def pvtmsg(c, m):
    m.reply("הבוט נוצר על ידי @itayki ופועל בערוץ https://t.me/redalertil2021")


@client.event()
def on_siren(sirens):
    for i in sirens:
        try:
            thecityname = i.city.name.he
            try:
                thezonename = i.city.zone.he
                thecountdownhebrew = i.city.countdown.he
            except AttributeError:
                thecityname = i.city
                thezonename = ""
                thecountdownhebrew = ""
            except:
                continue
        except AttributeError:
            thecityname = i.city
            thezonename = ""
            thecountdownhebrew = ""
        except:
            continue
        a = app.send_message(
            main_channel,
            f"צבע אדום ב: {thecityname}\n\n אזור: {thezonename}\n\n זמן: {thecountdownhebrew}\n\nערוץ https://t.me/redalertil2021",
            disable_web_page_preview=True,
        )
        for e in chats_to_forward:
            a.forward(e)
        del thecityname, thezonename, thecountdownhebrew


app.run()
