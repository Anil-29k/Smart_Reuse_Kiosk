import tkinter as tk
from tkinter import messagebox
from api import register_user, login_user, scan_qr, get_dashboard, get_leaderboard
from qr_scanner import scan_qr as scan_qr_camera
from dashboard import open_dashboard

user_id = None  # Global user id

# ---------- FUNCTIONS ----------

def register():
    name = name_entry.get()
    email = email_entry.get()
    password = password_entry.get()
    res = register_user(name, email, password)
    messagebox.showinfo("Register", str(res))

def login():
    global user_id
    email = email_entry.get()
    password = password_entry.get()
    res = login_user(email, password)
    if res.get("success"):
        user_id = res["user_id"]
        messagebox.showinfo("Login", "Login successful!")
    else:
        messagebox.showerror("Login", "Login failed!")

def scan_points():
    if not user_id:
        messagebox.showerror("Error", "Login first")
        return
    qr_data = scan_qr_camera()  # get QR from camera
    if qr_data:
        res = scan_qr(user_id, qr_data)  # send to backend
        messagebox.showinfo("Points Added", str(res))

def open_user_dashboard():
    if not user_id:
        messagebox.showerror("Error", "Login first")
        return
    open_dashboard(user_id)

# ---------- TKINTER GUI ----------

root = tk.Tk()
root.title("Waste App - User Frontend")
root.geometry("350x400")

tk.Label(root, text="Name").pack(pady=5)
name_entry = tk.Entry(root)
name_entry.pack()

tk.Label(root, text="Email").pack(pady=5)
email_entry = tk.Entry(root)
email_entry.pack()

tk.Label(root, text="Password").pack(pady=5)
password_entry = tk.Entry(root, show="*")
password_entry.pack()

tk.Button(root, text="Register", command=register, width=20).pack(pady=5)
tk.Button(root, text="Login", command=login, width=20).pack(pady=5)
tk.Button(root, text="Scan QR", command=scan_points, width=20).pack(pady=5)
tk.Button(root, text="Dashboard", command=open_user_dashboard, width=20).pack(pady=5)

root.mainloop()