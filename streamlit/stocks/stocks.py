import streamlit as st
import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
import requests

# Fungsi untuk mengambil data saham
def get_stock_data(ticker, start_date, end_date):
    stock_data = yf.download(ticker, start=start_date, end=end_date)
    stock_data = stock_data.sort_values(by='Date', ascending=False)  # Mengurutkan berdasarkan tanggal dari yang terbaru

    return stock_data

# Fungsi untuk membuat grafik pergerakan harga saham
def plot_stock_data(stock_data):
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.plot(stock_data['Close'], label='Close')
    ax.set_title('Pergerakan Harga Saham')
    ax.set_xlabel('Tanggal')
    ax.set_ylabel('Harga (USD)')
    ax.legend()
    st.pyplot(fig)

# Fungsi untuk mendapatkan data volume trading
def get_volume_data(ticker, start_date, end_date):
    stock_data = yf.download(ticker, start=start_date, end=end_date)
    return stock_data['Volume']

# Fungsi untuk mendapatkan riwayat dividen dari saham
def get_dividend_history(ticker):
    stock = yf.Ticker(ticker)
    dividend_history = stock.dividends
    dividend_history = dividend_history.sort_index(ascending=False)  # Mengurutkan dari yang terbaru
    return dividend_history

# Main function
def main():
    st.title('Aplikasi Data Saham')

    # Input ticker saham dan tahun
    ticker = st.text_input('Masukkan Ticker Saham (Contoh: BBNI.JK untuk Bank BNI)', 'BBNI.JK')
    year = st.slider('Pilih Tahun', min_value=2010, max_value=2024, value=2020)

    # Mendapatkan data saham
    start_date = str(year) + '-01-01'
    end_date = str(year) + '-12-31'
    stock_data = get_stock_data(ticker, start_date, end_date)
    volume_data = get_volume_data(ticker, start_date, end_date)


    if stock_data.empty:
        st.warning('Data saham tidak tersedia. Mohon periksa kembali ticker saham yang dimasukkan.')
    else:
        # Menampilkan data saham
        st.subheader('Data Saham')
        st.write(stock_data)

        # Menampilkan grafik pergerakan harga saham
        st.subheader('Grafik Pergerakan Harga Saham')
        plot_stock_data(stock_data)

        # Menampilkan informasi tambahan
        st.subheader('Informasi Tambahan')
        st.write('**Open:**', stock_data['Open'].iloc[-1])
        st.write('**High:**', stock_data['High'].iloc[-1])
        st.write('**Low:**', stock_data['Low'].iloc[-1])
        st.write('**Close:**', stock_data['Close'].iloc[-1])
        st.write('**Market Cap:**', yf.Ticker(ticker).info['marketCap'])

         # Grafik volume trading
        st.subheader('Volume Trading')
        st.line_chart(volume_data)

        # Perbandingan Saham
        st.subheader('Perbandingan Saham')
        tickers = st.text_input('Masukkan Ticker Saham untuk Perbandingan (pisahkan dengan koma)', 'BBNI.JK, BBRI.JK')
        tickers_list = [ticker.strip() for ticker in tickers.split(',')]
        comparison_data = pd.DataFrame()
        for t in tickers_list:
            comparison_data[t] = yf.download(t, start=start_date, end=end_date)['Close']
        st.line_chart(comparison_data)

        # Mendapatkan riwayat dividen
        st.subheader('Riwayat Dividen')
        dividend_history = get_dividend_history(ticker)
        st.write(dividend_history)


if __name__ == '__main__':
    main()
