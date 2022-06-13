'''
Making data slot of parking line with
conversion of list & dict to json for
the occupancy detection
'''

import os
import cv2
import json
import requests

refPt = []
cropping = False
data = []

f = open('Location-Camera.json')
camera_data = json.load(f)
# print('camera=', camera_data[0]['Camera'])

curDir = os.getcwd()
print(curDir)


def click_and_crop(event, x, y, flags, param):
    current_pt = {'Slot': 0, 'points': []}
    # grab references to the global variables
    global refPt, cropping
    if event == cv2.EVENT_LBUTTONDOWN:
        refPt.append((x, y))
        print('x,y : ', x, y)
        cropping = False
    if len(refPt) == 4:
        if data == []:
            data_already = 1
        else:
            data_already = len(data)+1

        cv2.line(image, refPt[0], refPt[1], (0, 255, 0), 1)
        cv2.line(image, refPt[1], refPt[2], (0, 255, 0), 1)
        cv2.line(image, refPt[2], refPt[3], (0, 255, 0), 1)
        cv2.line(image, refPt[3], refPt[0], (0, 255, 0), 1)

        temp_lst1 = list(refPt[0])
        temp_lst2 = list(refPt[1])
        temp_lst3 = list(refPt[2])
        temp_lst4 = list(refPt[3])

        current_pt['points'] = [temp_lst1, temp_lst2, temp_lst3, temp_lst4]
        current_pt['Slot'] = data_already
        data.append(current_pt)
        # data_already+=1
        refPt = []
        print(data)
    return data


path = "{}/setup_image".format(curDir)
dir_list = os.listdir(path)
print("Files and directories in '", path, "' :")

# prints all files
print(dir_list)

# name_of_location = input("Nama Lokasi: ")
# floor_of_location = int(input("Floor: "))

image_name = input("Setup Image: (without .jpg)")
# image_name = "{}_{}".format(name_of_location, floor_of_location)
image_dir = "{}/setup_image/{}.jpg".format(curDir, image_name)
print('image_dir', image_dir)

image = cv2.imread(image_dir)
resolution = image.shape
print(resolution)

cv2.namedWindow("Click to mark points")
cv2.imshow("Click to mark points", image)
cv2.setMouseCallback("Click to mark points", click_and_crop)

# keep looping until the 'q' key is pressed
while True:
    # display the image and wait for a keypress
    cv2.imshow("Click to mark points", image)
    key = cv2.waitKey(1) & 0xFF
    if cv2.waitKey(33) == 27:
        break

cv2.destroyAllWindows()  # important to prevent window from becoming inresponsive

# print(camera_data['Floor'])
# print(camera_data['Cluster'])

floor = int(input('Floor: '))
cluster = input('Cluster: ')
for item in camera_data:
    check_name = "{}_{}".format(item['Location'], item['Floor'])
    if check_name == image_name:
        camera = item['Camera']
        print("CAMERA", camera)
    else:
        print("not found!")

for i in range(len(data)):
    data[i]['Floor'] = floor
    data[i]['Cluster'] = cluster
    data[i]['Camera'] = camera

print('Slot Data: ', data)

try:
    if not os.path.exists('data-slot'):
        os.makedirs('data-slot')
except:
    print("Error: Creating directory of data")

json_name = "{}/data-slot/{}_{}-slot.json".format(curDir, image_name, cluster)
with open(json_name, 'w') as f:
    json.dump(data, f)

'''
POST json here
'''
file = open(json_name, "rb")
url = "https://android-api-btwe4mw5iq-et.a.run.app/ml/uploadSlot" #API Slot

response = requests.post(url, files={"file": file})
if response.status_code == 201:
    print("POST success!")
else:
    print("Retry")
