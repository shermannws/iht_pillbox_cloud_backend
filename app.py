from flask import Flask, request, jsonify
from model import train_model
from database import create_connection, fetch_data
import pandas as pd
import numpy as np
from gevent.pywsgi import WSGIServer

app = Flask(__name__)

@app.route('/predict', methods=['POST'])
def predict():
    data = request.get_json()
    input_administered_time = pd.Timestamp(data['administeredtime'])
    input_medication_type = data['medicationtype']

    connection = create_connection()
    records = fetch_data(connection)
    df = pd.DataFrame(records, columns=['medicationtype', 'administeredtime', 'consumedtime'])

    model, one_hot_encoder = train_model(df)

    # Convert administered time to milliseconds
    input_administered_time_ms = input_administered_time.timestamp() * 1000

    # Perform one-hot encoding for the input medication type
    input_medication_type_encoded = one_hot_encoder.transform([[input_medication_type]])
    input_medication_type_encoded_df = pd.DataFrame(input_medication_type_encoded.toarray(), columns=one_hot_encoder.get_feature_names_out(['medicationtype']))

    # Create a DataFrame with input data
    input_data = pd.DataFrame({
        'administeredtime_ms': [input_administered_time_ms]
    })

    # Concatenate the one-hot encoded medication type with the input data
    input_data = pd.concat([input_data, input_medication_type_encoded_df], axis=1)

    # Drop the consumedtime_ms column from the input data
    input_data.drop(columns=['consumedtime_ms'], inplace=True, errors='ignore')

    # Use the trained model to predict the time difference
    predicted_time_difference_ms = model.predict(input_data)

    # Convert the predicted time difference back to a human-readable format
    predicted_time_difference = pd.Timedelta(milliseconds=predicted_time_difference_ms[0]).to_pytimedelta()

    return jsonify({'predicted_time_difference': str(predicted_time_difference)})


@app.route('/predict-mock', methods=['POST'])
def predictMock():
    data = request.get_json()
    input_administered_time = pd.Timestamp(data['administeredtime'])
    input_medication_type = data['medicationtype']

    return jsonify({'predicted_time_difference': str("0:35:33.541243")})

@app.route('/predict-mockfast', methods=['POST'])
def predictMockFast():
    data = request.get_json()
    input_administered_time = pd.Timestamp(data['administeredtime'])
    input_medication_type = data['medicationtype']

    return jsonify({'predicted_time_difference': str("0:0:30.541243")})

if __name__ == '__main__':
    # app.run(debug=False, port=5000)
    # Production
    http_server = WSGIServer(('', 5000), app)
    http_server.serve_forever()