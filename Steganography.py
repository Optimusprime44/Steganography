import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image
import numpy as np


# Convert text to binary
def text_to_binary(text):
    return ''.join([format(ord(i), '08b') for i in text])


# Convert binary to text
def binary_to_text(binary_str):
    binary_values = [binary_str[i:i + 8] for i in range(0, len(binary_str), 8)]
    ascii_str = ''.join([chr(int(b, 2)) for b in binary_values])
    return ascii_str


# Encode data into an image
def encode_image(image_path, text, output_image):
    img = Image.open(image_path)
    img_array = np.array(img)

    # Flatten the image array
    flat_image = img_array.flatten()

    # Convert the text to binary
    binary_text = text_to_binary(text) + '1111111111111110'  # End of message marker

    # Check if the image has enough pixels to hide the message
    if len(binary_text) > len(flat_image):
        raise ValueError("Text is too long to encode in the image.")

    # Modify LSB of pixels to store the binary message
    for i in range(len(binary_text)):
        flat_image[i] = flat_image[i] & ~1 | int(binary_text[i])

    # Reshape the array and save the new image
    encoded_img = flat_image.reshape(img_array.shape)
    encoded_image = Image.fromarray(encoded_img)

    # Save the encoded image to the user-specified path
    encoded_image.save(output_image)
    print(f"Message encoded and saved as {output_image}.")


# Decode the message from an image
def decode_image(image_path):
    img = Image.open(image_path)
    img_array = np.array(img)

    # Flatten the image array
    flat_image = img_array.flatten()

    # Extract LSBs and construct the binary string
    binary_text = ''
    for pixel in flat_image:
        binary_text += str(pixel & 1)

        # Check for the end of the message marker
        if binary_text.endswith('1111111111111110'):
            break

    # Convert binary to text (excluding the end marker)
    hidden_text = binary_to_text(binary_text[:-16])
    print(f"Decoded message: {hidden_text}")
    return hidden_text


# GUI Application
class SteganographyApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Steganography Image Encoder/Decoder")
        self.root.geometry("500x400")
        self.root.configure(bg="#f0f4f8")

        # Title Label
        self.title_label = tk.Label(root, text="Steganography Tool", font=("Helvetica", 20, "bold"), bg="#34495e",
                                    fg="white", padx=10, pady=10)
        self.title_label.pack(fill=tk.X)

        # Frame for the options
        self.frame = tk.Frame(root, bg="#f0f4f8")
        self.frame.pack(pady=20)

        # Choose Image Button
        self.choose_image_button = tk.Button(self.frame, text="Choose Image", command=self.choose_image, bg="#3498db",
                                             fg="white", font=("Helvetica", 12), width=15)
        self.choose_image_button.grid(row=0, column=0, padx=10, pady=10)

        # Selected Image Path Label
        self.image_path_label = tk.Label(self.frame, text="No image selected", font=("Helvetica", 10), bg="#f0f4f8",
                                         wraplength=300)
        self.image_path_label.grid(row=0, column=1)

        # Message Label and Entry
        self.message_label = tk.Label(self.frame, text="Message to Encode:", bg="#f0f4f8", font=("Helvetica", 12))
        self.message_label.grid(row=1, column=0, padx=10, pady=10)
        self.message_entry = tk.Entry(self.frame, width=40, font=("Helvetica", 12))
        self.message_entry.grid(row=1, column=1, pady=10)

        # Encode and Decode Buttons
        self.encode_button = tk.Button(root, text="Encode Message", command=self.encode_message, bg="#2ecc71",
                                       fg="white", font=("Helvetica", 12), width=20)
        self.encode_button.pack(pady=10)
        self.decode_button = tk.Button(root, text="Decode Message", command=self.decode_message, bg="#e74c3c",
                                       fg="white", font=("Helvetica", 12), width=20)
        self.decode_button.pack(pady=10)

    def choose_image(self):
        file_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.png;*.jpg;*.jpeg")])
        self.image_path_label.config(text=file_path)

    def encode_message(self):
        image_path = self.image_path_label.cget("text")
        message = self.message_entry.get()

        if not image_path or image_path == "No image selected":
            messagebox.showerror("Error", "Please select an image.")
            return

        if not message:
            messagebox.showerror("Error", "Please enter a message to encode.")
            return

        # Use asksaveasfilename to get the path and filename from the user
        output_image = filedialog.asksaveasfilename(defaultextension=".png",
                                                    filetypes=[("PNG files", "*.png"), ("JPEG files", "*.jpg"),
                                                               ("All files", "*.*")],
                                                    title="Save the Encoded Image")

        if not output_image:
            messagebox.showerror("Error", "No save path specified.")
            return

        try:
            encode_image(image_path, message, output_image)
            messagebox.showinfo("Success", f"Message encoded and saved as {output_image}")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def decode_message(self):
        image_path = self.image_path_label.cget("text")

        if not image_path or image_path == "No image selected":
            messagebox.showerror("Error", "Please select an image.")
            return

        try:
            hidden_text = decode_image(image_path)
            messagebox.showinfo("Decoded Message", hidden_text)
        except Exception as e:
            messagebox.showerror("Error", str(e))


# Main Application
if __name__ == "__main__":
    root = tk.Tk()
    app = SteganographyApp(root)
    root.mainloop()
