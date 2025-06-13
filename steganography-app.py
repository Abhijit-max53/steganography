import tkinter as tk
from tkinter import filedialog, messagebox
from tkinterdnd2 import DND_FILES, TkinterDnD
from PIL import Image
import numpy as np
import os

def text_to_bin(text):
    return ''.join(format(ord(char), '08b') for char in text)

def bin_to_text(binary):
    chars = [binary[i:i+8] for i in range(0, len(binary), 8)]
    return ''.join(chr(int(char, 2)) for char in chars)

def hide_text(image_path, message, output_path):
    img = Image.open(image_path).convert('RGB')
    data = np.array(img)

    bin_message = text_to_bin(message) + '1111111111111110'  # End marker
    msg_index = 0

    for row in data:
        for pixel in row:
            for i in range(3):
                if msg_index < len(bin_message):
                    pixel[i] = pixel[i] & ~1 | int(bin_message[msg_index])
                    msg_index += 1

    encoded_img = Image.fromarray(data)
    encoded_img.save(output_path, format='PNG')

def extract_text(image_path):
    img = Image.open(image_path)
    data = np.array(img)

    binary = ''
    for row in data:
        for pixel in row:
            for i in range(3):
                binary += str(pixel[i] & 1)
                if binary[-16:] == '1111111111111110':
                    return bin_to_text(binary[:-16])
    return ""

class StegApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Steganography Project - Abhijit Modak")
        self.image_path = ""

        self.label = tk.Label(root, text="Enter your secret message:")
        self.label.pack()

        self.message_entry = tk.Entry(root, width=50)
        self.message_entry.pack()

        self.browse_btn = tk.Button(root, text="Select Image", command=self.select_image)
        self.browse_btn.pack()

        self.image_label = tk.Label(root, text="No image selected")
        self.image_label.pack()

        self.drop_label = tk.Label(root, text="Or drag and drop image here", fg="blue")
        self.drop_label.pack()
        self.drop_label.drop_target_register(DND_FILES)
        self.drop_label.dnd_bind("<<Drop>>", self.drop_image)

        self.encode_btn = tk.Button(root, text="Encode & Save", command=self.encode)
        self.encode_btn.pack()

        self.decode_btn = tk.Button(root, text="Decode Message", command=self.decode)
        self.decode_btn.pack()

    def select_image(self):
        path = filedialog.askopenfilename(filetypes=[("Image Files", "*.png *.jpg *.jpeg")])
        if path:
            self.image_path = path
            self.image_label.config(text=os.path.basename(path))

    def drop_image(self, event):
        path = event.data.strip('{}')
        if path.lower().endswith(('.png', '.jpg', '.jpeg')):
            self.image_path = path
            self.image_label.config(text=os.path.basename(path), fg="black")
        else:
            messagebox.showerror("Error", "Unsupported file type")

    def encode(self):
        if not self.image_path:
            messagebox.showwarning("Warning", "No image selected")
            return
        message = self.message_entry.get()
        if not message:
            messagebox.showwarning("Warning", "No message entered")
            return
        save_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG Image", "*.png")])
        if save_path:
            hide_text(self.image_path, message, save_path)
            messagebox.showinfo("Success", "Message hidden and image saved!")

    def decode(self):
        if not self.image_path:
            messagebox.showwarning("Warning", "No image selected")
            return
        hidden_msg = extract_text(self.image_path)
        messagebox.showinfo("Decoded Message", hidden_msg)

if __name__ == "__main__":
    root = TkinterDnD.Tk()
    app = StegApp(root)
    root.mainloop()
