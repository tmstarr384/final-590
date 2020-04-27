import lbs_data_extractor as de
import numpy as np
import tensorflow as tf
from tensorflow import keras

'''
Resource:
https://machinelearningmastery.com/how-to-choose-loss-functions-when-training-deep-learning-neural-networks/
'''

x_data , y_data = de.get_data('pisite.flat.all\\all')

num_instances = len(x_data)

x_data = np.array(x_data)
y_data = y_data

train_test_cutoff = int(0.7*num_instances)
x_train, y_train = x_data[:train_test_cutoff], {y: y_data[y][:train_test_cutoff] for y in y_data}
x_test, y_test = x_data[train_test_cutoff:], {y: y_data[y][train_test_cutoff:] for y in y_data}

x_train, x_test = x_train / 25.0, x_test / 25.0
print('Building model...')
def build_branch(inputs, numCategories, name, finalAct="softmax"):
	x = inputs
	x = keras.layers.Flatten()(x)
	x = keras.layers.Dense(int(0.2 * x_data.shape[1] * x_data.shape[2]))(x)
	x = keras.layers.Activation("relu")(x)
	x = keras.layers.Dense(numCategories)(x)
	x = keras.layers.Activation(finalAct,name=name)(x)
	return x

# model = keras.Sequential([
# 	keras.layers.Flatten(input_shape=(x_data.shape[1], x_data.shape[2])),
# 	keras.layers.Dense(int(0.2 * x_data.shape[1] * x_data.shape[2]), activation="relu"),
# 	keras.layers.Dense(y_data.shape[1], activation="linear")
# 	])

print('Building model...')
inputs = keras.layers.Input(shape=(x_data.shape[1], x_data.shape[2]))

print('Building model...')
model = keras.models.Model(
	inputs=inputs,
	outputs=[build_branch(inputs, 2, "act_" + str(i)) for i in range(2000)])
print('Model built')

model.compile(loss='sparse_categorical_crossentropy', metrics=['accuracy'])

model.fit(x_train, y_train, epochs=5)

test_loss, test_acc = model.evaluate(x_test, y_test)

print("Tested accuracy: ", test_acc)
print(model.summary())