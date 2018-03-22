########################################################################
# Load in the model and apply to the test data
#
# Author:   Michael Nguyen
# Email:    mn2769@columbia.edu
# Date:     3/20/18
########################################################################

import sys
import numpy as np
import matplotlib.pyplot as plt
import random

# ML
from keras.models import Model, load_model
import tensorflow as tf

# Custom scripts
sys.path.insert(0, '../util')
import convert as con
import unet_tools as tool
from unet_tools import mean_iou

########################################################################
# Global Constants
########################################################################
MODEL_PATH = 'model-dsbowl2018-1-no-erosion.h5'
# MODEL_PATH = 'model-dsbowl2018-1.h5'
TEST_PATH = '../../data/stage1_test/'
TRAIN_PATH = '../../data/stage1_train/'
TRUTH_PATH = '../../data/stage1_train/stage1_train_labels.csv'
IMG_WIDTH = 128
IMG_HEIGHT = 128
IMG_CHANNELS = 3
NUM_VISUAL = 5

if __name__ == '__main__':

	x_test = tool.process_testing(TEST_PATH, 
		IMG_HEIGHT, 
		IMG_WIDTH, 
		IMG_CHANNELS)

	x_train, y_train = tool.process_training(TRAIN_PATH, 
		TRUTH_PATH, 
		False,
		IMG_HEIGHT, 
		IMG_WIDTH, 
		IMG_CHANNELS)

	# Predict on train, val and test
	model = load_model(MODEL_PATH, custom_objects={'mean_iou': mean_iou})
	preds_train = model.predict(x_train[:int(x_train.shape[0])], verbose=1)
	preds_test = model.predict(x_test, verbose=1)

	# Threshold predictions
	preds_train_t = (preds_train > 0.5).astype(np.uint8)
	preds_test_t = (preds_test > 0.5).astype(np.uint8)


	# Visualize some results
	fig, ax = plt.subplots(NUM_VISUAL,3)
	ind_train = np.random.randint(0, high=x_train.shape[0], size=NUM_VISUAL)
	ind_test = np.random.randint(0, high=x_test.shape[0], size=NUM_VISUAL)

	for k in range( int(NUM_VISUAL) ):
		ind1 = ind_train[k]
		ind2 = ind_test[k]

		if k == 0:
			ax[k][0].set_title('Training Image with Truth Mask')
		ax[k][0].imshow( x_train[ind1], cmap='gray' )
		ax[k][0].imshow( np.squeeze(y_train[ind1]), alpha=0.5)

		if k == 0:
			ax[k][1].set_title('Training Image with Predicted Mask')
		ax[k][1].imshow( x_train[ind1], cmap='gray' )
		ax[k][1].imshow( np.squeeze(preds_train_t[ind1]), alpha=0.5)

		if k == 0:
			ax[k][2].set_title('Test Image with Predicted Mask')
		ax[k][2].imshow( x_test[ind2], cmap='gray' )
		ax[k][2].imshow( np.squeeze(preds_test_t[ind2]), alpha=0.5)

	plt.show()