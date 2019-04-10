# -*- coding: utf-8 -*-
"""
Created on Tue Aug  7 21:06:44 2018

@author: Davis
"""

from keras.models import Sequential#starts the neural network
from keras.layers import Convolution2D#used for images because 2d is used for images
from keras.layers import MaxPooling2D
from keras.layers import Flatten
from keras.layers import Dense#used for fully connected layers
from keras.layers import Dropout

# Initialising the CNN
classifier = Sequential()

# Step 1 - Convolution
classifier.add(Convolution2D(32, 3, 3, input_shape = (64, 64, 3), activation = 'relu'))#32 = how many feature detector with a row x column 3,3 , input_shape 64,64 amount of pixels, the more you put eg 256,256 it will take longer, 3 = colours, this is the tensorflow format  
#to remove linearity and negative pixels values use relu in activation
# Step 2 - Pooling
classifier.add(MaxPooling2D(pool_size = (2, 2)))
#add another layer
classifier.add(Convolution2D(32,3,3,activation='relu'))
classifier.add(MaxPooling2D(pool_size = (2, 2)))

#add third layer
classifier.add(Convolution2D(32,3,3,activation='relu'))
classifier.add(MaxPooling2D(pool_size = (2, 2)))

# Step 3 - Flattening
classifier.add(Flatten())

# Step 4 - Full connection
classifier.add(Dense(output_dim = 128, activation = 'relu'))
classifier.add(Dropout(0.50))
classifier.add(Dense(output_dim = 1, activation = 'sigmoid'))

# Compiling the CNN
classifier.compile(optimizer = 'adam', loss = 'binary_crossentropy', metrics = ['accuracy'])



from keras.preprocessing.image import ImageDataGenerator 


train_datagen = ImageDataGenerator(rescale = 1./255,
                                   shear_range = 0.2,
                                   zoom_range = 0.2,
                                   horizontal_flip = True)

test_datagen = ImageDataGenerator(rescale = 1./255)

training_set = train_datagen.flow_from_directory('dataset/training_set',
                                                 target_size = (64, 64),
                                                 batch_size = 200,
                                                 class_mode = 'binary')

test_set = test_datagen.flow_from_directory('dataset/test_set',
                                            target_size = (64, 64),
                                            batch_size = 200,
                                            class_mode = 'binary')#you might want to chane



history = classifier.fit_generator(training_set,
                         steps_per_epoch=(120/5),# 5 = batch size it is how many samples it takes at a time which is 24= 120/5
                         nb_epoch = 5,#you can lower it
                         validation_data = test_set,
                         validation_steps=(40/5))# samples_per_epoch number of images in training set, nb_epoch how many rounds you want to test

print(history.history) # issue with getting the accuracy was that i didnt assign classifier.fit to history in order to get the graph information.
#120 images in the training set
#40 in the test set/validation set



#CREATE GRAPH FOR LOSS
import matplotlib.pyplot as plt

plt.plot(history.history['loss'],color ='red',linewidth =2.5)
plt.plot(history.history['val_loss'],color='green',linewidth=2.5)
plt.xlabel('Epoch/cycles')
plt.ylabel('Loss')
plt.title('Training vs  Test loss curve')
plt.legend(['Training Loss','Test Loss'],bbox_to_anchor=(1.01, 1), loc=2, borderaxespad=0.)#moves the legend to the right corner
plt.show()

#CREATE GRAPH FOR ACCURACY

plt.plot(history.history['acc'],color ='red',linewidth =2.5)
plt.plot(history.history['val_acc'],color='green',linewidth=2.5)
plt.xlabel('Epoch/cycles')
plt.ylabel('Accuracy')
plt.title('Training vs  Test  accuracy')
plt.legend(['Training accuracy','Test accuracy'],bbox_to_anchor=(1.01, 1), loc=2, borderaxespad=0.)#moves the legend to the right corner
plt.show()



# I saved the convulotion network which means that it keeps its what it has learned without having to run the whole batch job again
from keras.models import load_model
#classifier.save('my_model.h5') #this is to save the model
classifier = load_model('my_model.h5')# change the name to make it more smarter

#classifier.summary()
#param is calculated by doing (filter_height x filter_width x input_channel + 1) * number of filters
# the first layer = (3 x 3 x 3 + 1) * 32 = 896
#for the next layer  input channel becomes 32 which came from the number of filters from the last 
#3 x 3 x 32 + 1 *32(number of filters)
# Compiling the CNN
classifier.compile(optimizer = 'adam', loss = 'binary_crossentropy', metrics = ['accuracy'])



# make new predictions
import os
import numpy as np
from keras.preprocessing import image
img_width, img_height = 64, 64


file_path ='C:/Users/Davis/Desktop/practice_flask/images/'
file = os.listdir(file_path)[0]

img = image.load_img(file_path+file, target_size=(64, 64))
img =  image.img_to_array(img)
img = np.expand_dims(img, axis=0)
images= np.vstack([img])
predictions= classifier.predict(images,batch_size=2)
if predictions[0] == 1:
    
    answer = "cracked"
else:
      answer = "not cracked"


path, dirs, files = next(os.walk('dataset/pred/'))
num_files_count = len(files)#counts the amount of files image files that are in the pred
    
#using a while loop you can put multiple images in it this is more efficient than the for loop
#I added an if statement to this because 0 = cracks and 1 = no cracks in order for the user to know the label of each image
x=1 
while x <= num_files_count:# applies model on all files located within the file directory
    img = image.load_img('dataset/pred/cracks%s.jpg'%(x), target_size=(img_width, img_height))
    img =  image.img_to_array(img)
    img = np.expand_dims(img, axis=0)
    images= np.vstack([img])
    
    predictions= classifier.predict(images,batch_size=2)
    if predictions[0] == 1:
        print('%d.cracked'%(x))
    else:
         print('%d. not cracked'%(x))
 
    #print(predictions)
    x += 1
    
# add code after each classification propose possible solution

    
#NEXT IS TO CREATE THE GRAPHS THAT SHOWS THAT COMPARES THE TRAINING ACCURACY AND TEST ACCURACY
import pandas as pd
pixel = pd.DataFrame(image)