import numpy as np

class Vertex:
	def __init__(self, index, props):
		self.index = index
		self.props = props
		self.edges = []

	def add_edge(self, edge):
		self.edges.append(edge)

	def getLocation(self):
		return np.array(self.props[:3])

class Edge:
	def __init__(self, name, verts):
		self.name = name
		self.v1_idx = int(name[:name.find(':')])
		self.v2_idx = int(name[name.find(':')+1:])
		verts[self.v1_idx].add_edge(self)
		verts[self.v2_idx].add_edge(self)
		self.faces = []

	def add_face(self, face):
		self.faces.append(face)

	def is_boundary(self):
		return (len(self.faces)==1)

	def retrieve_other_vert(self, vert, verts):
		if(vert.index == self.v1_idx):
			return verts[self.v2_idx]
		elif(vert.index == self.v2_idx):
			return verts[self.v1_idx]


class Face:
	def __init__(self, index, vertices):
		self.index = index
		self.vert_indices = vertices


# verts = dict {vert_id : Vertex object}
# edges = dict {'vert_id1:vert_id2' : Edge object}

class Mesh:
	def __init__(self, mesh_name):
		self.verts = {}
		self.edges = {}
		self.faces = {}

		mesh = open(mesh_name, "r+")
		lines = mesh.readlines()

		self.n_verts = 0
		self.n_faces = 0
		self.props = []
		vert_begins = False
		vert_index = 0
		face_begins = False
		face_index = 0

		for line in lines:
			line = line[:-1]
			if("element vertex" in line):
				self.n_verts = int(line.split(' ')[2])
				print(self.n_verts)
				continue
			if("property" in line):
				self.props.append((line.split(' ')[1], line.split(' ')[2]))
				continue
			if("element face" in line):
				self.n_faces = int(line.split(' ')[2])
				continue
			if("end_header" in line):
				vert_begins = True
				continue
			if(vert_begins):
				self.verts[vert_index] = Vertex(vert_index, list(map(float, line.split(' '))))
				vert_index += 1
				#print(vert_index)
				if(vert_index==self.n_verts):
					vert_begins = False
					face_begins = True
				continue
			if(face_begins):
				face_l = line.split(' ')[1:1+int(line.split(' ')[0])]
				face = Face(face_index, list(map(int, face_l)))
				self.faces[face_index] = face
				if(face_l[0]+":"+face_l[1] in self.edges):
					self.edges[face_l[0]+":"+face_l[1]].add_face(face)
				elif(face_l[1]+":"+face_l[0] in self.edges):
					self.edges[face_l[1]+":"+face_l[0]].add_face(face)
				else:
					edge = Edge(face_l[0]+":"+face_l[1], self.verts)
					edge.add_face(face)
					self.edges[face_l[0]+":"+face_l[1]] = edge
				if(face_l[1]+":"+face_l[2] in self.edges):
					self.edges[face_l[1]+":"+face_l[2]].add_face(face)
				elif(face_l[2]+":"+face_l[1] in self.edges):
					self.edges[face_l[2]+":"+face_l[1]].add_face(face)
				else:
					edge = Edge(face_l[1]+":"+face_l[2], self.verts)
					edge.add_face(face)
					self.edges[face_l[1]+":"+face_l[2]] = edge
				if(face_l[2]+":"+face_l[0] in self.edges):
					self.edges[face_l[2]+":"+face_l[0]].add_face(face)
				elif(face_l[0]+":"+face_l[2] in self.edges):
					self.edges[face_l[0]+":"+face_l[2]].add_face(face)
				else:
					edge = Edge(face_l[2]+":"+face_l[0], self.verts)
					edge.add_face(face)
					self.edges[face_l[2]+":"+face_l[0]] = edge

				face_index += 1
				if(face_index==self.n_faces):
					face_begins = False
		print(len(self.verts), len(self.faces), len(self.edges))


def get_closest_vert(vertID, sourceMeshVerts, targetMeshVerts):
	dist = -1
	border_verts = sourceMeshVerts
	border_verts_head = targetMeshVerts

	c1 = border_verts_head[next(iter(border_verts_head))]
	match_index = 0
	for verth in border_verts_head:
		ab_vec = border_verts_head[verth].getLocation() - border_verts[vertID].getLocation()
		if(dist==-1 or np.linalg.norm(ab_vec) < dist):
			dist = np.linalg.norm(ab_vec)
			c1 = border_verts_head[verth]
			match_index = verth
	return match_index

def dist_btw_verts(v1, v2):
	return np.linalg.norm(v1.getLocation() - v2.getLocation())

def create_face(mesh, face, edge_list):
	mesh.faces[len(mesh.faces)] = face
	for edge in edge_list:
		edge.add_face(face)

