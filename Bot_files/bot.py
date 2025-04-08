import requests
import os

""""
#tt video downloader not finished yet so here
you can get random image of cute cats

nfactorial please notice me!
"""

BOT_TOKEN = os.environ.get("BOT_TOKEN")

print(BOT_TOKEN)

API_URL = 'https://api.telegram.org/bot'

offset = -2

def get_image():

    get_img_responce = requests.get("https://api.thecatapi.com/v1/images/search")

    image_url = get_img_responce.json()[0]["url"]

    return image_url


while True:


    updates = requests.get(f'{API_URL}{BOT_TOKEN}/getUpdates?offset={offset + 1}').json()



    if updates["result"]:
        for result in updates["result"]:
            offset = result['update_id']
            chat_id = result['message']['from']['id']

            url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendPhoto?chat_id={chat_id}"

            payload = {
                "chat_id": chat_id,
                "photo": get_image(),
            }

            requests.post(url, data=payload)







