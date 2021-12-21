import json
from src.json_generator.annotation_json_generator.svg_segmentation import segmentation
import segemented_processing
import svg_segmentation
import cProfile

data = {}
data['annotations'] = []
annotation_data = []
name_idx = 0


def write_coco_annotaion(annotation_data):
    instance_id = 0

    for annotation in annotation_data:
        width = int(annotation[3] - annotation[1])
        height = int(annotation[4] - annotation[2])
        bbox = [annotation[1], annotation[2], width, height]
        area = width * height

        data['annotations'].append({'id': instance_id,
                                         #'image_id': annotation[0],
                                         'category_id': annotation[0],
                                         'bbox': bbox,
                                         'area': area,
                                         'segmentation': annotation[5]})
        instance_id += 1


    save_as_json(data)


def save_as_json(data):
    with open('D:/Test_Models/FAAI/test_files/annotation.json', 'w') as json_out:
        json.dump(data, json_out, indent=4)


if __name__ == '__main__':
    segmentation()
    segment_names = svg_segmentation.get_segmentation_names()
    name_count = len(segment_names)

    segemented_processing.make_polygon(segment_names)


