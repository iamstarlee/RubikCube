import cv2

def identify_color(hsv_value):
    h, s, v = hsv_value
    if 0 <= h <= 10 or 160 <= h <= 180:  # 红色
        return "Red"
    elif 10 < h <= 25:  # 橙色
        return "Orange"
    elif 25 < h <= 35:  # 黄色
        return "Yellow"
    elif 35 < h <= 85:  # 绿色
        return "Green"
    elif 85 < h <= 130:  # 蓝色
        return "Blue"
    elif s < 50 and v > 200:  # 白色
        return "White"
    return "Unknown"



if __name__ == '__main__':
    # 读取图像
    image = cv2.imread('input_images/0.png')

    # 调整图像大小（可选）
    image = cv2.resize(image, (640, 480))

    # 转为灰度图像
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # 高斯模糊，减少噪声
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)

    # 边缘检测
    edges = cv2.Canny(blurred, 50, 150)

    # 查找轮廓
    contours, _ = cv2.findContours(edges, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    # 绘制轮廓（可视化）
    output = image.copy()
    cv2.drawContours(output, contours, -1, (0, 255, 0), 2)
    cv2.imwrite('output_images/Contours.png', output)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


    # 转为 HSV 空间
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    # 定义颜色范围（例如红色）
    lower_red = (0, 120, 70)
    upper_red = (10, 255, 255)
    mask_red = cv2.inRange(hsv, lower_red, upper_red)

    # 应用掩膜
    output = cv2.bitwise_and(image, image, mask=mask_red)
    cv2.imwrite('output_images/Red_Mask.png', output)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    # 分割为网格并提取颜色
    rows, cols = 3, 3  # 假设魔方是 3×3
    h, w, _ = image.shape # 这里的尺寸是图片的，不是魔方的
    block_h, block_w = 45, 30

    init_x = 297
    init_y = 248
    # 应用到每个色块
    for i in range(rows):
        for j in range(cols):
             # 计算色块区域
            y1, y2 = i * block_h + init_y , (i + 1) * block_h + init_y
            x1, x2 = j * block_w + init_x, (j + 1) * block_w + init_x
            block = image[int(y1) : int(y2), int(x1) : int(x2)]

            # 转为 HSV 并计算平均颜色
            block_hsv = cv2.cvtColor(block, cv2.COLOR_BGR2HSV)
            avg_color = block_hsv.mean(axis=0).mean(axis=0)


            avg_h = block_hsv[:, :, 0].mean()
            avg_s = block_hsv[:, :, 1].mean()
            avg_v = block_hsv[:, :, 2].mean()
            print(f"Block ({i}, {j}): HSV = ({avg_h}, {avg_s}, {avg_v})")
            hsv_value = (avg_h, avg_s, avg_v)  # 计算的平均 HSV 值
            color = identify_color(hsv_value)
            print(f"Block ({i}, {j}) Color: {color}")
            
            # 在图像上标记颜色
            cv2.putText(image, color, (int(x1), int(y1)), cv2.FONT_HERSHEY_SIMPLEX, 0.3, (0, 255, 0), 1)


    cv2.imwrite('output_images/Result.png', image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
