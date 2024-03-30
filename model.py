import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import OneHotEncoder

def train_model(df):
    df['administeredtime'] = pd.to_datetime(df['administeredtime'])
    df['consumedtime'] = pd.to_datetime(df['consumedtime'])

    # Convert datetime objects to milliseconds
    df['administeredtime_ms'] = df['administeredtime'].astype(np.int64) // 10**6
    df['consumedtime_ms'] = df['consumedtime'].astype(np.int64) // 10**6
    
    # One-hot encode the medicationtype column
    # Assuming medicationtype column has categories like 'before' and 'after'
    one_hot_encoder = OneHotEncoder()
    medicationtype_encoded = one_hot_encoder.fit_transform(df[['medicationtype']])
    medicationtype_encoded_df = pd.DataFrame(medicationtype_encoded.toarray(), columns=one_hot_encoder.get_feature_names_out(['medicationtype']))
    df_encoded = pd.concat([df.drop(columns=['medicationtype', 'administeredtime', 'consumedtime']), medicationtype_encoded_df], axis=1)

    # Calculate time difference between administered and consumed time
    df_encoded['time_difference'] = df['consumedtime_ms'] - df['administeredtime_ms']

    # Split data into features and target
    X = df_encoded.drop(columns=['time_difference'])
    y = df_encoded['time_difference']

    # Split data into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

    # Create a new model without the consumedtime_ms feature
    X_train_new = X_train.drop(columns=['consumedtime_ms'])
    X_test_new = X_test.drop(columns=['consumedtime_ms'])

    # Train linear regression model
    model = LinearRegression()
    model.fit(X_train_new, y_train)
    
    return model, one_hot_encoder