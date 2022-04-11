# Imports

from Cluster import Cluster




clstr = Cluster()

# # Get the image object.
# clstr.load_image(
#     image_path = 'immunostain.jpg'
# )

# # clstr.show_image()

# # Define some training regions.

# # Done ahead of time...

# # Format is [x1, y1, x2, y2]
# t_rs = {
#     1: [573, 280, 625, 340],
#     2: [860, 200, 885, 205],
#     3: [380, 570, 445, 600]
# }

# # Find the centroids.
# clstr.generate_centroids(
#     image_object = clstr.image_object,
#     show_regions = False,
#     training_regions = t_rs
# )

# # Label each pixel using L2 distance.
# clstr.label_signal(
#     parallel = True,
#     source_image = clstr.image_object,
#     show_plots = False
# )

# Call R to get the k-means clusters.
# clstr.call_R()

# Collapse the images of k-means clusters.
clstr.collapse_k_means_images(
    search_location = '/home/aeros/Desktop/workspace/pib706/workshop_extension/workshop_4/r_scripts/'
)