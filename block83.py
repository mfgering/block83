import datetime
import os, os.path, sys
import requests
import cv2

def snap_curr(images_dir="images"):
	curr_image_url = "https://oxblue.com/archive/7f903adce7e782da7ab5d68efbe30861/current.jpg"
	now = datetime.datetime.now()

	out_fn = os.path.join(images_dir, f"block83-{now.year}-{now.month}-{now.day}-{now.hour}.jpg")
	curr_data = requests.get(curr_image_url).content
	with open(out_fn, "wb") as handler:
		handler.write(curr_data)

def make_movie(images_dir="images", mov_name="block83.avi"):
	#pylint: disable=no-member
	images = [img for img in os.listdir(images_dir) if img.endswith(".jpg")]
	frame = cv2.imread(os.path.join(images_dir, images[0])) 
	height, width, _ = frame.shape
	video = cv2.VideoWriter(mov_name, 0, 1, (width,height))
	for image in images:
		video.write(cv2.imread(os.path.join(images_dir, image)))
	cv2.destroyAllWindows()
	video.release()

def run():
	log_f = open("c:/foo/block83-log.txt", "w+")
	log_f.write("================== start\n")
	base_dir = '\\\\alpha.dawson\\heap\\block83'
	if len(sys.argv) > 1:
		base_dir = sys.argv[1]
	if not os.path.isdir(base_dir):
		print(f"'{base_dir}' is not a directory.")
		sys.exit(1)
	images_dir = os.path.join(base_dir, "images")
	mov_fn = os.path.join(base_dir, "block83.avi")
	snap_curr(images_dir)
	make_movie(images_dir, mov_fn)
	log_f.write("================== finished\n")
	print("Done")

def foo():
	print("Foo!")
	with open("c:/foo/block83-test.txt", "w+") as f:
		now = datetime.datetime.now()
		f.write(f"Running foo at {now}")