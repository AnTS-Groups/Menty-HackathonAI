import os
from pathlib import Path
from typing import Union

from fastapi import FastAPI, File, UploadFile, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
import groq
from dotenv import load_dotenv
load_dotenv()

DIREKTORI_DASAR = Path(__file__).resolve().parent
AKAR_PROYEK = DIREKTORI_DASAR.parent
DIREKTORI_FRONTEND = AKAR_PROYEK / "frontend"
DIREKTORI_TEMPLATE = DIREKTORI_FRONTEND / "templates"

KUNCI_API_GROQ = os.getenv("GROQ_API_KEY")
MODEL_WHISPER = "whisper-large-v3-turbo"
MODEL_LLM = "llama-3.3-70b-versatile"

if not KUNCI_API_GROQ:
    raise EnvironmentError("❌ KUNCI_API_GROQ tidak ditemukan. Periksa file .env Anda.")

try:
    klien_groq = groq.Groq(api_key=KUNCI_API_GROQ)
except Exception as e:
    print(f"Gagal menginisialisasi klien Groq: {e}")
    klien_groq = None

class ResponsTranskripsi(BaseModel):
    transkripsi: Union[str, None] = None

class ResponsAnalisis(BaseModel):
    analisis: Union[str, None] = None

class KesalahanLayanan(Exception):
    pass

class KesalahanGroq(KesalahanLayanan):
    pass

class KesalahanTranskripsi(KesalahanLayanan):
    pass

def transkripsi_audio(berkas_audio: UploadFile) -> str:
    if not klien_groq:
        raise KesalahanGroq("Klien Groq tidak tersedia.")

    try:
        berkas_audio.file.seek(0)
        ukuran_berkas = len(berkas_audio.file.read())
        berkas_audio.file.seek(0)
        if ukuran_berkas < 1024:
            raise KesalahanTranskripsi("Audio terlalu pendek atau kosong. Rekam minimal 5 detik.")

        transkripsi = klien_groq.audio.transcriptions.create(
            file=(berkas_audio.filename, berkas_audio.file),
            model=MODEL_WHISPER,
            response_format="text",
            language="id"
        )

        if not transkripsi.strip():
            raise KesalahanTranskripsi("Tidak dapat mendeteksi suara dalam rekaman. Audio mungkin terlalu sunyi atau tidak jelas.")

        return transkripsi
    except groq.APIError as e:
        print(f"Error API Groq transkripsi: {e}")
        raise KesalahanGroq(f"Error dari API Groq saat transkripsi: {e}")
    except Exception as e:
        print(f"Error transkripsi: {e}")
        raise KesalahanTranskripsi(f"Gagal mentranskripsi audio: {e}")

def analisis_teks_dengan_groq(teks: str) -> str:
    if not klien_groq:
        raise KesalahanGroq("Klien Groq tidak tersedia.")

    prompt_sistem = (
    "[ATURAN]"
    "Selalu jawab dalam Bahasa Indonesia."
    "JANGAN jawab dengan format markdown."
    "JIKA tidak ada pesan pengguna atau depresi terdeteksi, jawab dengan: 'Tidak ada indikasi depresi.'"
    "[AKHIR ATURAN]"
    "[INSTRUKSI]"
    "Tugas Anda adalah menganalisis pesan pengguna yang diberikan untuk tanda-tanda depresi."
    "Anda akan memberikan analisis mendetail berdasarkan kriteria berikut:"
    "- Frekuensi kata dan frasa negatif."
    "- Kehadiran pikiran bunuh diri atau menyakiti diri sendiri."
    "- Nada emosional dan intensitas."
    "Jawaban Anda harus jelas, ringkas, dan dapat ditindaklanjuti."
    "[AKHIR INSTRUKSI]"
    )
    try:
        penyelesaian_obrolan = klien_groq.chat.completions.create(
            messages=[
                {
                    "role": "system",
                    "content": prompt_sistem,
                },
                {
                    "role": "user",
                    "content": f"Teks transkripsi:\n\"{teks}\"",
                }
            ],
            model=MODEL_LLM,
        )
        return penyelesaian_obrolan.choices[0].message.content
    except groq.APIError as e:
        print(f"Error API Groq analisis: {e}")
        raise KesalahanGroq(f"Error dari API Groq saat analisis: {e}")
    except Exception as e:
        print(f"Error analisis: {e}")
        raise KesalahanGroq(f"Terjadi kesalahan saat menganalisis teks: {e}")

