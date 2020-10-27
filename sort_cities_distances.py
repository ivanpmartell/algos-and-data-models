from math import sqrt
def get_distance(p1, p2):
    dx = p1[0]-p2[0]
    dy = p1[1]-p2[1]
    return sqrt(dx**2 + dy**2)

fileDict = {"Cities": "data/dataset_TIST2015_Cities.txt"}

points = []
with open(fileDict["Cities"], 'r') as read_file:
    for line in read_file:
        values = line.rstrip().split('\t')
        points.append([values[0],values[3],[float(values[1]),float(values[2])]])

distances = []
i = 0
while (i < len(points)):
    j = i + 1
    while (j < len(points)):
        distances.append([points[i][0], points[i][1], points[i][-1], points[j][0], points[j][1], points[j][-1], get_distance(points[i][-1], points[j][-1])])
        j += 1
    i += 1
sorted_distances = sorted(distances, key=lambda x: x[-1])
with open('data/sorted_cities_distances.txt','w') as out_cd_file:
    with open('data/sorted_distances.txt', 'w') as out_d_file:
        for row in sorted_distances:
            out_cd_file.write(str(row) + '\n')
            out_d_file.write(str(row[-1]) + '\n')