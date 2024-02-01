

from imagedominantcolor import DominantColor


def get_dominant_colors(image_paths):
	return [(path, DominantColor(path).rgb) for path in image_paths]


def get_average_colors(image_paths):
	# averages = [(path, average)]
	return get_dominant_colors(image_paths)


def main():
	import os
	image_paths = os.listdir(".")
	print(get_average_colors(image_paths))


if __name__ == "__main__":
	main()