aplikasi = FastAPI(
    title="API Penganalisis Depresi Audio (Groq)",
    description="API untuk menganalisis indikator depresi dari file audio menggunakan layanan Groq.",
    version="2.0.0"
)

aplikasi.mount("/static", StaticFiles(directory=str(DIREKTORI_FRONTEND)), name="static")
template = Jinja2Templates(directory=str(DIREKTORI_TEMPLATE))

@aplikasi.get("/", response_class=HTMLResponse)
async def baca_akar(permintaan: Request):
    return template.TemplateResponse("index.html", {"request": permintaan})

@aplikasi.post("/transcribe", response_model=ResponsTranskripsi)
async def endpoint_transkripsi_audio(audio: UploadFile = File(...)):
    if not audio.content_type or "audio" not in audio.content_type:
        raise HTTPException(status_code=400, detail="File yang diunggah bukan file audio yang valid.")

    try:
        transkripsi = transkripsi_audio(audio)
        return {"transkripsi": transkripsi}
    except KesalahanTranskripsi as e:
        print(f"Error endpoint transkripsi: {e}")
        raise HTTPException(status_code=400, detail=str(e))
    except KesalahanGroq as e:
        print(f"Error endpoint Groq transkripsi: {e}")
        raise HTTPException(status_code=503, detail=str(e))
    except Exception as e:
        print(f"Error tak terduga transkripsi: {e}")
        raise HTTPException(status_code=500, detail=f"Terjadi kesalahan tak terduga: {e}")

@aplikasi.post("/analyze_text")
async def endpoint_analisis_teks(request: Request):
    try:
        data = await request.json()
        teks = data.get("teks")
        if not teks:
            raise HTTPException(status_code=400, detail="Teks tidak ditemukan dalam request.")
        analisis = analisis_teks_dengan_groq(teks)
        return {"analisis": analisis}
    except KesalahanGroq as e:
        print(f"Error endpoint Groq analisis: {e}")
        raise HTTPException(status_code=503, detail=str(e))
    except Exception as e:
        print(f"Error tak terduga analisis: {e}")
        raise HTTPException(status_code=500, detail=f"Terjadi kesalahan tak terduga: {e}")

@aplikasi.post("/analyze", response_model=ResponsAnalisis)
async def endpoint_analisis_audio(audio: UploadFile = File(...)):
    if not audio.content_type or "audio" not in audio.content_type:
        raise HTTPException(status_code=400, detail="File yang diunggah bukan file audio yang valid.")

    try:
        transkripsi = transkripsi_audio(audio)
        analisis = analisis_teks_dengan_groq(transkripsi)
        return {"analisis": analisis}
    except KesalahanTranskripsi as e:
        print(f"Error endpoint transkripsi analisis: {e}")
        raise HTTPException(status_code=400, detail=str(e))
    except KesalahanGroq as e:
        print(f"Error endpoint Groq analisis: {e}")
        raise HTTPException(status_code=503, detail=str(e))
    except Exception as e:
        print(f"Error tak terduga analisis: {e}")
        raise HTTPException(status_code=500, detail=f"Terjadi kesalahan tak terduga: {e}")

@aplikasi.on_event("startup")
async def acara_startup():
    print("Aplikasi telah dimulai dengan layanan Groq.")
    print(f"Model Transkripsi: {MODEL_WHISPER}")
    print(f"Model LLM: {MODEL_LLM}")