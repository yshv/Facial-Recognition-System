import pickle
import face_recognition
import cv2
import sys


name = input("Name: ")
try:
    f = open("ref_name.pkl", "rb")
    ref_dictt = pickle.load(f)
    f.close()
except:
    ref_dictt = {}
if ref_dictt:
    new_id = str(max(map(int, ref_dictt.keys())) + 1)
else:
    new_id = '1'
print("ID:", new_id)

ref_dictt[new_id] = name

f = open("ref_name.pkl", "wb")
pickle.dump(ref_dictt, f)
f.close()

try:
    f = open("ref_embed.pkl", "rb")
    embed_dictt = pickle.load(f)
    f.close()
except:
    embed_dictt = {}

webcam = cv2.VideoCapture(0)

num_pics = 0
while True:
    key = cv2.waitKey(1)
    check, frame = webcam.read()
    cv2.imshow("Capturing", frame)
    small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
    rgb_small_frame = small_frame[:, :, ::-1]

    face_locations = face_recognition.face_locations(rgb_small_frame)

    for (top, right, bottom, left) in face_locations:
        cv2.rectangle(frame, (left*4, top*4),
                      (right*4, bottom*4), (0, 0, 255), 2)

    cv2.imshow("Capturing", frame)

    if key == ord('s'):
        face_locations = face_recognition.face_locations(rgb_small_frame)
        if face_locations != []:
            face_encoding = face_recognition.face_encodings(frame)[0]
            if new_id in embed_dictt:
                embed_dictt[new_id] += [face_encoding]
            else:
                embed_dictt[new_id] = [face_encoding]
            num_pics += 1
            print("Picture taken", num_pics)
            if num_pics == 5:
                webcam.release()
                cv2.destroyAllWindows()
                break
        else:
            print("Could not capture face embeddings. Try again.")
    elif key == ord('q'):
        print("Turning off camera.")
        webcam.release()
        print("Camera off.")
        print("Program ended.")
        cv2.destroyAllWindows()
        break

f = open("ref_embed.pkl", "wb")
pickle.dump(embed_dictt, f)
f.close()
