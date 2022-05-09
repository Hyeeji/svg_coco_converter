import json
import open3d as o3d
import numpy as np
from pycocotools.coco import maskUtils

# http://www.open3d.org/docs/release/tutorial/geometry/pointcloud.html


def save_img(path, pcd):
    vis = o3d.visualization.Visualizer()
    vis.create_window(visible=False)
    vis.add_geometry(pcd)
    vis.update_geometry(pcd)
    vis.poll_events()
    vis.update_renderer()
    vis.capture_screen_image(path)
    vis.destroy_window()
    #
    # vis = o3d.visualization.Visualizer()
    # vis.create_window(visible=False)
    # vis.add_geometry(mesh)
    # vis.update_geometry(mesh)
    # vis.poll_events()
    # vis.update_renderer()
    # depth = vis.capture_depth_float_buffer(do_render=False)
    # vis.destroy_window()


def down_sampling(json_path):
    with open(json_path, 'r') as f:
        json_file = json.load(f)

    for image_idx, ann in enumerate(json_file['annotations']):
        seg_points = ann['segmentation'][0]
        R = maskUtils.frPyObjects(ann['segmentation'], 512, 512)
        original_area = maskUtils.area(R)
        # coco annotation에서 area를 뭐로 해야하나
        # https://github.com/cocodataset/cocoapi/issues/36
        x_coords, y_coords = seg_points[0::2], seg_points[1::2]

        pcs_np = []
        pcs_2d = []
        for x, y in zip(x_coords, y_coords):
            pcs_np.append([x, y, 0])
            pcs_2d.append([x, y])
        pcs_np = np.asarray(pcs_np)

        point_cloud = o3d.geometry.PointCloud()
        point_cloud.points = o3d.utility.Vector3dVector(pcs_np)
        # o3d.visualization.draw_geometries([point_cloud], width=512, height=512)
        save_img(f'./vis/{image_idx}_original.jpg', point_cloud)

        down_pcds = []
        for i in range(2, 10):
            down_pcds.append(point_cloud.voxel_down_sample(voxel_size=i))

        print(point_cloud)
        for down_idx, down_pcd in enumerate(down_pcds):
            downsampled_original_idx = []
            downsampled_pcd = np.asarray(down_pcd.points, dtype=int)[:, :2].tolist()
            for p in downsampled_pcd:
                if p in pcs_2d:
                    downsampled_original_idx.append(pcs_2d.index(p))
            downsampled_original_idx.sort()
            pcs_downsampled = []
            for i in pcs_np[downsampled_original_idx, :2].tolist():
                pcs_downsampled = pcs_downsampled + i
            pcs_downsampled = [pcs_downsampled]

            R = maskUtils.frPyObjects(pcs_downsampled, 512, 512)
            area = maskUtils.area(R)
            print(f'pcs_downsampled : {down_pcd},  area', area, (area / original_area) * 100)

            # o3d.visualization.draw_geometries([down_pcd], width=512, height=512)
            save_img(f'./vis/{image_idx}_{down_idx}_down.jpg', down_pcd)


if __name__ == '__main__':
    down_sampling('C:\\Users\\hyejiHan\\Documents\\GitHub\\svg_coco_converter\\test_files\\all.json')
