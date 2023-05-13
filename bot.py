from pyrogram import Client, filters, idle
import aiohttp, time, threading, json, asyncio, requests


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
main_channel = 0


pikud_locations_data = (requests.get("https://www.tzevaadom.co.il/static/cities.json")).json()
cities_data = pikud_locations_data["cities"]
areas_data = pikud_locations_data["areas"]
countdown_data = pikud_locations_data["countdown"]


@app.on_message(filters.command("start"))
async def pvtmsg(c, m):
    await m.reply("הבוט נוצר על ידי @itayki ופועל בערוץ https://t.me/redalertilchannel")


class siren_listener:
    def __init__(self, callback):
        self.callback = callback
        self.running = True
        self.last_data = []
        asyncio.create_task(self.__listener__())

    def stop(self):
        self.running = False

    async def __listener__(self):
        async with aiohttp.ClientSession(headers={"X-Requested-With":"XMLHttpRequest","Referer":"https://www.oref.org.il/"}) as session:
            while self.running:
                try:
                    await asyncio.sleep(2)
                    async with session.get("https://www.oref.org.il/WarningMessages/Alert/alerts.json") as response:
                        res_content = await response.text()
                        if len(res_content) > 4 and response.status == 200 and res_content:
                            alert_data = json.loads(res_content.encode().decode('utf-8-sig'))
                            cities_list = alert_data["data"]
                            filter_alerts = list({area for (area) in (cities_list) if (area not in self.last_data) or (cities_list.count(area) > 1 and self.last_data.count(area) == 1)})
                            filter_alerts.sort()
                            self.last_data = list(cities_list)
                            alert_data["data"] = filter_alerts
                            print(alert_data)
                            if len(filter_alerts) == 0:
                                continue

                            asyncio.create_task(self.callback(alert_data))
                        elif res_content != "" and self.last_data != []:
                            self.last_data = []
                except aiohttp.client_exceptions.ClientConnectorError:
                    pass


async def on_siren(sirens):
    print(sirens)
    for i in sirens["data"]:
        city_info = cities_data[i]
        try:
            alert_category = sirens["title"]
        except:
            alert_category = "לא ידוע"
        try:
            countdown_for_the_city = countdown_data[str(city_info["countdown"])]["he"]
        except:
            countdown_for_the_city = "לא ידוע"
        try:
            area_for_the_city = areas_data[str(city_info["area"])]["he"]
        except:
            area_for_the_city = "לא ידוע"
        try:
            pikud_desc = sirens["desc"]
        except:
            pikud_desc = "לא ידוע"
            
        a = await app.send_message(
            main_channel,
            f"🔴 <b>התרעת פיקוד העורף</b>\n\n<b>סוג:</b> {alert_category}\n<b>עיר:</b> {i}\n<b>אזור:</b> {area_for_the_city}\n<b>זמן (רלוונטי במקרה של ירי טילים ורקטות):</b> {countdown_for_the_city}\n<b>הנחיות:</b> {pikud_desc}\n\n<b>ערוץ @redalertilchannel</b>",
            disable_web_page_preview=True,
        )
        for e in chats_to_forward:
            await a.forward(e)

async def main():
    siren_listener_handler = siren_listener(on_siren)
    await app.start()
    await idle()
    siren_listener_handler.stop()


app.run(main())
