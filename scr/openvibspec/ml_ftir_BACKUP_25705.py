from __future__ import absolute_import
###########################################
# ML and AI Procedures for FTIR/Raman Spectroscopy
#
#
#
###########################################
import h5py
import numpy as np 
#import scipy.io as sio 
import sklearn
import os
import pickle
import matplotlib.pyplot as plt
# python 2.7 from sklearn.cross_validation import train_test_split 
from sklearn.model_selection import train_test_split
plt.style.use('ggplot')
###########################################
import sys
import openvibspec.models

from pathlib import Path
MODELPATH = Path('openvibspec/models').absolute()



def randomforest_train(x,y,n_samples=1000, n_features=4,
                           n_informative=2, n_redundant=0,
                           random_state=0, shuffle=False,n_jobs=2, save_file_path=str()):
	"""

	"""
	
	from sklearn.ensemble import RandomForestClassifier
	from sklearn.datasets import make_classification
	
	clf = RandomForestClassifier(n_jobs=2, random_state=0)
	
	clf.fit(x, y)


	filename = save_file_path
	
	pickle.dump(clf, open(filename, 'wb'))
	
	return x,y ,clf


def randomforest_load_eval(x,clf):
	preds = clf.predict(x)
	
	return preds, clf

	return x

def kmeans(x, c=4):
	from sklearn.cluster import KMeans

	kmeans = KMeans(n_clusters=c)
	kmeans.fit(x)
	y = kmeans.predict(x)
	return y

def hca(x):
	return x

def pca(x,pc):
	from sklearn.decomposition import PCA
	
	pca = PCA(n_components=pc)
	
	pca.fit(x)
	
	p = pca.transform(x)
	
	return p



def pca_all(x,pc):
	"""
	
	"""
	from sklearn.decomposition import PCA
	
	pca = PCA(n_components=pc)
	
	pca.fit(x)
	
	p = pca.transform(x)
	
	
	vr = pca.explained_variance_ratio_
	
	print("Explained Variance based on N PCs =",vr)
	
	cov = pca.get_covariance()
	
	it  = pca.inverse_transform(p)	
	
	scores = pca.score_samples(x)
	
	return p, vr, cov, it, scores


	
def plot_pca(p):
	import matplotlib.pyplot as plt 
	
	plt.style.use('ggplot')
	
	plt.scatter(p[:,1],p[:,2], color=['r']);
	
	plt.scatter(p[:,0],p[:,1], color=['b']);
	
	plt.show()
	
	plt.plot(np.cumsum(vr))
	
	plt.xlabel('number of components')
	
	plt.ylabel('cumulative explained variance');
	
	plt.show()
	return

def plot_specs_by_class(x,classes_array,class2plot):
	class2plot = int()
	dat = x[np.where(g == class2plot)]
	plt.plot(dat.T)
	plt.show()
	return(dat)
####################################################################################################
####################################################################################################
# PRETRAINED DEEP NEURAL NETWORKS
####################################################################################################


