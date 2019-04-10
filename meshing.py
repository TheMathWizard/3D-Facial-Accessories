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


def driver():
	face = Mesh('femface.ply')
	head = Mesh('head_border.ply')

	border_edges = {}
	border_verts = {}
	#border_gradient = {}


	border_edges_head = {}
	border_verts_head = {}
	#border_gradient_head = {}
	# figure the headLoop
	#for edge in backHead.edges:
	#	if(backHead.edges[edge].is_boundary()):
	#		border_edges_head[edge] = backHead.edges[edge]
	#print(len(border_edges_head))
	#return

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

	# extend face new vertices
	for vert in border_verts:

		# find closest point on border_verts_head
		dist = -1
		c1 = border_verts_head[next(iter(border_verts_head))]
		for verth in border_verts_head:
			ab_vec = border_verts_head[verth].getLocation() - border_verts[vert].getLocation()
			if(dist==-1 or np.linalg.norm(ab_vec) < dist):
				dist = np.linalg.norm(ab_vec)
				c1 = border_verts_head[verth]
		target_vector = c1.getLocation() - border_verts[vert].getLocation()
		target_vector *= 1



		face.props = np.append(face.verts[vert].getLocation() + target_vector, np.array((255, 255, 255, 255), dtype='float64')).tolist()
		new_id = len(face.verts)
		face.verts[new_id] = Vertex(new_id, face.props)
		face.edges[str(new_id)+':'+str(vert)] = Edge(str(new_id)+':'+str(vert), face.verts)

	# Create Faces
	for edge in border_edges:
		v1 = face.verts[border_edges[edge].v1_idx]
		for vert_edge in v1.edges:
			if(vert_edge.retrieve_other_vert(v1, face.verts).index >= currentVerts):
				e1 = vert_edge
				v_next1 = vert_edge.retrieve_other_vert(v1, face.verts)

		v2 = face.verts[border_edges[edge].v2_idx]
		for vert_edge in v2.edges:
			if(vert_edge.retrieve_other_vert(v2, face.verts).index >= currentVerts):
				e2 = vert_edge
				v_next2 = vert_edge.retrieve_other_vert(v2, face.verts)

		new_edge_name = str(v_next1.index)+':'+str(v_next2.index)
		face.edges[new_edge_name] = Edge(new_edge_name, face.verts)

		e3 = border_edges[edge]
		e4 = face.edges[new_edge_name]

		new_face = Face(len(face.faces), (v1.index, v2.index, v_next2.index, v_next1.index))
		face.faces[len(face.faces)] = new_face

		e1.add_face(new_face)
		e2.add_face(new_face)
		e3.add_face(new_face)
		e4.add_face(new_face)


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

		




