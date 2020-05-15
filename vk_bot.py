import vk_api
import vk_api.bot_longpoll as botlp

vk_session = vk_api.VkApi(token='07d398ad29a6c0f79c16e501a0308fb8723577568a1123b8dcab81f40dbec2123b67151c861949535872a')
longpoll = botlp.VkBotLongPoll(vk_session, 195364115)
for event in longpoll.listen():
    if event.type == botlp.VkBotEventType.MESSAGE_NEW:
        print(event.obj.message['text'])
        # vk = vk_session.get_api()
        # vk.messages.send(user_id=event.obj.message['from_id'],
                        # message=event.obj.message['text'],
                        # random_id=random.randint(0, 2 ** 64))
