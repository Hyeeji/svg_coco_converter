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
        width = int(annotation[4] - annotation[2])
        height = int(annotation[5] - annotation[3])
        bbox = [annotation[2], annotation[3], width, height]
        area = width * height
        #segmentation_name = annotation[-1]

        data['annotations'].append({'id': instance_id,
                                         'image_id': annotation[0],
                                         'category_id': annotation[1],
                                         #'segmentation_name': segmentation_name,
                                         'bbox': bbox,
                                         'area': area,
                                         'segmentation': [annotation[6]]})
        instance_id += 1


    save_as_json(data)


def save_as_json(data):
    with open('../../../test_files/annotations.json', 'w') as json_out:
        json.dump(data, json_out, indent=4)


if __name__ == '__main__':
    segmentation()
    segemented_processing.make_polygon()


