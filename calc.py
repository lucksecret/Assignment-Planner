import tkinter as tk
from tkinter import messagebox    
import ttkbootstrap as ttk
from ttkbootstrap.constants import PRIMARY, SECONDARY, OUTLINE
def kalkulator_barisan():
    root = ttk.Window(themename="litera") 
    root.title("Kalkulator Aritmatika dan Geometri")
    root.geometry("700x600") 
    a_arit_var = tk.StringVar()
    b_arit_var = tk.StringVar()
    n_arit_var = tk.StringVar()
    hasil_arit_un_var = tk.StringVar(value="U_n: -")
    hasil_arit_sn_var = tk.StringVar(value="S_n: -")
    a_geom_var = tk.StringVar()
    r_geom_var = tk.StringVar()
    n_geom_var = tk.StringVar()
    hasil_geom_un_var = tk.StringVar(value="U_n: -")
    hasil_geom_sn_var = tk.StringVar(value="S_n: -")

    def validasi_input_int(var_entri, nama_bidang):
        try:
            nilai = int(var_entri.get())
            if nilai <= 0:
                messagebox.showerror("Input Tidak Valid", f"Nilai untuk '{nama_bidang}' harus bilangan bulat positif.")
                return None
            return nilai
        except ValueError:
            messagebox.showerror("Input Tidak Valid", f"Nilai untuk '{nama_bidang}' harus berupa bilangan bulat.")
            return None

    def kalkulasi_aritmetika():
        a = validasi_input_int(a_arit_var, "Suku Pertama (a) Aritmetika")
        b = validasi_input_int(b_arit_var, "Beda (b) Aritmetika")
        n = validasi_input_int(n_arit_var, "Suku/Jumlah (n) Aritmetika")
        if a is not None and b is not None and n is not None:
            un = a + (n - 1) * b
            hasil_arit_un_var.set(f"U_{n}: {un}")
            sn_float = (n / 2.0) * (2 * a + (n - 1) * b)
            hasil_arit_sn_var.set(f"S_{n}: {int(sn_float)}")
        else:
            hasil_arit_un_var.set("U_n: -")
            hasil_arit_sn_var.set("S_n: -")

    def reset_bidang_aritmetika():
        a_arit_var.set("")
        b_arit_var.set("")
        n_arit_var.set("")
        hasil_arit_un_var.set("U_n: -")
        hasil_arit_sn_var.set("S_n: -")

    def kalkulasi_geometri():
        a = validasi_input_int(a_geom_var, "Suku Pertama (a) Geometri")
        r = validasi_input_int(r_geom_var, "Rasio (r) Geometri")
        n = validasi_input_int(n_geom_var, "Suku/Jumlah (n) Geometri")
        if a is not None and r is not None and n is not None:
            try:
                un_val = a * (r ** (n - 1))
                hasil_geom_un_var.set(f"U_{n}: {int(un_val)}")
            except OverflowError:
                messagebox.showerror("Kesalahan U_n", "Hasil U_n terlalu besar.")
                hasil_geom_un_var.set("U_n: Luber")
            except TypeError:
                messagebox.showerror("Kesalahan U_n", "Input U_n tidak valid untuk pemangkatan.")
                hasil_geom_un_var.set("U_n: Kesalahan Input")
            try:
                if r == 1:
                    sn_nilai = a * n
                else:
                    sn_float = a * ((r ** n) - 1) / (r - 1.0)
                    sn_nilai = int(sn_float)
                hasil_geom_sn_var.set(f"S_{n}: {sn_nilai}")
            except OverflowError:
                messagebox.showerror("Kesalahan S_n", "Hasil S_n terlalu besar.")
                hasil_geom_sn_var.set("S_n: Luber")
            except ZeroDivisionError:
                messagebox.showerror("Kesalahan S_n", "Pembagian S_n dengan nol.")
                hasil_geom_sn_var.set("S_n: Kesalahan")
            except TypeError:
                messagebox.showerror("Kesalahan S_n", "Input S_n tidak valid untuk pemangkatan.")
                hasil_geom_sn_var.set("S_n: Kesalahan Input")
        else:
            hasil_geom_un_var.set("U_n: -")
            hasil_geom_sn_var.set("S_n: -")

    def reset_bidang_geometri():
        a_geom_var.set("")
        r_geom_var.set("")
        n_geom_var.set("")
        hasil_geom_un_var.set("U_n: -")
        hasil_geom_sn_var.set("S_n: -")
    bingkai_aritmetika = ttk.LabelFrame(root, text="Barisan Aritmetika (Bulat)", padding=15)
    bingkai_aritmetika.pack(padx=10, pady=(10,5), fill="x", expand=False)
    ttk.Label(bingkai_aritmetika, text="Suku Pertama (a):").grid(row=0, column=0, padx=5, pady=5, sticky="w")
    ttk.Entry(bingkai_aritmetika, textvariable=a_arit_var, width=15).grid(row=0, column=1, padx=5, pady=5)
    ttk.Label(bingkai_aritmetika, text="Beda (b):").grid(row=1, column=0, padx=5, pady=5, sticky="w")
    ttk.Entry(bingkai_aritmetika, textvariable=b_arit_var, width=15).grid(row=1, column=1, padx=5, pady=5)
    ttk.Label(bingkai_aritmetika, text="Suku ke/Jumlah (n):").grid(row=2, column=0, padx=5, pady=5, sticky="w")
    ttk.Entry(bingkai_aritmetika, textvariable=n_arit_var, width=15).grid(row=2, column=1, padx=5, pady=5)
    bingkai_tombol_arit = ttk.Frame(bingkai_aritmetika)
    bingkai_tombol_arit.grid(row=3, column=0, columnspan=2, pady=10)
    ttk.Button(bingkai_tombol_arit, text="Hitung Semua", command=kalkulasi_aritmetika, bootstyle=PRIMARY).pack(side=tk.LEFT, padx=5)
    ttk.Button(bingkai_tombol_arit, text="Reset", command=reset_bidang_aritmetika, bootstyle=(SECONDARY, OUTLINE)).pack(side=tk.LEFT, padx=5)
    ttk.Label(bingkai_aritmetika, textvariable=hasil_arit_un_var).grid(row=4, column=0, columnspan=2, sticky="w", padx=5, pady=(5,0))
    ttk.Label(bingkai_aritmetika, textvariable=hasil_arit_sn_var).grid(row=5, column=0, columnspan=2, sticky="w", padx=5)
    bingkai_geometri = ttk.LabelFrame(root, text="Barisan Geometri (Bulat)", padding=15)
    bingkai_geometri.pack(padx=10, pady=(5,10), fill="x", expand=False)
    ttk.Label(bingkai_geometri, text="Suku Pertama (a):").grid(row=0, column=0, padx=5, pady=5, sticky="w")
    ttk.Entry(bingkai_geometri, textvariable=a_geom_var, width=15).grid(row=0, column=1, padx=5, pady=5)
    ttk.Label(bingkai_geometri, text="Rasio (r):").grid(row=1, column=0, padx=5, pady=5, sticky="w")
    ttk.Entry(bingkai_geometri, textvariable=r_geom_var, width=15).grid(row=1, column=1, padx=5, pady=5)
    ttk.Label(bingkai_geometri, text="Suku ke/Jumlah (n):").grid(row=2, column=0, padx=5, pady=5, sticky="w")
    ttk.Entry(bingkai_geometri, textvariable=n_geom_var, width=15).grid(row=2, column=1, padx=5, pady=5)
    bingkai_tombol_geom = ttk.Frame(bingkai_geometri)
    bingkai_tombol_geom.grid(row=3, column=0, columnspan=2, pady=10)
    ttk.Button(bingkai_tombol_geom, text="Hitung Semua", command=kalkulasi_geometri, bootstyle=PRIMARY).pack(side=tk.LEFT, padx=5)
    ttk.Button(bingkai_tombol_geom, text="Reset", command=reset_bidang_geometri, bootstyle="secondary-outline").pack(side=tk.LEFT, padx=5)
    ttk.Label(bingkai_geometri, textvariable=hasil_geom_un_var).grid(row=4, column=0, columnspan=2, sticky="w", padx=5, pady=(5,0))
    ttk.Label(bingkai_geometri, textvariable=hasil_geom_sn_var).grid(row=5, column=0, columnspan=2, sticky="w", padx=5)
    root.mainloop()
if __name__ == "__main__":
    kalkulator_barisan()