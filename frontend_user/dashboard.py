import tkinter as tk
from tkinter import messagebox
from api import get_dashboard, get_leaderboard, redeem_coupon

def open_dashboard(user_id):
    dashboard = tk.Toplevel()
    dashboard.title("Waste App Dashboard")
    dashboard.geometry("600x500")
    dashboard.configure(bg="#f0f2f5")

    # ----------------- User Points -----------------
    points_frame = tk.Frame(dashboard, bg="#4caf50", padx=20, pady=20)
    points_frame.pack(pady=20, fill="x")

    user_data = get_dashboard(user_id)
    points = user_data.get("points", 0)
    tk.Label(points_frame, text=f"Your Points: {points}", font=("Helvetica", 18), bg="#4caf50", fg="white").pack()

    # ----------------- Leaderboard -----------------
    leaderboard_frame = tk.Frame(dashboard, bg="#ffffff", padx=20, pady=10)
    leaderboard_frame.pack(pady=10, fill="x")

    tk.Label(leaderboard_frame, text="🏆 Leaderboard", font=("Helvetica", 16, "bold"), bg="#ffffff").pack()

    leaderboard = get_leaderboard()
    for i, user in enumerate(leaderboard, start=1):
        tk.Label(leaderboard_frame, text=f"{i}. {user['name']} - {user['points']} pts",
                 font=("Helvetica", 12), bg="#ffffff").pack(anchor="w")

    # ----------------- Coupon Redemption -----------------
    coupon_frame = tk.Frame(dashboard, bg="#2196f3", padx=20, pady=20)
    coupon_frame.pack(pady=20, fill="x")

    tk.Label(coupon_frame, text="Redeem Coupon", font=("Helvetica", 16), bg="#2196f3", fg="white").pack()

    coupon_entry = tk.Entry(coupon_frame, font=("Helvetica", 12))
    coupon_entry.pack(pady=10)

    def redeem():
        coupon_id = coupon_entry.get()
        res = redeem_coupon(user_id, coupon_id)
        messagebox.showinfo("Redeem", str(res))

    tk.Button(coupon_frame, text="Redeem", font=("Helvetica", 12), command=redeem, bg="white").pack(pady=5)