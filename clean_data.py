import pandas as pd
import sys

sys.stdout.reconfigure(encoding='utf-8')

def clean_data():
    print("--- BẮT ĐẦU LÀM SẠCH DỮ LIỆU ---")
    
    input_file = "FINAL_3Files_Vang_TyGia_VNIndex.csv"
    output_csv = "CLEANED_3Files_Vang_TyGia_VNIndex.csv"
    output_excel = "CLEANED_3Files_Vang_TyGia_VNIndex.xlsx"
    
    try:
        df = pd.read_csv(input_file)
        original_rows = len(df)
        print(f"Tổng số dòng ban đầu: {original_rows} dòng.")
    except Exception as e:
        print(f"Lỗi đọc file: {e}")
        return
    df_cleaned = df.dropna()
    
    cleaned_rows = len(df_cleaned)
    deleted_rows = original_rows - cleaned_rows
    
    print(f"Số dòng bị xóa (do khuyết dữ liệu): {deleted_rows} dòng.")
    print(f"Tổng số dòng sau khi làm sạch: {cleaned_rows} dòng.")
    
    df_cleaned.to_csv(output_csv, index=False, encoding='utf-8-sig')
    try:
        df_cleaned.to_excel(output_excel, index=False)
        print(f"\n[!] THÀNH CÔNG! Đã lưu file Excel sạch: {output_excel}")
    except Exception as e:
        print("\n[!] Đã lưu file CSV sạch (Để lưu file Excel cần cài openpyxl)")
        
    print(f"[!] Đã lưu file CSV sạch: {output_csv}")

    with open("log_xoa_dong.txt", "w", encoding="utf-8") as f:
        f.write(f"Tổng số dòng ban đầu: {original_rows}\n")
        f.write(f"Số dòng bị xóa: {deleted_rows}\n")
        f.write(f"Tổng số dòng còn lại: {cleaned_rows}\n")
    print("[!] Đã lưu log báo cáo số dòng bị xóa vào file: log_xoa_dong.txt")

if __name__ == "__main__":
    clean_data()
