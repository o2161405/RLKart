import trimesh
import numpy as np
import time
import math

full_mesh = trimesh.load('../model/full_mesh.obj', force='mesh')
road_mesh = trimesh.load('../model/lol1.obj', force='mesh')

MAX_DIST = 10000

def mesh_normalized_ray_lengths(character_position=[0, 0, 0], ray_amount=1, ray_rotation=180, show_trimesh_ui=False):

	def generate_rays(amount_per_360, rotation):
		ray_directions = np.zeros((amount_per_360, 3))  # Pre-allocate array for all rays

		for ray in range(amount_per_360):
		    angle = 2 * np.pi * ray / amount_per_360  # Use radians for trigonometric functions

		    # Convert rotation to radians
		    rotation_rad = math.radians((-rotation+90))

		    # Apply rotation to the base direction vector (0, 0, 1)
		    base_direction = np.array([0, 0, 1])
		    rotated_direction = np.dot(np.linalg.inv(np.array([[1, 0, 0], [0, math.cos(rotation_rad), -math.sin(rotation_rad)], [0, math.sin(rotation_rad), math.cos(rotation_rad)]])), base_direction)

		    # Combine base rotation with the original angle
		    final_direction = np.array([math.cos(angle + rotation_rad), 0, math.sin(angle + rotation_rad)])

		    # Update the ray direction with the final rotated vector
		    ray_directions[ray] = final_direction

		return ray_directions

	ray_directions = generate_rays(ray_amount, ray_rotation)
	origin = np.array([character_position[0]/100, (character_position[1]/100)+1, character_position[2]/100])
	ray_origins = np.tile(origin, (ray_directions.shape[0], 1))

	full_mesh_intersect_points = full_mesh.ray.intersects_id(
	ray_origins=ray_origins,
	ray_directions=ray_directions,
	multiple_hits=False,
	max_hits=1,
	return_locations=True)[2]

	full_mesh_out = []
	for i in full_mesh_intersect_points:
		output = math.sqrt((abs((i[0]*100) - character_position[0])**2) + (abs((i[2]*100) - character_position[2])**2))
		if output < MAX_DIST:
			full_mesh_out.append(round(output/MAX_DIST, 6))
			continue
		full_mesh_out.append(1)

	if show_trimesh_ui:
		full_mesh.unmerge_vertices()
		# make mesh white
		full_mesh.visual.face_colors = [255,255,255,255]
		ray_visualize = trimesh.load_path(np.hstack((ray_origins, ray_origins + ray_directions*100.0)).reshape(len(ray_directions), 2, 3))
		scene = trimesh.Scene([full_mesh, ray_visualize])
		scene.show()

	return full_mesh_out

