from flask import Flask, request, jsonify, Response
from model import train_model
from database import create_connection, fetch_data
import pandas as pd
import numpy as np
from gevent.pywsgi import WSGIServer
from flask_cors import CORS, cross_origin

app = Flask(__name__)
app.config['CORS_HEADERS'] = 'Content-Type'
CORS(app)

@app.before_request
def basic_authentication():
    if request.method.lower() == 'options':
        return Response()

@app.route('/predict', methods=['GET'])
@cross_origin(origin='*')
def predict():
    input_administered_time = pd.Timestamp(request.args.get('administeredtime'))
    input_medication_type= request.args.get('medicationtype')

    connection = create_connection()
    records = fetch_data(connection)
    df = pd.DataFrame(records, columns=['medicationtype', 'administeredtime', 'consumedtime'])
    df.dropna(subset=['consumedtime'], inplace=True)

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


@app.route('/predict-mock', methods=['GET'])
@cross_origin(origin='*')
def predictMock():
    input_administered_time = pd.Timestamp(request.args.get('administeredtime'))
    input_medication_type= request.args.get('medicationtype')

    return jsonify({'predicted_time_difference': str("0:35:33.541243")})

@app.route('/predict-mockfast', methods=['GET'])
@cross_origin(origin='*')
def predictMockFast():
    input_administered_time = pd.Timestamp(request.args.get('administeredtime'))
    input_medication_type= request.args.get('medicationtype')

    return jsonify({'predicted_time_difference': str("0:0:05.541243")})

if __name__ == '__main__':
    # app.run(debug=True, port=5000)
    http_server = WSGIServer(('', 5000), app)
    http_server.serve_forever()