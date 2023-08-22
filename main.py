from bs4 import BeautifulSoup
import requests
import spotipy
from spotipy.oauth2 import SpotifyOAuth
URL = "https://www.billboard.com/charts/hot-100/"
CLIENT_ID = "your-id"
CLIENT_SECRET = "your-secret-key"
REDIRECT_URL = "http://example.com"

### AUTHENTIFICATION
sp = spotipy.Spotify(
    auth_manager=SpotifyOAuth(
        scope="playlist-modify-private",
        redirect_uri="http://example.com",
        client_id=CLIENT_ID,
        client_secret=CLIENT_SECRET,
        show_dialog=True,
        cache_path="token.txt"
    )
)

###GETTING USER ID
user_id = sp.current_user()["id"]

#GETTING DATE
date = input("Which year do you want to travle to? Type this date in this format YYYY-MM-DD: ")
response = requests.get(URL + date)
response.raise_for_status()

website_html = response.text

soup = BeautifulSoup(website_html, "html.parser")

song_names_spans = soup.select("li ul  h3")

song_names = [song.getText().strip() for song in song_names_spans]

song_uris = []
year = date.split("-")[0]

###CREATING A LIST OF SONGS
for song in song_names:
    result = sp.search(q=f"track: {song} year:{year}", type="track")
    print(result)
    try:
        uri = result["tracks"]["items"][0]["uri"]
        song_uris.append(uri)
    except IndexError:
        print(f"{song} doesn't exist in Spotify. Skipped.")

###CREATING SPOTIFY PLAYLIST
playlist = sp.user_playlist_create(user=user_id, name=f"{date} Billboard 100", public=False)

#ADDING SONG TO SPOTIFY PLAYLIST
sp.playlist_add_items(playlist_id=playlist["id"], items=song_uris)