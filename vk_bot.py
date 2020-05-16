import vk_api
import vk_api.bot_longpoll as botlp
import requests
import bs4
from PIL import ImageDraw, Image, ImageFont


# vk_session = vk_api.VkApi(token=TOKEN)
# longpoll = botlp.VkBotLongPoll(vk_session, GROUP_ID)
# for event in longpoll.listen():
#     if event.type == botlp.VkBotEventType.MESSAGE_NEW:
#         print(event.obj.message['text'])
#         # vk = vk_session.get_api()
#         # vk.messages.send(user_id=event.obj.message['from_id'],
#         # message=event.obj.message['text'],
#         # random_id=random.randint(0, 2 ** 64))


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


covid_stat()
