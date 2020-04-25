import data_extractor as de
import numpy as np
import tensorflow as tf
from tensorflow import keras

x_data = de.format_x_data("rcsb_pdb_protprot_seq")
y_data = np.array(de.format_y_data('prot-prot_complexes.xls'))

x_train, y_train = x_data[:1817], y_data[:1817]
x_test, y_test = x_data[1817:], y_data[1817:]

x_train, x_test = x_train / 25.0, x_test / 25.0

model = keras.Sequential([
	keras.layers.Flatten(input_shape=(10, 1000)),
	keras.layers.Dense(2000, activation="relu"),
	keras.layers.Dense(3, activation="softmax")
	])

model.compile(optimizer="adam", loss="sparse_categorical_crossentropy", metrics=["accuracy"])

model.fit(x_train, y_train, epochs=5)


test_loss, test_acc = model.evaluate(x_test, y_test)

print("Tested accuracy: ", test_acc)