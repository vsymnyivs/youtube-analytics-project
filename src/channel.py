import json
import os
from googleapiclient.discovery import build


class Channel:
    """Класс для ютуб-канала"""
    api_key: str = os.getenv('YOUTUBE_API')

    def __init__(self, channel_id: str) -> None:
        """Экземпляр инициализируется id канала. Дальше все данные будут подтягиваться по API."""
        self.__channel_id = channel_id
        self.channel = self.get_service().channels().list(id=self.__channel_id, part='snippet,statistics').execute()
        self.title = self.channel["items"][0]["snippet"]["title"]
        self.description = self.channel["items"][0]["snippet"]["description"]
        self.url = f"https://www.youtube.com/channel/{self.__channel_id}"
        self.subscriber_count = self.channel["items"][0]["statistics"]["subscriberCount"]
        self.video_count = self.channel["items"][0]["statistics"]["videoCount"]
        self.view_count = self.channel["items"][0]["statistics"]["viewCount"]

    def __str__(self):
        """
        Вывод названия и ссылки на канал
        """
        return f"{self.title}({self.url})"

    def __add__(self, other):
        """
        Метод для операции сложения объектов
        """
        return int(self.subscriber_count) + int(other.subscriber_count)

    def __sub__(self, other):
        """
        Метод для операции вычитания объектов
        """
        return int(self.subscriber_count) - int(other.subscriber_count)

    def __gt__(self, other):
        """
        Метод для операции сравнения "больше" объектов
        """
        return int(self.subscriber_count) > int(other.subscriber_count)

    def __ge__(self, other):
        """
        Метод для операции сравнения "больше или равно" объектов
        """
        return int(self.subscriber_count) >= int(other.subscriber_count)

    def __lt__(self, other):
        """
        Метод для операции сравнения "меньше" объектов
        """
        return int(self.subscriber_count) < int(other.subscriber_count)

    def __le__(self, other):
        """
        Метод для операции сравнения "меньше или равно" объектов
        """
        return int(self.subscriber_count) <= int(other.subscriber_count)

    def __eq__(self, other):
        """
        Метод для операции приравнивания объектов
        """
        return int(self.subscriber_count) == int(other.subscriber_count)

    def print_info(self) -> None:
        """Выводит в консоль информацию о канале."""
        print(json.dumps(self.channel, indent=2, ensure_ascii=False))

    def to_json(self, file_name):
        """Сохраняет в Json файл значения атрибутов экземпляра - информацию о канале"""
        data = {'channel_id': self.channel_id,
                'title': self.title,
                'description': self.description,
                'url': self.url,
                'subscriber_count': self.subscriber_count,
                'video_count': self.video_count,
                'view_count': self.view_count
                }
        with open(file_name, 'w', encoding='UTF-8') as file:
            json.dump(data, file, ensure_ascii=False)

    @classmethod
    def get_service(cls):
        """Возвращает объект для работы с YouTube API"""
        return build('youtube', 'v3', developerKey=Channel.api_key)

    @property
    def channel_id(self):
        return self.__channel_id
