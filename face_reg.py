import face_recognition
import cv2
import numpy as np
import speech_recognition as sr


# Load a sample picture and learn how to recognize it.
obama_image = face_recognition.load_image_file("obama.jpg")
obama_face_encoding = face_recognition.face_encodings(obama_image)[0]

# Load a second sample picture and learn how to recognize it.
biden_image = face_recognition.load_image_file("biden.jpg")
biden_face_encoding = face_recognition.face_encodings(biden_image)[0]

vaibhav_image = face_recognition.load_image_file("new_vaibhav.jpeg")
vaibhav_face_encoding = face_recognition.face_encodings(vaibhav_image)[0]

rugved_image = face_recognition.load_image_file("rugved.jpeg")
rugved_face_encoding = face_recognition.face_encodings(rugved_image)[0]

# Create arrays of known face encodings and their names
known_face_encodings = [
    obama_face_encoding,
    biden_face_encoding,
    vaibhav_face_encoding,
    rugved_face_encoding 
]
known_face_names = [
    "Barack Obama",
    "Joe Biden",
    "vaibhav",
    "Zural"
]
#print('Learned encoding for', len(known_face_encodings), 'images.')

# Initialize some variables
face_locations = []
face_encodings = []
face_names = []
process_this_frame = True
