import trimesh
import numpy as np
import time

mesh = trimesh.load('a.obj', force='mesh')

ray_directions = np.array([[0, 0, -1],
						   [0, 0, 1],
						   [-1, 0, 0],
						   [1, 0, 0],
						   [-1, 0, -1],
						   [1, 0, 1],
						   [-1, 0, 1],
						   [1, 0, -1],
							])

t0 = time.time()

origin = np.array([(-14720/100), (1060.515/100), (-2954.655/100)])
ray_origins = np.tile(origin, (ray_directions.shape[0], 1))

intersect_location = mesh.ray.intersects_id(
        ray_origins=ray_origins,
        ray_directions=ray_directions,
        multiple_hits=False,
        max_hits=1,
        return_locations=True)[2]

t1 = time.time()

print(f"{intersect_location}\n{round(t1-t0, 5)}ms")

mesh.unmerge_vertices()
# make mesh white- ish
mesh.visual.face_colors = [255,255,255,255]
#mesh.visual.face_colors[index_tri] = [255, 0, 0, 255]

ray_visualize = trimesh.load_path(np.hstack((ray_origins, ray_origins + ray_directions*100.0)).reshape(len(ray_directions), 2, 3))

scene = trimesh.Scene([mesh, ray_visualize])

scene.show()
