from yandex_music import Client
import os
from config import YA_TOKEN

client = Client(YA_TOKEN).init()

type_to_name = {
    'track': 'трек',
    'artist': 'исполнитель',
    'album': 'альбом',
    'playlist': 'плейлист',
    'video': 'видео',
    'user': 'пользователь',
    'podcast': 'подкаст',
    'podcast_episode': 'эпизод подкаста',
}



def download_track(track, user):
    if not os.path.exists(user):
        os.makedirs(user)
    track_name = f"{track.title} - {track.artists[0].name}"
    simbols = """$/\\%{&}><?+|"#"""
    for char in simbols:
        track_name = track_name.replace(char, "")
    track_file=f'{user}/{track_name}.mp3'
    track.download(track_file)
    return track_file

# def download_playst(id, user):
#     tracks = []
#     # print(client.albums_with_tracks(id))
#     album = client.albums_with_tracks(id)
#     for i, volume in enumerate(album.volumes):
#         # print(album.volumes[0][0].id) 
#         if len(album.volumes) > 1:
#             tracks.append(f'💿 Диск {i + 1}')
#             print(f'💿 Диск {i + 1}')
#     tracks += volume
#     for track in tracks:
#         if isinstance(track, str):
#             print(track)
#         else:
#             artists = ''
#             if track.artists:
#                 artists = ' - ' + ', '.join(artist.name for artist in track.artists)
#                 print(track.title + artists)
#                 track_file = download_track(track, user)
#                 return track_file
            
def search(query, username):
    search_result = client.search(query)
    if search_result.tracks:
        # print(search_result)
        best = search_result.tracks.results[0]
        return download_track(best, username)
    else:
        return 'Не нашел такой трек('