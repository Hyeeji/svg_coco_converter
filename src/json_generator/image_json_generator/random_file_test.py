import os
import sys

class random_file:
    def __init__(self, root_path, origin_file, dest_file):
        self.dest_root_folder = dest_file
        self.origin_path = root_path + origin_file
        self.dest_path = root_path + dest_file

    def traversal_and_convert(self, cur_path, relative_cur_path, dest_path):
        next_file_list = os.listdir(cur_path)

        for next_file in next_file_list:
            next_dest_path = dest_path + '\\'  # 복사 경로상에서 다음 경로
            next_file_path = cur_path + '\\' + next_file  # 원본 경로상에서 파일명까지 포함한 다음 경로

            if os.path.isdir(next_file_path):
                next_dest_path += next_file
                try:
                    if not os.path.exists(next_dest_path):
                        os.makedirs(next_dest_path)
                    self.traversal_and_convert(next_file_path, relative_cur_path + '\\' + next_file, next_dest_path)
                except OSError:
                    print('Error: Creating directory ' + next_dest_path + '.')

            elif os.path.isfile(next_file_path):
                extension = next_file.split('.')[1]
                if extension == "svg":
                    new_file_name = next_file.replace('.svg', '.png')
                    next_dest_path += new_file_name
                else:
                    print(next_file + " is not .svg file.")
            else:
                continue

if __name__ == "__main__":

    DATA_ROOT = 'D:/Test_Models/FAAI'

    if len(sys.argv) != 5:
        print('ex) python image_json_generator.py origin_folder dest_folder 400(width) 300(height)')
    else:
        generator = random_file(DATA_ROOT, sys.argv[1], sys.argv[2])
        #generator.generate_image_json()