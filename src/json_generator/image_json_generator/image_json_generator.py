import os
from pathlib import WindowsPath
import sys
import json
from typing import OrderedDict
from svg_to_image import svg_convert
from generate_image import generate_single_image_json

class image_json_generator:
    def __init__(self, root_path, origin_file, dest_file, width, height):
        self.dest_root_folder = dest_file
        self.origin_path = root_path + origin_file
        self.dest_path = root_path + dest_file
        self.id_counter = 0
        self.images_json = OrderedDict()
        self.images_json['image'] = []
        self.width = width
        self.height = height

    def traversal_and_convert(self, cur_path, relative_cur_path, dest_path):
        next_file_list = os.listdir(cur_path)

        for next_file in next_file_list:
            next_dest_path = dest_path + '/'            # 복사 경로상에서 다음 경로
            next_file_path = cur_path + '/' + next_file # 원본 경로상에서 파일명까지 포함한 다음 경로

            if os.path.isdir(next_file_path):
                next_dest_path += next_file
                try:
                    if not os.path.exists(next_dest_path):
                        os.makedirs(next_dest_path)
                    self.traversal_and_convert(next_file_path, relative_cur_path + '/' + next_file , next_dest_path)
                except OSError:
                    print ('Error: Creating directory ' + next_dest_path + '.')

            elif os.path.isfile(next_file_path):
                extension = next_file.split('.')[1]
                if extension == "svg":
                    new_file_name = next_file.replace('.svg', '.png')
                    next_dest_path += new_file_name
                    svg_convert(next_file_path, next_dest_path, self.width, self.height)
                    self.images_json['image'].append(generate_single_image_json(self.id_counter, self.width, self.height, relative_cur_path + '/' + new_file_name))
                    self.id_counter += 1
                else:
                    print(next_file + "is not .svg file.")
            else:
                continue        

    def dump_image_result(self, out_path):
        with open(out_path + '/image.json', 'w') as json_file:
            json.dump(self.images_json, json_file, indent=4)

    def generate_image_json(self):
        self.traversal_and_convert(self.origin_path, self.dest_root_folder, self.dest_path)
        self.dump_image_result(self.origin_path)
        print("Generated " + self.origin_path + "/image.json successfully.")

if __name__ == "__main__":
    DATA_ROOT = 'C:/Users/tuna1/Documents/FashionDataSet/'

    if len(sys.argv) != 5 :
        print('ex) python image_json_generator.py origin_folder dest_folder 400(width) 300(height)')
    else:
        generator = image_json_generator(DATA_ROOT, sys.argv[1], sys.argv[2], int(sys.argv[3]), int(sys.argv[4]))
        generator.generate_image_json()