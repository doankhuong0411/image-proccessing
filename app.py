import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
import numpy as np
from sklearn.cluster import KMeans
import os

class ColorQuantizationApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Color Quantization")
        self.root.geometry("1280x800")

        # tên Title của app
        header_label = tk.Label(root, text="Color Quantization", justify='center', font=("Helvetica", 20))
        header_label.grid(row=0, column=0, columnspan=5, pady=10)

        # Hàng thứ 2
        # Cột 1
        self.image_label = tk.Label(root, text="Chưa có ảnh", font=("Helvetica", 12))
        self.image_label.grid(row=1, column=0, padx=20)

        self.load_button = tk.Button(root, text="Chọn ảnh", command=self.load_image)
        self.load_button.grid(row=1, column=1)

        # Cột 2
        self.k_entry_label = tk.Label(root, text="Nhập số K:")
        self.k_entry_label.grid(row=1, column=2)

        self.k_var = tk.StringVar()
        self.k_entry = tk.Entry(root, textvariable=self.k_var)
        self.k_entry.grid(row=1, column=3)

        self.apply_button = tk.Button(root, text="Áp dụng", command=self.apply_quantization)
        self.apply_button.grid(row=1, column=4)

        # Cột 3
        self.processed_image_label = tk.Label(root, text="Ảnh sau khi xử lý", font=("Helvetica", 12))
        self.processed_image_label.grid(row=1, column=5, padx=20)

        # Hàng thứ 3
        self.count_button = tk.Button(root, text="Đếm số pixel và màu sắc", command=self.count_pixels_and_colors)
        self.count_button.grid(row=2, column=4, pady=10)

    def load_image(self):
        file_path = filedialog.askopenfilename(title="Chọn ảnh", filetypes=[("Image files", "*.png;*.jpg;*.jpeg")])
        if file_path:
            image = Image.open(file_path)
            image.thumbnail((400, 400))
            photo = ImageTk.PhotoImage(image)

            self.image_label.config(image=photo)
            self.image_label.image = photo
            self.original_image = np.array(image)

    def apply_quantization(self):
        if hasattr(self, 'original_image'):
            try:
                num_colors = int(self.k_var.get())
                pixels = self.original_image.reshape((-1, 3))

                kmeans = KMeans(n_clusters=num_colors)
                kmeans.fit(pixels)

                new_colors = kmeans.cluster_centers_.astype(int)
                quantized_image = new_colors[kmeans.labels_].reshape(self.original_image.shape)

                quantized_image = Image.fromarray(quantized_image.astype(np.uint8))
                quantized_image.thumbnail((400, 400))
                processed_photo = ImageTk.PhotoImage(quantized_image)

                self.processed_image_label.config(image=processed_photo)
                self.processed_image_label.image = processed_photo

                # Lưu trữ ảnh sau khi xử lý để sử dụng trong so sánh
                self.processed_image = np.array(quantized_image)

                # Lưu ảnh xuống thư mục chứa code
                script_dir = os.path.dirname(os.path.abspath(__file__))
                output_path = os.path.join(script_dir, "done_image.jpg")
                quantized_image.save(output_path)

            except ValueError:
                tk.messagebox.showerror("Lỗi", "Vui lòng nhập một số nguyên dương cho giá trị K.")


    def count_pixels_and_colors(self):
        if hasattr(self, 'original_image'):
            num_pixels_original = np.prod(self.original_image.shape[:2])
            num_colors_original = len(np.unique(self.original_image.reshape(-1, 3), axis=0))

        if hasattr(self, 'processed_image'):
            num_pixels_processed = np.prod(self.processed_image.shape[:2])
            num_colors_processed = len(np.unique(self.processed_image.reshape(-1, 3), axis=0))

            messagebox.showinfo("Thông tin", f"Ảnh gốc:\nSố pixel: {num_pixels_original}\nSố màu sắc: {num_colors_original}\n\n"
                                            f"Ảnh sau khi xử lý:\nSố pixel: {num_pixels_processed}\nSố màu sắc: {num_colors_processed}")
        else:
            messagebox.showinfo("Thông tin", f"Ảnh gốc:\nSố pixel: {num_pixels_original}\nSố màu sắc: {num_colors_original}")

    
if __name__ == "__main__":
    root = tk.Tk()
    app = ColorQuantizationApp(root)
    root.mainloop()
