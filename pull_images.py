

import os
import requests
import shutil
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from concurrent.futures import ThreadPoolExecutor
from tqdm import tqdm


MAX_WORKERS = 32


def download(track):
	"Download and save track to current directory."
	try:
		res = requests.get(track["track"]["album"]["images"][0]["url"], stream = True)
	except IndexError:  # track doesn't have an online image
		return

	if res.status_code != 200:
		print(f"Image for \'{track['track']['name']}\' couldn't be retrieved.")
		return

	with open(f"{track['track']['id']}.png", "wb") as f:
		shutil.copyfileobj(res.raw, f)


def playlist_name(playlist_URL):
	# authenticate request
	auth_manager = SpotifyClientCredentials()
	sp = spotipy.Spotify(auth_manager=auth_manager)

	# pull from Spotify API
	playlist = sp.playlist(playlist_URL)  # assume that playlist_URL is valid

	return playlist["name"]


def pull_images(playlist_URL):
	# authenticate request
	auth_manager = SpotifyClientCredentials()
	sp = spotipy.Spotify(auth_manager=auth_manager)

	# pull from Spotify API
	playlist = sp.playlist(playlist_URL)  # assume that playlist_URL is valid
	tracks = playlist["tracks"]

	# loop over each set of 99 songs given by the api
	track_items = tracks["items"]
	while tracks["next"]:
		tracks = sp.next(tracks)
		track_items.extend(tracks["items"])
	# remove temporary .cache file created when multiple iterations of 99 songs are retrieved
	try:
		os.remove(".cache")
	except OSError as e:
		if e.errno != 2:  # file not found
			raise e

	# download images concurrently
	with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
		list(tqdm(executor.map(download, track_items), total=len(track_items)))

	return playlist["name"]


def main():
	import sys
	if len(sys.argv) != 2:
		print(f"One argument expected, {sys.argv.length()-1} provided.")
		return
	pull_images(sys.argv[1])



if __name__ == "__main__":
	main()

