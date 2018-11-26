import face_recognition
import cv2

# Program start
print("Program Starting...")
video_capture = cv2.VideoCapture(0)
dog = cv2.imread('dog.png')
kewl = cv2.imread('kewl.png')

# Class for filters for organized access
class Filters:
	@staticmethod
	def applydogfilter(dog,fc,x,y,w,h):
		face_width = w
		face_height = h
		
		dog = cv2.resize(dog,(int(face_width*1.5),int(face_height*1.75)))
		for i in range(int(face_height*1.75)):
			for j in range(int(face_width*1.5)):
				for k in range(3):
					if dog[i][j][k]<235:
						fc[y+i-int(0.375*h)-1][x+j-int(0.25*w)][k] = dog[i][j][k]
		return fc
	
	@staticmethod
	def applykewlfilter(kewl,fc,x,y,w,h):
		face_width = w
		face_height = h
		
		kewl = cv2.resize(kewl,(int(face_width*1),int(face_height*1.75)))
		for i in range(int(face_height*1.75)):
			for j in range(int(face_width*1)):
				for k in range(3):
					if kewl[i][j][k]<235:
						fc[y+i-int(0*h)-1][x+j-int(-0.01*w)][k] = kewl[i][j][k]
		return fc

		
face_locations = []
process_this_frame = True
opt = 0
opt = input("Select filter: Dog filter (d), Gentleman filter (g):   ")
opt = opt.lower()
while True:
	if not video_capture.isOpened():
		print('Unable to load camera.')
		sleep(5)
		pass
    # Capture frame-by-frame
	ret, frame = video_capture.read()
	gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
	# Grab a single frame of video
	ret, frame = video_capture.read()

    # Frame resize for faster processing
	small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
	
    # Convert image to BGR
	rgb_small_frame = small_frame[:, :, ::-1]
	if process_this_frame:
		# Find face locations 
		face_locations = face_recognition.face_locations(rgb_small_frame)
	process_this_frame = not process_this_frame

	for top, right, bottom, left in face_locations:
		top *= 4
		right *= 4
		bottom *= 4
		left *= 4
		nright = right - left
		nbottom = bottom - top
		#cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)

		if opt=="d":
			frame = Filters.applydogfilter(dog,frame,left, top, nright, nbottom)

		elif opt=="g":
			frame = Filters.applykewlfilter(kewl,frame,left, top, nright, nbottom)
			
    # Display frame
	cv2.imshow('Applying filter. Press "q" to exit.', frame)
	
	if cv2.waitKey(1) & 0xFF == ord('q'):
		print("Program closing...")
		break
		
# Release capture
video_capture.release()
cv2.destroyAllWindows()