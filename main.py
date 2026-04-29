import requests
from bs4 import BeautifulSoup
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import time

CLIENT_ID = "YOUR CLIENT_ID"
CLIENT_SECRET = "YOUR CLIENT_SECRET"
REDIRECT_URI = "YOUR REDIRECT_URI"

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
    client_id=CLIENT_ID,
    client_secret=CLIENT_SECRET,
    redirect_uri=REDIRECT_URI,
    scope="playlist-modify-private",
    cache_path="token.txt"
))

user = sp.current_user()
user_id = user['id']
print(f"✅ Connected as: {user['display_name']}\n")


date = input("Enter date (YYYY-MM-DD): ").strip()


print(f"🔍 Scraping Billboard Hot 100 for {date}...")
url = f"https://www.billboard.com/charts/hot-100/{date}/"
soup = BeautifulSoup(requests.get(url).text, "html.parser")

songs = []
for item in soup.select("li.o-chart-results-list__item"):
    title = item.select_one("h3")
    artist = item.select_one("span.c-label")
    if title and artist:
        songs.append((title.get_text().strip(), artist.get_text().strip()))

print(f"✅ Found {len(songs)} songs.\n")


playlist = sp.user_playlist_create(
    user=user_id,
    name=f"Billboard Hot 100 - {date}",
    public=False,
    description=f"Top 100 songs from {date}"
)

print("🎵 Playlist created. Adding songs...\n")


count = 0
for title, artist in songs[:100]:
    try:
        results = sp.search(q=f"{title} {artist}", type="track", limit=1)
        if results['tracks']['items']:
            sp.playlist_add_items(playlist['id'], [results['tracks']['items'][0]['uri']])
            print(f"✅ {title}")
            count += 1
    except:
        print(f"❌ {title}")
    time.sleep(0.5)

print(f"\n🎉 Done! {count} songs added to your playlist.")
print(f"Link: https://open.spotify.com/playlist/{playlist['id']}")