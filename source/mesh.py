import trimesh
import numpy as np
import time

mesh = trimesh.load('../model/a.obj', force='mesh')

# Should probably make a function to generate these
ray_directions = np.array([[0, 0, -1],
			   [0, 0, 1],
			   [-1, 0, 0],
			   [1, 0, 0],
			   [-1, 0, -1],
			   [1, 0, 1],
			   [-1, 0, 1],
			   [1, 0, -1],
			   ])

#origin = np.array([(1), (1), (1)])
#ray_origins = np.tile(origin, (ray_directions.shape[0], 1))

def get_raycasts(X, Y, Z):
	origin = np.array([(X/100), (Y/100), (Z/100)])
	ray_origins = np.tile(origin, (ray_directions.shape[0], 1))

	intersect_locations = mesh.ray.intersects_id(
	        ray_origins=ray_origins,
	        ray_directions=ray_directions,
	        multiple_hits=False,
	        max_hits=1,
	        return_locations=True)[2]

	return intersect_locations

#mesh.unmerge_vertices()
# make mesh white- ish
#mesh.visual.face_colors = [255,255,255,255]
#mesh.visual.face_colors[index_tri] = [255, 0, 0, 255]

#ray_visualize = trimesh.load_path(np.hstack((ray_origins, ray_origins + ray_directions*100.0)).reshape(len(ray_directions), 2, 3))

#scene = trimesh.Scene([mesh, ray_visualize])

#scene.show()
