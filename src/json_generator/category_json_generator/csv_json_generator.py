import os
import json
import csv
from src.json_generator.common.svg_process import gather_name_from_first_level_node
from src.json_generator.category_json_generator.category_json_generator import dump_category_result


def fetch_category_from_csv(csv_path):
    categories = set()

    with open(csv_path, encoding="utf8") as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            fullname = row['layer1'] + '-' + row['layer2'] + '-' + row['layer3']
            categories.add(fullname)

    return categories



if __name__ == "__main__":
    # 컨트롤클로더에서 송부한 svg_database.xlsx 파일을 csv로 변환하여 저장한 경로. 보안 문제가 있으니 저장소에 올리지 말것
    BASE_CSV_PATH = 'D:/Test_Models/FAAI/svg_database_base.csv'
    STICKER_CSV_PATH = 'D:/Test_Models/FAAI/svg_database_sticker.csv'
    OUT_PATH = '../../../test_files/categories_from_excel.json'

    base_cat = fetch_category_from_csv(BASE_CSV_PATH)
    sticker_cat = fetch_category_from_csv(STICKER_CSV_PATH)
    base_cat.update(sticker_cat)
    dump_category_result(OUT_PATH, base_cat)
