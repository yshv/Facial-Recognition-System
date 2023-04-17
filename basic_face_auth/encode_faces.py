from imutils import paths
import face_recognition
import argparse
import pickle
import cv2
import os
import base64
import json
import numpy as np

'''
def encode_faces(dataset, name):
    # grab the paths to the input images in our dataset

    json_dataset = json.loads(dataset)

    print('[INFO] quantifying faces...')
    # initialize the list of known encoding and known names
    knownEncodings = list()
    knownNames = list()

    # iterate over the path to each image
    for (i, json_image) in enumerate(json_dataset['images']):
        # extract the name from path
        # for example, path: dataset/name/image1.jpg
        # if we use os.path.sep to split it
        # and pick the second from last index
        # we will get 'name' which, in this case, is a label
        print(f'[INFO] processing images {i+1}/{len(json_dataset)}')

        # decode the image data from base64
        image_bytes = base64.b64decode(json_image)
        # cv2.imshow('image', image_bytes)
        # load the input image and convert it from BGR (OpenCV ordering)
        # to dlib ordering (RGB)
        image = cv2.imdecode(np.frombuffer(image_bytes, np.uint8), cv2.IMREAD_COLOR)
        # image = face_recognition.load_image_file(image_bytes)
        cv2.imshow('image', image)
        image = cv2.resize(image, (0,0), fx=0.5, fy=0.5)
        rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        
        # detect the face in each frame 
        # and return (x,y)-coordinate of the bounding box
        boxes = face_recognition.face_locations(rgb, model='cnn')
        
        # compute the face embedding
        encodings = face_recognition.face_encodings(rgb, boxes)
        
        # iterate over encodings
        # the reason we have to iterate over encoding even it's a single image
        # is sometimes one person's face might appear in more than 1 place in the image
        # for example, that person is looking at the mirror
        for encoding in encodings:
            # add each encoding and name to the list
            knownEncodings.append(encoding)
            knownNames.append(name) 
            
    # save encoding to pickle
    print('[INFO] saving encodings...')
    data = {'encodings': knownEncodings, 'names': knownNames}
    # with open(args['encoding'], 'wb') as file:
    #     file.write(pickle.dumps(data))
    
    return data
'''
    
def encode_faces(photoUrls, name):
    # grab the paths to the input images in our dataset
    print('[INFO] quantifying faces...')
    # initialize the list of known encoding and known names
    knownEncodings = list()
    knownNames = list()
    print(photoUrls)
    # iterate over the path to each image
    for (i, photoUrl) in enumerate(photoUrls):
        # extract the name from path
        # for example, path: dataset/name/image1.jpg
        # if we use os.path.sep to split it
        # and pick the second from last index
        # we will get 'name' which, in this case, is a label
        print(f'[INFO] processing images {i+1}/{len(photoUrls)}')
        photo = photoUrl.split(',')[1]

        # Decode the base64-encoded string
        # photo = bytes(photo, 'utf-8')
        img_data = base64.b64decode(photo)

        # Convert the image data to a NumPy array
        img_array = np.frombuffer(img_data, dtype=np.uint8)

        # Decode the array to an OpenCV image
        img = cv2.imdecode(img_array, flags=cv2.IMREAD_COLOR)

        # Display the image
        cv2.imshow('Image', img)

        image = cv2.resize(image, (0,0), fx=0.5, fy=0.5)
        rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        
        # detect the face in each frame 
        # and return (x,y)-coordinate of the bounding box
        boxes = face_recognition.face_locations(rgb, model='cnn')
        
        # compute the face embedding
        encodings = face_recognition.face_encodings(rgb, boxes)
        
        # iterate over encodings
        # the reason we have to iterate over encoding even it's a single image
        # is sometimes one person's face might appear in more than 1 place in the image
        # for example, that person is looking at the mirror
        for encoding in encodings:
            # add each encoding and name to the list
            knownEncodings.append(encoding)
            knownNames.append(name) 
            
    # save encoding to pickle
    print('[INFO] saving encodings...')
    data = {'encodings': knownEncodings, 'names': knownNames}
    # with open(args['encoding'], 'wb') as file:
    #     file.write(pickle.dumps(data))
    
    return data



if __name__ == '__main__':
    # with open('test_data.json', 'r') as file:
    #     dataset = file.read()
    dataset = ['data:image/jpeg;base64,/9j/4AAQSkZJRgABAQAAAQABAAD…tPttda/3+tKlW7KYVSgoLHryfNzay/go9wBSycUqVKrwJH//Z', 'data:image/jpeg;base64,/9j/4AAQSkZJRgABAQAAAQABAAD…kiP5A/OlSrydMKJVxrWFvT/Uxuck8+Cj3GXbGOtKlSroQR//Z']
    encode_faces(dataset,'yihan')