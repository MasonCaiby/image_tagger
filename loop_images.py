import os
import pickle
import cv2
import argparse
import sys

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


def loop_images(proj_dir, directory, save_freq=100):
    classes = get_classes(proj_dir)
    print(classes)

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


def get_classes(project_dir):
    classes_path = os.path.join(project_dir, 'classes.txt')

    try:
        with open(classes_path, 'r') as classes_text:
            classes = classes_text.read().split('\n')
            print(classes)
        if input("Would you like to add classes (y/n) ").lower() == 'y':
            classes = add_classes(len(classes), classes)
            with open(classes_path, 'w') as classes_text:
                classes_text.write('\n'.join(classes))
                
    except OSError as e:
        if e.errno == 2:
            classes = []
            classes = add_classes(0, classes)
            with open(classes_path, 'w') as classes_text:
                classes_text.write('\n'.join(classes))
        else:
            sys.exit("That's a weird error")

    return classes

def add_classes(start_number, classes):
    for i in range(start_number, 10):
        this_class = input('input class number {}: '.format((i+1)%10))
        if this_class == '':
            break
        else:
            classes.append(this_class)
    return classes


if __name__ == '__main__':
#     loop_images('test_images/', save_freq=5)
    parser = argparse.ArgumentParser()
    parser.add_argument("-proj_dir", "--proj_dir", help="Person to send email to")
    parser.add_argument("-dir", "--dir", help="Person to send email to")
    args = parser.parse_args()

    loop_images(args.proj_dir, args.dir, save_freq=100)
