import cv2
import math
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
    mx, my = midpt(pt1,pt2)
    dx, dy = pt2[0] - pt1[0], pt2[1] - pt1[1]
    length = np.hypot(dx, dy)
    dx, dy = dx/length, dy/length
    mx, my = mx+int(dx*offset_px), my+int(dy*offset_px)
    nx, ny = int(-dy * 8), int(dx * 8)
    cv2.line(img, (mx - nx, my - ny), (mx + nx, my + ny), color, thickness=1)
def show_geometry_image(img,x_px=200,y_px=200):
    # x_px, y_px: how many pixels correspond to 1 inch
    h_px, w_px, _ = img.shape
    plt.figure(figsize=(w_px/x_px, h_px/y_px))
    plt.imshow(img[:, :, ::-1],aspect=x_px/y_px)# Convert BGR to RGB color channels
    plt.axis("off")
    plt.show()
    plt.close()
def show_many_images(*imgs, nrows=1, x_px=200, y_px=200):
    """Displays 2+ OpenCV images assumed to have the same dimensions
    and physical sizing based on pixels-per-inch scaling."""
    n=len(imgs)
    ncols = math.ceil(n / nrows) #same int(np.ceil())
    h_px, w_px, _ = imgs[0].shape
    total_w_in = (w_px * ncols) / x_px
    total_h_in = (h_px * nrows) / y_px
    fig, axes = plt.subplots(nrows, ncols, figsize=(total_w_in, total_h_in))
    axes_flat = axes.flatten()
    #loop thru all of axes_flat so unneeded parts are cleanly hidden
    for j in range(len(axes_flat)):
        if j < len(imgs):
            axes_flat[j].imshow(imgs[j][:, :, ::-1], aspect=x_px / y_px)
            axes_flat[j].axis("off")
        else:
            axes_flat[j].axis("off")
    plt.tight_layout()
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
def draw_path(img, *pts, color=(0, 0, 0), thickness=2):
    #Draws line segments sequentially through 2+ pts
    if len(pts) < 2: #pts is a tuple
        return None
    for j in range(len(pts) - 1):
        cv2.line(img, pts[j], pts[j + 1], color, thickness)
def find_eq_tri(pt1, pt2, orient=1):
    """Finds pt3 such that pt1, pt2, and pt3 form an equilateral triangle.
    When orient=1, pt3 is chosen such that pt1 -> pt2 -> pt3 is CW (CCW in raw Cartesian space)"""
    x1, y1 = pt1
    x2, y2 = pt2
    dx,dy = x2 - x1, y2 - y1
    c = 1/2 #math.cos(angle) #angle = -orient * math.pi / 3.0
    s = orient*3**0.5/2 #math.sin(angle)
    x3 = x1 + (dx * c - dy * s)
    y3 = y1 + (dx * s + dy * c)
    return int(x3), int(y3) #round() is still float
