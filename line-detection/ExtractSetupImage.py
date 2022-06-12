import os.path
import json
import cv2

f = open('Location-Camera.json')
camera_data = json.load(f)

curDir = os.getcwd()
print(curDir)

try:
    if not os.path.exists('setup_image'):
        os.makedirs('setup_image')
except:
    print("Error: Creating directory of data")


def extractImage(location, floor, url):
    # url = "https://storage.googleapis.com/carkir-video/Detection%20of%20free%20parking%20spaces%20%20v0.1.mp4"

    location_name = "{}_{}".format(location, floor)
    cap = cv2.VideoCapture(url)

    while True:
        success, capture = cap.read()
        frame = cv2.resize(capture, (640, 480), interpolation=cv2.INTER_AREA)

        if success:
            name = "{}/setup_image/{}.jpg".format(curDir, location_name)
            print("Creating.. " + name)

            cv2.imwrite(name, frame)
            break
        else:
            break

    cap.release()
    cv2.destroyAllWindows()


# def extractImage(data = camera_data):
for data in camera_data:
    print('name: ', data['Location'])
    print('floor: ', data['Floor'])
    print('camera: ', data['Camera'])
    extractImage(data['Location'], data['Floor'], data['Camera'])


