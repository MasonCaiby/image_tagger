import os
import pickle
import cv2
import argparse

from image_tagger import tag_image
from image_vars import colors


def get_previous_labels(directory):
    pickle_path = os.path.join(directory, 'image_labels.pickle')

    if os.path.isfile(pickle_path):
        with open(pickle_path, 'rb') as handle:
            image_labels = pickle.load(handle)
    else:
        image_labels = {}

    return image_labels, pickle_path


def save_pickle_file(pickle_path, image_labels):
    with open(pickle_path, 'wb') as handle:
        pickle.dump(image_labels, handle, protocol=pickle.HIGHEST_PROTOCOL)
    print('Saved data')


def loop_images(directory, save_freq=100):


    cv2_window = cv2.namedWindow("image_window", cv2.WINDOW_NORMAL)
    cv2.resizeWindow("image_window", 1000, 700)
    cv2.moveWindow("image_window", 0,0)
    image_labels, pickle_path = get_previous_labels(directory)

    for i, image in enumerate(os.listdir(directory)):
        image_path = os.path.join(directory,image)
        previous_labels = image_labels.get(image_path, None)
        print('previous labels: ', previous_labels)

        image_dict, quit = tag_image(image_path, colors, previous_labels, "image_window")
        if image_dict:
            image_labels[image_path] = image_dict

        if not i % save_freq:
            save_pickle_file(pickle_path, image_labels)

        if quit == 'quit':
            cv2.destroyAllWindows()
            break

    if i % save_freq:
        save_pickle_file(pickle_path, image_labels)
    cv2.destroyAllWindows()

if __name__ == '__main__':
#     loop_images('test_images/', save_freq=5)
    parser = argparse.ArgumentParser()
    parser.add_argument("-directory", "--directory", help="Person to send email to")
    args = parser.parse_args()

    loop_images(args.directory, save_freq=100)
