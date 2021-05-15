from bs4 import BeautifulSoup
import requests
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import os

date = input("Which year do you want to travel to? Type the date in this format YYYY-MM-DD: ")
url = f"https://www.billboard.com/charts/hot-100/{date}"
response = requests.get(url)
soup = BeautifulSoup(response.text, "html.parser")
songs_list = soup.find_all(name="span", class_="chart-element__information__song")
new_songs_list = [song.getText() for song in songs_list]
# print(new_songs_list)

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=os.environ["ClientID"],
                                               client_secret=os.environ["ClientSecret"],
                                               redirect_uri="http://example.com",
                                               show_dialog=True,
                                               scope="playlist-modify-private",
                                               cache_path="token.txt",
                                               )
                     )

user = sp.current_user()["id"]
test = new_songs_list[0:1]
uri_list = []
for song in new_songs_list:
    result = sp.search(q=f"track:{song} year:{date[:4]}", type="track")
    # print(result)
    try:
        uri = result["tracks"]["items"][0]["uri"]
        uri_list.append(uri)
    except IndexError:
        print(f"{song} doesn't exist in Spotify. Skipped.")
playlist_id = \
    sp.user_playlist_create(user, f"{date} Billboard 100", public=False, description=f"Top 100 songs on {date}")["id"]
result = sp.playlist_add_items(playlist_id=playlist_id, items=uri_list)
# print(uri_list)
