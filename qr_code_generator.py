import qrcode
from tkinter import *
from tkinter import messagebox
import os

def generate_qr_code():
    try:
        folder = location_entry.get().strip()
        if not folder:
            messagebox.showerror("Error", "Please enter a save location!")
            return
        
        folder = folder.replace("\\", "/")
        
        if not os.path.exists(folder):
            os.makedirs(folder)
        
        file_name = name_entry.get().strip()
        if not file_name:
            messagebox.showerror("Error", "Please enter a file name!")
            return
        
        qr_version = size_entry.get().strip()
        if not qr_version.isdigit() or not (1 <= int(qr_version) <= 40):
            messagebox.showerror("Error", "Size must be a number between 1 and 40!")
            return
        
        qr = qrcode.QRCode(
            version=int(qr_version),
            box_size=10,
            border=5
        )
        qr.add_data(text_entry.get())
        qr.make(fit=True)
        img = qr.make_image()
        
        file_path = os.path.join(folder, f"{file_name}.png")
        img.save(file_path)
        messagebox.showinfo("Success", f"QR Code saved successfully at:\n{file_path}")
    
    except Exception as e:
        messagebox.showerror("Error", f"Failed to generate QR code:\n{e}")

window = Tk()
window.title("QR Code Generator")
window.geometry("700x700")
window.config(bg='SteelBlue3')

def create_input_frame(parent, label_text, y_pos, width=0.7, height=0.12):
    frame = Frame(parent, bg="SteelBlue3")
    frame.place(relx=0.1, rely=y_pos, relwidth=width, relheight=height)
    Label(frame, text=label_text, bg="SteelBlue3", fg='azure', font=('Courier',13,'bold')).place(relx=0.05, rely=0.1)
    entry = Entry(frame, font=('Century',12))
    entry.place(relx=0.05, rely=0.5, relwidth=0.9, relheight=0.4)
    return entry

heading_frame = Frame(window, bg="azure", bd=5)
heading_frame.place(relx=0.15, rely=0.05, relwidth=0.7, relheight=0.1)
Label(heading_frame, text="Generate QR Code", bg='azure', font=('Times', 20, 'bold')).place(relx=0, rely=0, relwidth=1, relheight=1)

text_entry = create_input_frame(window, "Enter text/URL:", 0.15)
location_entry = create_input_frame(window, "Enter save location:", 0.3)
name_entry = create_input_frame(window, "Enter QR Code name:", 0.45)
size_entry = create_input_frame(window, "Enter size (1-40):", 0.6)

Button(window, text='Generate Code', font=('Courier',15,'normal'), command=generate_qr_code).place(relx=0.35, rely=0.75, relwidth=0.25, relheight=0.05)

window.mainloop()
