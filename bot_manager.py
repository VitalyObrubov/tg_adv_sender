import datetime
from telethon import TelegramClient, events
from config import BotConfig, SenderConfig
from adv_sender import adv_send
from logger import * 

bot_config = BotConfig()
sender_config = SenderConfig()

@errors_catching_async
async def start_adv_send(event: events.NewMessage.Event):
    client_adv = TelegramClient('session_name_adv', bot_config.api_id, bot_config.api_hash)
    await client_adv.start()
    start_time = datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S")
    errors = await adv_send(client_adv)    
    end_time = datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S")

    log = f"Отправка начата в {start_time}\n"
    log += "Параметры отправки:\n"
    log += f"   поиск списка групп по '{sender_config.group_list_keyword}'\n"
    log += f"   поиск рекламы по '{sender_config.adv_post_keyword}'\n"
    if errors:
        log += f"Ошибки отправки:\n"
        log += "\n".join(errors)+"\n"
    log += f"Отправка завершена в {end_time}\n" 
    message = await event.respond(log)

@errors_catching_async
@events.register(events.NewMessage(chats=bot_config.admins))
async def handler(event: events.NewMessage.Event): 
    mess_text = event.message.message

    if "/start_task" in mess_text:
        await start_adv_send(event)
    elif "/set_list" in mess_text:
        value = mess_text.split(" ",1)[1]
        txt_config = sender_config.set_config("group_list_keyword",value)
        await event.respond(txt_config)
    elif "/set_adv" in mess_text:
        value = mess_text.split(" ",1)[1]
        txt_config = sender_config.set_config("adv_post_keyword",value)
        await event.respond(txt_config)
    elif "/set_debug" in mess_text:
        value = mess_text.split(" ",1)[1]
        txt_config = sender_config.set_config("debug",value)
        await event.respond(txt_config)
    else:
        answer = """
                    Доступные команды:
                    /start - вызов этого сообщения
                    /start_task - запуск рассылки
                    /set_list <текст> - установить фразу поиска поста со списком групп 
                    /set_adv <текст> - установить фразу поиска поста с рекламой
                    /set_debug <1|0> - включить(выключить режим отладки)
                """
        await event.respond(answer)


if __name__ == '__main__':
    client = TelegramClient('session_name_bot',bot_config.api_id, bot_config.api_hash)
    client.start(bot_token=bot_config.token)
    
    logging.info("Start bot pooling")

    with client:
        # This remembers the events.NewMessage we registered before
        
        client.add_event_handler(handler)
        client.start(bot_token=bot_config.token)
        print('(Press Ctrl+C to stop this)')
        client.run_until_disconnected()
   
