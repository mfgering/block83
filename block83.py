import datetime
import os, os.path, sys
import requests
import cv2
import re

def snap_curr(images_dir="images"):
	curr_image_url = "https://oxblue.com/archive/7f903adce7e782da7ab5d68efbe30861/current.jpg"
	now = datetime.datetime.now()
	fmt = 'block83-%Y-%m-%d-%H.jpg'
	fname = now.strftime(fmt)
	out_fn = os.path.join(images_dir, fname)
	curr_data = requests.get(curr_image_url).content
	with open(out_fn, "wb") as handler:
		handler.write(curr_data)

def make_movie(images_dir="images", mov_name="block83.avi", marked_dir="images-marked"):
	#pylint: disable=no-member
	images = sorted([img for img in os.listdir(images_dir) if img.endswith(".jpg")])
	frame = cv2.imread(os.path.join(images_dir, images[0]))
	height, width, _ = frame.shape
	video = cv2.VideoWriter(mov_name, 0, 1, (width,height))
	for image in images:
		img = get_marked_image(image, images_dir, marked_dir)
		video.write(img)
	cv2.destroyAllWindows()
	video.release()

def get_marked_image(images_dir, marked_dir, image_name):
	#pylint: disable=no-member
	image_fn = os.path.join(images_dir, image_name)
	marked_fn = os.path.join(marked_dir, image_name)
	try:
		img = cv2.imread(marked_fn)
	except Exception as exc:
		img = make_marked(image_name, image_fn, marked_fn)
	return img

def make_marked(image_name, image_fn, marked_fn):
	#pylint: disable=no-member
	# Try creating it from unmarked version
	img = None
	try:
		img = cv2.imread(image_fn)
		img_datetime = get_datetime(image_name)
		txt = img_datetime.strftime("%m/%d/%y %H:00")
		font                   = cv2.FONT_HERSHEY_SIMPLEX
		h, w, ch = img.shape

		bottomLeftCornerOfText = ((int)(0.65*w), (int)(0.1*h))
		fontScale              = 3
		fontColor              = (255,255,255)
		lineType               = cv2.LINE_AA
		thickness = 4
		cv2.putText(img,txt, 
			bottomLeftCornerOfText, 
			font, 
			fontScale,
			fontColor,
			thickness,
			lineType)
		cv2.imwrite(marked_fn, img)
	finally:
		pass		
	return img

def get_datetime(image_name):
	dt = datetime.datetime.now()
	pattern = r".*-(\d+)-(\d+)-(\d+)-(\d+)\..*"
	m = re.match(pattern, image_name)
	if m is not None:
		year = int(m.group(1))
		mon = int(m.group(2))
		day = int(m.group(3))
		hour = int(m.group(4))
		dt = datetime.datetime(year, mon, day, hour)
	return dt

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
	#dt = get_datetime("block83-2020-04-07-12.jpg")
	#exit
	log_f = open("c:/foo/block83-log.txt", "w+")
	log_f.write("================== start\n")
	#base_dir = '\\\\alpha.dawson\\heap\\block83'
	base_dir = 'images'
	if len(sys.argv) > 1:
		base_dir = sys.argv[1]
	if not os.path.isdir(base_dir):
		print(f"'{base_dir}' is not a directory.")
		sys.exit(1)
	images_dir = os.path.join(base_dir, "images")
	mov_fn = os.path.join(base_dir, "block83.avi")
	#snap_curr(images_dir)
	make_movie(images_dir, mov_fn)
	log_f.write("================== finished\n")
	print("Done")

def bar():
	image_name = 'block83-2020-04-07-10.jpg'
	image_fn = './images/'+image_name
	marked_fn = './images-marked/'+image_name
	img = make_marked(image_name, image_fn, marked_fn)
print("****FOR TESTING ONLY****")
bar()