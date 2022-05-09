import json
import random

#1
#랜덤한 파일 이름을 뽑는코드

if __name__ == '__main__':
    with open('./category_names.json', 'r') as f:
        category_list = json.load(f)

    random_category = set()
    test_category = set()
    train_category = set()

    test = []

    for i in range(len(category_list)):
        num = str(i)
        current_category = category_list[num]

        test.append(len(category_list[num]))

        file_name = random.sample(current_category, 30)

        '''if len(current_category) < 30:
            file_name = random.sample(current_category, len(current_category))  # number change
        else:
            # number change'''

        random_category.update(file_name)

    random_c = list(random_category)

    total_num = len(random_c)
    test_num = total_num * 0.2

    with open('./random_file_name.json', 'w') as f:
        json.dump(random_c, f, indent=4)

    with open('./random_file_name.json', 'r') as f:
        new_category_list = json.load(f)

    new_file_name = random.sample(new_category_list, int(test_num))

    test_category.update(new_file_name)

    with open('./test_file_name.json', 'w') as f:
        json.dump(new_file_name, f, indent=4)

    train_category = random_category - test_category
    train_category = list(train_category)

    with open('./train_file_name.json', 'w') as f:
        json.dump(train_category, f, indent=4)








