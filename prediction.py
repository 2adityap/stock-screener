import pandas as pd
import pandas_datareader as web
import numpy as np
import tensorflow as tf
from sklearn.preprocessing import MinMaxScaler
from keras.layers import LSTM
from keras.layers import Dense
from keras.models import Sequential
import math
import matplotlib.pyplot as mtlplt
import yfinance as yf

def create_df(symbol, start, end):
    data = yf.download(symbol, start = start, end = end)
    data_frame = pd.DataFrame(data)
    data_frame.to_csv('stockdata.csv',index = "Date")
    df = pd.read_csv('stockdata.csv')
    return df

def graph(dataframe):
    mtlplt.figure(figsize=(20,9))
    mtlplt.title("Closing Data")
    mtlplt.plot(dataframe["Close"])
    mtlplt.xticks(range(0,dataframe.shape[0],500),dataframe["Date"].loc[::500],rotation=45)
    mtlplt.xlabel('Date', fontsize=20)
    mtlplt.ylabel('Close price in $(USD)',fontsize=20)
    mtlplt.show()

def feature_scaling(dataset):
    scale = MinMaxScaler(feature_range=(0,1)) #scales features between
    scaled_data = scale.fit_transform(dataset)
    return scaled_data

def train_close_prices(dataframe):
    close_data = dataframe.filter(["Close"])
    close_dataset = close_data.values #convert to array
    training_length = math.ceil(len(close_dataset)*.8) #80:20 ratio applied

    scale = MinMaxScaler(feature_range=(0,1)) #scales features between
    scaled_data = scale.fit_transform(close_dataset)

    training_data = scaled_data[0:training_length, :]
    Xtrain = []
    Ytrain = []

    for i in range(60, len(training_data)):
        Xtrain.append(training_data[i-60:i])
        Ytrain.append(training_data[i])
    Xtrain = np.array(Xtrain)
    Ytrain = np.array(Ytrain)
    Xtrain = np.reshape(Xtrain, (Xtrain.shape[0], Xtrain.shape[1],1))

    model = Sequential()
    neurons = 50
    model.add(LSTM(neurons, return_sequences=True, input_shape=(Xtrain.shape[1],1)))
    model.add(LSTM(neurons, return_sequences=False))

    model.add(Dense(25))
    model.add(Dense(1))
    model.compile(optimizer='adam', loss='mse')
    history_data = model.fit(Xtrain, Ytrain, batch_size=50, epochs=200, verbose=2, validation_split=0.2)

    graph_convergence(history_data)

    testing_data = scaled_data[training_length-60:,:]
    Xtest = []
    Ytest = close_dataset[training_length:, :]
    for i in range(60, len(testing_data)):
        Xtest.append(testing_data[i-60:i])
    Xtest = np.array(Xtest)
    Xtest = np.reshape(Xtest, (Xtest.shape[0], Xtest.shape[1],1))

    predictions = model.predict(Xtest)
    predictions = scale.inverse_transform(predictions)

    training = close_data[:training_length]
    validation = close_data[training_length:]
    validation['Predictions'] = predictions

    graph_algorithm_training(training, validation, dataframe)
    print(dataframe)
    predict_next_day(model, dataframe, scale)

def graph_convergence(history_data):
    mtlplt.figure(figsize=(20,10))
    mtlplt.title('Training validation loss')
    mtlplt.plot(history_data.history['loss'])
    mtlplt.plot(history_data.history['val_loss'])
    mtlplt.ylabel('Training loss')
    mtlplt.xlabel('epochs')
    mtlplt.legend(['train' , 'validation'], loc = 'upper left')
    mtlplt.show()

def graph_algorithm_training(training, validation, dataframe):
    ## Visualize trainning, validating and predicting values in graph
    mtlplt.figure(figsize=(20,10))
    mtlplt.title('Trained Model')
    mtlplt.xticks(range(0,dataframe.shape[0],500),dataframe['Date'].loc[::500],rotation=45)
    mtlplt.xlabel('Date', fontsize=20)
    mtlplt.ylabel('Close Stock Price $ (USD)', fontsize=20)
    mtlplt.plot(training['Close'])
    mtlplt.plot(validation[['Close', 'Predictions']])
    mtlplt.legend(['Training', 'Validation', 'Predictions'], loc='lower right')
    mtlplt.show()

def predict_next_day(model, dataframe, scale):
    df = dataframe.filter(["Close"])
    last60days = df[-60:].values
    last60days_scaled = scale.transform(last60days)
    X_test = []
    X_test.append(last60days_scaled)
    X_test = np.array(X_test)
    X_test = np.reshape(X_test, (X_test.shape[0], X_test.shape[1], 1))

    predicted_price = model.predict(X_test)
    predicted_price = scale.inverse_transform(predicted_price)
    print(predicted_price)

def main():
    #Something to do with start price that affects wrong output
    df = create_df("NVDA", "2013-01-01", "2021-01-04")
    train_close_prices(df)


if __name__ == "__main__":
    main()
