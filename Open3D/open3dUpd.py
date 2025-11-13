"""
Assignment 5 — Data Visualization
Author: <Your Name>
Project: USS Hermes (Open3D)
"""

import open3d as o3d
import numpy as np
import os

def show_and_save(geometry, window_name, filename):
    vis = o3d.visualization.Visualizer()
    vis.create_window(window_name=window_name)
    
    # If a list, add each geometry
    if isinstance(geometry, list):
        for g in geometry:
            vis.add_geometry(g)
    else:
        vis.add_geometry(geometry)
    
    vis.poll_events()
    vis.update_renderer()
    vis.capture_screen_image(filename)
    vis.destroy_window()

# ============================================================
# Setup: define model folder path
# ============================================================

# Path to the Hermes folder (relative to this script)
base_dir = os.path.dirname(os.path.abspath(__file__))
hermes_dir = os.path.join(base_dir, "Hermes")

# Verify that directory exists
if not os.path.exists(hermes_dir):
    raise FileNotFoundError(f"Hermes folder not found at: {hermes_dir}")

# List of OBJ parts (update names if your files differ)
filenames = [
    "hermes1.obj", "hermes2.obj", "hermes3.obj", "hermes4.obj",
    "hermes5.obj", "hermes6.obj", "hermes7.obj", "hermes8.obj",
    "hermes9.obj", "hermes10.obj", "hermes11.obj", "hermes12.obj"
]

# ============================================================
# Step 1: Loading and Visualization
# ============================================================

print("\n=== Step 1: Loading and Combining Meshes ===")

all_meshes = []
for f in filenames:
    path = os.path.join(hermes_dir, f)
    if not os.path.exists(path):
        print(f"⚠️ File not found: {path}")
        continue
    mesh_part = o3d.io.read_triangle_mesh(path)
    if mesh_part.is_empty():
        print(f"⚠️ Warning: {f} loaded but contains no geometry.")
    all_meshes.append(mesh_part)

if len(all_meshes) == 0:
    raise RuntimeError("No .obj files loaded. Check filenames or paths.")

# Combine all meshes into one
combined_mesh = all_meshes[0]
for m in all_meshes[1:]:
    combined_mesh += m

print("Vertices:", len(combined_mesh.vertices))
print("Triangles:", len(combined_mesh.triangles))
print("Has vertex colors:", combined_mesh.has_vertex_colors())
print("Has vertex normals:", combined_mesh.has_vertex_normals())

o3d.visualization.draw_geometries([combined_mesh], window_name="Step 1 — Original Combined Mesh")
show_and_save(combined_mesh, "Step 1: Original Mesh", "step1_mesh.png")

# ============================================================
# Step 2: Conversion to Point Cloud
# ============================================================

print("\n=== Step 2: Converting to Point Cloud ===")
pcd = combined_mesh.sample_points_uniformly(number_of_points=50000)
print("Points:", len(pcd.points))
print("Has colors:", pcd.has_colors())
o3d.visualization.draw_geometries([pcd], window_name="Step 2 — Point Cloud")
show_and_save(pcd, "Step 2: Point Cloud", "step2_pointcloud.png")

# ============================================================
# Step 3: Surface Reconstruction (Poisson)
# ============================================================

print("\n=== Step 3: Surface Reconstruction (Poisson) ===")
pcd.estimate_normals()
mesh_poisson, densities = o3d.geometry.TriangleMesh.create_from_point_cloud_poisson(pcd, depth=8)

# Crop to remove outer artifacts
bbox = pcd.get_axis_aligned_bounding_box()
mesh_crop = mesh_poisson.crop(bbox)

print("Vertices:", len(mesh_crop.vertices))
print("Triangles:", len(mesh_crop.triangles))
print("Has color:", mesh_crop.has_vertex_colors())
o3d.visualization.draw_geometries([mesh_crop], window_name="Step 3 — Reconstructed Mesh")
show_and_save(mesh_crop, "Step 3: Poission Reconstruction", "step3_poisson.png")


# ============================================================
# Step 4: Voxelization
# ============================================================

print("\n=== Step 4: Voxelization ===")
voxel_grid = o3d.geometry.VoxelGrid.create_from_point_cloud(pcd, voxel_size=0.05)
print("Number of voxels:", len(voxel_grid.get_voxels()))
o3d.visualization.draw_geometries([voxel_grid], window_name="Step 4 — Voxel Grid")
show_and_save(voxel_grid, "Step 4: Voxel Grid", "step4_voxels.png")

