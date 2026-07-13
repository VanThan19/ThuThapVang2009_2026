import yfinance as yf
import pandas as pd
import sys

sys.stdout.reconfigure(encoding='utf-8')

def download_exchange_rate(start_date, end_date, output_file="ty_gia_2009_2026.csv"):
    """
    Sử dụng thư viện tài chính yfinance (dữ liệu từ Yahoo Finance) 
    để tải toàn bộ dữ liệu lịch sử Tỷ giá ngoại tệ (USD/VND).
    Đây là phương pháp ưu việt, tải toàn bộ mười mấy năm chỉ trong vài giây.
    """
    print(f"Đang kết nối để tải Tỷ giá USD/VND từ {start_date} đến {end_date}...")
    
    ticker = yf.Ticker("VND=X")
    
    df = ticker.history(start=start_date, end=end_date)
    
    if df.empty:
        print("Lỗi: Không lấy được dữ liệu.")
        return

    df = df.reset_index()
    
    df['Date'] = df['Date'].dt.tz_localize(None)

    df = df[['Date', 'Open', 'High', 'Low', 'Close']]
    
    df.columns = ['Ngày', 'Mở cửa', 'Cao nhất', 'Thấp nhất', 'Đóng cửa (Tỷ giá chốt)']
    
    df.to_csv(output_file, index=False, encoding='utf-8-sig')
    
    print(f"THÀNH CÔNG RỰC RỠ! Đã tải {len(df)} dòng dữ liệu tỷ giá.")
    print(f"File đã được lưu tại: {output_file}")
    
    print("\n--- XEM TRƯỚC 5 NGÀY ĐẦU TIÊN ---")
    print(df.head())

if __name__ == "__main__":
    start_date = "2009-01-01"
    end_date = "2026-12-31" 
    
    output_filename = "ty_gia_2009_2026.csv"
    download_exchange_rate(start_date, end_date, output_filename)
