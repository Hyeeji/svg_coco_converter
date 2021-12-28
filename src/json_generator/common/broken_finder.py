import sys
import time
import datetime
import json
import xml.etree.ElementTree as ET
from pathlib import Path

class broken_finder:
    def __init__(self, root_path, origin_folder):
        self.origin_folder = origin_folder
        self.root_path = Path(root_path)
        self.origin_path = self.root_path / Path(origin_folder)
        self.broken_json = {}
        self.broken_json['broken'] = []

    def traversal_and_convert(self):
        id_counter = 0
        start = time.time()

        print('Gathering all .svg files under "' + self.origin_folder + '" ...')
        svg_glob = self.origin_path.glob('**/*.svg')
        
        print('Searching broken files...')

        for cur_svg in svg_glob:
            relative_cur_svg = str(Path(cur_svg).relative_to(self.root_path))

            doc = ET.parse(cur_svg)
            root = doc.getroot()

            if root.tag == 'html':
                self.broken_json['broken'].append(self.generate_single_broken_json(id_counter, relative_cur_svg))
                id_counter += 1

        #* Print result
        sec = time.time() - start
        times = str(datetime.timedelta(seconds=sec)).split(".")
        times = times[0]
        print("Runtime: ", times)
        print('Found ' + str(id_counter) + ' brokenfiles.')

    def generate_single_broken_json(self, file_id, file_name):
        data = {}
        data['id'] = file_id
        data['file_name'] = file_name
        return data

    def dump_broken_result(self, out_path):
        with open(out_path + '\\broken.json', 'w') as json_file:
            json.dump(self.broken_json, json_file, indent=4)

    def generate_broken_json(self):
        self.traversal_and_convert()
        self.dump_broken_result(str(self.origin_path))
        print("Generated " + str(self.origin_path) + "\\broken.json successfully.")

if __name__ == "__main__":
    DATA_ROOT = 'C:\\Users\\tuna1\\Documents\\AIFasion\\'

    if len(sys.argv) != 2 :
        print('ex) python broken_finder.py origin_folder')
    else:
        finder = broken_finder(DATA_ROOT, sys.argv[1])
        finder.generate_broken_json()
