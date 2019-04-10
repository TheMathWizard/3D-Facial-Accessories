import numpy as np
import scipy
import scipy.misc
from scipy import cluster

f = open('full_stitched.ply','r+')

verts = 0
count = 0
start = False
colors = []
lines = f.readlines()
for line in lines:
	if(line.startswith("element vertex")):
		verts = int(line[15:])
		continue
	if(line=='end_header\n'):	
		start = True	
		continue
	if(start==True):
		count+=1
		rgb_color = list(map(float, line.split(' ')[3:]))
		if(rgb_color!=[255.0,255.0,255.0]):
			print(rgb_color)
			colors.append(rgb_color)
		if(count==verts):
			print(colors[0])
			break

f.close()

print(len(colors), verts)

colors = np.array(colors)
NUM_CLUSTERS = 5

print('finding clusters')
codes, dist = cluster.vq.kmeans(colors, NUM_CLUSTERS)
print('cluster centres:\n', codes)

vecs, dist = cluster.vq.vq(colors, codes)         # assign codes
counts, bins = scipy.histogram(vecs, len(codes))    # count occurrences

index_max = scipy.argmax(counts)                    # find most frequent
peak = codes[index_max]
print(peak)
lst = list(map(int, peak))
color = ' ' + ' '.join(map(str, lst))
print(color)


f = open('full_stitched.ply','r+')
f2 = open('full_coloured.ply','w+')

verts = 0
count = 0
start = False
colors = []
lines = f.readlines()
for line in lines:
	if(line.startswith("element vertex")):
		verts = int(line[15:])
		f2.write(line)
		continue
	if(line=='end_header\n'):
		start = True
		f2.write(line)
		continue
	if(start==True):
		count+=1
		rgb_color = list(map(float, line.split(' ')[3:]))
		if(rgb_color==[255.0,255.0,255.0]):
			f2.write(' '.join(line.split(' ')[:3])+color+'\n')
		else:
			f2.write(line)
		if(count==verts):
			start=False
		continue
	f2.write(line)

f.close()
f2.close()
