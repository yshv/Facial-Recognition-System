from imutils import paths
import face_recognition
import argparse
import pickle
import cv2
import os
import base64
import json
import numpy as np
from PIL import Image
import io

    
def encode_faces(json_data, name):
    # grab the paths to the input images in our dataset
    print('[INFO] quantifying faces...')
    # initialize the list of known encoding and known names
    knownEncodings = list()
    knownNames = list()
    # print(photoUrls)
    data = json.loads(json_data)
    photoUrls = data['images']
    name = data['username']
    # iterate over the path to each image
    for (i, photoUrl) in enumerate(photoUrls):
        # extract the name from path
        # for example, path: dataset/name/image1.jpg
        # if we use os.path.sep to split it
        # and pick the second from last index
        # we will get 'name' which, in this case, is a label
        print(f'[INFO] processing images {i+1}/{len(photoUrls)}')
        # print(photoUrl)
        photo = photoUrl.split(',')[1]
        # Decode the base64-encoded string
        photo = bytes(photo, 'utf-8')
        img_data = base64.b64decode(photo)
        img = Image.open(io.BytesIO(img_data))
        print(img.size)
        # img.show()
        # Resize the image to 1/4 of its original size
        resized_image = img.resize((int(img.size[0]/2), int(img.size[1]/2)))

        # Convert the image to RGB
        rgb_image = resized_image.convert('RGB')

        # Convert the RGB image to a NumPy array
        rgb_array = np.array(rgb_image)

        # Detect the face in each frame and return (x,y)-coordinate of the bounding box
        boxes = face_recognition.face_locations(rgb_array, model='cnn')

        # Compute the face embedding
        encodings = face_recognition.face_encodings(rgb_array, boxes)

        for encoding in encodings:
            # add each encoding and name to the list
            knownEncodings.append(encoding.tolist())
            knownNames.append(name) 
            
    # save encoding to pickle
    print('[INFO] saving encodings...')
    data = {'encodings': knownEncodings, 'names': knownNames}
    # print(data)
    return data

if __name__ == '__main__':
    # with open('test_data.json', 'r') as file:
    #     dataset = file.read()
    dataset = ['data:image/jpeg;base64,/9j/4AAQSkZJRgABAQAAAQABAAD/+FSOvzSgB3QJvZ0Uxj4Ip4zHOxsjXDUPFwVlsY9HPCFXTyvODwseWmxYLAdDZayQ9Sf4Ejb6ljrFNjN1aYLij/2Q==']
    encode_faces(dataset,'yihan')