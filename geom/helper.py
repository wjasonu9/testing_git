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
def get_intersection(p1, p2, p3, p4, Int=False):
    """Finds the intersection point of two lines defined by (p1, p2) and (p3, p4).
    Assumes lines are not parallel; no error handling for parallel/collinear lines."""
    x1, y1 = p1
    x2, y2 = p2
    x3, y3 = p3
    x4, y4 = p4
    denom = (x1 - x2) * (y3 - y4) - (y1 - y2) * (x3 - x4)
    intersect_x = ((x1 * y2 - y1 * x2) * (x3 - x4) - (x1 - x2) * (x3 * y4 - y3 * x4)) / denom
    intersect_y = ((x1 * y2 - y1 * x2) * (y3 - y4) - (y1 - y2) * (x3 * y4 - y3 * x4)) / denom
    if not Int:
        return (intersect_x, intersect_y)
    return (int(intersect_x), int(intersect_y))
def draw_perp(img, pt, line_p1, line_p2, color=(0, 0, 0), thickness=1):
    """Draws a perpendicular segment from pt to the line defined by (line_p1, line_p2)"""
    dx, dy = line_p2[0] - line_p1[0], line_p2[1] - line_p1[1] #get line's direction vector
    perp_pt2 = (pt[0] - dy, pt[1] + dx) #another point on perpendicular line
    proj_pt = get_intersection(line_p1, line_p2, pt, perp_pt2,Int=True)
    cv2.line(img, pt, proj_pt, color, thickness)