def driver():
	face = Mesh('baseFace.ply')
	head = Mesh('head_border.ply')

	border_edges = {}
	border_verts = {}
	#border_gradient = {}


	border_edges_head = {}
	border_verts_head = {}
	#border_gradient_head = {}

	# find top vertex head
	max_val = 0
	top_vert = head.verts[0]
	for vert in head.verts:
		if(head.verts[vert].getLocation()[2] > max_val):
			max_val = head.verts[vert].getLocation()[2]
			top_vert = head.verts[vert]
	print(top_vert.getLocation())


	# find border edge head
	while(True):
		if(top_vert.index in border_verts_head):
			break
		border_verts_head[top_vert.index] = top_vert
		for edge in top_vert.edges:
			if(edge.is_boundary() and edge.name not in border_edges_head):
				border_edges_head[edge.name] = edge
				top_vert = edge.retrieve_other_vert(top_vert, head.verts)
				break
	print(len(border_verts_head), len(border_edges_head))

	# find border gradient head
	'''for vert in border_verts_head:
		grad = np.array((0,0,0), dtype='float64')
		for edge in border_verts_head[vert].edges:
			if(edge.name not in border_edges_head):
				if(edge.v1_idx==vert):
					grad += head.verts[edge.v1_idx].getLocation() - head.verts[edge.v2_idx].getLocation()
				elif(edge.v2_idx==vert):
					grad += head.verts[edge.v2_idx].getLocation() - head.verts[edge.v1_idx].getLocation()
		norm = np.linalg.norm(grad)
		grad = grad / norm
		border_gradient_head[vert] = grad'''

	# find top vertex
	max_val = 0
	top_vert = face.verts[0]
	for vert in face.verts:
		if(face.verts[vert].getLocation()[1] > max_val):
			max_val = face.verts[vert].getLocation()[1]
			top_vert = face.verts[vert]

	# find border edge
	while(True):
		if(top_vert.index in border_verts):
			break
		border_verts[top_vert.index] = top_vert
		for edge in top_vert.edges:
			if(edge.is_boundary() and edge.name not in border_edges):
				border_edges[edge.name] = edge
				top_vert = edge.retrieve_other_vert(top_vert, face.verts)
				break

	print(len(border_verts), len(border_edges))

	# find border gradient
	'''for vert in border_verts:
		grad = np.array((0,0,0), dtype='float64')
		for edge in border_verts[vert].edges:
			if(edge.name not in border_edges):
				if(edge.v1_idx==vert):
					grad += face.verts[edge.v1_idx].getLocation() - face.verts[edge.v2_idx].getLocation()
				elif(edge.v2_idx==vert):
					grad += face.verts[edge.v2_idx].getLocation() - face.verts[edge.v1_idx].getLocation()
		norm = np.linalg.norm(grad)
		grad = grad / norm
		border_gradient[vert] = grad'''

	currentVerts = len(face.verts)


	mid_verts = []
	# extend face new vertices
	first = True
	path_chosen_edge_name = ''
	last_vert_edge_name = ''
	#Associate each midset with an edge
	for vert in border_verts:
		# find closest point on border_verts_head & creates the edge

		match_index = get_closest_vert(vert, border_verts, border_verts_head)
		target_vector = border_verts_head[match_index].getLocation() - border_verts[vert].getLocation()

		face.props = np.append(face.verts[vert].getLocation() + target_vector, np.array((255, 255, 255, 255), dtype='float64')).tolist()
		new_id = len(face.verts)
		face.verts[new_id] = Vertex(new_id, face.props)
		face.edges[str(new_id)+':'+str(vert)] = Edge(str(new_id)+':'+str(vert), face.verts)

		#filling up the midset with the intermediate vertices
		if(len(mid_verts) == 0):
			# Create New MidSet
			mid_verts.append({new_id : [match_index]})
		else:
			mid_set = mid_verts[len(mid_verts)-1]
			for key in mid_set:
				mid_set = mid_set[key]
			init_vertex = border_verts_head[mid_set[0]] #last match_index

			if(first): #figure out the direction of traversal in the first iteration
				count = 0
				#finding the first direction of traversal
				for vert_edge in init_vertex.edges:
					if(vert_edge.is_boundary()):
						path_chosen_edge_name = vert_edge.name

				while (init_vertex.index != match_index and count < 10):
					count+=1
					for vert_edge in init_vertex.edges:
						if(vert_edge.is_boundary() and vert_edge.name!=last_vert_edge_name):
							last_vert_edge_name = vert_edge.name
							init_vertex = vert_edge.retrieve_other_vert(init_vertex, head.verts)
							mid_set.append(init_vertex.index)
							break
				
				if(count==10):
					last_vert_edge_name = path_chosen_edge_name
					for vert_edge in init_vertex.edges:
						if(vert_edge.is_boundary() and vert_edge.name==last_vert_edge_name):
							last_vert_edge_name = vert_edge.name
							init_vertex = vert_edge.retrieve_other_vert(init_vertex, head.verts)
							mid_set.append(init_vertex.index)
							break
				first = False
			else:
				while (init_vertex.index != match_index):
					for vert_edge in init_vertex.edges:
						if(vert_edge.is_boundary() and vert_edge.name!=last_vert_edge_name):
							last_vert_edge_name = vert_edge.name
							init_vertex = vert_edge.retrieve_other_vert(init_vertex, head.verts)
							mid_set.append(init_vertex.index)
							break

			#Create New MidSet
			mid_verts.append({new_id : [match_index]}) 


	#Close up the last MidSet
	diction = mid_verts[0]
	for key in diction:
		match = diction[key]
	match_index = match[0]
	mid_set = mid_verts[len(mid_verts)-1]
	for key in mid_set:
		mid_set = mid_set[key]
	init_vertex = border_verts_head[mid_set[0]]
	while (init_vertex.index != match_index):
		for vert_edge in init_vertex.edges:
			if(vert_edge.is_boundary() and vert_edge.name!=last_vert_edge_name):
				last_vert_edge_name = vert_edge.name
				init_vertex = vert_edge.retrieve_other_vert(init_vertex, head.verts)
				mid_set.append(init_vertex.index)
				break

	#print(mid_verts)
	#return

	# Create Faces

	for j, mid_set in enumerate(mid_verts):
		#print(j)
		new_id = -1
		for key in mid_set:
			new_id = key
			mid_set = mid_set[key]

		#first_vert_id = mid_set[0]
		#last_vert_id = mid_set[len(mid_set)-1]

		if(len(mid_set)==1):
			#print('triangle')
			root_vert = face.verts[new_id]
			found = False
			for edge in root_vert.edges:
				if(found):
					break
				v = edge.retrieve_other_vert(root_vert, face.verts)
				for secnd_edge in v.edges:
					if(found):
						break
					v2 = secnd_edge.retrieve_other_vert(v, face.verts)
					for thrd_edge in v2.edges:
						v3 = thrd_edge.retrieve_other_vert(v2, face.verts)
						#if(i>138 and i<143):
						#	print(dist_btw_verts(v3, last_mid_vert_head))
						if(dist_btw_verts(v3, root_vert)<0.0000000001):
							face.edges[str(v3.index)+':'+str(root_vert.index)] = Edge(str(v3.index)+':'+str(root_vert.index), face.verts)
							e4 = face.edges[str(v3.index)+':'+str(root_vert.index)]
							new_face = Face(len(face.faces), (root_vert.index, v.index, v2.index, v3.index))
							create_face(face, new_face, [edge, secnd_edge, thrd_edge, e4]) #adds new_face to face mesh and attaches the face to each edge
							found = True
							#print('triangle')
							break

		if(len(mid_set)==2):
			#print('quad')
			root_vert = face.verts[new_id]
			last_mid_vert_head = border_verts_head[mid_set[1]]
			found = False
			for edge in root_vert.edges:
				if(found):
					break
				v = edge.retrieve_other_vert(root_vert, face.verts)
				for secnd_edge in v.edges:
					if(found):
						break
					v2 = secnd_edge.retrieve_other_vert(v, face.verts)
					for thrd_edge in v2.edges:
						v3 = thrd_edge.retrieve_other_vert(v2, face.verts)
						#if(i>138 and i<143):
						#	print(dist_btw_verts(v3, last_mid_vert_head))
						if(dist_btw_verts(v3, last_mid_vert_head)<0.0000000001):
							face.edges[str(v3.index)+':'+str(root_vert.index)] = Edge(str(v3.index)+':'+str(root_vert.index), face.verts)
							e4 = face.edges[str(v3.index)+':'+str(root_vert.index)]
							new_face = Face(len(face.faces), (root_vert.index, v.index, v2.index, v3.index))
							create_face(face, new_face, [edge, secnd_edge, thrd_edge, e4]) #adds new_face to face mesh and attaches the face to each edge
							found = True
							#print('quad')
							break

		if(len(mid_set)>2):
			#print('multiple', len(mid_set)-1)
			num_faces = len(mid_set)-1
			root_vert = face.verts[new_id]
			last_mid_vert_head = border_verts_head[mid_set[len(mid_set)-1]]
			found = False

			for edge in root_vert.edges:
				if(found):
					break
				left_edge = edge
				v = edge.retrieve_other_vert(root_vert, face.verts)
				for secnd_edge in v.edges:
					if(found):
						break
					base_edge = secnd_edge
					v2 = secnd_edge.retrieve_other_vert(v, face.verts)
					for thrd_edge in v2.edges:
						right_edge = thrd_edge
						v3 = thrd_edge.retrieve_other_vert(v2, face.verts)
						if(dist_btw_verts(v3, last_mid_vert_head)<0.0000000001):
							found = True
							break

			
			last_vert = root_vert
			l = True
			for i in range(num_faces-1):
				vr = border_verts[get_closest_vert(mid_set[i+1], border_verts_head, border_verts)]
				face.props = np.append(border_verts_head[mid_set[i+1]].getLocation(), np.array((255, 255, 255, 255), dtype='float64')).tolist()
				tmp_id = len(face.verts)
				face.verts[tmp_id] = Vertex(tmp_id, face.props)	
				if(dist_btw_verts(vr, v)<dist_btw_verts(vr, v2)):
					face.edges[str(tmp_id)+':'+str(v.index)] = Edge(str(tmp_id)+':'+str(v.index), face.verts)
					e2 = face.edges[str(tmp_id)+':'+str(v.index)]
					face.edges[str(tmp_id)+':'+str(last_vert.index)] = Edge(str(tmp_id)+':'+str(last_vert.index), face.verts)
					e3 = face.edges[str(tmp_id)+':'+str(last_vert.index)]
					new_face = Face(len(face.faces), (last_vert.index, v.index, tmp_id))
					create_face(face, new_face, [left_edge, e2, e3]) #adds new_face to face mesh and attaches the face to each edge
					#print('tri-inside')
					left_edge = e2

				else:
					if(l):
						face.edges[str(tmp_id)+':'+str(v2.index)] = Edge(str(tmp_id)+':'+str(v2.index), face.verts)
						e2 = face.edges[str(tmp_id)+':'+str(v2.index)]
						face.edges[str(tmp_id)+':'+str(last_vert.index)] = Edge(str(tmp_id)+':'+str(last_vert.index), face.verts)
						e3 = face.edges[str(tmp_id)+':'+str(last_vert.index)]
						new_face = Face(len(face.faces), (last_vert.index, v.index, v2.index, tmp_id))
						create_face(face, new_face, [left_edge, base_edge, e2, e3]) #adds new_face to face mesh and attaches the face to each edge
						#print('quad-inside')
						left_edge = e2

						l = False
					else:
						face.edges[str(tmp_id)+':'+str(v2.index)] = Edge(str(tmp_id)+':'+str(v2.index), face.verts)
						e2 = face.edges[str(tmp_id)+':'+str(v2.index)]
						face.edges[str(tmp_id)+':'+str(last_vert.index)] = Edge(str(tmp_id)+':'+str(last_vert.index), face.verts)
						e3 = face.edges[str(tmp_id)+':'+str(last_vert.index)]
						new_face = Face(len(face.faces), (last_vert.index, v2.index, tmp_id))
						create_face(face, new_face, [left_edge, e2, e3]) #adds new_face to face mesh and attaches the face to each edge
						#print('tri-inside')
						left_edge = e2

				last_vert = face.verts[tmp_id]

			#Final face
			face.edges[str(v3.index)+':'+str(last_vert.index)] = Edge(str(v3.index)+':'+str(last_vert.index), face.verts)
			e3 = face.edges[str(v3.index)+':'+str(last_vert.index)]
			if(l):
				new_face = Face(len(face.faces), (last_vert.index, v.index, v2.index, v3.index))
				create_face(face, new_face, [left_edge, base_edge, right_edge, e3]) #adds new_face to face mesh and attaches the face to each edge
				#print('quad-last')
			else:
				new_face = Face(len(face.faces), (last_vert.index, v2.index, v3.index))
				create_face(face, new_face, [left_edge, right_edge, e3]) #adds new_face to face mesh and attaches the face to each edge
				#print('tri-last')


	# Write to ply
	f = open("extendedFace.ply", "w+")
	f.write('ply\n')
	f.write('format ascii 1.0\n')
	f.write('comment created by Parth \n')
	f.write('element vertex '+str(len(face.verts))+'\n')
	f.write('property float x\n')
	f.write('property float y\n')
	f.write('property float z\n')
	f.write('property uchar red\n')
	f.write('property uchar green\n')
	f.write('property uchar blue\n')
	f.write('property uchar alpha\n')
	f.write('element face '+str(len(face.faces))+'\n')
	f.write('property list uchar int vertex_indices\n')
	f.write('end_header\n')

	for vert in face.verts:
		f.write(' '.join(list(map(str, face.verts[vert].props[:3]))) +' ' + ' '.join(list(map(str, list(map(int, face.verts[vert].props[3:])))))+'\n')

	for face_elem in face.faces:
		indices = face.faces[face_elem].vert_indices
		f.write(str(len(indices))+' '+' '.join(list(map(str, indices)))+'\n')

	f.close()

if __name__=='__main__':
	driver()

		




