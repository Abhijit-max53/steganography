from PIL import Image

def text_to_bin(text):
    return ''.join(format(ord(char), '08b') for char in text)

def bin_to_text(binary):
    chars = [binary[i:i+8] for i in range(0, len(binary), 8)]
    return ''.join([chr(int(char, 2)) for char in chars])

def encode_image(input_path, message, output_path):
    img = Image.open(input_path)
    if img.mode != 'RGB':
        img = img.convert('RGB')

    binary = text_to_bin(message) + '1111111111111110'  # EOF marker
    pixels = list(img.getdata())

    new_pixels = []
    bin_index = 0

    for pixel in pixels:
        r, g, b = pixel
        if bin_index < len(binary):
            r = r & ~1 | int(binary[bin_index])
            bin_index += 1
        if bin_index < len(binary):
            g = g & ~1 | int(binary[bin_index])
            bin_index += 1
        if bin_index < len(binary):
            b = b & ~1 | int(binary[bin_index])
            bin_index += 1
        new_pixels.append((r, g, b))
    img.putdata(new_pixels)
    img.save(output_path)

def decode_image(stego_path):
    img = Image.open(stego_path)
    pixels = list(img.getdata())

    binary = ''
    for pixel in pixels:
        for color in pixel:
            binary += str(color & 1)
    end_marker = '1111111111111110'
    if end_marker in binary:
        binary = binary[:binary.find(end_marker)]
    return bin_to_text(binary)






import tkinter as tk
from tkinter import filedialog, messagebox
from stego_utils import encode_image, decode_image

def browse_image():
    path = filedialog.askopenfilename()
    entry_img.delete(0, tk.END)
    entry_img.insert(0, path)

def encode():
    input_path = entry_img.get()
    message = text_box.get("1.0", tk.END).strip()
    output_path = "encoded_image.png"
    try:
        encode_image(input_path, message, output_path)
        messagebox.showinfo("Success", f"Message encoded into {output_path}")
    except Exception as e:
        messagebox.showerror("Error", str(e))

def decode():
    input_path = entry_img.get()
    try:
        msg = decode_image(input_path)
        output_box.delete("1.0", tk.END)
        output_box.insert(tk.END, msg)
    except Exception as e:
        messagebox.showerror("Error", str(e))

app = tk.Tk()
app.title("Image Steganography")

tk.Label(app, text="Image Path:").pack()
entry_img = tk.Entry(app, width=50)
entry_img.pack()
tk.Button(app, text="Browse", command=browse_image).pack()

tk.Label(app, text="Enter message to hide:").pack()
text_box = tk.Text(app, height=4, width=50)
text_box.pack()

tk.Button(app, text="Encode Message", command=encode).pack(pady=5)
tk.Button(app, text="Decode Message", command=decode).pack(pady=5)

tk.Label(app, text="Decoded Output:").pack()
output_box = tk.Text(app, height=4, width=50)
output_box.pack()

app.mainloop()
