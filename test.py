# This is a demo of running face recognition on a Raspberry Pi.
# This program will print out the names of anyone it recognizes to the console.

# To run this, you need a Raspberry Pi 2 (or greater) with face_recognition and
# the picamera[array] module installed.
# You can follow this installation instructions to get your RPi set up:
# https://gist.github.com/ageitgey/1ac8dbe8572f3f533df6269dab35df65

import face_recognition
import picamera
import numpy as np
from knotpy import *

# Get a reference to the Raspberry Pi camera.
# If this fails, make sure you have a camera connected to the RPi and that you
# enabled your camera in raspi-config and rebooted first.

credentials = {
	'uuid': '',
	'token': '',
	'servername': 'localhost',
	'port': 3000
}
conn = KnotConnection('socketio', credentials)

myThings = conn.myDevices()

conn = KnotConnection('socketio', credentials)

camera = picamera.PiCamera()
camera.resolution = (320, 240)
output = np.empty((240, 320, 3), dtype=np.uint8)

# Load a sample picture and learn how to recognize it.
print("Loading known face image(s)")
obama_image = face_recognition.load_image_file("obama_small.jpg")
obama_face_encoding = face_recognition.face_encodings(obama_image)[0]

lucasface = face_recognition.load_image_file("lucas.jpg")
lucasface_encoding = face_recognition.face_encodings(lucasface)[0]

# Load a second sample picture and learn how to recognize it.
lucasinsta = face_recognition.load_image_file("lucas1.jpg")
lucasinsta_encoding = face_recognition.face_encodings(lucasinsta)[0]

paulo = face_recognition.load_image_file("paulo.png")
paulo_encoding = face_recognition.face_encodings(paulo)[0]

suzy = face_recognition.load_image_file("suzy.jpeg")
suzy_encoding = face_recognition.face_encodings(suzy)[0]

barbara = face_recognition.load_image_file("barbara.jpeg")
barbara_encoding = face_recognition.face_encodings(barbara)[0]

antonio = face_recognition.load_image_file("antonio.jpeg")
antonio_encoding = face_recognition.face_encodings(antonio)[0]

florencia = face_recognition.load_image_file("florencia.jpeg")
florencia_encoding = face_recognition.face_encodings(florencia)[0]

anderson = face_recognition.load_image_file("anderson.jpeg")
anderson_encoding = face_recognition.face_encodings(anderson)[0]

known_face_encodings = [
    obama_face_encoding,
    lucasface_encoding,
    paulo_encoding,
    suzy_encoding,
    barbara_encoding,
    antonio_encoding,
    florencia_encoding,
    anderson_encoding
]

known_face_names = [
    "Lucas",
    "Paulo",
    "Suzy",
    "Barbara",
    "Antonio",
    "Florencia",
    "Anderson"
]
# Initialize some variables
face_locations = []
face_encodings = []

name = "Unknown"
while True:
    print("Capturing image.")
    # Grab a single frame of video from the RPi camera as a numpy array
    camera.capture(output, format="rgb")

    # Find all the faces and face encodings in the current frame of video
    face_locations = face_recognition.face_locations(output)
    print("Found {} faces in image.".format(len(face_locations)))
    face_encodings = face_recognition.face_encodings(output, face_locations)

    # Loop over each face found in the frame to see if it's someone we know.
    for face_encoding in face_encodings:
        # See if the face is a match for the known face(s)
        match = face_recognition.compare_faces(known_face_encodings, face_encoding)
        
        name1 = name
        if True in match:
            first_match_index = match.index(True)                
            name = known_face_names[first_match_index]

            if name1 != name:   
                print("Nome eh diferente do nome anterior, enviando")
                for thing in myThings:
                    # print(thing)
                    print(60*'-')
                    # print('DATA')
                    data = conn.setData(thing['uuid'],2,False)
                    # time.sleep(3)
                    # data = conn.setData(thing['uuid'],1,False)
                    # data2 = conn.setData(thing['uuid'],2,False)
                    print(data)
                    '''print('Set data')
                    if thing.get('schema'):
                        for sensor in thing.get('schema'):
                            if sensor['name'] == 'LED':
                                conn.setData(thing['uuid'], sensor['sensor_id'], True)
                    print(60*'*')'''
        else:
            name = "Unknown"
            print("aqui eh o else pro Unknown")
            for thing in myThings:
                print(thing)
                print(60*'-')
                print('DADOS')
                data = conn.setData(thing['uuid'],1,False)
                # time.sleep(3)
                # data = conn.setData(thing['uuid'],2, False)
                # data2 = conn.setData(thing['uuid'],1,False)
                print(data)
                '''print('Set data')
                if thing.get('schema'):
                    for sensor in thing.get('schema'):
                        if sensor['name'] == 'LED':
                            conn.setData(thing['uuid'], sensor['sensor_id'], True)
                print(60*'*')'''

        print("I see someone named {}!".format(name))

