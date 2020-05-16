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
    img.save("stats.png")
    photo = upload.photo_messages(['stats.png'])
    vk_photo_id = f"photo{photo[0]['owner_id']}_{photo[0]['id']}_{photo[0]['access_key']}"
    vk.messages.send(peer_id=user_id,
                     message='Стата по вашему запросу',
                     random_id=random.randint(0, 2 ** 64),
                     attachment=vk_photo_id
                     )


def weather():
    try:
        city_id = vk_response[0]['city']['id']
        city_response = vk_user.database.getCitiesById(city_ids=[city_id])
        city_name = city_response[0]['title']
        params = {
            'q': city_name,
            'units': 'metric',
            'appid': '5ffd78188a2352cc9d6281eb6b29f0ff'
        }
        response = requests.get("https://api.openweathermap.org/data/2.5/weather", params=params)
        json_response = response.json()
        temperature = json_response['main']['temp']
        feels_like = json_response['main']['feels_like']
        vk.messages.send(user_id=user_id,
                         message=f"Температура на {value}: {int(temperature)}℃, ощущается как {int(feels_like)}℃.",
                         random_id=random.randint(0, 2 ** 64))
    except KeyError:
        vk.messages.send(user_id=user_id,
                         message="У вас нет города в профиле :(",
                         random_id=random.randint(0, 2 ** 64))


if __name__ == "__main__":
    vk_session = vk_api.VkApi(
        token='1a5fcaf38c53b866a6c3d8caf7ef788f91365a47d13dc5081b5f9481629c87403ae6138cab5a613fd86fc')
    vk_user_session = vk_api.VkApi("+79244364735", "MathTop666")
    try:
        vk_user_session.auth(token_only=True)
    except vk_api.AuthError as error_msg:
        print(error_msg)
    longpoll = VkBotLongPoll(vk_session, 195364115)
    print('Бот активировался')
    vk = vk_session.get_api()
    vk_user = vk_user_session.get_api()
    upload = vk_api.VkUpload(vk_session)
    for event in longpoll.listen():
        if event.type == VkBotEventType.MESSAGE_NEW:
            msg_text = event.obj.message['text']
            user_id = event.obj.message['from_id']
            timestamp = event.obj.message['date']
            value = datetime.fromtimestamp(timestamp)
            vk_response = vk.users.get(user_ids=[user_id], fields="city, country")
            if msg_text == "/weather":
                weather()
            elif msg_text == '/covid':
                covid_stat()
            elif msg_text == '/help':
                vk.messages.send(user_id=user_id,
                                 message="/weather - погода по городу в профиле;\n/covid - без комментариев.",
                                 random_id=random.randint(0, 2 ** 64))
            else:
                vk.messages.send(user_id=user_id,
                                 message="Я не знаю, что вам сказать:\nвведите /help для получения списка команд.",
                                 random_id=random.randint(0, 2 ** 64))
