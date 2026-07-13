import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import sys


sys.stdout.reconfigure(encoding='utf-8')

def draw():
    print("--- ĐANG VẼ BIỂU ĐỒ ---")
    try:
        df = pd.read_csv("FINAL_DuLieu_Vang_TyGia_2009_2026.csv")
        
        df['Ngày'] = pd.to_datetime(df['Ngày'])

        fig, ax1 = plt.subplots(figsize=(12, 6))

        color1 = 'tab:orange'
        ax1.set_xlabel('Thời gian (Năm)', fontsize=12, fontweight='bold')
        ax1.set_ylabel('Giá Vàng SJC - Bán ra (Ngàn VNĐ / Lượng)', color=color1, fontsize=12, fontweight='bold')
        line1, = ax1.plot(df['Ngày'], df['Bán ra'], color=color1, linewidth=2, label='Giá Vàng SJC')
        ax1.tick_params(axis='y', labelcolor=color1)
        ax1.grid(True, linestyle='--', alpha=0.5)

        ax2 = ax1.twinx()  
        color2 = 'tab:blue'
        ax2.set_ylabel('Tỷ giá USD/VND (Chốt phiên)', color=color2, fontsize=12, fontweight='bold')
        line2, = ax2.plot(df['Ngày'], df['Đóng cửa (Tỷ giá chốt)'], color=color2, linewidth=2, label='Tỷ giá USD')
        ax2.tick_params(axis='y', labelcolor=color2)

        ax1.xaxis.set_major_locator(mdates.YearLocator())
        ax1.xaxis.set_major_formatter(mdates.DateFormatter('%Y'))
        plt.xticks(rotation=45)

        plt.title('BIỂU ĐỒ SO SÁNH BIẾN ĐỘNG GIÁ VÀNG SJC VÀ TỶ GIÁ USD/VND', fontsize=14, fontweight='bold', pad=15)
        
        lines = [line1, line2]
        labels = [l.get_label() for l in lines]
        ax1.legend(lines, labels, loc='upper left')

        fig.tight_layout()

        output_img = "BieuDo_Vang_TyGia.png"
        plt.savefig(output_img, dpi=300)
        print(f"[!] Đã xuất bản thành công bản vẽ siêu nét ra file: {output_img}")
        
        print("[!] Đang mở cửa sổ biểu đồ. (Hãy bấm tắt cửa sổ biểu đồ khi xem xong để kết thúc)...")
        plt.show()

    except FileNotFoundError:
        print("Lỗi: Không tìm thấy file FINAL_DuLieu_Vang_TyGia_2009_2026.csv. Hãy đảm bảo bạn đã chạy file merge_data.py trước nhé!")
    except Exception as e:
        print(f"Lỗi không xác định: {e}")

if __name__ == "__main__":
    draw()