class DeepLearn:
	
	
	"""
	Deep learning based procedures for the use in spectroscopy.

	Here you can find pretrained deep neural networks, which can be used for classification / RMieS-Correction, or further training.
	To ensure a smooth use of your data, the spectroscopic specifications of the used training data are shown below:
		
		Attributes of the raw data:

			- Spectroscopic data recording was performed on a Agilent Cary 620/670 FTIR Imaging System with 128x128 pixel MCT (Mercury Cadmium Telluride) and FPA for whole slide.
			- Data recording with 128 scans, results in a wavenumber range of 950 to 3700 cm^1.
			- With a spectral resolution of ca. 4 cm^1 this resulted in 1428 datapoints on the z-axis.
			- The pixel has a edge length of 5.65µm.
			- Per detector field this results in a FOV of ca. 715x715 µm^2.

		Data sources:
			Tissue was formaldehyde-fixed paraffin-embedded (FFPE) from human colon.
			- https://www.biomax.us/CO1002b
			- https://www.biomax.us/tissue-arrays/Colon/CO722
		
		You can find further information on data collection in: 

			[1] https://pubs.rsc.org/en/content/articlelanding/fd/2016/c5fd00157a#!divAbstract
#--------------------------------------------------------------------------------------------------------------------------------------------------------------------

	Components of the class are the following methods:

	DeepLearn.net()

		This method returns the basic structure of the used deep neural networks in form of a graph. 
		For further use, this structure was bound to the python interfaces of TensorFlow and Keras to allow a permanent integration in most modern workflows.
		It is currently divided into two main classes. First, the spectral classification and second the RMieS-correction of FTIR spectral data, using a fast deep learning algorithm.
		

		Specifications of the used training data:

			We used complete uncorrected FTIR data in the range of the fingerprint region between a wavenumber of 950 to 1800 cm^1.

			The groundtruth was based on the segmentation of the used random forest from [1]. 
			These in turn were created from a multi-step process of pre-segmentation of RMieS-corrected spectra and pathologist annotation. 

			With regard to the learning behaviour of the deep neuronal networks, it could be shown that no new classifier has to be built but 
			that the existing networks in transfer learning can be used for a variety of applications,  while the false positive number could be significantly reduced. [2]
			

			The data from groundtruth was processed under the following conditions:
				
				- Agilent Resolution Pro Software.
				- Fourier Transformation using Merz phase correction.
				- Blackman-Harris-4-term apodization and zero filling of 2.





		Specifications for own use:

			The spectral data must be available as 2d-numpy array which is structured as follows:

				x_data = x_axis*y_axis, z_axis 

				It is important for the application to observe the data points on the z-axis

				The classification ( dl.net(x_data,classify=True) ) of the individual RMieS-uncorrected spectra (semantic segmentation) is carried 
				out on the first 450 wavenumbers between 950 and 1800 cm^1.

				The correction ( dl.net(x_data, miecorr=True) ) of the raw data is done on the first 909 wavenumbers between 950 and 2300 cm^1.




		Examples:

			import openvibspec.ml_ftir as ovml

			dl = ovml.DeepLearn()
			
			x_pred, model = dl.net(x_data[:,:450],classify=True)

			x_corr, model = dl.net(x_data[:,:909], miecorr=True)

		Args:
			x_data(numpy array):
			
			classify=False(str): if True it uses the entered data (x_data) to predict previously learned 19 classes on uncorrected FTIR spectra of human colon tissue
			
			miecorr=False(str):  if True it uses the entered data (x_data) to predict the regression of the RMieS-Correction Function based on Bassan

		References:
			[2] Classification of (RMieS) uncorrected FTIR spectra with deep neural networks.
			https://academic.oup.com/bioinformatics/article-abstract/36/1/287/5521621
			
			[3] Deep neural networks for the correction of RMie Scattering in FTIR data.
			https://arxiv.org/abs/2002.07681	
#--------------------------------------------------------------------------------------------------------------------------------------------------------------------

	DeepLearn.transfer()

		The transfer function is based on using the data representations discovered by the existing networks for faster learning on new data. 
		For example, the networks trained on ffpe can be used to create classification networks for other tissues and their laboratory preparation with significantly less data. 
		For further informations regarding the theoretical part of this procedure, please see reference [2].

		Besides the spectral data a groundtruth as label is needed for the transfer learning.

		Models and weights are automatically saved in the working directory in *h5 and *json format using following naming convention:


			model_ptMLP_MieReg_%d-%m-%Y_%I-%M-%S_%p

		



		Examples:
			import openvibspec.ml_ftir as ovml

			dl = ovml.DeepLearn()

			dl.transfer(x_data[:5,:909],y_data, batch=10, train_epochs=10, miecorr=True, trainable=False)

			dl.transfer(x_data[:5,:909],x_data_corrected[:5,:909], batch=10, train_epochs=10, miecorr=True, trainable=False)
		
		Args:

			x_data(numpy array): 2D array shape(x_axis*y_axis, z_axis)  

			y_data(numpy array): label vector with classes assigned as numbers from 1 to n 

			batch(int): number of examples per batch

			train_epochs(int): number of iterations per training

			add_l(list of int()): possible list for adding layers

			classify=True(str): classification modus
			
			miecorr=True(str): regresssion modus

			trainable=False(str): if trainable=True: allows the adjustment of the already loaded weights from the pretrained networks 

#--------------------------------------------------------------------------------------------------------------------------------------------------------------------
	
	DeepLearn.load_and_predict()

		This function allows to load and use the trained network which was saved under DeepLearn.transfer()
	

		Examples:

				import openvibspec.ml_ftir as ovml
	
				dl = ovml.DeepLearn()
				
				a =  dl.load_and_predict(x_new_data[:,:450],'model_ptMLP_class_DATE_TIME')

		Args:

			x_new_data(numpy array): 2D array shape(x_axis*y_axis, z_axis)  
			
			model_ptMLP_class_DATE_TIME(str): model_ptMLP_MieReg_* or model_ptMLP_class_*

			
	"""

		

	def net(self,x,classify=False, miecorr=False, predict=False,train=False ,show=False):
		import keras
		from keras.layers import Input, Dense
		from keras.optimizers import RMSprop, Adam, SGD
		from keras.models import model_from_json
		from keras.callbacks import ModelCheckpoint

		####################################################################################################
		#	DETERMINE WICH MODEL PARAMETERS YOUN WNAT TO USE
		#		CLASSIFY == TRUE GIVES THE MODEL TRAINED TO CLASSIFY ALL CELLUAR COMPONENTS BASED ON SPECTRA
		#					BETWEEN 950-1800 WVN 
		#	
		#		MIECORR == TRUE GIVES THE CORRESPONDING NEURAL NETWORK FOR PERFORMING EFFICIENT RMIE-CORRECTION
		#				   ON FFPE-BASED TISSUE SPECTRA
		#	
		####################################################################################################

		if classify == True:

			if x.shape[1] != 450:
			
				raise ValueError('This is a classification problem: Your spectral data needs 450 datapoints in WVN range of 950-1800 1/cm')
			
			json_file = open(os.path.join(str(MODELPATH)+'/model_weights_classification.json'), 'r')

			loaded_model_json = json_file.read()

			loaded_model = model_from_json(loaded_model_json)
			
			if show == True:
				print(loaded_model.summary())
			
			loaded_model.load_weights(os.path.join(str(MODELPATH)+"/model_weights_classification.best.hdf5"))
			
			print("Loaded model from disk")
			
			model = loaded_model.compile(loss='categorical_crossentropy', optimizer='rmsprop', metrics=['accuracy'])

			from sklearn.preprocessing import normalize
			

			trX = normalize(x, axis=1, norm='l2')

			return loaded_model.predict(trX), load_model

		if miecorr == True:

			if x.shape[1] != 450:
			
				raise ValueError('This is a regression problem: Your spectral data needs 909 datapoints in WVN range of 950-2300 1/cm')
			####################################################################################################
			#	THIS MODEL NEEDS THE FIRST 909 WVN. RANGE FROM 950-2300 WVN 1/cm
			#	
			#	
			#	
			####################################################################################################x

			json_file = open(os.path.join(str(MODELPATH)+'/model_weights_regression.json'), 'r')
			
			loaded_model_json = json_file.read()

			loaded_model = model_from_json(loaded_model_json)
			
			if show == True:
				print(loaded_model.summary())
			
			loaded_model.load_weights(os.path.join(str(MODELPATH)+"/model_weights_regression.best.hdf5"))
			
			print("Loaded model from disk")
			
			loaded_model.compile(loss='mean_squared_error', optimizer='adam')


			
		
			return loaded_model.predict(x), load_model

	
	def transfer(self,x, y, batch,train_epochs,add_l=[], classify=False, miecorr=False, trainable=False ):
		import keras
		from keras.models import Model
		from keras.optimizers import RMSprop, Adam, SGD
		from keras.models import model_from_json
		from keras.callbacks import ModelCheckpoint
		from keras.models import Sequential
		from datetime import datetime
