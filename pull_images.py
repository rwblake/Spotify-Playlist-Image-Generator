

import os
import requests
import shutil
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials


def pull_images(playlist_URL):
	# authenticates request
	auth_manager = SpotifyClientCredentials()
	sp = spotipy.Spotify(auth_manager=auth_manager)

	# assume that playlist_URL is valid
	playlist = sp.playlist(playlist_URL)

	tracks = [{"name":     item["track"]["name"],
	           "id":       item["track"]["id"],
	           "image_URL":item["track"]["album"]["images"][0]["url"]
	          }
	          for item in playlist["tracks"]["items"]
	         ]

	os.mkdir(playlist["name"])  # to store images
	os.chdir(playlist["name"])
	os.mkdir("images")
	os.chdir("images")

	for track in tracks:
		res = requests.get(track["image_URL"], stream = True)
		if res.status_code != 200:
			print(f"Image for \'{track['name']}\' couldn't be retrieved.")
			continue

		try:
			with open(f"{track['name']}.png", "wb") as f:
				shutil.copyfileobj(res.raw, f)
		except OSError as e:  # invalid character in song name
			if e.errno != 22:
				raise e
			with open(f"{track['id']}.png", "wb") as f:
				shutil.copyfileobj(res.raw, f)


	os.chdir("..")
	# end up in the new playlist directory



def main():
	import sys
	if len(sys.argv) != 2:
		sys.stderr.write(f"One argument expected, {sys.argv.length()-1} provided.")
		return
	pull_images(sys.argv[1])



if __name__ == "__main__":
	main()

