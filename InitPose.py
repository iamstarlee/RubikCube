import cv2
import numpy as np

# 假设有立方体模型的3D顶点
object_points = np.array([
    [0, 0, 0],   # 立方体的一个角
    [1, 0, 0],   # 立方体的另一个角
    [1, 1, 0],   # 立方体的另一个角
    [0, 1, 0],   # 立方体的另一个角
    [0, 0, 1],   # 立方体的上面角
    [1, 0, 1],   # 立方体的上面角
    [1, 1, 1],   # 立方体的上面角
    [0, 1, 1]    # 立方体的上面角
], dtype=np.float32)

# 假设图像中对应的2D点
image_points = np.array([
    [320, 240],   # 图像中对应点1
    [420, 240],   # 图像中对应点2
    [420, 340],   # 图像中对应点3
    [320, 340],   # 图像中对应点4
    [320, 140],   # 图像中对应点5
    [420, 140],   # 图像中对应点6
    [420, 240],   # 图像中对应点7
    [320, 240]    # 图像中对应点8
], dtype=np.float32)

# 相机内参（假设已经通过标定得到）
camera_matrix = np.array([
    [800, 0, 320],
    [0, 800, 240],
    [0, 0, 1]
], dtype=np.float32)

dist_coeffs = np.zeros((4, 1))  # 假设无畸变

# 使用solvePnP计算旋转向量和平移向量
success, rotation_vector, translation_vector = cv2.solvePnP(object_points, image_points, camera_matrix, dist_coeffs)

# 如果计算成功，输出旋转和平移
if success:
    print("Rotation Vector:\n", rotation_vector)
    print("Translation Vector:\n", translation_vector)
