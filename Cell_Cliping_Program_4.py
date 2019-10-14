# 240919@1441
# Find cells of a table using intersecting points of horizontal and vertical lines from the data of a jason file.
import json

v = []
h = []
l = []

line_segments = [] # Horizontal_Line or h_line
test_segments = [] # Vertical_Line or v_line
cell_points = []
cell_list = []
V_line_end_pt = []
H_line_end_pt = []

with open("table.json") as jfile:
    data = json.load(jfile)

    for i in range(len(data['table.png']['regions'])):
        d1 = data['table.png']['regions'][i]['shape_attributes']
        key = data['table.png']['regions'][i]['region_attributes']['table']
        if key == 'v_line':
            l.append(d1['width'])
        else:
            l.append(d1['height'])
    max_ex = max(l)

    for i in range(len(data['table.png']['regions'])):
        d2 = data['table.png']['regions'][i]['shape_attributes']
        # d2 = dict(list(d1.items())[1:])
        key = data['table.png']['regions'][i]['region_attributes']['table']

        if key == 'v_line':
            a, b, c, d = d2['x'], d2['y'] - max_ex, d2['x'], d2['y'] + d2['height'] + max_ex
            v.append([a,b])
            v.append([c,d])
        else:
            a, b, c, d = d2['x'] - max_ex, d2['y'], d2['x'] + d2['width'] + max_ex, d2['y']
            h.append([a,b])
            h.append([c,d])

for i in range(0,len(h),2):
    line_segments.append((h[i],h[i+1]))

for j in range(0,len(v),2):
    test_segments.append((v[j],v[j+1]))

### Defining Function to find intersecting points
# Thanks to scicomp.stackexchange.com
# https://scicomp.stackexchange.com/questions/8895/vertical-and-horizontal-segments-intersection-line-sweep
def find_intersection( p0, p1, p2, p3 ) :

    s10_x = p1[0] - p0[0]
    s10_y = p1[1] - p0[1]
    s32_x = p3[0] - p2[0]
    s32_y = p3[1] - p2[1] 

    denom = s10_x * s32_y - s32_x * s10_y

    if denom == 0 : return None # collinear

    denom_is_positive = denom > 0

    s02_x = p0[0] - p2[0]
    s02_y = p0[1] - p2[1]

    s_numer = s10_x * s02_y - s10_y * s02_x

    if (s_numer < 0) == denom_is_positive : return None # no collision

    t_numer = s32_x * s02_y - s32_y * s02_x

    if (t_numer < 0) == denom_is_positive : return None # no collision

    if (s_numer > denom) == denom_is_positive or (t_numer > denom) == denom_is_positive : return None # no collision


    # collision detected

    t = t_numer / denom

    intersection_point = [ p0[0] + (t * s10_x), p0[1] + (t * s10_y) ]
    return intersection_point

# Check all lines for intersections
intersections = set()
for test_segment in test_segments:
    for line_segment in line_segments:
        p0, p1 = test_segment[0], test_segment[1]
        p2, p3 = line_segment[0], line_segment[1]
        result = find_intersection(p0, p1, p2, p3)
        if result is not None:
            intersections.add(tuple(result))

### Converting float to integer of intersections 
def cast_data(data_list, data_type):
    return list(map(lambda sub: list(map(data_type, sub)), data_list))

intersections_int = cast_data(intersections,int)

### Function for finding end points of V_line and H_line 
def closest_V(lst, k, l):
    return lst[ min(range(len(lst)), key = lambda i: abs(int(lst[i][1]) - k)  if l == int(lst[i][0]) else 99999)]

def closest_H(lst, k, l):
    return lst[ min(range(len(lst)), key = lambda i: abs(int(lst[i][0]) - k) if l == int(lst[i][1]) else 99999)]

### Sorting intersecting points according to V_line and H_line
lx = sorted(intersections_int)
ly = sorted(lx, key = lambda q : q[1])   

### Finding V_line and H_line end points
for z in range(len(test_segments)):
    V_line_end_pt.append(closest_V(lx, test_segments[z][1][1], test_segments[z][1][0]))

for z in range(len(line_segments)):
    H_line_end_pt.append(closest_H(ly, line_segments[z][1][0], line_segments[z][1][1]))

### Finding Cell_points 
for i in range(len(lx)):
    x0 = lx[i][0]
    y0 = lx[i][1]

    if([x0, y0] in V_line_end_pt or [x0, y0] in H_line_end_pt): # If list of tuple write (x0, y0)
        continue
    else:
        for j in range(len(V_line_end_pt)):
            x1 = ly[ly.index([x0, y0]) + j + 1][0]
            if ([x1, y0] in V_line_end_pt): # If list of tuple write (x1, y0)
                continue
            else:
                break

        for k in range(len(H_line_end_pt)):      
            y1 = lx[lx.index([x0, y0]) + k + 1][1]
            if ([x0, y1] in H_line_end_pt):  # If list of tuple write (x0, y1)
                continue
            else:
                break

    cell_points = [(x0, y0), (x0, y1), (x1, y0), (x1, y1)]
    cell_list.append(cell_points)

for element in cell_list:
    print(element)