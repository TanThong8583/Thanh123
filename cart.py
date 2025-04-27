# cart.py
import tkinter as tk
from tkinter import messagebox
from data_utils import luu_hoadon
from datetime import datetime

gio_hang = []
# Không nên quá phụ thuộc vào biến toàn cục

def cap_nhat_gio_hang(frame, root, data, vai_tro):  # Thêm tham số vai_tro
    from ui import xem_hoadon  # Import trong hàm để tránh vòng lặp import

    for widget in frame.winfo_children():
        widget.destroy()

    tk.Label(frame, text="\U0001F6D2 Giỏ hàng", font=("Arial", 14, "bold"), bg="white").pack(pady=5)

    tong_tien = 0
    for sp in gio_hang:
        row = tk.Frame(frame, bg="white")
        row.pack(fill="x", padx=5, pady=2)

        tk.Label(row, text=sp['tenSP'], width=15, anchor="w", bg="white").pack(side="left")
        tk.Label(row, text=f"{int(sp['giaBan']):,}đ", width=10, anchor="center", bg="white").pack(side="left")
        tk.Button(row, text="-", command=lambda sp=sp: giam_so_luong(sp, frame, root, data, vai_tro)).pack(side="left") # Truyền vai_tro nếu cần
        tk.Label(row, text=sp['soluong'], width=3, anchor="center", bg="white").pack(side="left")
        tk.Button(row, text="+", command=lambda sp=sp: tang_so_luong(sp, frame, root, data, vai_tro)).pack(side="left") # Truyền vai_tro nếu cần

        tong_tien += int(sp['giaBan']) * sp['soluong']

    tk.Label(frame, text=f"\U0001F9FE Tổng tiền: {tong_tien:,}đ", font=("Arial", 12, "bold"), bg="white", fg="red").pack(pady=10)

    if vai_tro == "mua":
        tk.Button(frame, text="\U0001F4B3 Thanh toán", font=("Arial", 12, "bold"), bg="#00b894", fg="white",
                    command=lambda: thanh_toan(root, frame, data)).pack(pady=5)
        tk.Button(frame, text="📄 Xem hóa đơn", font=("Arial", 10), command=xem_hoadon).pack(pady=5)

def them_vao_gio(sp, gio_frame, root, data, vai_tro): # Thêm tham số vai_tro
    if vai_tro == "quanly":
        messagebox.showwarning("Không thể mua", "Người quản lý không thể mua hàng!")
        return

    for item in gio_hang:
        if item['maSP'] == sp['maSP']:
            item['soluong'] += 1
            break
    else:
        sp_copy = sp.copy()
        sp_copy['soluong'] = 1
        gio_hang.append(sp_copy)

    cap_nhat_gio_hang(gio_frame, root, data, vai_tro) # Truyền vai_tro

def giam_so_luong(sp, gio_frame, root, data, vai_tro): # Thêm tham số vai_tro
    sp['soluong'] -= 1
    if sp['soluong'] <= 0:
        gio_hang.remove(sp)
    cap_nhat_gio_hang(gio_frame, root, data, vai_tro) # Truyền vai_tro

def tang_so_luong(sp, gio_frame, root, data, vai_tro): # Thêm tham số vai_tro
    sp['soluong'] += 1
    cap_nhat_gio_hang(gio_frame, root, data, vai_tro) # Truyền vai_tro

def thanh_toan(root, gio_frame, data):
    if not gio_hang:
        messagebox.showinfo("Thông báo", "Giỏ hàng đang trống!")
        return
    if not messagebox.askyesno("Xác nhận", "Bạn có chắc chắn muốn thanh toán không?"):
        return
    tong = sum(int(sp['giaBan']) * sp['soluong'] for sp in gio_hang)
    hoadon = {
        "thoigian": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "sanpham": gio_hang.copy(),
        "tong": tong
    }
    luu_hoadon(hoadon)
    gio_hang.clear()
    messagebox.showinfo("Thành công", "\U0001F7E2 Thanh toán thành công! Hóa đơn đã được lưu.")
    cap_nhat_gio_hang(gio_frame, root, data, "mua") # Sau thanh toán, cập nhật lại giỏ hàng (vai trò không quan trọng ở đây)