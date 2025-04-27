# ui.py
import tkinter as tk
from tkinter import messagebox, filedialog, simpledialog
import os
from PIL import Image, ImageTk
from models import SanPham
from data_utils import load_sanpham, luu_sanpham
from cart import gio_hang, cap_nhat_gio_hang, them_vao_gio

def xem_hoadon():
    if not os.path.exists("hoadon.json"):
        messagebox.showinfo("Thông báo", "Chưa có hóa đơn nào.")
        return
    with open("hoadon.json", "r", encoding="utf-8") as f:
        import json
        ds = json.load(f)

    win = tk.Toplevel()
    win.title("Hóa đơn đã mua")
    win.geometry("400x400")

    box = tk.Text(win)
    box.pack(fill="both", expand=True)

    for hd in ds:
        box.insert("end", f"🕒 {hd['thoigian']}\n")
        for sp in hd['sanpham']:
            box.insert("end", f"  - {sp['tenSP']} x{sp['soluong']} = {int(sp['giaBan'])*sp['soluong']:,}đ\n")
        box.insert("end", f"  🧾 Tổng cộng: {hd['tong']:,}đ\n\n")

def xoa_sanpham(sp, root):
    if not messagebox.askyesno("Xác nhận", f"Bạn có chắc muốn xóa '{sp['tenSP']}' không?"):
        return
    data = load_sanpham()
    data = [item for item in data if item['maSP'] != sp['maSP']]
    luu_sanpham(data)
    messagebox.showinfo("Thành công", "Đã xóa sản phẩm.")
    root.destroy()
    tao_giaodien(data, "quanly")

def sua_sanpham(sp, root):
    data = load_sanpham()
    ten_moi = simpledialog.askstring("Sửa tên", "Nhập tên mới:", initialvalue=sp['tenSP'])
    if not ten_moi: return
    gia_moi = simpledialog.askstring("Sửa giá", "Nhập giá mới:", initialvalue=sp['giaBan'])
    if not gia_moi: return

    for item in data:
        if item['maSP'] == sp['maSP']:
            item['tenSP'] = ten_moi
            item['giaBan'] = gia_moi
            break

    luu_sanpham(data)
    messagebox.showinfo("Thành công", "Đã sửa sản phẩm.")
    root.destroy()
    tao_giaodien(data, "quanly")

