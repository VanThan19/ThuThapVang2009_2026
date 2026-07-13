import sys
import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime, timedelta
import time
import os
import io

sys.stdout.reconfigure(encoding='utf-8')

def get_gold_price(date_str):
    """
    Hàm cào toàn bộ bảng giá vàng (tất cả các loại) của 1 ngày từ giavang.org.
    """
    url = f"https://giavang.org/trong-nuoc/sjc/lich-su/{date_str}.html"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'
    }
    
    try:
        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code != 200:
            return None
            
        soup = BeautifulSoup(response.content, 'html.parser')
        table = soup.find('table')
        if not table:
            return None
            
        html_io = io.StringIO(str(table))
        df_list = pd.read_html(html_io)
        if df_list and len(df_list) > 0:
            df = df_list[0]
            df['Ngày'] = date_str
            return df
            
    except Exception as e:
        print(f"Lỗi ngày {date_str}: {e}")
        return None
        
    return None

def scrape_gold_history(start_date, end_date, output_file="gia_vang_2009_2026.csv"):
    start = datetime.strptime(start_date, "%Y-%m-%d")
    end = datetime.strptime(end_date, "%Y-%m-%d")
    
    mode = 'a' if os.path.exists(output_file) else 'w'
    header = not os.path.exists(output_file)
    
    if os.path.exists(output_file):
        try:
            df_existing = pd.read_csv(output_file)
            if not df_existing.empty and 'Ngày' in df_existing.columns:
                last_date_str = df_existing['Ngày'].iloc[-1]
                last_date = datetime.strptime(last_date_str, "%Y-%m-%d")
                if last_date >= start:
                    start = last_date + timedelta(days=1)
                    print(f"[*] Chạy TIẾP TỤC từ ngày {start.strftime('%Y-%m-%d')} để không bị mất dữ liệu cũ...")
        except Exception as e:
            pass
            
    current = start
    if current > end:
        print("Đã thu thập đủ dữ liệu!")
        return
        
    total_days = (end - current).days + 1
    count = 0
    
    print(f"Bắt đầu thu thập dữ liệu từ {current.strftime('%Y-%m-%d')} đến {end_date} (Còn lại: {total_days} ngày)...")
    
    while current <= end:
        date_str = current.strftime("%Y-%m-%d")
        count += 1
        
        print(f"[{count}/{total_days}] Đang lấy dữ liệu ngày {date_str}...", end=" ")
        df = get_gold_price(date_str)
        
        if df is not None and not df.empty:
            df.to_csv(output_file, mode=mode, header=header, index=False, encoding='utf-8-sig')
            header = False 
            mode = 'a' 
            print("=> THÀNH CÔNG")
        else:
            print("=> TRỐNG (Có thể là cuối tuần/lễ)")
            
        time.sleep(2)
        
        current += timedelta(days=1)

if __name__ == "__main__":
    start_date = "2009-01-01"
    end_date = "2026-12-31"
    
    output_filename = "gia_vang_2009_2026.csv"
    scrape_gold_history(start_date, end_date, output_filename)
    
    print(f"\nHoàn thành! Đã lưu dữ liệu vào file: {output_filename}")
