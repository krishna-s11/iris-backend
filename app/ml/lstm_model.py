import numpy as np
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
from tensorflow.keras.models import Sequential, load_model
from tensorflow.keras.layers import LSTM, Dense, Dropout
import ccxt

def fetch_historical_data(symbol="BTC/USDT", timeframe="1h", limit=1000):
    exchange = ccxt.binance()
    ohlcv = exchange.fetch_ohlcv(symbol, timeframe, limit=limit)
    df = pd.DataFrame(ohlcv, columns=["timestamp", "open", "high", "high", "low", "close", "volume"])
    df["timestamp"] = pd.to_datetime(df["timestamp"], unit="ms")
    return df[["close"]]

def prepare_data(data, look_back=60):
    scaler = MinMaxScaler(feature_range=(0, 1))
    scaled_data = scaler.fit_transform(data)
    X, y = [], []
    for i in range(look_back, len(scaled_data)):
        X.append(scaled_data[i-look_back:i, 0])
        y.append(scaled_data[i, 0])
    X, y = np.array(X), np.array(y)
    X = np.reshape(X, (X.shape[0], X.shape[1], 1))
    return X, y, scaler

def build_lstm_model(look_back=60):
    model = Sequential()
    model.add(LSTM(units=50, return_sequences=True, input_shape=(look_back, 1)))
    model.add(Dropout(0.2))
    model.add(LSTM(units=50, return_sequences=False))
    model.add(Dropout(0.2))
    model.add(Dense(units=1))
    model.compile(optimizer="adam", loss="mean_squared_error")
    return model

def train_and_save_model(symbol="BTC/USDT", look_back=60, epochs=10):
    df = fetch_historical_data(symbol)  # This line caused the error
    X, y, scaler = prepare_data(df[["close"]], look_back)
    train_size = int(len(X) * 0.8)
    X_train, X_test = X[:train_size], X[train_size:]
    y_train, y_test = y[:train_size], y[train_size:]
    
    model = build_lstm_model(look_back)
    model.fit(X_train, y_train, epochs=epochs, batch_size=32, verbose=1)
    model.save("lstm_model.h5")
    print("Model saved to lstm_model.h5")
    return model, scaler

def predict_next_price(symbol="BTC/USDT", look_back=60):
    exchange = ccxt.binance()
    ticker = exchange.fetch_ticker(symbol)
    current_price = ticker['last']
    df = fetch_historical_data(symbol)
    _, _, scaler = prepare_data(df[["close"]], look_back)
    last_60_days = df[["close"]].tail(look_back).values
    last_60_days_scaled = scaler.transform(last_60_days)
    X_test = np.array([last_60_days_scaled])
    X_test = np.reshape(X_test, (X_test.shape[0], X_test.shape[1], 1))
    model = load_model("d:/New_Backend/lstm_model.h5")
    predicted_price = model.predict(X_test)
    predicted_price = scaler.inverse_transform(predicted_price)
    return current_price, predicted_price[0, 0]
