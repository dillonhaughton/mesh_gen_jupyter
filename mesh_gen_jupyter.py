'''
Author:  Dillon Haughton
Date:    Jun 7th, 2021
Version: 1.0

Purpose: To provide a non-programmer user friendly interface to visualize and alter 3d meshes. Provided professors a means to generate 
		 3D quizes and elearning content for their students. Ideally the meshes provided in this would be generated in meshroom. and
		 any alterations done in blender or meshlab. Ideally only a knowledge of Jupyter notebooks would be needed and this code
		 will run as a backend.


'''


import trimesh
import matplotlib.colors as cl
import numpy as np
import k3d


# Functions
#-----------------------------------------------------------------
def qualities(mesh_file):
	# Will generate colors and uv map from mesh
	tri_mesh = trimesh.load(mesh_file)
	colors   = tri_mesh.visual.to_color().vertex_colors
	colors   = colors[:,:-1]
	hexer    = [(A[0]<<16) + (A[1]<<8) + A[2] for A in colors]
	uv       = tri_mesh.visual.uv

	return tri_mesh, hexer, uv


def qualities_multiple_textures(mesh_file):
	# Will generate colors and uv map from mesh
	tri_mesh = trimesh.load(mesh_file)
	
	dump = tri_mesh.dump(concatenate=False)
	Colors = []
	uvs = []
	for i in dump:
		colors = i.visual.to_color().vertex_colors
		colors = colors[:,:-1]
		hexer  = [(A[0]<<16) + (A[1]<<8) + A[2] for A in colors]
		Colors += [hexer]
		uvs    += [i.visual.uv]

	return dump, Colors, uvs	
#-----------------------------------------------------------------

# Classes
#-----------------------------------------------------------------

class mesh_gen:
	def __init__(self):

		self.plot = k3d.plot(grid_visible=False, menu_visibility=True, auto_rendering=True, background_color=0x000000, lighting=0, camera_rotate_speed=5)

	def add_mesh(self, filename, texture, name):
		Mesh, colors, uv_map = qualities(filename)
		texture        = open(texture, 'rb').read()
		self.plot += k3d.mesh(Mesh.vertices, Mesh.faces, colors = colors, uvs=uv_map, texture=texture, texture_file_format='png', name=name)

	def add_multimesh(self, filename, texture_files, name):
		Mesh, colors, uv_map = qualities_multiple_textures(filename)
		texture_maps = [open(i,'rb').read() for i in texture_files]
		name = [name] * len(Mesh)
		for i,j in enumerate(Mesh):
			self.plot += k3d.mesh(j.vertices, j.faces, colors = colors[i], uvs=uv_map[i], texture=texture_maps[i], texture_file_format='png', name=name[i])


	def add_label(self, vertices, text, name):

		label = k3d.label(text, vertices, is_html=True, name=name, color=0xFFFFFF)
		self.plot += label

	def add_color(self, filename, color, name, opacity=0.15):
		tri_mesh = trimesh.load(filename)
		try:
			dump = tri_mesh.dump(concatenate=False)
			for i in dump:
				self.plot += k3d.mesh(i.vertices, i.faces, color=color, opacity = opacity, name=name)

		except:
				
			self.plot += k3d.mesh(tri_mesh.vertices, tri_mesh.faces, color = color, opacity = opacity, name = name)		 	

	def display(self):
		self.plot.display()	

	def to_html(self, filename):
		snap = self.plot.get_snapshot()
		with open(filename, 'w') as fp:
			fp.write(snap)	


