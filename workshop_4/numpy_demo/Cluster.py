# Imports

# Image appending
import cv2

# Finding images
import glob

# Appending
import numpy as np

# Image I/O
import imageio

# Displaying
import matplotlib.pyplot as plt

# Multiprocessing
from multiprocessing import Pool

# Spawning processes
import subprocess

# Timing
# Source: https://datatofish.com/measure-time-to-run-python-script/
import time




class Cluster():
    
    """Clustering tools"""
    
    def call_R(
        self
    ):

        """Make a call to R to generate the k-means clusters."""
        
        subprocess.Popen(
            ["Rscript", "./r_scripts/clusters.r"]
        )
    

    def collapse_k_means_images(
        self,
        search_location
    ):

        """Make a panel of k-means clusters images."""
        
        # Get all the .png images at search_location.
        images = glob.glob(
            pathname = search_location + '*.png'
        )

        # glob is not guaranteed to give images back in 
        # the right order, so process the image names
        # into a dictionary.
        images_ordered = {}

        # Keep track of the maximum image number.
        max_image_number = 0

        # Go over each image.
        for i in images:

            # Split on the underscore at the end of
            # the path.
            split_up = i.split('/')[-1].split('_')[1].split('.')[0]

            # Now create the key.
            images_ordered[split_up] = i

            # New max?
            if int(split_up) > max_image_number:
                max_image_number = int(split_up)

        # Read the images in.
        read_images = [imageio.imread(images_ordered[str(i)]) for i in range(1, max_image_number + 1)]
        
        # Create a panel.
        
        # OpenCV solution (doesn't have issue
        # with removing annotations).
        # Source: https://note.nkmk.me/en/python-opencv-hconcat-vconcat-np-tile/
        cv2.imwrite('k_means.png', cv2.hconcat(read_images))
    

    def generate_centroids(
        self,
        image_object,
        show_regions,
        training_regions
    ):
        
        """Generate centroids given training data."""

        # Initialize an array to hold the centroids.
        self.centroids = []
        
        # Use each of the training regions to get a distribution
        # of colors.

        for k, v in training_regions.items():
            
            # Slices have to be with the XY system
            # that python uses, see https://scipy-lectures.org/advanced/image_processing/index.html#basic-manipulations

            # Get the training slice.
            training_slice = image_object[slice(v[1], v[3]), slice(v[0], v[2])]
            
            # Calculate the centroid.
            # Source: https://stackoverflow.com/questions/18714587/how-to-calculate-centroid-in-python/18721175#18721175
            # Source: https://numpy.org/doc/stable/reference/generated/numpy.mean.html#numpy.mean
            self.centroids.append(
                np.mean(
                    training_slice,
                    axis = (0, 1)
                )
            )
            
            if show_regions is True:
            
                # Show the image (coordinates inverted).
                # Source: https://stackoverflow.com/questions/42644158/matplotlib-not-displaying-image/42644660#42644660
                plt.imshow(image_object[slice(v[1], v[3]), slice(v[0], v[2])])
                plt.show()
    

    # L2 distance
    def l_two_distance(
        self,
        point,
        cntrds,
        cutoff
    ):

        """Calculate the L2 distance between two points in 3D space."""
        
        # Simply calculate the L2 distance between
        # two points in 3-D space.

        # See if the point is within cutoff of any
        # of the centroids.

        # Have to keep the right dimensions.
        for cntrd in cntrds:
            if np.linalg.norm(point-cntrd) <= cutoff:
                
                point[0], point[1], point[2] = 255, 255, 255

                # Don't need to check any other centroids.
                break

            else:

                point[0], point[1], point[2] = 0, 0, 0

        return point

    
    def load_image(
        self,
        image_path,
        show_image=False
    ):

        """Load an image."""

        try:
            
            # Load and set the image at image_path.
            self.image_object = imageio.imread(image_path)
        
        except FileNotFoundError:

            print('Path \'' + image_path + '\' was not found.  Quitting...')

            return 1
    
    
    def label_signal(
        self,
        source_image,
        parallel = False,
        show_plots = False
    ):

        """Go pixel-by-pixel and label the pixel as a positive signal or not."""

        # Create a list to hold the merged image.
        # Source: https://stackoverflow.com/a/63848370
        merged_image = []
        
        # This is based on some L2 cutoff distance that we define.
        # for l_two_cutoff in range(10, 30, 10):
        # for l_two_cutoff in range(10, 140, 10):
        # for l_two_cutoff in range(110, 120, 1):
        for l_two_cutoff in [115+i*0.5 for i in range(0, 10)]:
            
            # Close the plot.
            # Source: https://stackoverflow.com/a/37736370
            plt.close()
            
            # Make a copy every run through the loop,
            # otherwise, we'll be changing the original
            # array and not start with a fresh copy.
            copied = source_image.copy()
            
            # Apply the function over each element.
            # Source: https://stackoverflow.com/questions/22424096/apply-functions-to-3d-numpy-array/47146925#47146925
            x,y,z = copied.shape[0], copied.shape[1], copied.shape[2]
            
            reshaped = copied.reshape(
                x*y,
                z
            )

            # Do everything in parallel?
            if parallel is True:

                # Time everything.
                startTime = time.time()
                
                # The L2 calculation is expensive, so split the
                # image into chunks, giving each one to a processor.
                split_up =  self.split(
                    a = reshaped,
                    n = 40
                )

                # Multiprocessing based on example at https://docs.python.org/3/library/multiprocessing.html#introduction
                with Pool(40) as p:

                    split_process = p.map(self.norm_along_axis, [(l_two_cutoff, i) for i in split_up])

                    # Put the image back together.
                    # Source: https://numpy.org/doc/stable/reference/generated/numpy.vstack.html#numpy.vstack
                    reshaped = np.vstack(split_process)
                
                # Stop the timer.
                executionTime = (time.time() - startTime)
                print('Norm calculation time: ' + str(executionTime))
            
            else:

                # Time everything.
                startTime = time.time()
                
                reshaped = self.norm_along_axis(
                    incoming = (l_two_cutoff, reshaped)
                )

                # Stop the timer.
                executionTime = (time.time() - startTime)
                print('Norm calculation time: ' + str(executionTime))
            
            reshaped = reshaped.reshape(
                x,
                y,
                z
            )
            
            # Save the NumPy array as binary so that
            # we can load the image info later.
            np.save(
                file = str(l_two_cutoff) + '_cutoff.binary',
                arr = reshaped
            )

            # Save the plot.

            # Note the saving order here.
            # Source: https://stackoverflow.com/a/47343051
            plt.imshow(reshaped)
            plt.title(str(l_two_cutoff) + ' Cutoff')
            plt.savefig(str(l_two_cutoff) + '_cutoff.png')

            # "Quick and dirty" to get numpy array from image
            # WITH title and axes.

            # Append the annotated image to the merged image.
            merged_image.append(imageio.imread(str(l_two_cutoff) + '_cutoff.png'))

            if show_plots is True:
                
                # Show the plot.
                plt.show()
        
        plt.close()
        # NumPy (save the merged image).
        # plt.imshow(np.concatenate(merged_image))
        # plt.savefig('all_cutoffs.png')
        
        # OpenCV solution (doesn't have issue
        # with removing annotations).
        # Source: https://note.nkmk.me/en/python-opencv-hconcat-vconcat-np-tile/
        cv2.imwrite('all_cutoffs.png', cv2.hconcat(merged_image))
        
    
    def norm_along_axis(
        self,
        incoming
    ):

        """Parallelized version of a norm along an axis."""

        # The arguments (incoming) are passed as tuples.        
        return np.apply_along_axis(
            func1d = self.l_two_distance, 
            axis = 1, 
            arr = incoming[1], 
            cntrds = self.centroids, 
            cutoff = incoming[0]
        )


    def show_image(
        self
    ):

        """Show a loaded image."""

        # Has the image been loaded?
        try:
            
            plt.imshow(self.image_object)
            plt.show()

        except AttributeError:

            print('The image was not loaded!')
    

    def split(
        self,
        a, 
        n
    ):

        """Generate chunks of size n"""

        # Source: https://stackoverflow.com/a/2135920

        # a is a list and n is the number of chunks.        
        k, m = divmod(len(a), n)

        return list(a[i*k+min(i, m):(i+1)*k+min(i+1, m)] for i in range(n))

    
    def write_cutoff_for_R(
        self
    ):
    
        """Write output that R can use."""
        
        # Cutoff of around 70 looks good.

        # Read it in.
        loaded = np.load(
            file = '70_cutoff.binary.npy', 
            allow_pickle = True
        )

        # Write out a simple format for R to use.

        # Open the file to write the image pixels.
        with open('R_lines.csv', 'w') as f:

            # Transpose the array to match standard plotting order.
            # loaded = np.transpose(
            #     a = loaded
            # )

            # Write the header.
            f.write('x,y,signal\n')
            
            # Loop over image rows and columns.
            for x in range(0, len(loaded)):
                for y in range(0, len(loaded[x])):

                    # Keep the non-zero entries.
                    if np.all((loaded[x][y] != 0)):
                        
                        # Write the file.

                        # Note the inversion of coordinates here.
                        f.write(','.join([str(x), str(y), '1']) + '\n')