import tensorflow as tf
from tensorflow import keras
import numpy as np
import cv2
import json
import os

print(tf.__version__)

class_dictionary = {}
class_dictionary[0] = 'empty'
class_dictionary[1] = 'occupied'

model = tf.keras.models.load_model('saved_model/carkir')

f = open('data-slot.json')
data = json.load(f)

the_image = 'test_image.jpg'
img = cv2.imread(the_image)


def make_prediction(image):
    #Rescale image
    img = image/255.

    #Convert to a 4D tensor
    image = np.expand_dims(img, axis=0)
    print(image.shape)

    # make predictions on the preloaded model
    class_predicted = model.predict(image)
    inID = np.argmax(class_predicted[0])
    label = class_dictionary[inID]
    return label

def assign_spots_map(image, spot_dict=data, make_copy=True, color=[255, 0, 0], thickness=2):
    if make_copy:
        new_image = np.copy(image)
    final_spot_dict = {}
    for spot in spot_dict:
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
        final_spot_dict['{}'.format(spot['id'])] = spot_place
        cv2.rectangle(new_image, (int(top_left_x), int(top_left_y)),
                      (int(bot_right_x), int(bot_right_y)), color, thickness)
    return new_image, final_spot_dict


marked_spot_images, spots = assign_spots_map(img)
print('spots: ', spots)
cv2.imwrite('marked_spot.jpg', marked_spot_images)


def predict_on_image(image, spot_dict=spots, make_copy=True, color=[0, 255, 0], alpha=0.5):
    if make_copy:
        new_image = np.copy(image)
        overlay = np.copy(image)
    cnt_empty = 0
    all_spots = 0
    for no, spot in spot_dict.items():
        all_spots += 1
        x1 = spot[0]
        y1 = spot[1]
        x2 = spot[2]
        y2 = spot[3]
        # (x1, y1, x2, y2) = spot
        # (x1, y1, x2, y2) = (int(x1), int(y1), int(x2), int(y2))
        # crop this image
        spot_img = image[y1:y2, x1:x2]
        spot_img = cv2.resize(spot_img, (48, 48))

        label = make_prediction(spot_img)
        #         print(label)
        if label == 'empty':
            cv2.rectangle(overlay, (x1, y1), (x2, y2), color, -1)
            cnt_empty += 1
        if label == 'occupied':
            cv2.rectangle(overlay, (x1, y1), (x2, y2), [0, 0, 255], -1)

    cv2.addWeighted(overlay, alpha, new_image, 1 - alpha, 0, new_image)

    cv2.putText(new_image, "Available: %d spots" % cnt_empty, (30, 95),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.7, (255, 255, 255), 2)

    cv2.putText(new_image, "Total: %d spots" % all_spots, (30, 125),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.7, (255, 255, 255), 2)
    save = True

    if save:
        filename = 'with_marking.jpg'
        cv2.imwrite(filename, new_image)

    return new_image


predicted_images = predict_on_image(img)