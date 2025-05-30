# Kalkulator Barisan Aritmatika dan Geometri

Aplikasi desktop sederhana. Kalkulator ini membantu menemukan suku ke-n dan jumlah n suku pertama untuk barisan aritmatika maupun geometri.

## Fitur

*   **Perhitungan Barisan Aritmatika:**
    *   Input: Suku pertama (a), beda (b), dan suku ke/jumlah suku (n).
    *   Output: Suku ke-n (U_n) dan jumlah n suku pertama (S_n).
*   **Perhitungan Barisan Geometri:**
    *   Input: Suku pertama (a), rasio (r), dan suku ke/jumlah suku (n).
    *   Output: Suku ke-n (U_n) dan jumlah n suku pertama (S_n).
*   **Validasi Input:**
    *   Memastikan semua input (a, b, r, n) adalah bilangan bulat.
    *   Menampilkan pesan kesalahan untuk input yang tidak valid.
*   **Penanganan Kesalahan:**
    *   Menangani potensi `OverflowError` untuk hasil yang sangat besar pada perhitungan geometri.
    *   Menangani `ZeroDivisionError` jika rasio (r) adalah 1 dalam rumus S_n standar untuk deret geometri (kasus khusus untuk r=1 sudah diimplementasikan).
    *   Menangani `TypeError` jika input tidak sesuai untuk operasi pangkat.
*   **Fungsionalitas Reset:** Memungkinkan pengguna untuk menghapus kolom input dan hasil untuk bagian aritmatika dan geometri.

##Screenshot

![My Application Screenshot](./Assets/screenshot.png)
[Watch the Demo Video](./Assets/Demo.mp4)

**Contoh Tampilan:**
| Kalkulator Aritmatika dan Geometri |
| [Barisan Aritmetika (Bulat)] |
| Suku Pertama (a): [ input_a_arit ] |
| Beda (b): [ input_b_arit ] |
| Suku ke/Jumlah (n): [ input_n_arit ] |
| [Hitung Semua] [Reset] |
| U_n: - |
| S_n: - |
| |
| [Barisan Geometri (Bulat)] |
| Suku Pertama (a): [ input_a_geom ] |
| Rasio (r): [ input_r_geom ] |
| Suku ke/Jumlah (n): [ input_n_geom ] |
| [Hitung Semua] [Reset] |
| U_n: - |
| S_n: - |
