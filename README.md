---
# Logo Menty

![Logo](https://github.com/AnTS-Groups/Menty-HackathonAI/blob/main/menty_logo_baru.png?raw=true)

---


---

# Team Name

Team name is: AnTS Groups

---
---

# Member Team

Member team: 

1. Ananda Rauf Maududi: Leader Team(CEO)
2. Ridho Ari Saputro: CTO
3. Danu Febriansyah: Wakil ketua tim(CO-Founder)

---


---
# Video Demo

[Video Demo](https://youtu.be/Wajg7H3etAg)


---

---
# Screenshoot Tampilan Menty

![SS Tampilan](https://github.com/AnTS-Groups/Menty-HackathonAI/blob/main/SS/SS1.png?raw=true)
![SS Tampilan](https://github.com/AnTS-Groups/Menty-HackathonAI/blob/main/SS/SS2.png?raw=true)
![SS Tampilan](https://github.com/AnTS-Groups/Menty-HackathonAI/blob/main/SS/SS3.png?raw=true)
---

---
[Live Demo Website](https://koalitee-menty.hf.space) 
---

---

# 📄 Menty | Are U OK?  
*AI-Powered Voice-Based Mental Wellness Companion*  
> 🎙️ **Rekam suara → Analisis AI → Dapatkan insight emosional**  
> 🔒 Privasi terjaga — *hasil tidak disimpan permanen*  
> 🚨 *Bukan alat diagnosis medis — hanya untuk refleksi diri & edukasi*

---

## 📑 Table of Contents

- [🎯 Overview](#-overview)
- [✨ Fitur Utama](#-fitur-utama)
- [🛠️ Teknologi & Stack](#️-teknologi--stack)
- [📦 Struktur Proyek](#-struktur-proyek)
- [🚀 Instalasi & Setup](#-instalasi--setup)
  - [1. Persyaratan Sistem](#1-persyaratan-sistem)
  - [2. Setup Lingkungan](#2-setup-lingkungan)
  - [3. Konfigurasi API](#3-konfigurasi-api)
  - [4. Jalankan Aplikasi](#4-jalankan-aplikasi)
- [⚙️ Cara Kerja Sistem](#️-cara-kerja-sistem)
- [🌐 Antarmuka Pengguna (UI)](#-antarmuka-pengguna-ui)
- [🛡️ Privasi & Etika](#️-privasi--etika)
- [⚠️ Catatan Penting](#️-catatan-penting)
- [📚 Referensi](#-referensi)

---

## 🎯 Overview

**Menty** adalah aplikasi web ringan yang memungkinkan pengguna **merekam suara**, lalu menganalisis konten emosional & linguistik ucapan menggunakan **Large Language Model (Groq + Llama 3)** untuk memberikan *feedback reflektif* tentang kemungkinan indikasi stres atau depresi.

Aplikasi ini dibangun untuk:
- ✅ Meningkatkan kesadaran diri terhadap kesehatan mental  
- ✅ Menjadi *first-step* sebelum mencari bantuan profesional  
- ✅ Edukasi publik tentang ekspresi verbal & kesejahteraan emosional

> ℹ️ **Disclaimer**: Hasil analisis **bukan diagnosis klinis**. Jika pengguna mengalami gejala berat, sistem menyarankan kontak profesional.

---

## ✨ Fitur Utama

| Fitur | Deskripsi |
|-------|-----------|
| 🔴 Rekam Suara Real-Time | Gunakan mikrofon browser (WebM/Opus), durasi maks 45 detik |
| 📝 Transkripsi & Analisis Langsung | Audio dikirim ke `/analyze`, diproses oleh Groq API → hasil analisis dalam satu respons |
| 🧠 AI-Powered Insight | Model Llama 3 menilai: nada emosional, pola pikir negatif, kecenderungan isolasi, dll |
| 🌓 Mode Gelap & Responsif | UI modern (Tailwind + Poppins), mobile-friendly, dukungan dark/light mode |
| 🔐 Privasi Terjamin | Data tidak disimpan di server setelah analisis selesai |
| 📢 Visual Feedback | Animasi gelombang suara, loading spinner, pesan status interaktif |

---

## 🛠️ Teknologi & Stack

| Komponen | Teknologi |
|---------|-----------|
| **Backend** | Python 3.10+, FastAPI |
| **LLM Engine** | Groq Cloud (`groq==0.36.0`) + Llama 3 70B (atau model lain) |
| **Frontend** | HTML + Alpine.js (reaktif ringan) + Tailwind CSS (CDN) |
| **Audio Processing** | Web Audio API, `MediaRecorder`, format WebM/Opus |
| **Server** | Uvicorn (ASGI) |
| **Templating** | Jinja2 (untuk `index.html`) |
| **Lainnya** | `python-multipart` (upload file), `python-dotenv` (konfigurasi) |

---

## 📦 Struktur Proyek

```bash
menty/
├── requirements.txt          # Project dependencies
├── .env                      # Environment variables (contoh: GROQ_API_KEY=...)
│
├── backend/                  # Backend service (FastAPI)
│   └── main.py               # Entry point FastAPI (routes, Groq processing, API handlers)
│
└── frontend/
    └── templates/
        └── index.html        # Halaman utama: rekam audio, analisis, dan menampilkan hasil
```

### 🔧 `requirements.txt`
```txt
python-dotenv
fastapi==0.122.0
uvicorn[standard]==0.38.0
jinja2==3.1.6
python-multipart==0.0.20
groq==0.36.0
```

---

## 🚀 Instalasi & Setup

### 1. Persyaratan Sistem
- Python 3.9+
- Browser modern (Chrome, Firefox, Edge — dukungan `MediaRecorder`)
- Koneksi internet (untuk akses Groq API)

### 2. Setup Lingkungan
```bash
# Clone & masuk ke direktori (jika perlu)
git clone https://github.com/AnTS-Groups/Menty.git
cd menty

# Buat virtual environment (opsional tapi disarankan)
python -m venv venv
source venv/bin/activate   # Linux/macOS
# venv\Scripts\activate    # Windows

# Install dependencies
pip install -r requirements.txt
```

### 3. Konfigurasi API

Buat file `.env` di root direktori:
```env
GROQ_API_KEY=sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
```

> 💡 Pastikan `GROQ_API_KEY` tersedia dari [Groq Console](https://console.groq.com/keys).  
> Sistem membaca kunci secara otomatis via `python-dotenv`.

### 4. Jalankan Aplikasi
```bash
uvicorn backend.main:aplikasi --host 0.0.0.0 --port 8000 --reload
```

Buka di browser:  
👉 [http://localhost:8000](http://localhost:8000)

---

## ⚙️ Cara Kerja Sistem

1. **User klik mikrofon** → browser minta izin akses mic (`getUserMedia`)
2. **Rekam audio** (format WebM/Opus) → disimpan sementara di memori (`audioChunks`)
3. **Klik berhenti** → `Blob` audio dikirim ke endpoint `/analyze` via `POST`
4. **Server**:
   - Terima file audio
   - Kirim ke Groq API untuk **transkripsi + analisis dalam satu prompt** *(lihat `main.py`)*
   - Prompt meminta:
     ```text
     Analisis transkripsi berikut dari sudut pandang kesehatan mental.
     Nilai: nada emosional, kecenderungan putus asa, isolasi sosial, kelelahan psikologis.
     Beri respons singkat (1 paragraf), berempati, edukatif, dan hindari diagnosa medis.
     ```
5. **Respons JSON** dikirim ke frontend:
   ```json
   { "analysis": "Berdasarkan ucapan Anda..." }
   ```
6. **UI menampilkan hasil** dengan format HTML (bold keyword penting via `formatAnalysis`)

---

## 🌐 Antarmuka Pengguna (UI)

### Komponen Utama (`index.html`)
| Bagian | Fitur |
|-------|-------|
| 🎯 Header | Nama app, tagline, disclaimer etika |
| 📊 Hasil Analisis | Card dengan ikon shield, teks hasil (format HTML aman) |
| ❗ Error Handling | Notifikasi merah jika gagal rekam/analisis |
| ✅ Konfirmasi (opsional) | Saat transkripsi terpisah — *saat ini langsung analisis* |
| 🎚️ Kontrol Rekam | Tombol besar dengan animasi: idle → recording (merah + pulse) → processing (spinner) |
| 📈 Visualisasi | Gelombang suara dinamis saat merekam (simulasi tinggi acak) |
| ℹ️ Petunjuk Penggunaan | Teks bantuan di bawah tombol |

---

## 🛡️ Privasi & Etika

- 🔒 **Tidak ada penyimpanan permanen**: File audio & teks dihapus setelah respons dikirim.
- 📜 **Transparansi**: Pengguna melihat transkripsi (jika dipisah di masa depan) sebelum analisis.
- 🧭 **Etika AI**: Prompt dirancang untuk:
  - Menghindari label stigmatisasi (misal: "kamu depresi")
  - Fokus pada *pola ucapan*, bukan diagnosis
  - Memberi saran: *"Pertimbangkan berbicara dengan konselor..."*
- 🌍 **Aksesibilitas**: Kontras warna tinggi, ukuran teks responsif, keyboard-navigable.

---

## ⚠️ Catatan Penting

| Topik | Detail |
|------|--------|
| 🚫 Bukan Alat Medis | Hanya untuk refleksi pribadi. Tidak menggantikan psikolog/psikiater. |
| 🎧 Kualitas Audio | Hasil akurat bila: suara jelas, minim noise, durasi 10–30 detik |
| 🌐 Koneksi Internet | Diperlukan untuk transkripsi & Groq API |
| 📱 Browser Support | Chrome, Edge, Firefox (Safari terbatas — `MediaRecorder` tidak selalu support Opus) |
| ⏱️ Timeout | Rekaman otomatis berhenti setelah **45 detik** (aman & UX-friendly) |

---

## 📚 Referensi

### Referensi
- [Groq API Documentation](https://console.groq.com/docs)
- [FastAPI Tutorial](https://fastapi.tiangolo.com/)
- [Web Audio API — MDN](https://developer.mozilla.org/en-US/docs/Web/API/Web_Audio_API)
- Prinsip WHO untuk AI & Kesehatan Mental: *Transparansi, Non-maleficence, Autonomy*










