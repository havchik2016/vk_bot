import requests
import random
from datetime import datetime
import vk_api
import bs4
from PIL import ImageDraw, Image, ImageFont
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType


def covid_stat():
    rus_req = requests.get('https://www.worldometers.info/coronavirus/country/russia/')
    soap2 = bs4.BeautifulSoup(rus_req.content, 'lxml')
    nt = ImageFont.truetype('16546.ttf', 35)
    rus_stats = [i.text.strip().replace(',', ' ') for i in soap2.find_all('div', {'class': 'maincounter-number'})]
    img = Image.open('11.png')
    draw = ImageDraw.Draw(img)
    for cords, text in [[(237, 200), rus_stats[0]], [(390, 360), rus_stats[1]], [(482, 520), rus_stats[2]]]:
        draw.text(cords, text, font=nt, fill=(0, 0, 0))
    img.show()


def weather():
    vk_session = vk_api.VkApi(token=TOKEN)
    vk_user_session = vk_api.VkApi(login, password)
    try:
        vk_user_session.auth(token_only=True)
    except vk_api.AuthError as error_msg:
        print(error_msg)
    longpoll = VkBotLongPoll(vk_session, GROUP_ID)
    print('Бот активировался')
    for event in longpoll.listen():
        if event.type == VkBotEventType.MESSAGE_NEW:
            user_id = event.obj.message['from_id']
            timestamp = event.obj.message['date']
            value = datetime.fromtimestamp(timestamp)
            vk = vk_session.get_api()
            vk_user = vk_user_session.get_api()
            vk_response = vk.users.get(user_ids=[user_id], fields="city, country")
            try:
                city_id = vk_response[0]['city']['id']
                city_response = vk_user.database.getCitiesById(city_ids=[city_id])
                city_name = city_response[0]['title']
                response = requests.get(
                    f"https://api.openweathermap.org/data/2.5/weather?q={city_name}&units=metric&appid=yourkey")
                json_response = response.json()
                temperature = json_response['main']['temp']
                feels_like = json_response['main']['feels_like']
                vk.messages.send(user_id=user_id,
                                 message=f"Температура на {value}: {int(temperature)}℃, ощущается как {int(feels_like)}℃.",
                                 random_id=random.randint(0, 2 ** 64))
            except KeyError:
                vk.messages.send(user_id=user_id,
                                 message="У вас нет города :(",
                                 random_id=random.randint(0, 2 ** 64))


if __name__ == "__main__":
    weather()
