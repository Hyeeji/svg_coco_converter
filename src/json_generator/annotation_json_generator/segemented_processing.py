import os
import cairosvg
import cv2
import numpy as np
import annotation_json_generator
import json
import copy

segmentation_data = []
annotation_data = []

def convert_svg_to_png(svg_path):
    # Convert each sub-SVG into image

    segmented_file_path = svg_path
    out_img_filepath = svg_path.replace('.svg', '.png')
    #print("Writing {0}...".format(out_img_filepath))
    cairosvg.svg2png(url=segmented_file_path, write_to=segmented_file_path.replace('.svg', '.png'))

    # TODO: Pyvips dll load 문제 있음...
    # image = pyvips.Image.new_from_file(segmented_file_path, dpi=600)
    # image.write_to_file("test.png")

    return out_img_filepath

def process_img(img_path, width_stride, segment_names, name_idx, category_path):
    img = cv2.imread(img_path, cv2.IMREAD_UNCHANGED) # Alpha channel read

    # Since all meaningful information is colored in black (or whatever), we only care about the pixels which is not transparent
    bw_img = (img[:,:,3] > 0) # alhpa != 0

    width = bw_img.shape[1]
    height = bw_img.shape[0]

    tops = []
    bottoms = []

    current_w = 0
    while current_w < width:
        column_arr = bw_img[:,current_w]
        positive_indices = np.where(column_arr) # for each column of pixels
        if len(positive_indices[0]) == 0: # if there is no meaningful pixel, continue
            current_w += width_stride
            continue

        # if there is meaningful pixel, gather topmost and bottommost pixel
        tops.append((current_w, np.max(positive_indices)))
        bottoms.append((current_w, np.min(positive_indices)))

        # for every width_stride column
        current_w += width_stride

    # Connect topmost and bottommost pixels and close the loop(=polygon)
    point_num = len(bottoms)
    for i in range(point_num):
        tops.append(bottoms[point_num-i-1])
    if len(tops) == 0:
        return

    tops.append(tops[0]) # force closing


    # -- Plotting for debug
    x_vals = []
    y_vals = []

    for point in tops:
        x_vals.append(point[0])
        y_vals.append(point[1])
        segmentation_data.append(int(point[0]))
        segmentation_data.append(int(point[1]))

    xmin = min(x_vals)
    ymin = min(y_vals)
    xmax = max(x_vals)
    ymax = max(y_vals)

    bbox_point = [int(xmin), int(ymin), int(xmax), int(ymax)]
    make_annotation_data(bbox_point, segment_names, name_idx, category_path)


def make_annotation_data(bbox_points, segment_names, name_idx, category_path):
    global annotation_data, segmentation_data
    name_count = len(segment_names)

    xmin = bbox_points[0]
    ymin = bbox_points[1]
    xmax = bbox_points[2]
    ymax = bbox_points[3]

    with open(category_path) as category_json:  # root argument로 받기
        all_category = json.load(category_json)
    category_id = None

    if name_idx < name_count:
        category_name = segment_names[name_idx]
        for category in all_category:
            if category['name'] == category_name:
                category_id = category['id']
                break
        name_idx += 1

    annotation_data.append([category_id, xmin, ymin, xmax, ymax, copy.deepcopy(segmentation_data)])

    # img name, category key, segmentaion 정보까지 넘겨서 annotation_json_generator에서 annotation 만들기
    # img 상대경로 추적해서 image.json 파일에 있는 file name 하고 비교해서 같으면 id 가져오기
    # category key name 받아와서 같은 name 있는지 category.json 파일에서 찾고 id 가져오기


def make_polygon(segment_names):
    segmented_root_path = 'D:/Test_Models/FAAI/segmented_files'
    WIDTH_STRIDE = 10
    #category_path = input("category_path : ")
    #category_path = os.path.dirname(os.path.realpath(path)) + '/' + 'categories.json'
    category_path = 'C:\\Users\\hyejiHan\\Documents\\GitHub\\svg_coco_converter\\test_files\\categories.json'

    # for each folder that contains sub-SVG,
    for segmented_svg_folder in os.listdir(segmented_root_path):
        svg_segment_folder = os.path.join(segmented_root_path,segmented_svg_folder)
        name_idx = 0

        # for each sub-SVG,
        for segmented_file in os.listdir(svg_segment_folder):
            if os.path.splitext(segmented_file)[1].find(".svg") is not -1:
                segmented_file_path = os.path.join(svg_segment_folder, segmented_file)

                # 1) convert svg to image
                out_img_file = convert_svg_to_png(segmented_file_path)
                print(segmented_file + 'is drawing to png')

                # 2) process image and generate polygon
                process_img(out_img_file, WIDTH_STRIDE, segment_names, name_idx, category_path)
                print(segmented_file + 'generate polygon')
                name_idx += 1
                segmentation_data.clear()
        annotation_json_generator.write_coco_annotaion(annotation_data)

