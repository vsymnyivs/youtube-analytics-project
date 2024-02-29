import os
from googleapiclient.discovery import build


class Video:
    """
    Класс для видео
    """
    api_key: str = os.getenv('YOUTUBE_API')
    youtube = build('youtube', 'v3', developerKey=api_key)

    def __init__(self, video_id: str) -> None:
        self.video_id = video_id
        self.video_response = self.youtube.videos().list(part='snippet,statistics,contentDetails,topicDetails',
                                                         id=video_id).execute()
        self.url = f"https://www.youtube.com/channel/{self.video_id}"
        self.title = self.video_response["items"][0]["snippet"]["title"]
        self.view_count = self.video_response["items"][0]["statistics"]["viewCount"]
        self.like_count = self.video_response["items"][0]["statistics"]["likeCount"]

    def __str__(self):
        """
        Возвращает заголовок
        """
        return f"{self.title}"


class PLVideo(Video):
    """
    Класс для плейлиста
    """
    def __init__(self, video_id: str, playlist_id):
        super().__init__(video_id)
        self.playlist_id = playlist_id
        self.playlist_videos = self.youtube.playlistItems().list(playlistId=playlist_id,
                                                                 part='contentDetails',
                                                                 maxResults=50,
                                                                 ).execute()
