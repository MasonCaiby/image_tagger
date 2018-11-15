import cv2
import numpy as np
from image_vars import colors

def add_banner(image_source, cv2_window):

    image = cv2.imread(image_source)
    height, width, channel = image.shape

    final_image = np.zeros((height+100, width, 3), dtype=np.uint8)
    final_image[100:, :, :] = image

    return final_image

def draw_old_boxes():
    for ref_point in ref_points:
        cv2.rectangle(image, ref_point[0], ref_point[1], colors[ref_point[2]], line_width)

def tag_image(image_source, colors, image_dict, cv2_window):
    global ref_point, image, clone, ref_points, line_width

    try:
        image = cv2.imread(image_source)
        height, width, channel = image.shape
        original = image.copy()
    except Exception as e:
        return None, None

    line_width = 3

    cv2.setMouseCallback(cv2_window, click_and_crop)

    if image_dict:
        ref_points = image_dict['ref_points']
        draw_old_boxes()

    else:
        ref_points = []

    clone = image.copy()

    while True:
        # display the image and wait for a keypress
        cv2.imshow(cv2_window, image)
        key = cv2.waitKey(1) & 0xFF

        if key >= 48 and key < 58:
            if len(ref_point) < 2:
                print("Hmmm looks like you are trying to define a class while"
                      " mouse is pressed down")
                continue
            input_class = key - 48
            try:
                ref_point[2] = input_class
            except:
                ref_point.append(input_class)
            if ref_point not in ref_points:
                ref_points.append(ref_point)
            print(ref_points)

            # draw a rectangle around the region of interest
            rect_color = colors[input_class]
            cv2.rectangle(clone, ref_point[0], ref_point[1], rect_color, line_width)
            cv2.imshow(cv2_window, clone)
            image = clone.copy()
        # if the 'r' key is pressed, reset the cropping region
        if key == ord("r"):
            ref_points = []
            image = original.copy()
            clone = image.copy()

        elif key == ord("x"):
            print('removing ', rect)
            ref_points.remove(rect)
            image = original.copy()
            draw_old_boxes()
            clone = image.copy()

        # if the 'q' key is pressed, break from the loop
        elif key == ord("q"):
            image_dict = {'width' : width,
                          'height': height,
                          'ref_points': ref_points}
            return image_dict, 'quit'

        elif key == ord(" "):
            if image_dict == None:
                image_dict = {'width' : width,
                              'height': height,
                              'ref_points': ref_points}

            else:
                image_dict['ref_points'] = ref_points

            return image_dict, None

def click_and_crop(event, x, y, flags, param):
    # grab references to the global variables
    global ref_point, image, rect

    # if the left mouse button was clicked, record the starting
    # (x, y) coordinates
    if event == cv2.EVENT_LBUTTONDOWN:
        ref_point = [(x, y)]

        # check if event is moving a box
        rect = check_moving(x,y)
        if rect:
            print(rect, ' selected')


    # check to see if the left mouse button was released
    elif event == cv2.EVENT_LBUTTONUP:
        # record the ending (x, y) coordinates
        ref_point.append((x, y))

    elif len(ref_point) == 1 and event == cv2.EVENT_MOUSEMOVE:
        image = clone.copy()
        cv2.rectangle(image, ref_point[0], (x,y), (0,0,0), line_width)


def check_moving(x,y):
    rects = None

    for rect in ref_points:
        high_y = min(rect[0][1], rect[1][1])
        low_y = max(rect[0][1], rect[1][1])
        left_x = min(rect[0][0], rect[1][0])
        right_x = max(rect[0][0], rect[1][0])

        if (((left_x - line_width <= x <= left_x + line_width) or
             (right_x - line_width <= x <= right_x + line_width)) and
             (low_y - line_width >= y >= high_y + line_width)):
            rects = rect
            break

        elif (((high_y <= y <= high_y + line_width) or
              (low_y <= y <= low_y + line_width)) and
              (left_x - line_width/2 <= x <= right_x + line_width/2)):
            rects = rect
            break


    return rects

if __name__ == '__main__':
    image_source = 'ir_test.png'
    tag_image(image_source, colors, {'width': 1280,
                                     'height': 720,
                                     'ref_points': [[(235, 305), (386, 462), 1],
                                                   [(471, 346), (621, 521), 2],
                                                   [(581, 220), (756, 341), 3]]
                                    })
