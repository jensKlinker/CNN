# Clean workspace
rm(list=ls())

# Load MXNet
require(mxnet)

# Loading data and set up
#-------------------------------------------------------------------------------

# Load train and test datasets
train <- read.csv("C:/Users/Admin/Desktop/CNN/Train_Test_Sets/train_set.csv")
test <- read.csv("C:/Users/Admin/Desktop/CNN/Train_Test_Sets/test_set.csv")
length(train)

# Set up train and test datasets
train <- data.matrix(train)
train_x <- t(train[, -1])
write.csv(train_x, "C:/Users/Admin/Desktop/CNN/Train_Test_Sets/train_x.csv", row.names = FALSE)
train_y <- train[, 1]
write.csv(train_y, "C:/Users/Admin/Desktop/CNN/Train_Test_Sets/train_y.csv", row.names = FALSE)
train_array_x <- train_x
#Adapt dim array to dimensions of the images (in this case 28hX28w + 1 label x 729 images)
dim(train_array_x) <- c(16, 16, 1, ncol(train_x))
write.csv(train_array_x, "C:/Users/Admin/Desktop/CNN/Train_Test_Sets/train_array.csv", row.names = FALSE)

test_x <- t(test[, -1])
test_y <- test[, 1]
test_array_x <- test_x
#Adapt dim array to dimensions of the images (in this case 28hX28w + 1 label x 729 images)
dim(test_array_x) <- c(16, 16, 1, ncol(test_x))


# Set up the symbolic model
#-------------------------------------------------------------------------------

data <- mx.symbol.Variable('data')
# 1st convolutional layer
conv_1 <- mx.symbol.Convolution(data = data, kernel = c(5, 5), num_filter = 20)
tanh_1 <- mx.symbol.Activation(data = conv_1, act_type = "tanh")
pool_1 <- mx.symbol.Pooling(data = tanh_1, pool_type = "max", kernel = c(2, 2), stride = c(2, 2))
# 2nd convolutional layer
conv_2 <- mx.symbol.Convolution(data = pool_1, kernel = c(5, 5), num_filter = 50)
tanh_2 <- mx.symbol.Activation(data = conv_2, act_type = "tanh")
pool_2 <- mx.symbol.Pooling(data=tanh_2, pool_type = "max", kernel = c(2, 2), stride = c(2, 2))
# 1st fully connected layer
flatten <- mx.symbol.Flatten(data = pool_2)
fc_1 <- mx.symbol.FullyConnected(data = flatten, num_hidden = 500)
tanh_3 <- mx.symbol.Activation(data = fc_1, act_type = "tanh")
# 2nd fully connected layer
fc_2 <- mx.symbol.FullyConnected(data = tanh_3, num_hidden = 40)
# Output. Softmax output since we'd like to get some probabilities.
NN_model <- mx.symbol.SoftmaxOutput(data = fc_2)

# Pre-training set up
#-------------------------------------------------------------------------------

# Set seed for reproducibility
mx.set.seed(100)

# Device used. CPU in my case.
devices <- mx.cpu()

# Training
#-------------------------------------------------------------------------------

# Train the model
model <- mx.model.FeedForward.create(NN_model,
                                     X = train_array_x,
                                     y = train_y,
                                     ctx = devices,
                                     num.round = 60,
                                     array.batch.size = 40,
                                     learning.rate = 0.01,
                                     momentum = 0.9,
                                     eval.metric = mx.metric.accuracy
                                     )

# Testing
#-------------------------------------------------------------------------------

# Predict labels
predicted <- predict(model, test_array_x)
# Assign labels
predicted_labels <- max.col(t(predicted)) - 1
# Get accuracy
sum(diag(table(test[, 1], predicted_labels)))/length(test_y)
# Get Label Predictions
pred.label = max.col(t(predicted))-1
table(pred.label, test_y)