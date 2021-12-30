import sys
import time
import datetime
import json
from pathlib import Path
from cairosvg import svg2png
from tqdm import tqdm

class image_json_generator:
    def __init__(self, root_path, origin_folder, dest_folder, width, height):
        self.origin_folder = origin_folder
        self.dest_folder = dest_folder
        self.root_path = Path(root_path)
        self.dest_root_folder = Path(dest_folder).mkdir(exist_ok=True)
        self.origin_path = self.root_path / Path(origin_folder)
        self.dest_path = self.root_path / Path(dest_folder)
        self.images_json = {}
        self.images_json['image'] = []
        self.width = width
        self.height = height

    def traversal_and_convert(self):
        id_counter = 0
        deleted_files = []
        start = time.time()

        print('Gathering all .svg files under "' + self.origin_folder + '" ...')
        svg_list = list(self.origin_path.glob('**/*.svg'))

        print('Total: ' + str(len(svg_list)) + ' files')

        for cur_svg in tqdm(svg_list, desc='Progress', mininterval=0.5, unit='image'):
            #* Generate destination path
            cur_png_str = str(cur_svg)
            cur_png_str = cur_png_str.replace(self.origin_folder, self.dest_folder)
            cur_png = Path(cur_png_str)
            cur_png = cur_png.with_suffix('.png')
            cur_png.parent.mkdir(parents=True, exist_ok=True) #? Make directory if destination path doesn't exists

            relative_cur_png = str(Path(cur_png).relative_to(self.root_path))

            #* Convert to png
            try:
                svg2png(url=str(cur_svg)
                        ,write_to=str(cur_png)
                        ,parent_width=self.width
                        ,parent_height=self.height)
            except TypeError:
                deleted_files.append(str(cur_svg))
                cur_svg.unlink()  #? Delete src file if it is broken
            else:
                self.images_json['image'].append(self.generate_single_image_json(id_counter, relative_cur_png))
                id_counter += 1  
        
        #* Print result
        sec = time.time() - start
        times = str(datetime.timedelta(seconds=sec)).split(".")
        times = times[0]
        print("Runtime: ", times)
        print('Converted ' + str(id_counter) + ' files.')
        if deleted_files:
            print('Deleted ' + str(len(deleted_files)) + ' files.')
            print(deleted_files)

    def generate_single_image_json(self, file_id, file_name):
        data = {}
        data['id'] = file_id
        data['width'] = self.width
        data['height'] = self.height
        data['file_name'] = file_name
        return data

    def dump_image_result(self, out_path):
        with open(out_path + '\\image.json', 'w') as json_file:
            json.dump(self.images_json, json_file, indent=4)

    def generate_image_json(self):
        self.traversal_and_convert()
        self.dump_image_result(str(self.origin_path))
        print("Generated " + str(self.origin_path) + "\\image.json successfully.")

if __name__ == "__main__":
    DATA_ROOT = 'C:\\Users\\tuna1\\Documents\\AIFasion\\'

    if len(sys.argv) != 5 :
        print('ex) python image_json_generator.py origin_folder dest_folder 400(width) 300(height)')
    else:
        generator = image_json_generator(DATA_ROOT, sys.argv[1], sys.argv[2], int(sys.argv[3]), int(sys.argv[4]))
        generator.generate_image_json()
