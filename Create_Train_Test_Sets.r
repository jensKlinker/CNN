# This script is used to resize images from 64x64 to 28x28 pixels

# Clear workspace
rm(list=ls())

# Load EBImage library
require(EBImage)

# Load data
cwd <- getwd()
#Set this path to where your supersampled and encoded dataset is saved
#X <- read.csv("C:/Users/Admin/Desktop/CNN/Encoded_Dataset/Encoded_Image_List.csv", header = F)
X <- read.csv("C:/Users/Admin/Desktop/CNN/Encoded_Dataset/Encoded_Simeion_Set.csv", header = F)

#Set this path to where your supersampled and encoded labels are saved
#labels <- read.csv("C:/Users/Admin/Desktop/CNN/Encoded_Labels/Encoded_Single_Label_List.csv", header = F)
labels <- read.csv("C:/Users/Admin/Desktop/CNN/Encoded_Labels/Encoded_Simeion_Set.csv", header = F)
nrow(labels)
nrow(X)
length(X)

# Dataframe of resized images
rs_df <- data.frame()

# Main loop: for each image, resize and set it to greyscale
for(i in 1:(nrow(X)))
{
    # Try-catch
    result <- tryCatch({
    # Image (as 1d vector)
    img_vector <- as.numeric(X[i,])
    # Add label
    label <- labels[i,]
    # Combine label and image
    vec <- c(label, img_vector)
    # Stack in rs_df using rbind
    rs_df <- rbind(rs_df, vec)
    rs_df <- unname(rs_df)
    # Print status
    print(paste("Done",i,"of",nrow(X),sep = " "))},
    # Error function (just prints the error). Btw you should get no errors!
    error = function(e){print(e)})
}


# Set names. The first columns are the labels, the other columns are the pixels.
names(rs_df) <- c(paste("Label", length(labels)), paste("pixel", c(1:length(X))))

# Train-test split
#-------------------------------------------------------------------------------
# Simple train-test split. No crossvalidation is done here.

# Set seed for reproducibility purposes
set.seed(100)

# Shuffled df
shuffled <- rs_df[sample(1:nrow(X)),]

# Train-test split
split <- nrow(X)*0.9
train_set <- shuffled[1:split, ]
test_set <- shuffled[(split+1):nrow(X), ]

# Save train-test datasets
write.csv(train_set, "C:/Users/Admin/Desktop/CNN/Train_Test_Sets/train_set.csv", row.names = FALSE)
write.csv(test_set, "C:/Users/Admin/Desktop/CNN/Train_Test_Sets/test_set.csv", row.names = FALSE)

# Done!
print("Done!")
