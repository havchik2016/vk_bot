import requests
import random
from datetime import datetime
import vk_api
from vk_api import audio, keyboard
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
        city_name = " ".join(msg_text_parts[1:])
        params = {
            'q': city_name,
            'units': 'metric',
            'appid': 'apikey'
        }
        response = requests.get("https://api.openweathermap.org/data/2.5/weather", params=params)
        json_response = response.json()
        temperature = json_response['main']['temp']
        feels_like = json_response['main']['feels_like']
        sunrise, sunset = datetime.fromtimestamp(
            json_response['sys']['sunrise'] - 36000 + json_response['timezone']), datetime.fromtimestamp(
            json_response['sys']['sunset'] - 36000 + json_response['timezone'])
        # sunrise.replace(hour=sunrise.hour - (10 - json_response['timezone'] // (60 ** 2)))
        # sunset.replace(hour=sunset.hour - (10 - json_response['timezone'] // (60 ** 2)))
        wind = json_response['wind']['speed']
        ico = json_response['weather'][0]['icon']
        icon = open('icon.png', 'wb')
        icon.write(requests.get(f"http://openweathermap.org/img/wn/{ico}@2x.png").content)
        icon.close()
        ico = Image.open('icon.png')
        resized_ico = ico.resize((400, 400), Image.ANTIALIAS)
        fn_main = ImageFont.truetype('14155.ttf', 136)
        fn_sunrise = ImageFont.truetype('14155.ttf', 113)
        fn_date = ImageFont.truetype('14155.ttf', 82)
        color = (0, 0, 0)
        img = Image.open('weather.png')
        draw = ImageDraw.Draw(img)
        draw.text((129, 906), f'Температура воздуха: {int(temperature)}°', font=fn_main, fill=color)
        draw.text((129, 1077), f'RealFeel®: {int(feels_like)}°', font=fn_main, fill=color)
        draw.text((129, 1244), f'Скорость ветра: {wind} м/с', font=fn_main, fill=color)
        draw.text((129, 1440), f"Рассвет: {':'.join(str(sunrise.time()).split(':')[:-1])}", font=fn_sunrise, fill=color)
        draw.text((1253, 1440), f"Закат: {':'.join(str(sunset.time()).split(':')[:-1])}", font=fn_sunrise, fill=color)
        draw.text((1700, 604), value.date().strftime('%d.%m'), font=fn_date, fill=color)
        draw.text((438, 752), json_response['weather'][0]['description'], font=fn_date, fill=color)
        img.paste(resized_ico, (80, 530), resized_ico)
        img.save("weather_stat.png")
        photo = upload.photo_messages(['weather_stat.png'])
        vk_photo_id = f"photo{photo[0]['owner_id']}_{photo[0]['id']}_{photo[0]['access_key']}"
        vk.messages.send(user_id=user_id,
                         message='Держи, хорошего дня:)',
                         attachment=vk_photo_id,
                         random_id=random.randint(0, 2 ** 64))
    except KeyError:
        vk.messages.send(user_id=user_id,
                         message="Город не найден :(",
                         random_id=random.randint(0, 2 ** 64))


def playlist():
    try:
        audio = vk_api.audio.VkAudio(user_session, convert_m3u8_links=True)
        spisok = list(audio.get(owner_id=user_id))
        random.shuffle(spisok)
        songs = spisok[:5]
        songs_ids = ','.join([f"audio{song['owner_id']}_{song['id']}" for song in songs])
        vk.messages.send(user_id=user_id,
                         random_id=random.randint(0, 2 ** 64),
                         message='Держи небольшой плейлист',
                         attachment=songs_ids)
    except vk_api.exceptions.AccessDenied:
        vk.messages.send(user_id=user_id,
                         random_id=random.randint(0, 2 ** 64),
                         message='У вас закрыт плейлист :(')


if __name__ == "__main__":
    vk_session = vk_api.VkApi(
        token='token')
    user_session = vk_api.VkApi(login='login', password='password')
    user_session.auth()
    longpoll = VkBotLongPoll(vk_session, 195364115)
    print('Бот активировался')
    vk = vk_session.get_api()
    upload = vk_api.VkUpload(vk_session)
    for event in longpoll.listen():
        if event.type == VkBotEventType.MESSAGE_NEW:
            clear_text = event.obj.message['text']
            msg_text_parts = clear_text.strip().split()
            command = msg_text_parts[0]
            user_id = event.obj.message['from_id']
            timestamp = event.obj.message['date']
            value = datetime.fromtimestamp(timestamp)
            if command == "/weather":
                weather()
            elif command == '/covid':
                covid_stat()
            elif command in ['/help', 'Начать']:
                vk.messages.send(user_id=user_id,
                                 message="/weather <city_name> - погода по городу city_name;\n/covid - без комментариев;\n/playlist - рандомные 5 песен из Вашего плейлиста ВК, если он открыт (или меньше, если у вас их меньше);\n/help - это сообщение.",
                                 random_id=random.randint(0, 2 ** 64))
            elif command == '/playlist':
                playlist()
            else:
                vk.messages.send(user_id=user_id,
                                 message="Я не знаю, что вам сказать:\nвведите /help для получения списка команд.",
                                 random_id=random.randint(0, 2 ** 64))
