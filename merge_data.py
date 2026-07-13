import pandas as pd
import sys

sys.stdout.reconfigure(encoding='utf-8')

def process_and_merge():
    print("--- BẮT ĐẦU XỬ LÝ VÀ GỘP DỮ LIỆU ---")
    
    try:
        df_rate = pd.read_csv("ty_gia_2009_2026.csv")
        df_rate['Ngày'] = pd.to_datetime(df_rate['Ngày'])
        print(f"[+] Đã đọc file Tỷ giá: {len(df_rate)} dòng.")
    except Exception as e:
        print(f"Lỗi đọc file tỷ giá: {e}")
        return

    try:
        df_gold = pd.read_csv("gia_vang_2009_2026.csv")
        df_gold['Ngày'] = pd.to_datetime(df_gold['Ngày'])
        print(f"[+] Đã đọc file Giá vàng: {len(df_gold)} dòng.")
    except Exception as e:
        print(f"Lỗi đọc file giá vàng: {e}")
        print("Có thể file chưa tải xong. Vui lòng đợi gold_scraper.py chạy xong 100%!")
        return

    try:
        df_vnindex = pd.read_csv("vnindex_2009_to_5_2026.csv")
       
        df_vnindex['Ngày'] = pd.to_datetime(df_vnindex['time'], errors='coerce')
        df_vnindex = df_vnindex.rename(columns={
            'open': 'VNIndex_Mở_cửa',
            'high': 'VNIndex_Cao_nhất',
            'low': 'VNIndex_Thấp_nhất',
            'close': 'VNIndex_Đóng_cửa',
            'volume': 'VNIndex_Khối_lượng'
        })
        df_vnindex = df_vnindex.drop(columns=['time'])
        df_vnindex = df_vnindex.drop_duplicates(subset=['Ngày'], keep='first')
        print(f"[+] Đã đọc file VN-Index: {len(df_vnindex)} dòng.")
    except Exception as e:
        print(f"Lỗi đọc file VN-Index: {e}")
        return

    df_gold_sjc = df_gold[df_gold['Loại vàng'].str.contains("SJC", na=False)].copy()
    
    if 'Thời gian' in df_gold_sjc.columns:
        df_gold_sjc = df_gold_sjc.drop(columns=['Thời gian'])

    df_gold_sjc = df_gold_sjc.drop_duplicates(subset=['Ngày'], keep='first')
    
    print(f"[+] Sau khi lọc vàng SJC chuẩn: {len(df_gold_sjc)} dòng.")

    df_final = pd.merge(df_gold_sjc, df_rate, on='Ngày', how='outer')
    df_final = pd.merge(df_final, df_vnindex, on='Ngày', how='outer')
    df_final = df_final.sort_values(by='Ngày').reset_index(drop=True)

    max_gold_date = df_gold_sjc['Ngày'].max()

    # Không ffill() để giữ nguyên dữ liệu trống (NaN) của VN-Index vào các ngày lễ, tết, cuối tuần
    # theo đúng yêu cầu của Thầy.
    # df_final = df_final.ffill()
    
    df_final = df_final[df_final['Ngày'] <= max_gold_date]
    
    output_csv = "FINAL_DuLieu_Vang_TyGia_2009_2026.csv"
    output_excel = "FINAL_DuLieu_Vang_TyGia_2009_2026.xlsx"
    
    df_final.to_csv(output_csv, index=False, encoding='utf-8-sig')
    try:
        df_final.to_excel(output_excel, index=False)
        print(f"\n[!] THÀNH CÔNG! Đã lưu file Excel: {output_excel}")
    except Exception as e:
        print("\n[!] Đã lưu file CSV (Để lưu file Excel cần cài openpyxl: pip install openpyxl)")
        
    print(f"[!] Đã lưu file CSV: {output_csv}")
    print(f"Tổng số dòng dữ liệu hoàn chỉnh: {len(df_final)} dòng.")

if __name__ == "__main__":
    process_and_merge()
