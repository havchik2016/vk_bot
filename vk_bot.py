import requests
import random
from datetime import datetime
import vk_api
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType

def weather():
    vk_session = vk_api.VkApi(token='1a5fcaf38c53b866a6c3d8caf7ef788f91365a47d13dc5081b5f9481629c87403ae6138cab5a613fd86fc')
    vk_user_session = vk_api.VkApi("+79244364735", "MathTop666")
    try:
        vk_user_session.auth(token_only=True)
    except vk_api.AuthError as error_msg:
        print(error_msg)
    longpoll = VkBotLongPoll(vk_session, 195364115)
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
                    f"https://api.openweathermap.org/data/2.5/weather?q={city_name}&units=metric&appid=5ffd78188a2352cc9d6281eb6b29f0ff")
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