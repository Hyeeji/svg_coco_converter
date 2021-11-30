import os
import json
from collections import OrderedDict
    
def generate_single_image_json(file_id, file_width, file_height, file_name):
    data = OrderedDict()
    
    data['id'] = file_id
    data['width'] = file_width
    data['height'] = file_height
    data['file_name'] = file_name

    return data