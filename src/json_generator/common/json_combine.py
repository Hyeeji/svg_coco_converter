import json
import glob

if __name__ == '__main__':
    data = {}

    with open('../../../test_files/categories.json') as category:
        categories = json.load(category)

    with open('../../../test_files/images.json') as image:
        images = json.load(image)

    with open('../../../test_files/annotations.json') as annotation:
        annotations = json.load(annotation)

    data['categories'] = categories['categories']
    data['images'] = images['images']
    data['annotations'] = annotations['annotations']

    with open('../../../test_files/all.json', 'w') as all_json:
        json.dump(data, all_json, indent=4)

