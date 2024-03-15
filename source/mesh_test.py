import trimesh
import numpy as np
import time

mesh = trimesh.load('../model/a_test.obj', force='mesh')

t0 = time.time()

X, Y, Z = [-12203.0, 1060.51611328125, -2954.655029296875]
ray_origins = np.array([[0, 0, 0]]) # We need at least 1 element in here

inbetween_gap = 2
definition = 15 # 15x15 grid

for i in range(1, definition + 1):
	for j in range(1, definition + 1):
		new_ray = np.array([
			((X/100) + (i * inbetween_gap) - inbetween_gap) - (((definition * inbetween_gap) / 2) - (inbetween_gap / 2)),
			(Y/100) + 10,
			((Z/100) + (j * inbetween_gap) - inbetween_gap) - (((definition * inbetween_gap) / 2) - (inbetween_gap / 2)),
			])
		ray_origins = np.vstack((ray_origins, new_ray))

"""locations, index_ray, index_tri = mesh.ray.intersects_location(
        ray_origins=ray_origins,
        ray_directions=ray_directions)"""

ray_origins = ray_origins[1:]
direction = np.array([0, -1, 0])
ray_directions = np.tile(direction, (ray_origins.shape[0], 1))

#ray_visualize = trimesh.load_path(np.hstack((ray_origins,
                                             #ray_origins + ray_directions*20.0)).reshape(len(ray_origins), 2, 3))

intersect_locations = mesh.ray.intersects_id(
        ray_origins=ray_origins,
        ray_directions=ray_directions,
        multiple_hits=False,
        max_hits=1,
        return_locations=True)[2]

t1 = time.time()
print(t1-t0)
exit()

print(intersect_locations)
print(len(intersect_locations))

#mesh.unmerge_vertices()
mesh.visual.face_colors = [255,255,255,255]
scene = trimesh.Scene([mesh, ray_visualize])
scene.show()