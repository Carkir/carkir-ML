'''
Carkir ML main code
Load model carkir.h5
GET the location, floor, cluster, and slot points
Detection on every slot points on the video
POST the empty (1) / occupied (0)
Looping the video to act as a real camera
'''

import tensorflow as tf
import numpy as np
import cv2
import json
import requests
import time
import os

print(tf.__version__)

class_dictionary = {}
class_dictionary[0] = 'empty'
class_dictionary[1] = 'occupied'

model = tf.keras.models.load_model('carkir.h5')

curDir = os.getcwd()
# path = "{}/setup_image".format(curDir)
# dir_list = os.listdir(path)
# print("Files and directories in '", path, "' :")

# prints all files
# print(dir_list)
# image_name = input("Name of Location: ")
image_name = "BLK-HDPTZ12_1"
# image_floor = input("Floor: ")
image_floor = 1.0
# image_cluster = input("Cluster: ")
image_cluster = "A"
json_name = "{}_{}-slot".format(image_name, image_cluster)
response = requests.get('https://android-api-btwe4mw5iq-et.a.run.app/ml/getSlot/{}'.format(json_name))
print(response.status_code)
if response.status_code == 201:
    print("GET success!")

data = json.loads(response.text) #list
# f = open('Tomas_Sak_1_A-slot.json')
# data = json.load(f)
print('JSON-slot: ', data)

the_image = 'setup_image/Tomas_Sak_1.jpg'
img = cv2.imread(the_image)


def make_prediction(image):
    #Rescale image
    img = image/255.

    #Convert to a 4D tensor
    image = np.expand_dims(img, axis=0)
    # print(image.shape)

    # make predictions on the preloaded model
    class_predicted = model.predict(image)
    inID = np.argmax(class_predicted[0])
    label = class_dictionary[inID]
    return label

def assign_spots_map(image, spot_dict=data, make_copy=True, color=[255, 0, 0], thickness=2):
    if make_copy:
        new_image = np.copy(image)
    final_spot_list = []
    for spot in spot_dict:
        final_spot_dict = {}
        spot_points = spot['points']
        x1 = spot_points[0][0]
        x2 = spot_points[1][0]
        x3 = spot_points[2][0]
        x4 = spot_points[3][0]
        y1 = spot_points[0][1]
        y2 = spot_points[1][1]
        y3 = spot_points[2][1]
        y4 = spot_points[3][1]
        top_left_x = min([x1, x2, x3, x4])
        top_left_y = min([y1, y2, y3, y4])
        bot_right_x = max([x1, x2, x3, x4])
        bot_right_y = max([y1, y2, y3, y4])
        spot_place = (top_left_x, top_left_y, bot_right_x, bot_right_y)
        final_spot_dict['points'] = spot_place
        final_spot_dict['Floor'] = spot['Floor']
        final_spot_dict['Cluster'] = spot['Cluster']
        final_spot_dict['Slot'] = spot['Slot']
        cv2.rectangle(new_image, (int(top_left_x), int(top_left_y)), (int(bot_right_x), int(bot_right_y)), color, thickness)
        final_spot_list.append(final_spot_dict)
        # print(final_spot_dict)
        # print(final_spot_list)
    return new_image, final_spot_list


marked_spot_images, spots = assign_spots_map(img)
cv2.imwrite('marked_spot{}.jpg'.format(image_name), marked_spot_images)


def detection(x):
    # threading.Timer(5.0, detection).start()
    new_image = np.copy(image)
    overlay = np.copy(image)
    cnt_empty = 0
    all_spots = 0
    color = [0, 255, 0]
    alpha = 0.5
    for item in spots:
        result_data = {}
        result_data['Floor'] = float(item['Floor'])
        result_data['Cluster'] = item['Cluster']
        result_data['Slot'] = float(item['Slot'])
        all_spots += 1
        (x1, y1, x2, y2) = item['points']
        (x1, y1, x2, y2) = (int(x1), int(y1), int(x2), int(y2))
        # crop this image
        spot_img = new_image[y1:y2, x1:x2]
        spot_img = cv2.resize(spot_img, (48, 48))

        label = make_prediction(spot_img)
        # print(label)
        if label == 'empty':
            cv2.rectangle(overlay, (int(x1), int(y1)), (int(x2), int(y2)), color, -1)
            cnt_empty += 1
            result_data['Occupancy'] = float(1.0)
        if label == 'occupied':
            cv2.rectangle(overlay, (x1, y1), (x2, y2), [0, 0, 255], -1)
            result_data['Occupancy'] = float(0.0)

        post_data.append(result_data)
        # print(result_data)
        # print(post_data)

    print('Dict ', post_data)
    print('Empty: ', cnt_empty)

    cv2.addWeighted(overlay, alpha, new_image, 1 - alpha, 0, new_image)

    cv2.putText(new_image, "Available: %d spots" % cnt_empty, (30, 95),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.7, (255, 255, 255), 2)

    cv2.putText(new_image, "Total: %d spots" % all_spots, (30, 125),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.7, (255, 255, 255), 2)

    # name = "{}/extract_detect/detect{}.jpg".format(curDir, x)
    # print("Creating.. " + name)
    # cv2.imwrite(name, new_image)

    json_name = "{}.json".format(image_name)
    with open(json_name, 'w') as f:
        json.dump(post_data, f)
    file = open(json_name, "rb")
    url = "https://android-api-btwe4mw5iq-et.a.run.app/ml/uploadOccupancy"  # API

    response = requests.post(url, files={"file": file})
    if response.status_code == 201:
        print("POST success!")


try:
    if not os.path.exists('extract_detect'):
        os.makedirs('extract_detect')
except:
    print("Error: Creating directory of data")


def getImage(x):
    image_gotten = np.copy(image)
    name = "{}/extract_detect/extract{}.jpg".format(curDir, x)
    print("Creating.. " + name)
    # cv2.imwrite(name, image_gotten)


# video_name = "https://storage.googleapis.com/carkir-video/Detection%20of%20free%20parking%20spaces%20%20v0.1.mp4"
video_name = data[0]['Camera']
cap = cv2.VideoCapture(video_name)
ret = True
frame_rate = 10
prev = 0
count = 0
n = 0

frame_width = int(cap.get(3))
frame_height = int(cap.get(4))
size = (frame_width, frame_height)

while ret:
    time_elapsed = time.time() - prev
    ret, frame = cap.read()

    if ret:
        image = cv2.resize(frame, (640, 480), interpolation=cv2.INTER_AREA)
        cv2.imshow('video', image)
        n += 1
        count += 1
        # print(count)
        post_data = []
        result_data = {'Floor': 1, 'Cluster': 'A', 'Slot': 0, 'Occupancy': 0}
        if count == 50:
            count = 0
            # getImage(n)
            detection(n)
    else:
        print("Try looping")
        cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
        ret = True

    if cv2.waitKey(10) & 0xFF == ord('q'):
        print("Video interrupted!")
        break


cap.release()
cv2.destroyAllWindows()

