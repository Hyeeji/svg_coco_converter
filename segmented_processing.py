import os
# from svglib.svglib import svg2rlg
# from reportlab.graphics import renderPM
# import pyvips
import cairosvg
import cv2
import numpy as np
import matplotlib.pyplot as plt

def convert_svg_to_png(svg_path):
    # Convert each sub-SVG into image

    out_img_filepath = svg_path.replace('.svg', '.png')
    print("Writing {0}...".format(out_img_filepath))
    cairosvg.svg2png(url=segmented_file_path, write_to=segmented_file_path.replace('.svg', '.png'))

    # TODO: Pyvips dll load 문제 있음...
    # image = pyvips.Image.new_from_file(segmented_file_path, dpi=600)
    # image.write_to_file("test.png")

    return out_img_filepath

def process_img(img_path, width_stride):
    img = cv2.imread(img_path, cv2.IMREAD_UNCHANGED) # Alpha channel read

    # Since all meaningful information is colored in black (or whatever), we only care about the pixels which is not transparent
    bw_img = (img[:,:,3] > 0) # alhpa != 0

    width = bw_img.shape[1]
    height = bw_img.shape[0]

    tops = []
    bottoms = []

    current_w = 0
    while current_w < width:
        column_arr = bw_img[:,current_w]
        positive_indices = np.where(column_arr) # for each column of pixels
        if len(positive_indices[0]) == 0: # if there is no meaningful pixel, continue
            current_w += width_stride
            continue

        # if there is meaningful pixel, gather topmost and bottommost pixel
        tops.append((current_w, np.max(positive_indices)))
        bottoms.append((current_w, np.min(positive_indices)))

        # for every width_stride column
        current_w += width_stride

    # Connect topmost and bottommost pixels and close the loop(=polygon)
    point_num = len(bottoms)
    for i in range(point_num):
        tops.append(bottoms[point_num-i-1])
    tops.append(tops[0]) # force closing


    # -- Plotting for debug
    x_vals = []
    y_vals = []

    for point in tops:
        x_vals.append(point[0])
        y_vals.append(point[1])

    plt.xlim(0, width)
    plt.ylim(0, height)
    plt.gca().invert_yaxis()
    plt.imshow(img)
    plt.plot(x_vals, y_vals, color='red')

    plt.show()
    plt.clf()



if __name__ == '__main__':
    segmented_root_path = './segmented_files'
    WIDTH_STRIDE = 1

    # for each folder that contains sub-SVG,
    for segmented_svg_folder in os.listdir(segmented_root_path):
        svg_segment_folder = os.path.join(segmented_root_path,segmented_svg_folder)

        # for each sub-SVG,
        for segmented_file in os.listdir(svg_segment_folder):
            if os.path.splitext(segmented_file)[1].find(".svg") is not -1:
                segmented_file_path = os.path.join(svg_segment_folder,segmented_file)

                # 1) convert svg to image
                out_img_file = convert_svg_to_png(segmented_file_path)

                # 2) process image and generate polygon
                process_img(out_img_file, WIDTH_STRIDE)




