import tkinter as tk
from tkinter import messagebox, filedialog, simpledialog
import os, json
from PIL import Image, ImageTk
from datetime import datetime

class SanPham:
    def __init__(self, maSP, tenSP, giaBan, image):
        self.maSP = maSP
        self.tenSP = tenSP
        self.giaBan = giaBan
        self.image = image

    def chuyen_dict(self):
        return {'maSP': self.maSP, 'tenSP': self.tenSP, 'giaBan': self.giaBan, 'image': self.image}

def load_sanpham():
    if not os.path.exists("danhsach_aoquan.json"):
        return []
    with open("danhsach_aoquan.json", "r", encoding="utf-8") as f:
        content = f.read()
        return json.loads(content) if content.strip() else []

def luu_sanpham(data):
    with open("danhsach_aoquan.json", "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def luu_hoadon(hoadon):
    ds = []
    if os.path.exists("hoadon.json"):
        with open("hoadon.json", "r", encoding="utf-8") as f:
            content = f.read()
            if content.strip():
                ds = json.loads(content)
    ds.append(hoadon)
    with open("hoadon.json", "w", encoding="utf-8") as f:
        json.dump(ds, f, ensure_ascii=False, indent=2)

gio_hang = []
vai_tro_toan_cuc = ""

# ================= GIỎ HÀNG ===================
def cap_nhat_gio_hang(frame, root, data):
    for widget in frame.winfo_children():
        widget.destroy()

    tk.Label(frame, text="\U0001F6D2 Giỏ hàng", font=("Arial", 14, "bold"), bg="white").pack(pady=5)

    tong_tien = 0
    for sp in gio_hang:
        row = tk.Frame(frame, bg="white")
        row.pack(fill="x", padx=5, pady=2)

        tk.Label(row, text=sp['tenSP'], width=15, anchor="w", bg="white").pack(side="left")
        tk.Label(row, text=f"{int(sp['giaBan']):,}đ", width=10, anchor="center", bg="white").pack(side="left")
        tk.Button(row, text="-", command=lambda sp=sp: giam_so_luong(sp, frame, root, data)).pack(side="left")
        tk.Label(row, text=sp['soluong'], width=3, anchor="center", bg="white").pack(side="left")
        tk.Button(row, text="+", command=lambda sp=sp: tang_so_luong(sp, frame, root, data)).pack(side="left")

        tong_tien += int(sp['giaBan']) * sp['soluong']

    # Tổng tiền
    tk.Label(frame, text=f"\U0001F9FE Tổng tiền: {tong_tien:,}đ", font=("Arial", 12, "bold"), bg="white", fg="red").pack(pady=10)

    # Nút thanh toán và hóa đơn (chỉ người mua mới có)
    if vai_tro_toan_cuc == "mua":
        tk.Button(frame, text="\U0001F4B3 Thanh toán", font=("Arial", 12, "bold"), bg="#00b894", fg="white",
                  command=lambda: thanh_toan(root, frame, data)).pack(pady=5)
        tk.Button(frame, text="📄 Xem hóa đơn", font=("Arial", 10), command=xem_hoadon).pack(pady=5)



def them_vao_gio(sp, gio_frame, root, data):
    if vai_tro_toan_cuc == "quanly":
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

    cap_nhat_gio_hang(gio_frame, root, data)

def giam_so_luong(sp, gio_frame, root, data):
    sp['soluong'] -= 1
    if sp['soluong'] <= 0:
        gio_hang.remove(sp)
    cap_nhat_gio_hang(gio_frame, root, data)

def tang_so_luong(sp, gio_frame, root, data):
    sp['soluong'] += 1
    cap_nhat_gio_hang(gio_frame, root, data)

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
    cap_nhat_gio_hang(gio_frame, root, data)

# ================ HÓA ĐƠN ================
def xem_hoadon():
    if not os.path.exists("hoadon.json"):
        messagebox.showinfo("Thông báo", "Chưa có hóa đơn nào.")
        return
    with open("hoadon.json", "r", encoding="utf-8") as f:
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

# ================ GIAO DIỆN ================
def chon_vai_tro():
    def chon(vai_tro):
        global vai_tro_toan_cuc
        vai_tro_toan_cuc = vai_tro
        chon_win.destroy()
        tao_giaodien(load_sanpham(), vai_tro)

    chon_win = tk.Tk()
    chon_win.title("Chọn vai trò")
    chon_win.geometry("300x200")
    tk.Label(chon_win, text="Bạn là ai?", font=("Arial", 14, "bold")).pack(pady=20)
    tk.Button(chon_win, text="👤 Người mua", width=20, command=lambda: chon("mua")).pack(pady=10)
    tk.Button(chon_win, text="🛠 Người quản lý", width=20, command=lambda: chon("quanly")).pack(pady=10)
    chon_win.mainloop()
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
        gio_frame.pack(side="left", fill="y", padx=10, pady=10)
        tk.Label(gio_frame, text="\U0001F6D2 Giỏ hàng", font=("Arial", 14, "bold"), bg="white").pack(pady=5)

        cap_nhat_gio_hang(gio_frame, root, data)

       

    # ===== DANH SÁCH SẢN PHẨM =====
    sp_frame = tk.Frame(frame_chinh, bg="#e3f2fd")
    sp_frame.pack(side="left", fill="both", expand=True, padx=10, pady=10)

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
            img = Image.open(sp['image']).resize((180, 120))
            photo = ImageTk.PhotoImage(img)
            label = tk.Label(frame, image=photo)
            label.image = photo
            label.pack()
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
                      command=lambda sp=sp: them_vao_gio(sp, gio_frame, root, data)).pack()

    root.mainloop()



def them_sanpham(root):
    data = load_sanpham()
    ten = simpledialog.askstring("Tên sản phẩm", "Nhập tên:")
    if not ten: return
    gia = simpledialog.askstring("Giá bán", "Nhập giá:")
    if not gia: return
    image_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.jpg *.png")])
    if not image_path: return

    if not os.path.exists("images"): os.makedirs("images")
    maSP = f"SP{len(data)+1}"
    save_path = f"images/{maSP}.jpg"
    Image.open(image_path).save(save_path)

    sp = SanPham(maSP, ten, gia, save_path)
    data.append(sp.chuyen_dict())
    luu_sanpham(data)
    root.destroy()
    tao_giaodien(data, "quanly")

if __name__ == "__main__":
    chon_vai_tro()
