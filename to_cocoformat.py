import json

def write_coco_annotaion(annotation_data):

    data = {}

    data['annotations'] = []

    for annotation in annotation_data:
        data['annotations'].append({'id': annotation[0],
                                    'Group': annotation[1],
                                    'segementation': []})



