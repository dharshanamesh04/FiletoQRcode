import customtkinter as ctk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
import qrcode
import os

# App setup
ctk.set_appearance_mode("dark")   # or "light"
ctk.set_default_color_theme("blue")

app = ctk.CTk()
app.title("✨ QR Code Generator")
app.geometry("850x750")
app.configure(fg_color=("#BBD2C5", "#2A2A72"))  # gradient-like background tone

# ---------- Functions ----------
def browse_location():
    folder = filedialog.askdirectory()
    if folder:
        location_entry.delete(0, "end")
        location_entry.insert(0, folder)

def generate_qr_code():
    try:
        folder = location_entry.get().strip()
        if not folder:
            messagebox.showerror("Error", "Please select a save location!")
            return

        file_name = name_entry.get().strip()
        if not file_name:
            messagebox.showerror("Error", "Please enter a QR Code name!")
            return

        qr_version = size_entry.get().strip()
        if not qr_version.isdigit() or not (1 <= int(qr_version) <= 40):
            messagebox.showerror("Error", "Size must be between 1 and 40!")
            return

        qr = qrcode.QRCode(version=int(qr_version), box_size=10, border=4)
        qr.add_data(text_entry.get())
        qr.make(fit=True)
        img = qr.make_image(fill_color="black", back_color="white")

        os.makedirs(folder, exist_ok=True)
        file_path = os.path.join(folder, f"{file_name}.png")
        img.save(file_path)

        # Preview
        img_preview = img.resize((250, 250))
        img_tk = ImageTk.PhotoImage(img_preview)
        preview_label.configure(image=img_tk, text="")
        preview_label.image = img_tk

        messagebox.showinfo("Success", f"QR Code saved at:\n{file_path}")

    except Exception as e:
        messagebox.showerror("Error", str(e))

# ---------- Gradient Frame ----------
main_frame = ctk.CTkFrame(app, corner_radius=25, fg_color=("white", "#1F1F2E"))
main_frame.place(relx=0.5, rely=0.5, anchor="center", relwidth=0.85, relheight=0.9)

# ---------- Title ----------
title = ctk.CTkLabel(main_frame, text="✨ QR Code Generator", font=("Poppins", 28, "bold"))
title.pack(pady=(30, 10))

desc = ctk.CTkLabel(main_frame, text="Create beautiful QR Codes instantly", font=("Poppins", 15))
desc.pack(pady=(0, 20))

# ---------- Inputs ----------
text_entry = ctk.CTkEntry(main_frame, placeholder_text="Enter text or URL", width=500, height=45, corner_radius=12)
text_entry.pack(pady=10)

location_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
location_frame.pack(pady=10)

location_entry = ctk.CTkEntry(location_frame, placeholder_text="Select save location", width=400, height=45)
location_entry.pack(side="left", padx=10)
browse_btn = ctk.CTkButton(location_frame, text="Browse", width=100, corner_radius=10, command=browse_location)
browse_btn.pack(side="left", padx=5)

name_entry = ctk.CTkEntry(main_frame, placeholder_text="Enter QR Code name", width=500, height=45)
name_entry.pack(pady=10)

size_entry = ctk.CTkEntry(main_frame, placeholder_text="Enter size (1–40)", width=500, height=45)
size_entry.pack(pady=10)

generate_btn = ctk.CTkButton(main_frame, text="Generate QR Code", width=260, height=50,
                             corner_radius=15, fg_color="#7F00FF", hover_color="#E100FF",
                             font=("Poppins", 15, "bold"), command=generate_qr_code)
generate_btn.pack(pady=25)

# ---------- Preview Section ----------
preview_frame = ctk.CTkFrame(main_frame, corner_radius=15, fg_color=("#E8E8E8", "#141414"))
preview_frame.pack(pady=10)
preview_label = ctk.CTkLabel(preview_frame, text="QR Preview", width=260, height=260,
                             corner_radius=12, fg_color=("white", "#1E1E1E"),
                             text_color=("gray20", "gray80"))
preview_label.pack(padx=20, pady=20)

# ---------- Theme Toggle ----------
def toggle_theme():
    current = ctk.get_appearance_mode()
    ctk.set_appearance_mode("light" if current == "dark" else "dark")

theme_btn = ctk.CTkButton(app, text="🌓 Toggle Theme", width=150, corner_radius=10, command=toggle_theme)
theme_btn.place(x=20, y=20)

app.mainloop()

