import os
import configparser
class BotConfig:
    def __init__(self) -> None:
        config_path=os.path.join(os.path.dirname(__file__), 'bot_config.ini')
        raw_config = configparser.ConfigParser()  # создаём объекта парсера
        raw_config.read(config_path)  # читаем конфиг
        # Вставляем api_id и api_hash
        self.api_id = raw_config["bot"]["api_id"]
        self.api_hash = raw_config["bot"]["api_hash"]
        self.token = raw_config["bot"]["token"]
        self.group_link = raw_config["bot"]["adv_group"]
        self.admins = []
        for admin in raw_config["admins"].values():
            self.admins.append(admin)

class SenderConfig:
    def __init__(self) -> None:
        config_path=os.path.join(os.path.dirname(__file__), 'sender_config.ini')
        raw_config = configparser.ConfigParser()  # создаём объекта парсера
        raw_config.read(config_path)  # читаем конфиг

        self.group_list_keyword = raw_config["sender"]["group_list_keyword"]
        self.adv_post_keyword = raw_config["sender"]["adv_post_keyword"]
        self.debug=raw_config["sender"]["debug"]

    def set_config(self, key:str ,value:str):
        config_path=os.path.join(os.path.dirname(__file__), 'sender_config.ini')
        config = configparser.ConfigParser()  # создаём объекта парсера
        config.read(config_path)  # читаем конфиг  
        # Меняем значения из конфиг. файла.
        config.set("sender", key, value)    
        # Вносим изменения в конфиг. файл.
        with open(config_path, "w") as config_file:
            config.write(config_file)
        self.__init__()
        res = "Параметры конфига:\n" 
        res += f"Поиска групп по '{self.group_list_keyword}'\n"  
        res += f"Поиск рекламы по '{self.adv_post_keyword}'\n"  
        res += f"Отладка:{self.debug}\n"  
        return res    