# -*- coding: utf-8 -*-
"""Sammy Levy - Intro to ML Lab

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1WPf4Uq6qLeLhqkaamYDdM3ynA_ZGKG8D

# Lab 4

In Lab 4, we will be coding Linear and Logistic regression using only Numpy! You will also be asked to use what you know about gradient descent to tweak the algorithms for better results. While teams should collaborate and help each other, each member of a group should complete their own code.

This skeleton is intended to be somewhat sparse in order to give you the opportunity to become familiar with the intuition behind gradient descent and to make you very familiar with Numpy. Please reach out to us for any conceptual/mathematical questions or if you are stuck on something and need a hint - we don't want you spending hours on this!

If you are unfamiliar with Numpy, don't worry! There are a ton of great resources on it and the its documentation is very well-written (*cough cough* OpenCV). You can figure our how to do most things with a simple Google Search, but here are some functions, operators, etc. that I found useful in this lab:

    .dot() and @, .astype(), .T, unique(), mean(), sum(), inv(), pinv(), reshape(), vstack(), hstack(), .unique(), .concatenate(), .shape(), .any()

### Some notes on using Colab

If you've never used Colab before, this section is for you! Some things to note:

* The different boxes in this document are segments of Python code. Many of them contain errors and won't work if you try to run them right away (using the play button on the left). You need to fill in the blanks to make them work!

* If you update a block of code, even if you re-run it, you must also re-run all the blocks after it up to the point where you're currently working. They don't run themselves!
"""

import numpy as np
import csv
from numpy.core.memmap import dtype
import matplotlib.pyplot as plt

# You may use these sklearn tools in your implementation, but no others.
from sklearn.model_selection import train_test_split
from sklearn.utils import shuffle

from google.colab import drive
drive.mount('/content/drive')

WEATHER_PATH = "/content/drive/MyDrive/Colab Notebooks/Pocket Racers Lab 4/weatherHistory.csv"
data = np.loadtxt(WEATHER_PATH, delimiter=",", dtype=str)

# remove first and last columns
data = data[:,1:-1]


header = data[0]


data = data[1:]

"""##Part 1: Single line fit!

In this part of the lab, you will be using only the humidity data to estimate the temperature using linear regression. Then we well compare the results of a single feature linear regression with the closed form solution. Experiment with the learning rate and number of itterations and try to find the optimal learning rate for 40 itterations (we got it to 59.5).
"""

# Right now, the data is in one large matrix. Seperate out x as the humidity
# and y as the temperature.


# data[row slice, column slice] 

# get 5th column, all rows
x = data[:,4]

# get 3rd column, all rows
y = data[:,2]

x = x.astype('float')
y = y.astype('float')

# Code the mean squared error function given x, y, a, and b.
def MSE(x, y, a, b):
    mse = 0
    for i in range(len(x)):
        predicted = a*x[i] + b
        mse += (y[i] - predicted)**2
    return mse / len(x)

# Code the gradient descent function. This will return the new values of a and b
# after the gradient has been calculated and the learning rate has been applied.
def grad_des(x, y, a, b, lr):
  m = float(len(x))

  for i in range(len(x)):
    y_pred = a*x[i] + b
    a = a - lr * (-2/m) * (y[i] - y_pred) * x[i]
    b = b - lr * (-2/m) * (y[i] - y_pred)


  return a, b

# Initialize a and b.
a = 0
b = 0
lr = 5

losses = []
for i in range(40):
  losses.append(MSE(x, y, a, b))
  # Update a and b using the values from your gradient descent function.
  a, b = grad_des(x, y, a, b, lr)

print(f"Final Training Loss: {losses[-1]}")
plt.plot(losses)
plt.title("single feature loss over time")

"""This is your **loss graph**. Hang onto it, because you'll need it later for the checkoff.

In addition, remember what we taught you guys about how your training should improve the loss: it should decay towards a minimum as the gradient descent iterations continue. Pay attention to the y-axis here, which indicates the loss. If your error blows up towards infinity or doesn't decrease very quickly, you should be able to recognize and rectify the issue with your hyperparameters!
"""

# Let's take a look at what our line of best fit looks like!
plt.scatter(x, y)
plt.plot(x, a*x+b, color='orange')

