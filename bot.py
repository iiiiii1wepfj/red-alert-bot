from pyrogram import Client, filters
import requests, time, threading, json


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


@app.on_message(filters.command("start"))
def pvtmsg(c, m):
    m.reply("הבוט נוצר על ידי @itayki ופועל בערוץ https://t.me/redalertilchannel")


class siren_listener:
    def __init__(self, callback):
        self.callback = callback
        self.running = True
        self.last_data = ""
        self.thread = threading.Thread(target=self.__listener__)
        self.thread.start()

    def stop(self):
        self.running = False

    def __listener__(self):
        while self.running:
            try:
                time.sleep(2)
                response = requests.get("https://www.oref.org.il/WarningMessages/Alert/alerts.json", headers={"X-Requested-With":"XMLHttpRequest","Referer":"https://www.oref.org.il/"})
                res_content = (response.content).decode("utf-8-sig")
                if len(res_content) > 4 and response.status_code == 200 and res_content != self.last_data:
                    alert_data = json.loads(res_content)
                    threading.Thread(target=self.callback, args=(alert_data,)).start()
                    self.last_data = res_content
            except:
                pass


def on_siren(sirens):
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
            
        a = app.send_message(
            main_channel,
            f"🔴 <b>התרעת פיקוד העורף</b>\n\n<b>סוג:</b> {alert_category}\n<b>עיר:</b> {i}\n<b>אזור:</b> {area_for_the_city}\n<b>זמן (רלוונטי במקרה של ירי טילים ורקטות):</b> {countdown_for_the_city}\n<b>הנחיות:</b> {pikud_desc}\n\n<b>ערוץ @redalertilchannel</b>",
            disable_web_page_preview=True,
        )
        for e in chats_to_forward:
            a.forward(e)


siren_listener_handler = siren_listener(on_siren)
app.run()
siren_listener_handler.stop()
