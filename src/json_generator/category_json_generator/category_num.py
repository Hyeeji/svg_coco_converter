import json

with open('../../../test_files/test.json', 'r') as f:
    json_file = json.load(f)

class_id_to_num = dict()

for i in json_file['categories']:
    class_id_to_num[i['id']] = 0

for ann in json_file['annotations']:
    if ann['category_id'] != 'None':
        class_id_to_num[ann['category_id']] += 1

num_list = []
for class_id, num in class_id_to_num.items():
    if num != 0:
        print(f'class_id : {class_id}, num : {num}')
        num_list.append(num)
