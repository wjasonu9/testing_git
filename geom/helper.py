import cv2
import matplotlib.pyplot as plt
import numpy as np

font = cv2.FONT_HERSHEY_SIMPLEX
color = (0, 0, 0)  # Black
def midpt(pt1, pt2):
    return ((pt1[0] + pt2[0]) // 2, (pt1[1] + pt2[1]) // 2)
def double_arrow_line(img, pt1, pt2, color = (0, 0, 0), thickness=2, tip_length=0.03):
    #pt1 and pt2 are where the arrows appear
    m = midpt(pt1, pt2)
    cv2.arrowedLine(img, m, pt1, color, thickness, tipLength=tip_length * 2)
    cv2.arrowedLine(img, m, pt2, color, thickness, tipLength=tip_length * 2)
def add_tick(img, pt1, pt2, offset_px=0):
    mx, my = (pt1[0] + pt2[0]) // 2 + offset_px, (pt1[1] + pt2[1]) // 2
    dx, dy = pt2[0] - pt1[0], pt2[1] - pt1[1]
    length = np.hypot(dx, dy)
    nx, ny = int(-dy / length * 8), int(dx / length * 8)
    cv2.line(img, (mx - nx, my - ny), (mx + nx, my + ny), color, thickness=2)
def show_geometry_image(img):
    h_px, w_px, _ = img.shape
    plt.figure(figsize=(w_px/2e2, h_px/2e2))
    plt.imshow(img[:, :, ::-1])# Convert BGR to RGB color channels
    plt.axis("off")
    plt.show()
    plt.close()
