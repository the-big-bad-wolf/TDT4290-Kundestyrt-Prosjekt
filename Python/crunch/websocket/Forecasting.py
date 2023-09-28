import numpy as np
import matplotlib.pyplot as plt
import tensorflow as tf
from sklearn.preprocessing import MinMaxScaler

# 1. Generate a more stable synthetic time series with a mid-way spike
time = np.arange(0, 4000)
seasonality = 10 * np.sin(0.1 * time)
noise = np.random.normal(0, 2, len(time))
spike = 60 * np.exp(-(((time - 2000) / 300) ** 2))  # Gaussian spike centered at t=2000
synthetic_data = seasonality + noise + spike

# 1.5 Establish a reference average from the first 1,000 data points
reference_avg = np.mean(synthetic_data[:1000])


# 2. Create sequences of data
SEQUENCE_LENGTH = 90
X = []
y = []

for i in range(len(synthetic_data) - SEQUENCE_LENGTH):
    X.append(synthetic_data[i : i + SEQUENCE_LENGTH])
    y.append(synthetic_data[i + SEQUENCE_LENGTH])

X = np.array(X)
y = np.array(y)
X = np.reshape(X, (X.shape[0], X.shape[1], 1))

# 3. Split data into training and testing sets
split_point = int(0.8 * len(X))
X_train = X[:split_point]
y_train = y[:split_point]
X_test = X[split_point:]
y_test = y[split_point:]

# 4. Scale the data
scaler = MinMaxScaler()
X_train_scaled = scaler.fit_transform(X_train.reshape(-1, 1)).reshape(X_train.shape)
X_test_scaled = scaler.transform(X_test.reshape(-1, 1)).reshape(X_test.shape)
y_train_scaled = scaler.fit_transform(y_train.reshape(-1, 1))
y_test_scaled = scaler.transform(y_test.reshape(-1, 1))

# 5. Update the LSTM model
model = tf.keras.models.Sequential()
model.add(
    tf.keras.layers.LSTM(
        100,
        input_shape=(X_train_scaled.shape[1], X_train_scaled.shape[2]),
        return_sequences=True,
    )
)
model.add(tf.keras.layers.Dropout(0.2))
model.add(tf.keras.layers.LSTM(100))
model.add(tf.keras.layers.Dropout(0.2))
model.add(tf.keras.layers.Dense(1))
model.compile(optimizer=tf.keras.optimizers.Adam(learning_rate=0.001), loss="mse")

# 6. Train the model
model.fit(
    X_train_scaled, y_train_scaled, epochs=100, batch_size=32, validation_split=0.2
)

# 7. Predictions
predictions_scaled = model.predict(X_test_scaled)

# 8. Transform predictions back to original scale
predictions = scaler.inverse_transform(predictions_scaled).flatten()

# 9. Plot true values vs predictions
plt.figure(figsize=(10, 6))
plt.plot(y_test, label="True Values", color="blue")
plt.plot(predictions, label="Predictions", color="red", linestyle="dashed")

# Highlight areas where predictions are above the reference average
above_ref = np.ma.masked_where(predictions <= reference_avg, predictions)
plt.fill_between(
    range(len(predictions)),
    reference_avg,
    above_ref,
    color="yellow",
    label="Above Ref Avg",
)

plt.axhline(reference_avg, color="green", linestyle="--", label="Reference Avg")

plt.legend()
plt.title("True Values vs Predictions with Reference Average")
plt.show()
