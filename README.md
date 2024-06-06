# Spotify Playlist Image Generator
## Generate an aesthetic mosaic playlist image from album art in a spotify playlist.
Input a spotify playlist URL, and optionally a reference image that you want your mosaic to mimic.

## Setup
- To make use of this package, you need to create an app at the [developer.spotify.com] website. For this, follow these steps:
1. Browse to https://developer.spotify.com/dashboard/applications.
2. Log in with your Spotify account.
3. Click on ‘Create an app’.
4. Pick an ‘App name’ and ‘App description’ of your choice and mark the checkboxes.
5. After creation, you see your ‘Client Id’ and you can click on ‘Show client secret` to unhide your ’Client secret’.
6. Now, set your ‘Client Id’ and ‘Client secret’ as environment variables on your computer:
```console
export SPOTIFY_CLIENT_ID=yourspotifyclientid
export SPOTIFY_CLIENT_SECRET=yourspotifyclientsecret
```
- Install [python 3](https://www.python.org/) (tested with version 3.10):
Follow the instructions to download and install on the website.
- Install the required python dependencies as listed in requirements.txt:
```console
pip install -r requirements.txt
```
- Now you're all set! The following is how you can run the program:
## Usage
Run ``main.py`` with python 3 in the command line, with your chosen options e.g.
* ``python3 main.py https://open.spotify.com/playlist/4OIVU71yO7SzyGrh0ils2i?si=231924eb54c74b02 pleasant_photograph.jpg`` - The standard method of running the program.
* ``python3 main.py https://open.spotify.com/playlist/4OIVU71yO7SzyGrh0ils2i?si=231924eb54c74b02`` - Create a random mosaic of the playlist.
* ``python3 main.py -n -w 10 -f https://open.spotify.com/playlist/4OIVU71yO7SzyGrh0ils2i?si=231924eb54c74b02 pleasant_photograph.jpg`` - The final image will contain no duplicates, be 10x10 album covers in resolution, and will redownload the playlist to ensure it is up-to-date.
### Options
Run ``python3 main.py -h`` to display the list of options shown below:
```
usage: main.py [-h] [-w WIDTH] [-n] [-f] playlist_URL [reference_image]

positional arguments:
  playlist_URL          spotify playlist URL
                        ('https://open.spotify.com/playlist/...') OR local
                        folder path
  reference_image       path to reference image (must be square)

options:
  -h, --help            show this help message and exit
  -w WIDTH, --width WIDTH
                        width of mosaic in images (default 64x64)
  -n, --no-duplicates   only use each image once
  -f, --force-download  force image re-downloading when playlist has
                        previously been used
```
