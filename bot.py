from dataclasses import dataclass
from pyrogram import Client, filters, idle
import aiohttp
import asyncio
import json
import requests

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

pikud_locations_data = (requests.get("https://www.tzevaadom.co.il/static/cities.json")).json()
cities_data = pikud_locations_data["cities"]
areas_data = pikud_locations_data["areas"]
countdown_data = pikud_locations_data["countdown"]


point_symbol = u'\u2022'


@dataclass
class City:
	name: str
	category: int


@app.on_message(filters.command("start"))
async def pvtmsg(c, m):
    await m.reply("הבוט נוצר על ידי @itayki ופועל בערוץ https://t.me/redalertilchannel")


class SirenListener:
    def __init__(self, callback):
        self.callback = callback
        self.running = True
        self.last_data = []
        asyncio.create_task(self.listener())

    async def listener(self):
        async with aiohttp.ClientSession(headers={"X-Requested-With":"XMLHttpRequest","Referer":"https://www.oref.org.il/"}) as session:
            while self.running:
                try:
                  await asyncio.sleep(2)
                  async with session.get("https://www.oref.org.il/WarningMessages/Alert/alerts.json") as response:
                    res_content = await response.text()
                    if len(res_content) > 4 and response.status == 200 and res_content:
                        alert_data = json.loads(res_content.encode().decode('utf-8-sig'))
                        cities_list = list(map(lambda i: City(name=i, category=int(alert_data["cat"])), alert_data["data"]))
                        filter_alerts = list(
                        {
                            area.name
                            for area in cities_list
                            if area not in self.last_data
                            or (cities_list.count(area) > 1 and self.last_data.count(area) == 1)
                          }
                        )
                        filter_alerts.sort()
                        self.last_data = cities_list
                        if len(filter_alerts) == 0:
                            continue
                        asyncio.create_task(self.callback(alert_data))
                    elif res_content != "" and self.last_data != []:
                        self.last_data = []

                except Exception as e:
                    print(f"An error occurred: {e}")

    def stop(self):
        self.running = False


async def on_siren(sirens):
    areasdict = {}
    alertcat = sirens["title"]
    alertcatid = int(sirens["cat"])
    pikud_desc = sirens["desc"]
    
    msg_ = []

    for i in sirens["data"]:
        city_info = cities_data[i]
        thearea = areas_data[str(city_info["area"])]["he"]
        if thearea not in areasdict:
            areasdict[thearea] = []
        areasdict[thearea].append(f'{i} ({countdown_data[str(city_info["countdown"])]["he"]})' if alertcatid == 1 else i)
    msg_.append(f"🔴 <b>{alertcat}</b>")
    for k, v in areasdict.items():
        msgtxt = f"\n<b>{k}</b>\n" + "\n".join([f"{point_symbol} {i}" for i in v])
        msg_.append(msgtxt)

    msg_end = f"\n<b>{pikud_desc}</b>\n<b>ערוץ @redalertilchannel</b>"
    msg_.append(msg_end)

    msg = "\n".join(msg_)

    a = await app.send_message(
        main_channel,
        msg,
        disable_web_page_preview=True,
    )

    await asyncio.gather(*[a.forward(e) for e in chats_to_forward])

async def main():
    await app.start()
    siren_listener_handler = SirenListener(on_siren)
    await idle()
    siren_listener_handler.stop()


app.run(main())