# Now let's find the true optimal solution using the closed form equation. Use
# np.polyfit or other such functions only to check your work.
# Don't forget what you need to add to the X matrix in order for the closed form
# to work!

# fit first-degree polynomial to data points x and y
th = np.polyfit(x, y, 1)

# extract coefficients
a1, b1 = th

# Compare our closed form with our gradient descent. The closed form solution
# should be the same thing as the result of polyfit.

a2, b2 = np.polyfit(x, y, 1)
print(f"Grad Desc:   a: {a} b: {b} MSE: {MSE(x, y, a, b)}")
print(f"Closed form: a: {a1} b: {b1} MSE: {MSE(x, y, a1, b1)}")
print(f"Poly Fit:    a: {a2} b: {b2}")

plt.scatter(x, y)
plt.plot(x, a*x+b, color='orange')
plt.plot(x, a1*x+b1, color='yellow')
plt.title("closed and gd best fit lines")

"""To get checked off for this part, show us you:
- loss graph
- the graph with your 2 best fit lines
- the final MSE for your gradient descent and closed form solutions
- your grad_des function

##Part 2: Multiple input features

In this part we will modify our gradient descent function to accept all of the possible input features. This will require converting the precipitation type and weather summaries to one-hot encodings (see slides 20-25 and 33). Then we will have to change our equations to be in matrix notation.
"""

# First, lets get our x and y data one-hot encoded.
# hot_X should be the data where the categorical fields are converted into
#     one-hot encodings (temperature data excluded). 
# As a sanity check, the dimensions should be (96453, 38).
# hot_y should still just be the temperature data.
def encode_onehot(array):
  # return a sorted unique array, along with the 
  # indices to reconstruct the original array
  unique, inverse = np.unique(array, return_inverse=True)

  # create an identity matrix, and uses the inverse array to index into the
  # identity matrix and return a one-hot encoded version of the input array
  onehot = np.eye(unique.shape[0])[inverse]
  return onehot

# one-hot encode summary and precip
summary_onehot = encode_onehot(data[:, 0])
precip_onehot = encode_onehot(data[:, 1])

bias = np.ones((len(data[:, 2:]), 1))
# concatenate the one-hot encoded data with the rest of the data array
hot_X = np.c_[summary_onehot, precip_onehot, data[:, 3:], np.ones((len(data), 1))].astype(float)

print(f"Dimensions: {len(hot_X[0])} columns, {len(hot_X)} rows")


hot_y = y.astype(float)
hot_y = hot_y.reshape(-1, 1)

print(f"hot_y has {len(hot_y)} elements")

print(hot_y.shape)

"""Now update your gradient descent and Mean Squared Error function to be able to learn from multiple features. See how low you can get the error after 40 iterations.

You may notice a higher error than we got in part 1, especially when compared with an extrememly low closed form error. Think about why this may be the case and what hyperparameters you can tune to improve this.
"""

def grad_des2(X, y, theta, learning_rate):
  y = y.reshape(-1, 1)
  dt = x.T @ (y - X@theta) / len(X) * -1
  return theta - learning_rate * dt
  # grad_L = 1 / y.shape[0] * (-2 * X.T @ y + 2 * X.T @ X @ theta)
  # return theta - learning_rate * grad_L

def MSE2(X, y, theta):
  yhat = X @ theta
  yhat.reshape(-1, 1)
  return np.mean((y - yhat) ** 2)
  # error = 1 / y.shape[0] * (y - X @ theta).T @ (y - X @ theta)

theta = np.zeros((len(hot_X[0]), 1))
MSE2(hot_X, hot_y, theta)

# lr = 1

# theta = np.zeros((len(hot_X[0]), 1))

# losses = []
# losses.append(MSE2(hot_X, hot_y, theta))

# for i in range(40):
#   gradient = grad_des2(hot_X, hot_y, theta, lr)
#   theta = theta - lr * gradient
#   losses.append(MSE2(hot_X, hot_y, theta))
  

# print(f"Final Training Loss: {losses[-1]}")
# plt.plot(losses)
# plt.title("Multi feature loss over time")

learning_rate = 0.0004

theta = np.zeros((len(hot_X[0]), 1))

losses = []
losses.append(MSE2(hot_X, hot_y, theta))

