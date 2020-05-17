def rect_contains_point(rect_x1_y1_x2_y2, point):
    return rect_x1_y1_x2_y2[0] <= point[0] <= rect_x1_y1_x2_y2[2] and rect_x1_y1_x2_y2[1] <= point[1] < rect_x1_y1_x2_y2[3]