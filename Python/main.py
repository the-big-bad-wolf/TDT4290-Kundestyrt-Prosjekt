import numpy as np
from SimpleARIMAForecasting import establish_reference, predict_next_direction

# Alt dette er bare for å simulere data og teste, skal fjernes:)

# Initial data
initial_data = np.random.rand(10800)
reference_avg = establish_reference(initial_data)

# Simulering med 90 datapunkt, 10 ganger. Skal simulere at vi får 90 datapunkt fra Tobii hver gang vi skal predikere neste datapunkt.
for _ in range(10):  # could be an infinite loop
    new_data_chunk = np.random.rand(90)
    direction = predict_next_direction(new_data_chunk, reference_avg)
    print(f"Forecasted direction for next value: {direction}")