for i in range(40):
  theta = grad_des2(hot_X, hot_y, theta, learning_rate)
  losses.append(MSE2(hot_X, hot_y, theta))
  

print(f"Final Training Loss: {losses[-1]}")
plt.plot(losses)
plt.title("Multi feature loss over time")

# Now solve for theta using the closed form and compare your final training loss between
# the closed form and regression solution

th2 = np.linalg.pinv(hot_X.T @ hot_X) @ (hot_X.T @ hot_y)

closed_form_loss = MSE2(hot_X, hot_y, th2)

print(f"Final Training Loss (Gradient Descent): {losses[-1]}")
print(f"Final Training Loss (Closed Form): {closed_form_loss}")

"""As you can (probably) see, the gradient descent error is worse than the single input version and much worse than the closed form solution. Think about why this is and how can improve it (hint: we talked about this technique in our lecture). Copy your code above into the cell below to make any modifications to improve your gradient descent!"""

def grad_des_batch(X, y, theta, learning_rate, batch_size):
    """
    Compute gradient descent update with batching
    """
    y = y.reshape(-1, 1)
    num_samples = X.shape[0]
    num_batches = num_samples // batch_size

    # loop over each batch
    for i in range(num_batches):
        # get the start and end indices of the current batch
        start = i * batch_size
        end = (i + 1) * batch_size
        
        # extract the features and targets for the current batch
        X_batch = X[start:end]
        y_batch = y[start:end]

        # compute the gradient for the current batch
        dt = X_batch.T @ (y_batch - X_batch @ theta) / len(X_batch) * -1
        
        # update the parameters using the gradient
        theta = theta - learning_rate * dt

    return theta

# set the learning rate
lr = 9e-7

# set the batch size
batch_size = 32

# set theta to array of zeroes
theta = np.zeros((len(hot_X[0]), 1))

# initialize an empty list to store the losses
losses = []

# append the initial loss to the list
losses.append(MSE2(hot_X, hot_y, theta))

# loop 40 times
for i in range(40):
    # update the parameters using batch gradient descent
    theta = grad_des_batch(hot_X, hot_y, theta, lr, batch_size)

    # append the current loss to the list
    losses.append(MSE2(hot_X, hot_y, theta))
  
# print the final training loss
print(f"Final Training Loss: {losses[-1]}")

# plot the losses over time
plt.plot(losses)
plt.title("Modified multi feature loss over time")

"""To get checked off for this part, show us:
- both of you loss graphs
- closed form error
- your code for both GD algorithms
- an explanation of what you changed and why

##Part 3: Logistic Regression and K-fold Cross Validation

In this part of the lab you will be esimating if someone will suffer a heart attack in the next 10 years based on health statistics. This time, we will be using K-fold cross validation to determine the viability of our model. In lecture, we did not give you the full equation for logistic regression, I suggest deriving it before starting that part of the lab. Try to do it yourself! (The answer should be **simple** - if you are coding a disgusting equation, that is wrong and you should stop.)
"""

HAM_PATH = "/content/drive/MyDrive/Colab Notebooks/Pocket Racers Lab 4/framingham.csv"
health_data = np.loadtxt(HAM_PATH, delimiter=",", dtype=str)

# But wait! The data is not complete! Take a look to see what is wrong with it
# and remove any offending datapoints (rows) - this is the "cleaning" stage of
# the ML pipeline.
# Challenge: do this in one line.
# for h in health_data_dirty:
#   if "NA" not in h:
#     health_data = np.append(health_data, h)

health_data = np.array([x for x in health_data if 'NA' not in x])

print(health_data)

# Create your X and Y data and clean it! Binarize the assigned-sex-at-birth
# column and add the bias term to your X data

health_x = health_data[1:,1:-1]

health_y = health_data[1:,-1]

# Binarize the assigned-sex-at-birth column

# gender_column = health_data[1:, 0]
# binary_gender_column = [1 if gender == '1' else 0 for gender in gender_column]

# Add bias

bias_column = np.ones((len(health_x), 1))
health_x = np.concatenate((bias_column, health_x), axis = 1)

# Clean the data

health_x = health_x.astype('double')
health_y = health_y.astype('double')

# # Separate your training data into 5 folds for cross validation

