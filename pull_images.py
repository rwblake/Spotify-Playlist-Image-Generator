

import os
import requests
import shutil
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials


def _pull_images_helper(tracks):
	for track in tracks["items"]:
		res = requests.get(track["track"]["album"]["images"][0]["url"], stream = True)
		if res.status_code != 200:
			print(f"Image for \'{track['track']['name']}\' couldn't be retrieved.")
			continue

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


def pull_images(playlist_URL):
	# authenticates request
	auth_manager = SpotifyClientCredentials()
	sp = spotipy.Spotify(auth_manager=auth_manager)

	# assume that playlist_URL is valid
	playlist = sp.playlist(playlist_URL)
	tracks = playlist["tracks"]

	# create folder structure
	if os.path.isdir(playlist["name"]):
		raise Exception("Album folder already exists. Please delete before running.")
	os.mkdir(playlist["name"])
	os.chdir(playlist["name"])
	os.mkdir("images")
	os.chdir("images")

	# loop over each set of 99 songs given by the api
	_pull_images_helper(tracks)  # download and save images
	while tracks["next"]:
		print("hi")
		tracks = sp.next(tracks)
		_pull_images_helper(tracks)

	# finish in the new playlist directory
	os.chdir("..")


def main():
	import sys
	if len(sys.argv) != 2:
		sys.stderr.write(f"One argument expected, {sys.argv.length()-1} provided.")
		return
	pull_images(sys.argv[1])



if __name__ == "__main__":
	main()

