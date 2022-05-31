'''
Making data slot of parking line with
conversion of list & dict to json for
the occupancy detection
'''

import cv2
import json

refPt = []
cropping = False
data = []
image = cv2.imread('setup_image.jpg')
resolution = image.shape
print(resolution)


def click_and_crop(event, x, y, flags, param):
    current_pt = {'id': 0, 'points': []}
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
        current_pt['id'] = data_already
        data.append(current_pt)
        # data_already+=1
        refPt = []
        print(data)
    return data


# image = cv2.resize(img, None, fx=0.6, fy=0.6)
# clone = image.copy()
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

with open('data-slot.json', 'w') as f:
    json.dump(data, f)
