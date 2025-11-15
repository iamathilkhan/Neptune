from matplotlib import scale
import tensorflow as tf
from keras.models import Sequential
from keras.layers import Dense, Input
import pandas as pd
from sklearn.preprocessing import StandardScaler

ds = pd.read_csv('neptune_ocean_dataset.csv')

filter = ['water_temperature_celsius', 'temperature_drop_celsius', 'rainfall_mm', 'barometric_pressure_mb', 'month']

x = ds[filter]
y = ds['fishing_opportunity']

scalar = StandardScaler()
X = scalar.fit_transform(x)

input = Input(shape=(5,))

model = Sequential()
model.add(input)
model.add(Dense(16, activation='relu'))
model.add(Dense(32, activation='relu'))
model.add(Dense(1, activation='sigmoid'))

model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])
model.fit(X, y, epochs=20, validation_split=0.2, batch_size=20)

model.save('fish.h5')
print('Fishing model ready ✅')

filter_d = ['water_temperature_celsius', 'temperature_drop_celsius', 'rainfall_mm','skin_ice_temperature_celsius']

xd = ds[filter_d]
yd = ds['disaster_risk']

Xd = scalar.fit_transform(xd)

model_d = Sequential()
model_d.add(Input(shape=(4,)))
model_d.add(Dense(16, activation='relu'))
model_d.add(Dense(32, activation='relu'))
model_d.add(Dense(1, activation='sigmoid'))

model_d.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])
model_d.fit(Xd, yd, batch_size=20, epochs=30, validation_split=0.2)

model_d.save('disaster.h5')
print('Disaster model ready ✅')