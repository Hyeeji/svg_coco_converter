import os
import sys
import cairosvg
import cv2
import numpy as np
import annotation_json_generator
import json
import copy
import time
from tqdm import tqdm
from pathlib import Path
import matplotlib.pyplot as plt
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))

segmentation_data = []
annotation_data = []


def convert_svg_to_png(svg_path):
    # Convert each sub-SVG into image
    svg_path = str(svg_path)
    segmented_file_path = svg_path
    out_img_filepath = svg_path.replace('.svg', '.png')
    #print("Writing {0}...".format(out_img_filepath))
    cairosvg.svg2png(url=segmented_file_path, write_to=segmented_file_path.replace('.svg', '.png'), parent_width=512,
                     parent_height=512)

    # TODO: Pyvips dll load 문제 있음...
    # image = pyvips.Image.new_from_file(segmented_file_path, dpi=600)
    # image.write_to_file("test.png")

    return out_img_filepath


def process_img(img_path, width_stride, segment_name, category_path, image_path, file_path, current_w):
    img = cv2.imread(img_path, cv2.IMREAD_UNCHANGED) # Alpha channel read

    bw_img = (img[:,:,3] > 0) # alhpa != 0

    width = bw_img.shape[1]
    height = bw_img.shape[0]

    tops = []
    bottoms = []

    last_point = current_w

    while current_w < width:
        column_arr = bw_img[:,current_w]
        positive_indices = np.where(column_arr) # for each column of pixels

        if (current_w - last_point) > width_stride:
            break

        if len(positive_indices[0]) == 0: # if there is no meaningful pixel, continue
            current_w += width_stride
            if len(tops) == 0:
                last_point = current_w
            continue

        # if there is meaningful pixel, gather topmost and bottommost pixel
        tops.append((current_w, np.max(positive_indices)))
        bottoms.append((current_w, np.min(positive_indices)))

        # for every width_stride column
        current_w += width_stride
        last_point = current_w

    point_num = len(bottoms)

    for i in range(point_num):
        tops.append(bottoms[point_num-i-1])
    if len(tops) == 0:
        return

    tops.append(tops[0]) # force closing

    x_vals = []
    y_vals = []

    for point in tops:
        x_vals.append(point[0])
        y_vals.append(point[1])
        segmentation_data.append(int(point[0]))
        segmentation_data.append(int(point[1]))

    #plt.scatter(x_vals, y_vals, s=0.5, c=colors[color_index])

    xmin = min(x_vals)
    ymin = min(y_vals)
    xmax = max(x_vals)
    ymax = max(y_vals)

    bbox_point = [int(xmin), int(ymin), int(xmax), int(ymax)]
    make_annotation_data(bbox_point, segment_name, category_path, image_path, file_path)

    if (current_w - last_point) > width_stride:
        process_img(img_path, width_stride, segment_name, category_path, image_path, file_path, current_w)


def make_annotation_data(bbox_points, segment_name, category_path, image_path, file_path):
    global annotation_data, segmentation_data

    xmin = bbox_points[0]
    ymin = bbox_points[1]
    xmax = bbox_points[2]
    ymax = bbox_points[3]

    with open(image_path) as image_json:
        all_image = json.load(image_json)
    image_id = None

    with open(category_path) as category_json:  # root argument로 받기
        all_category = json.load(category_json)
    category_id = None

    for filename in all_image['images']:
        if filename['file_name'] == file_path:
            image_id = filename['id']
            break

    for category in all_category['categories']:
        if category['name'] == segment_name:
            category_id = category['id']
            break

    annotation_data.append([image_id, category_id, xmin, ymin, xmax, ymax, copy.deepcopy(segmentation_data)])

    segmentation_data.clear()

    # img name, category key, segmentaion 정보까지 넘겨서 annotation_json_generator에서 annotation 만들기
    # img 상대경로 추적해서 image.json 파일에 있는 file name 하고 비교해서 같으면 id 가져오기
    # category key name 받아와서 같은 name 있는지 category.json 파일에서 찾고 id 가져오기


def make_polygon():
    segmented_root_path = 'D:/Test_Models/FAAI/test_segmented_files'
    p = Path(segmented_root_path)
    WIDTH_STRIDE = 1
    dest_path = 'ImageDataSet/'
    category_path = 'C:\\Users\\hyejiHan\\Documents\\GitHub\\svg_coco_converter\\test_files\\categories.json'
    image_path = 'C:\\Users\\hyejiHan\\Documents\\GitHub\\svg_coco_converter\\test_files\\images.json'

    for segmented_file_path in p.glob('**/*.svg'):
        # 1) convert svg to image
        out_img_file = convert_svg_to_png(segmented_file_path)
        print(segmented_file_path)

        # 2) process image and generate polygon
        first = str(segmented_file_path).split('segmented_files')

        second = first[1].rsplit(sep='\\', maxsplit=1)
        temp = second[0].replace('\\', '/')

        file_name = temp + '.png'
        file_path = dest_path + file_name
        file_path = file_path.replace('//', '/')

        segment_names_1 = second[1].split(sep='_', maxsplit=1)
        segment_name = segment_names_1[1].rsplit(sep='.', maxsplit=1)[0]

        process_img(out_img_file, WIDTH_STRIDE, segment_name, category_path, image_path, file_path, 0)

    annotation_json_generator.write_coco_annotaion(annotation_data)

if __name__ == '__main__':
    '''segmented_root_path = 'D:/Test_Models/FAAI/segmented_files'
    p = Path(segmented_root_path)

    for i in p.glob('**/*.svg'):
        print(i)'''
    make_polygon()