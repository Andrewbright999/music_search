from mutagen.easyid3 import EasyID3
from mutagen.id3 import ID3NoHeaderError

from yandex_music import Client
from config import YA_TOKEN


client = Client(YA_TOKEN).init()


class Track:
    def __init__(self, query: str) -> None:
        search_result = client.search(query)
        if search_result.tracks:
            self.track = search_result.tracks.results[0]
            simbols = """$/\\%{&}><?+|"#"""
            self.title = self.track.title
            self.file_path = self.title
            self.artists = [name["name"] for name in self.track.artists]
            self.albumartists = [name["name"] for name in self.track.albums[0].artists]
            self.album = [title["title"] for title in self.track.albums]
            for char in simbols:
                self.file_path = self.file_path.replace(char, "")
            self.file_path=f'{self.file_path}.mp3'
        else:
            raise 'Не нашел такой трек('

    def set_tags(self):
        try:
            tags = EasyID3(self.file_path)
        except ID3NoHeaderError:
            tags = EasyID3()
        # tags = EasyID3(self.file_path)
        tags['title'] = self.title
        tags['artist'] = self.artists
        tags['albumartist'] = self.albumartists
        tags['album'] = self.album
        tags.save(self.file_path)
    
    def download_track(self):
        self.track.download(self.file_path)
        return self.file_path