# ============================================================
# Step 5: Adding a Plane
# ============================================================

print("\n=== Step 5: Adding a Plane ===")
plane = o3d.geometry.TriangleMesh.create_box(width=3.0, height=3.0, depth=0.02)
plane.translate((0, 0, -0.5))
plane.paint_uniform_color([0.8, 0.8, 0.8])
print("Plane added below the model.")
o3d.visualization.draw_geometries([mesh_crop, plane], window_name="Step 5 — Object + Plane")
show_and_save([mesh_crop, plane], "Step 5: Mesh + PLane", "step5_mesh_plane.png")

# ============================================================
# Step 6: Surface Clipping
# ============================================================

print("\n=== Step 6: Clipping Points Above Plane ===")
points = np.asarray(pcd.points)
mask = points[:, 2] > -0.2  # keep points above z=-0.2
clipped_points = points[mask]
clipped_pcd = o3d.geometry.PointCloud()
clipped_pcd.points = o3d.utility.Vector3dVector(clipped_points)

print("Remaining vertices:", len(clipped_points))
print("Has color:", clipped_pcd.has_colors())
o3d.visualization.draw_geometries([clipped_pcd], window_name="Step 6 — Clipped Model")
show_and_save(clipped_pcd, "Step 6: Clipped Point Cloud", "step6_clipped.png")

# ============================================================
# Step 7.1: Half Gradient Coloring + Extremes
# ============================================================

print("\n=== Step 7: Gradient Coloring and Extremes ===")
points = np.asarray(clipped_pcd.points)
x_vals = points[:, 0]  # Using X-axis for gradient
min_x, max_x = np.min(x_vals), np.max(x_vals)

# Color gradient: red (min) → blue (max)
colors = (x_vals - min_x) / (max_x - min_x)
colors = np.stack([colors, np.zeros_like(colors), 1 - colors], axis=1)
clipped_pcd.colors = o3d.utility.Vector3dVector(colors)

# Highlight extremes
min_sphere = o3d.geometry.TriangleMesh.create_sphere(radius=0.03)
min_sphere.translate(points[np.argmin(x_vals)])
min_sphere.paint_uniform_color([1, 0, 0])  # red

max_sphere = o3d.geometry.TriangleMesh.create_sphere(radius=0.03)
max_sphere.translate(points[np.argmax(x_vals)])
max_sphere.paint_uniform_color([0, 1, 0])  # green

print(f"Min X: {min_x:.3f}, Max X: {max_x:.3f}")
o3d.visualization.draw_geometries(
    [clipped_pcd, min_sphere, max_sphere],
    window_name="Step 7.1 — Gradient & Extremes"
)
show_and_save([clipped_pcd, min_sphere, max_sphere], "Step 7.1: Gradient + Extrema", "step7.1_gradient_extremes.png")

# ============================================================
# Step 7.2: Full Gradient Coloring + Extremes
# ============================================================

# Use the original full point cloud from Step 2
points_full = np.asarray(pcd.points)  # original full ship
pcd_full = pcd  # full ship point cloud

# Apply gradient along X-axis
colors_full = (points_full - points_full.min(axis=0)) / (points_full.max(axis=0) - points_full.min(axis=0))
pcd_full.colors = o3d.utility.Vector3dVector(colors_full)

# Find extrema along X-axis
min_idx = np.argmin(points_full[:, 0])
max_idx = np.argmax(points_full[:, 0])
min_point = points_full[min_idx]
max_point = points_full[max_idx]

# Highlight extrema with named spheres
min_sphere = o3d.geometry.TriangleMesh.create_sphere(radius=0.05)
min_sphere.paint_uniform_color([1, 0, 0])  # red
min_sphere.translate(min_point)

max_sphere = o3d.geometry.TriangleMesh.create_sphere(radius=0.05)
max_sphere.paint_uniform_color([0, 1, 0])  # green
max_sphere.translate(max_point)

print("Full Ship - Min Point:", min_point)
print("Full Ship - Max Point:", max_point)

o3d.visualization.draw_geometries([pcd_full, min_sphere, max_sphere],
                                  window_name="Step 7.2 — Full Ship Gradient & Extremes")


show_and_save([pcd_full, min_sphere, max_sphere], 
              "Step 7.2: Full Ship Gradient + Extremes", 
              "step7.2_fullship_gradient.png")


print("\n✅ All steps completed successfully.")