def tao_giaodien(data, vai_tro):
    root = tk.Tk()
    root.title("🛍️ SHOP BÁN HÀNG")
    root.geometry("1200x700")
    root.configure(bg="white")

    tk.Label(root, text="\U0001F6CD HỆ THỐNG BÁN HÀNG", font=("Arial", 20, "bold"), fg="white", bg="#0d47a1").pack(fill="x", pady=10)

    frame_chinh = tk.Frame(root, bg="white")
    frame_chinh.pack(fill="both", expand=True)

    # ===== CHỈ hiển thị giỏ hàng nếu là NGƯỜI MUA =====
    if vai_tro == "mua":
        gio_frame = tk.Frame(frame_chinh, bg="white", width=300)
        gio_canvas = tk.Canvas(gio_frame, bg="white", highlightthickness=0)
        gio_scrollbar = tk.Scrollbar(gio_frame, orient="vertical", command=gio_canvas.yview)
        gio_canvas.configure(yscrollcommand=gio_scrollbar.set)

        gio_scrollbar.pack(side="right", fill="y")
        gio_canvas.pack(side="left", fill="both", expand=True)

        gio_inner_frame = tk.Frame(gio_canvas, bg="white", width=300)
        gio_canvas.create_window((0, 0), window=gio_inner_frame, anchor="nw")
        gio_inner_frame.bind("<Configure>", lambda event, canvas=gio_canvas: canvas.configure(scrollregion=canvas.bbox("all")))

        tk.Label(gio_inner_frame, text="\U0001F6D2 Giỏ hàng", font=("Arial", 14, "bold"), bg="white").pack(pady=5)
        cap_nhat_gio_hang(gio_inner_frame, root, data, vai_tro)  # Truyền vai_tro

        gio_frame.pack(side="left", fill="y", padx=10, pady=10)

    # ===== DANH SÁCH SẢN PHẨM =====
    sp_canvas = tk.Canvas(frame_chinh, bg="#e3f2fd", highlightthickness=0)
    sp_scrollbar = tk.Scrollbar(frame_chinh, orient="vertical", command=sp_canvas.yview)
    sp_canvas.configure(yscrollcommand=sp_scrollbar.set)

    sp_scrollbar.pack(side="right", fill="y")
    sp_canvas.pack(side="left", fill="both", expand=True, padx=10, pady=10)

    sp_frame = tk.Frame(sp_canvas, bg="#e3f2fd")
    sp_canvas.create_window((0, 0), window=sp_frame, anchor="nw")
    sp_frame.bind("<Configure>", lambda event, canvas=sp_canvas: canvas.configure(scrollregion=canvas.bbox("all")))

    # Nút thêm sản phẩm cho quản lý
    if vai_tro == "quanly":
        tk.Button(sp_frame, text="➕ Thêm sản phẩm", command=lambda: them_sanpham(root)).pack(pady=10)

    grid = tk.Frame(sp_frame, bg="#e3f2fd")
    grid.pack()
    cols = 3
    for i, sp in enumerate(data):
        frame = tk.Frame(grid, bg="white", relief="groove", bd=1, padx=5, pady=5)
        frame.grid(row=i // cols, column=i % cols, padx=10, pady=10)

        # Ảnh sản phẩm
        if os.path.exists(sp['image']):
            try:
                img = Image.open(sp['image']).resize((180, 120))
                photo = ImageTk.PhotoImage(img)
                label = tk.Label(frame, image=photo)
                label.image = photo
                label.pack()
            except Exception as e:
                print(f"Lỗi khi tải ảnh {sp['image']}: {e}")
                tk.Label(frame, text="[Lỗi ảnh]", width=20, height=6).pack()
        else:
            tk.Label(frame, text="[Không ảnh]", width=20, height=6).pack()

        # Tên và giá
        tk.Label(frame, text=sp['tenSP'], font=("Arial", 10), bg="white").pack()
        tk.Label(frame, text=f"{int(sp['giaBan']):,}đ", font=("Arial", 10, "bold"), fg="red", bg="white").pack()

        # Nút hành động tùy vai trò
        action_frame = tk.Frame(frame, bg="white")
        action_frame.pack(pady=5)

        if vai_tro == "quanly":
            tk.Button(action_frame, text="✏️ Sửa", bg="#fdcb6e", command=lambda sp=sp: sua_sanpham(sp, root)).pack(side="left", padx=5)
            tk.Button(action_frame, text="🗑️ Xóa", bg="#d63031", fg="white", command=lambda sp=sp: xoa_sanpham(sp, root)).pack(side="left")
        else:  # người mua
            tk.Button(action_frame, text="🛒 Mua", bg="#00b894", fg="white",
                                command=lambda sp=sp: them_vao_gio(sp, gio_inner_frame, root, data, vai_tro)).pack() # Truyền vai_tro

    root.mainloop()

def them_sanpham(root):
    data = load_sanpham()
    ten = simpledialog.askstring("Tên sản phẩm", "Nhập tên:")
    if not ten:
        return
    gia = simpledialog.askstring("Giá bán", "Nhập giá:")
    if not gia:
        return
    image_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.jpg *.png")])
    if not image_path:
        return

    if not os.path.exists("images"): os.makedirs("images")
    maSP = f"SP{len(data)+1}"
    save_path = f"images/{maSP}.jpg"
    Image.open(image_path).save(save_path)

    sp = SanPham(maSP, ten, gia, save_path)
    data.append(sp.chuyen_dict())
    luu_sanpham(data)
    root.destroy()
    tao_giaodien(data, "quanly")

def chon_vai_tro():
    def chon(vai_tro):
        chon_win.destroy()
        tao_giaodien(load_sanpham(), vai_tro) # Truyền vai_tro trực tiếp

    chon_win = tk.Tk()
    chon_win.title("Chọn vai trò")
    chon_win.geometry("300x200")
    tk.Label(chon_win, text="Bạn là ai?", font=("Arial", 14, "bold")).pack(pady=20)
    tk.Button(chon_win, text="👤 Người mua", width=20, command=lambda: chon("mua")).pack(pady=10)
    tk.Button(chon_win, text="🛠 Người quản lý", width=20, command=lambda: chon("quanly")).pack(pady=10)
    chon_win.mainloop()

if __name__ == "__main__":
    chon_vai_tro()