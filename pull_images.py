

import os
import requests
import shutil
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials


def _pull_images_helper(tracks):
	"""Download and save all track images in the current directory."""
	for track in tracks:
		try:
			res = requests.get(track["track"]["album"]["images"][0]["url"], stream = True)
		except IndexError:  # track doesn't have an online image
			continue

		if res.status_code != 200:
			print(f"Image for \'{track['track']['name']}\' couldn't be retrieved.")
			continue

		with open(f"{track['track']['id']}.png", "wb") as f:
			shutil.copyfileobj(res.raw, f)
		# doesn't allow actual song names currently
		"""
		try:
			with open(f"{track['track']['name']}.png", "wb") as f:
				shutil.copyfileobj(res.raw, f)
		except OSError as e:  # invalid character in song name, or song name includes directory
			if e.errno != 22 and e.errno != 2:
				raise e
			with open(f"{track['track']['id']}.png", "wb") as f:
				shutil.copyfileobj(res.raw, f)
		except FileExistsError:  # songs with the same name
			with open(f"{track['track']['id']}.png", "wb") as f:
				shutil.copyfileobj(res.raw, f)
		"""


def pull_images(playlist_URL):
	# authenticate request
	auth_manager = SpotifyClientCredentials()
	sp = spotipy.Spotify(auth_manager=auth_manager)

	# pull from Spotify API
	playlist = sp.playlist(playlist_URL)  # assume that playlist_URL is valid
	tracks = playlist["tracks"]

	# create folder structure
	if os.path.isdir(playlist["name"]):
		print("Album folder already exists. No images retrieved.")
		return playlist["name"]
	os.mkdir(playlist["name"])
	os.chdir(playlist["name"])
	os.mkdir("images")
	os.chdir("images")

	# loop over each set of 99 songs given by the api
	_pull_images_helper(tracks["items"])
	while tracks["next"]:
		tracks = sp.next(tracks)
		_pull_images_helper(tracks["items"])
	# remove temporary .cache file created when multiple iterations of 99 songs are retrieved
	try:
		os.remove(".cache")
	except OSError as e:
		if e.errno != 2:  # file not found
			raise e

	# finish in the main directory
	os.chdir("../..")
	return playlist["name"]


def main():
	import sys
	if len(sys.argv) != 2:
		print(f"One argument expected, {sys.argv.length()-1} provided.")
		return
	pull_images(sys.argv[1])



if __name__ == "__main__":
	main()

