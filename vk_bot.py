import vk_api
import vk_api.bot_longpoll as botlp

vk_session = vk_api.VkApi(token=TOKEN)
longpoll = botlp.VkBotLongPoll(vk_session, GROUP_ID)
for event in longpoll.listen():
    if event.type == botlp.VkBotEventType.MESSAGE_NEW:
        print(event.obj.message['text'])
        # vk = vk_session.get_api()
        # vk.messages.send(user_id=event.obj.message['from_id'],
                        # message=event.obj.message['text'],
                        # random_id=random.randint(0, 2 ** 64))
