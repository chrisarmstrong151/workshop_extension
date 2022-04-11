# Set the working directory
setwd('/home/aeros/Desktop/workspace/pib706/workshop_extension/workshop_4/r_scripts')




# Libraries

# Data table
library(data.table)
setDTthreads(threads = 4)

# Plotting
library(ggplot2)




# Load the data
loaded <- read.table(
    file = 'R_lines.csv', 
    sep = ',', 
    stringsAsFactors = FALSE, 
    header = TRUE
)

# SLOW

# Apply a rotation matrix to each element in loaded.
rotation_matrix = matrix

# Define the angle.
angle = -pi/2

# How large is the y-axis?
y_axis_length <- 960

rotated <- lapply(seq(1, nrow(loaded)), function(row) {

    # Get the row x and y coordinates.

    # Add 1 to each coordinate since NumPy is
    # 0-indexed and R is 1-indexed.
    row_x <- loaded[row, c('x')]+1
    row_y <- loaded[row, c('y')]+1
    
    # Perform the rotation.
    data.frame(
        x = row_x*cos(angle)-row_y*sin(angle),
        y = row_x*sin(angle)+row_y*cos(angle) + y_axis_length
    )

})

# Get rid of the NULLs.
# Source: https://stackoverflow.com/questions/33004238/r-removing-null-elements-from-a-list/33004339#33004339
rotated[sapply(rotated, is.null)] <- NULL

# Collapse.
collapsed <- data.table::rbindlist(rotated)

# CHECK

# The coordinates are valid?
print(c(min(collapsed$x), max(collapsed$x)))
print(c(min(collapsed$y), max(collapsed$y)))

# Try k-means with 1, 2, ..., 7 clusters.
for(cluster_size in seq(1, 7)) {
    
    # Get the clusters.
    clustered <- kmeans(
        x = collapsed, 
        centers = cluster_size
    )

    # Add the labels to the data.
    collapsed$Cluster <- as.factor(clustered$cluster)

    # Plot and save.

    # Nice colors: http://applied-r.com/rcolorbrewer-palettes/#:~:text=RColorBrewer%20is%20an%20R%20packages,data%2C%20dark%20for%20high%20data
    p <- ggplot(
        data = collapsed, 
        mapping = aes(
            x = x, 
            y = y,
            color = Cluster
        )
    ) + 
    geom_point() + 
    scale_colour_brewer(
        palette = 'Set2'
    ) + 
    ggtitle(
        paste(c('k = ', as.character(cluster_size)), collapse = '')
    ) + 
    theme(
        plot.title = element_text(
            hjust = 0.5
        )
    )

    p

    ggsave(
        paste(c('cluster_', as.character(cluster_size), '.png'), collapse = ''),
        plot = last_plot(),
        path = './',
        width = 800,
        height = 800,
        units = c('px'),
        dpi = 300
    )
}