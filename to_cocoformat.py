import json


data = {}
data['annotations'] = []

def write_coco_annotaion(annotation_data):

    '''for annotation in annotation_data:
        data['annotations'].append({'name': annotation[0],
                                    'tag': annotation[1],
                                    'segementation': annotation[2]})'''

    data['annotations'].append({'name' : annotation_data[0][0],
                                 'tag' : annotation_data[0][1],
                                 'segementation' : annotation_data[1]})
    print(annotation_data[0], annotation_data[1])