# X_train, X_test, y_train, y_test = train_test_split(health_x, health_y, test_size=0.2, random_state=0)
# X_train, y_train = shuffle(X_train, y_train)
# k = 5

# X_folds = []
# y_folds = []


# # A quick check:
# for fold in range(k):
#   print(X_folds[fold].shape)
#   print(y_folds[fold].shape)

# Separate your training data into 5 folds for cross validation

X_train, X_test, y_train, y_test = train_test_split(health_x, health_y, test_size=0.2, random_state=0)
X_train, y_train = shuffle(X_train, y_train)
k = 5

X_folds = np.array_split(X_train, k)
y_folds = np.array_split(y_train, k)

# A quick check:
for fold in range(k):
  print(X_folds[fold].shape)
  print(y_folds[fold].shape)

# # Now lets code all of our relevant equations.

# def sigmoid(x):
#   pass

# def accuracy(X, y, theta): 
#   #this is just correct/total
#   pass

# def cross_entropy_loss(X, y, theta):
#     pass

# def log_grad_desc(X, y_hat, y):
#   pass

# Now lets code all of our relevant equations.

def sigmoid(x):
  return 1/(1 + np.exp(-x))

def accuracy(X, y, theta):
  #this is just correct/total
  pred = sigmoid(np.dot(X, theta))
  pred[pred >= 0.5] = 1
  pred[pred < 0.5] = 0
  return np.mean(pred == y)

def cross_entropy_loss(X, y, theta):
    pred = sigmoid(np.dot(X, theta))
    return -1 * np.mean(y * np.log(pred) + (1 - y) * np.log(1 - pred))

def log_grad_desc(X, y_hat, y):
  return np.dot(X.T, y_hat - y)

# # Now lets validate our model. Use the validation error to tune your
# #hyperparameters. Also, compare your validation and training errors

# lr = # Set learning rate

# val_losses = []
# train_losses = []
# for fold in range(k):
#   theta = np.random.randn(health_x.shape[1]) # Reinitialize theta

#   # Set your validation and training datasets
#   X_val = 
#   y_val = 
#   X_train = 
#   y_train = 
#   for i in range(5000):
#     # Do gradient descent
#     pass
#   val_losses.append(cross_entropy_loss(X_val, y_val, theta))
#   train_losses.append(cross_entropy_loss(X_train, y_train, theta))


# print(f"train_losses: {sum(train_losses)/len(train_losses)}")
# print(f"val_losses: {sum(val_losses)/len(val_losses)}")



# Now lets validate our model. Use the validation error to tune your
#hyperparameters. Also, compare your validation and training errors

lr = 5e-7

val_losses = []
train_losses = []
for fold in range(k):
  theta = np.random.randn(health_x.shape[1]) # Reinitialize theta

  # Set your validation and training datasets
  X_val = X_folds[fold]
  y_val = y_folds[fold]
  X_train = np.concatenate([X_folds[i] for i in range(k) if i != fold], axis=0)
  y_train = np.concatenate([y_folds[i] for i in range(k) if i != fold], axis=0)
  for i in range(5000):
    # Do gradient descent
    grad = log_grad_desc(X_train, sigmoid(np.dot(X_train, theta)), y_train)
    theta = theta - lr * grad
  val_losses.append(cross_entropy_loss(X_val, y_val, theta))
  train_losses.append(cross_entropy_loss(X_train, y_train, theta))

print(f"train_losses: {sum(train_losses)/len(train_losses)}")
print(f"val_losses: {sum(val_losses)/len(val_losses)}")

# # Training - once you have tuned your hyperparameters, train your model once
# # more on all the training data and then test it on the test dataset

# lr = 
# theta = np.random.randn(car_x.shape[1])

# for i in range(5000):
#   #Gradient Descent
#   pass

# print(f"Testing Accuracy: {accuracy(X_test, y_test, theta)}")


theta = np.random.randn(health_x.shape[1])

for i in range(5000):
  # Gradient Descent
  grad = log_grad_desc(X_train, sigmoid(np.dot(X_train, theta)), y_train)
  theta = theta - lr * grad

print(f"Testing Accuracy: {accuracy(X_test, y_test, theta)}")

"""To be checked off for this part, show us your code for gradient descent and the resulting outputs and losses."""
