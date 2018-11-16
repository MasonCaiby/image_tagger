import os
import random
import pickle


def make_names_yolo(proj_dir, image_labels):
    if proj_dir == './':
        dir_name = os.getcwd()
        print(dir_name)
    else:
        dir_name = proj_dir
    print(dir_name)

    classes_path = os.path.join(proj_dir, 'classes.txt')
    names_path = os.path.join(dir_name, 'classes.names')
    with open(classes_path, 'r') as classes_text:
        classes = classes_text.read()
        num_classes = len(classes.split('\n'))
        with open(names_path, 'w') as names_test:
            names_test.write(classes)
    print("Made names file at: {}".format(names_path))

    return num_classes

def make_yolo_box(box, width, height):
    image_class = box[2]
    x_center = ((box[0][0] + box[1][0]) / 2) / width
    y_center = ((box[0][1] + box[1][1]) / 2) / height
    x_width = abs(box[0][0] - box[1][0]) / width
    y_height = abs(box[0][1] - box[1][1]) / height

    return '{} {} {} {} {}\n'.format(image_class, x_center, y_center,
                                     x_width, y_height)

def make_train_valid_boxes(proj_dir, image_labels, validation_file, train_file):

    for image, image_dict in image_labels.items():
        width = image_dict['width']
        height = image_dict['height']
        ref_points = image_dict['ref_points']
        boxes = []
        if len(ref_points) == 0:
            continue

        if random.random() < 0.2:
            validation_file += image + '\n'
        else:
            train_file += image + '\n'

        text_path = image.split('.')[0]

        with open(image.split('.')[0]+'.txt', 'w') as box_file:
            for box in ref_points:
                box_file.write(make_yolo_box(box, width, height))

    with open(os.path.join(proj_dir, 'train.txt'), 'w') as train_path:
        train_path.write(train_file)
    with open(os.path.join(proj_dir, 'validate.txt'), 'w') as valid_path:
        valid_path.write(validation_file)


def yolo_exporter(proj_dir, image_labels):
    ''' yolo takes:
        # classes = 2 # get len(of classes)
        # train  = cat-dog-train.txt  # make this from image_labels
        # valid  = cat-dog-test.txt  # make this from image_labels
        # names = classes.names  # this will come from classes.txt
        # backup = backup/ # Let's set this to the proj_dir
    '''
    with open(os.path.join(proj_dir,'image_dicts.txt'), 'r') as image_labels_txt:
        image_labels_dicts = image_labels_txt.read().split('\n')

    for image_labels_dict in image_labels_dicts:
        num_classes = make_names_yolo(proj_dir, image_labels)
        make_train_valid_boxes(proj_dir, image_labels)

        with open('yolo_train.obj', 'w') as obj_file:
            obj_file.write('''classes = {}
                              \rtrain = ../train.txt
                              \rvalid = ../validate.txt
                              \rnames = ../classes.names
                              \rbackup = {}'''.format(num_classes, '../backup/'))


if __name__ == '__main__':
    with open('test_images/image_labels.pickle', 'rb') as handle:
        image_labels = pickle.load(handle)

    yolo_exporter('./', image_labels)
