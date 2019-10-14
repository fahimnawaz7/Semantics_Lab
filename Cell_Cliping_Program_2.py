# 220919@1311
# Find cells of a table using intersecting points of horizontal and vertical lines from the data of a jason file.
import json

v = []
h = []

line_segments = []  # Horizontal Line
test_segments = []  # Vertical Line

m = 5 # Width of hrizontal line 

cell_points = []
cell_list = []

with open("table.json") as jfile:
	data = json.load(jfile)

	for i in range(len(data['table.png']['regions'])):
		d1 = data['table.png']['regions'][i]['shape_attributes']
		d2 = dict(list(d1.items())[1:])
		key = data['table.png']['regions'][i]['region_attributes']['table']


		if key == 'v_line':
			a, b, c, d = d2['x'], d2['y'] - m, d2['x'], d2['y'] + d2['height'] + m
			v.append([a,b])
			v.append([c,d])
		else:
			a,b,c,d = d2['x']-m, d2['y'], d2['x']+d2['width']+m, d2['y']
			h.append([a,b])
			h.append([c,d])

#print('H = ',h)
#print('V = ',v)

for i in range(0,len(h),2):
	line_segments.append((h[i],h[i+1]))

for j in range(0,len(v),2):
    test_segments.append((v[j],v[j+1]))

# print('H =',line_segments)
# print('V =',test_segments)	

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

# Create input data.
# black lines
#line_segments = [[(1,4), (4,4)], [(2,3), (5,3)], [(3,2), (6,2)], [(6.5, 1), (7,1)], [(7.5, 0), (8.5,0)]]
# red lines
#test_segments = [[(4.5,0), (4.5,4.5)], [(6.25, 0), (6.25, 4.5)]]
# Check all lines for intersections
intersections = set()
for test_segment in test_segments:
    for line_segment in line_segments:
        p0, p1 = test_segment[0], test_segment[1]
        p2, p3 = line_segment[0], line_segment[1]
        result = find_intersection(p0, p1, p2, p3)
        if result is not None:
            intersections.add(tuple(result))

### Sorting intersecting points according to Vertical line 
lx = sorted(intersections)
ly = sorted(lx, key = lambda q : q[1])   
# print(lx)
# print(ly)

NumberOfLastV_LinePoints = 1 + len(list(filter(lambda x : lx[-1][0] in x, lx)))	

for i in range(len(lx) - NumberOfLastV_LinePoints):
    x0 = int(lx[i][0])
    if x0 == int(lx[i + 1][0]):
        y0 = int(lx[i][1])
        y1 = int(lx[i + 1][1])
    else:#Do when i == 4
        i=i+1
        continue
    x1 = int(ly[ly.index((x0, y0)) + 1][0])

    cell_points = [(x0,y0), (x0,y1), (x1,y0), (x1,y1)]
    cell_list.append(cell_points)

for element in cell_list:
	print(element)