<<<<<<< HEAD
		from sklearn.preprocessing import normalize
			

		"""
ALL PARTS OF THE TRANSFER-LEARNING NETWORKS ON FTIR SPECTROSCOPIC DATA

		"""
		trX = normalize(x, axis=1, norm='l2')
=======
		
		#	ALL PARTS OF THE TRANSFER-LEARNING NETWORKS ON FTIR SPECTROSCOPIC DATA

		
	
>>>>>>> 394dcd7595fe01d01e7aa6587a9922346b64b830
		def onehot(y):
			import keras
			from keras.utils import np_utils

			c = np.max(y) + 1
			
			y1hot = np_utils.to_categorical(y, num_classes=c)
			
			return(y1hot)

		def add_layer():
			from keras.utils import np_utils
			from keras.layers import Input, Dense 
			from keras.models import Model
			from keras import models

			yoh = onehot(y)

			sm = int(yoh.shape[1])
			
			print("training on",sm,"classes")
			json_file = open(os.path.join(str(MODELPATH)+'/model_weights_classification.json'), 'r')
			
			loaded_model_json = json_file.read()
			
			loaded_model = model_from_json(loaded_model_json)
			
			loaded_model.load_weights(os.path.join(str(MODELPATH)+"/model_weights_classification.best.hdf5"))
			
			
			
			if trainable == False:
				for layer in loaded_model.layers:
					layer.trainable = False
			else: 
				for layer in loaded_model.layers:
					layer.trainable = True
			
			
			
			if not add_l:
				preds = Dense(sm, name='newlast', activation='softmax')(loaded_model.layers[-3].output)

				model = Model(inputs=loaded_model.input, outputs=preds)

				model.compile(loss='categorical_crossentropy', optimizer='rmsprop', metrics=['accuracy'])

				history = model.fit(trX,yoh,batch_size=batch,epochs=train_epochs )

				print(model.summary())

			if add_l:
				
				
				def add_2_model(add_l):
					
					base = Model(inputs=loaded_model.input, outputs=loaded_model.layers[-3].output)
					
					model = Sequential()
					model.add(base)
					model.add(Dense(add_l[0], input_dim=450,activation='relu'))

					for layer_size in add_l[1:]:
						model.add(Dense(layer_size,activation='relu'))
					

					model.add(Dense(sm,activation='softmax'))

					return model

				model = add_2_model(add_l)
				
				model.compile(loss='categorical_crossentropy', optimizer='rmsprop', metrics=['accuracy'])
				
				history = model.fit(trX,yoh,batch_size=batch,epochs=train_epochs )
				
				print(model.summary())


			dtstr = datetime.now().strftime("%d-%m-%Y_%I-%M-%S_%p")
			
			model_json = model.to_json()
			
			with open("model_ptMLP_class_"+dtstr+".json", "w") as json_file:
				json_file.write(model_json)

			model.save_weights("model_ptMLP_class_"+dtstr+".h5")

			print("Saved model to disk to","model_ptMLP_class_"+dtstr+".json")
			print("and weights to")
			print("Saved model to disk to","model_ptMLP_class_"+dtstr+".h5")






			###########################PLOTTING##########################
			history_dict = history.history
			
			history_dict.keys()
			
			a = np.array(history_dict['acc'])
			
			print(a.shape)
			
			l = np.array(history_dict['loss'])
			
			e = range(1, len(a) +1)
			
			plt.plot(e, a, 'bo',color='red', label='Acc Training')
			
			plt.plot(e, l, 'b', label='Loss Training')
			
			plt.xlabel('Epochs')
			
			plt.legend()
			
			plt.savefig('model.pdf')
			
			
			return(model, history_dict)
		


		def simple_val_of_data(x,y):
			from sklearn.model_selection import train_test_split
			from random import randrange
			from sklearn.preprocessing import normalize

			trX = normalize(x, axis=1, norm='l2')
			
			seed = randrange(999)
			
			print('used random seed was', seed)
			
			x_train, x_test, y_train, y_test = train_test_split(trX, y, test_size=0.4,random_state=seed)
			
			return x_train, x_test, y_train, y_test

		def train_layer():
			from keras.utils import np_utils
			from keras.layers import Input, Dense 
			from keras.models import Model
			from keras import models
			
			sm = int(y.shape[1])
			
			
			json_filer = open(os.path.join(str(MODELPATH)+'/model_weights_regression.json'), 'r')
			
			loaded_model_jsonr = json_filer.read()
			
			loaded_modelr = model_from_json(loaded_model_jsonr)
			
			loaded_modelr.load_weights(os.path.join(str(MODELPATH)+"/model_weights_regression.best.hdf5"))
			
			
			
			if trainable == False:
				for layer in loaded_modelr.layers:
					layer.trainable = False
			else: 
				for layer in loaded_modelr.layers:
					layer.trainable = True
			
			loaded_modelr.compile(loss='mean_squared_error', optimizer='adam')
			
			history = loaded_modelr.fit(x,y, batch_size=batch, epochs=train_epochs )

			dtstr = datetime.now().strftime("%d-%m-%Y_%I-%M-%S_%p")
			
			print(loaded_modelr.summary())
			
			model_json = loaded_modelr.to_json()
			with open("model_ptMLP_MieReg_"+dtstr+".json", "w") as json_file:
				json_file.write(model_json)
			
			loaded_modelr.save_weights("model_ptMLP_MieReg_"+dtstr+".h5")
			
			print("Saved model to disk to","model_ptMLP_MieReg_"+dtstr+".json")
			print("and weights to")
			print("Saved model to disk to","model_ptMLP_MieReg_"+dtstr+".h5")
			
			return

		if classify == True:
			if x.shape[1] != 450:
				raise ValueError('This is a classification problem: x needs to be 450 datapoints in WVN range of 950-1800 1/cm')

			mod, h  = add_layer()

		
		if miecorr == True:
			if y.shape[1] != x.shape[1]:
				raise ValueError('This is a regression problem: x and y need 909 datapoints in WVN range of 950-2300 1/cm')

		
			train_layer()


	def load_and_predict(self, x, modelname, save=False):
		import keras
		from keras.models import Model
		from keras.optimizers import RMSprop, Adam, SGD
		from keras.models import model_from_json
		from keras.callbacks import ModelCheckpoint
		from keras.models import Sequential
		from datetime import datetime
		
		json_file = open(str(modelname)+'.json', 'r')
		print(str(modelname)+'.json' ) 
		loaded_model_json = json_file.read()
		
		loaded_model = model_from_json(loaded_model_json)
		
		loaded_model.load_weights(str(modelname)+".h5") 
		
		print("Loaded model from disk")
		
		model = loaded_model.compile(loss='categorical_crossentropy', optimizer='rmsprop', metrics=['accuracy'])
		if save == True:

			np.save(str(modelname)+'_prediction.npy',loaded_model.predict(x))
		
		else:
			return loaded_model.predict(x)

#--------------------------------------------------
#--------------------------------------------------
# LOAD AND SAVE MODELS SKLEARN
#--------------------------------------------------
#--------------------------------------------------
def save_model(model, name='model', timestamp=None):
	from  sklearn.externals import joblib
	import datetime
	st = datetime.datetime.fromtimestamp(ts).strftime('%Y_%m_%d_%H:%M:%S')
	
	if timestamp == True:
		joblib.dump(model, name+st)
	else:
		joblib.dump(model, name)
	
	return

def load_model(model):
	from  sklearn.externals import joblib
	m = joblib.load(model)
	return(m)