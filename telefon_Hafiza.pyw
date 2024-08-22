import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import numpy as np
import cv2
import os
import threading  # threading modülünü ekleyin

#Gerekenler
#ModuleNotFoundError: No module named 'numpy' kod = python -m pip install numpy
#ModuleNotFoundError: No module named 'cv2' kod = python -m pip install opencv-python
#python -m PyInstaller --onefile --noconsole telefon_Hafiza.pyw
#python -m PyInstaller --onefile --noconsole --distpath "C:\KendiKlasorun" telefon_Hafiza.pyw

# Video oluşturmak için fonksiyon
def create_video(filename, size_gb, progress_var, progress_label):
    # Hedef boyutu byte cinsinden hesapla
    target_size_bytes = size_gb * 1024 * 1024 * 1024
    width, height = 1920, 1080  # Full HD çözünürlük
    frame_size = width * height * 3  # RGB için piksel başına 3 byte
    frame_rate = 30

    # VideoWriter objesi oluştur
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(filename, fourcc, frame_rate, (width, height))

    current_size = 0

    try:
        while current_size < target_size_bytes:
            # Rastgele bir frame oluştur
            frame = np.random.randint(0, 256, (height, width, 3), dtype=np.uint8)
            out.write(frame)

            # Güncel boyutu al
            current_size = os.path.getsize(filename)

            # İlerleme yüzdesini hesapla
            progress_percentage = (current_size / target_size_bytes) * 100

            # İlerleme çubuğunu ve etiketi güncelle
            progress_var.set(progress_percentage)
            progress_label.config(text=f"{progress_percentage:.2f}%")
            root.update_idletasks()

        messagebox.showinfo("Başarılı", f"Video başarıyla kaydedildi: {filename}")
    except Exception as e:
        messagebox.showerror("Hata", f"Video oluşturma sırasında bir hata oluştu: {e}")

    out.release()
    cv2.destroyAllWindows()

# GB cinsinden boyutu byte'a dönüştüren işlev
def gb_to_bytes(gb):
    bytes = gb * (1024 * 1024 * 1024)
    return bytes

# Byte cinsinden değeri GB'a dönüştüren işlev
def bytes_to_gb(bytes):
    gb = bytes / (1024 * 1024 * 1024)
    return gb

# Kullanıcı tarafından girilen byte değerini GB'a dönüştüren işlev
def convert_bytes_to_gb():
    try:
        bytes_value = float(entry_bytes.get())
        gb_value = bytes_to_gb(bytes_value)
        entry_size.delete(0, tk.END)  # Mevcut değeri temizle
        entry_size.insert(0, f"{gb_value:.2f}")  # GB değerini gir
    except ValueError:
        messagebox.showerror("Hata", "Geçersiz giriş")

# Video oluşturma işlevi (thread içinde çalıştırılacak)
def on_create_video():
    try:
        size_gb = float(entry_size.get())
        filename = entry_filename.get().strip()  # Başında veya sonunda boşlukları kaldır
        if not filename:
            raise ValueError("Dosya adı boş olamaz.")

        # Dosya kaydetme penceresini aç
        file_path = filedialog.asksaveasfilename(defaultextension=".mp4",
                                                 filetypes=[("MP4 dosyaları", "*.mp4")],
                                                 title="Videoyu Kaydet",
                                                 initialfile=filename)  # Pencerede başlangıç dosya adını ayarla

        if file_path:
            progress_var.set(0)
            progress_label.config(text="0%")
            
            # Yeni bir thread başlat ve video oluşturma işlemini başlat
            threading.Thread(target=create_video, args=(file_path, size_gb, progress_var, progress_label)).start()
    except ValueError as ve:
        messagebox.showerror("Hata", str(ve))
    except Exception as e:
        messagebox.showerror("Hata", f"Bir hata oluştu: {e}")

# Ana pencere oluştur
root = tk.Tk()
root.title("Video Oluşturucu")
root.geometry("343x400")  # Pencere boyutunu 343x400 piksel olarak ayarla
root.configure(bg='#282828')  # Pencere arka plan rengini beyaz olarak ayarla

# Widget'ları oluştur ve aralıklarla yerleştir
tk.Label(root, text="Boyut (Bytes):", fg="blue", bg='#282828').grid(row=0, column=0, pady=10, padx=10, sticky="w")
entry_bytes = tk.Entry(root)
entry_bytes.grid(row=0, column=1, pady=10, padx=10)

# Byte girişi için alan ve dönüştürme butonu
convert_button = tk.Button(root, text="GB'ye Çevir", command=convert_bytes_to_gb)
convert_button.grid(row=0, column=2, pady=10, padx=10)

tk.Label(root, text="Boyut (GB):", fg="red", bg='#282828').grid(row=1, column=0, pady=10, padx=10, sticky="w")
entry_size = tk.Entry(root)
entry_size.grid(row=1, column=1, pady=10, padx=10)

tk.Label(root, text="Dosya Adı:", fg="green", bg='#282828').grid(row=2, column=0, pady=10, padx=10, sticky="w")
entry_filename = tk.Entry(root)
entry_filename.grid(row=2, column=1, pady=10, padx=10)

# Yeşil arka planlı "Video Oluştur" butonunu oluştur ve yerleştir
create_button = tk.Button(root, text="Video Oluştur", command=on_create_video, bg='green')
create_button.grid(row=2, column=2, pady=10, padx=10, sticky="e")

# İlerleme çubuğunu aralıklı olarak yerleştir
progress_var = tk.DoubleVar()
progress_bar = ttk.Progressbar(root, variable=progress_var, maximum=100)
progress_bar.grid(row=3, columnspan=3, pady=10, padx=10, sticky="we")

# İlerleme etiketini aralıklı olarak yerleştir
progress_label = tk.Label(root, text="0%", bg='#282828', fg="white")
progress_label.grid(row=4, columnspan=3, pady=10, padx=10, sticky="we")

# Tkinter olay döngüsünü başlat
root.mainloop()
