import os, sys, re, tempfile, subprocess
from flask import Flask, request, jsonify, render_template_string
from PIL import Image, ImageOps

app = Flask(__name__)

PRODUCTS = {
    "8681413502057": {"name": "Mila Su 0.5L", "bin": "SARI", "type": "Plastik (PET)", "tip": "Kapagi ayirip siseyi ezerek Sari kutuya atin.", "grams": 18, "co2": 45},
    "8690525060478": {"name": "Pınar Su", "bin": "SARI", "type": "Plastik (PET)", "tip": "Siviyi bosaltip siseyi sikistirarak Sari kutuya atin.", "grams": 14, "co2": 110},
    "8681630429533": {"name": "Züber Ice Tea", "bin": "MAVI", "type": "Metal / Aluminyum", "tip": "Icinde sivi birakmadan Mavi metal kutusuna atin.", "grams": 12, "co2": 97},
    "8690624101011": {"name": "Meyve Suyu Karton 200ml", "bin": "KIRMIZI", "type": "Kagit / Karton", "tip": "Pipeti cikarip Kirmizi kagit kutusuna atin.", "grams": 12, "co2": 22},
}

state = {
    "sensor_active": False,
    "expected_bin": None,
    "last_product": None,
    "last_result": None,
    "points": 0,
    "total_grams": 0,
    "total_co2": 0,
    "contaminated_prevented": 0
}
rapid_engine = None

def run_ocr(img_path):
    global rapid_engine
    ocr_bin = os.path.abspath("ocr_bin")
    if sys.platform == "darwin" and os.path.exists(ocr_bin):
        return subprocess.check_output([ocr_bin, img_path], stderr=subprocess.DEVNULL, text=True)
    try:
        from rapidocr_onnxruntime import RapidOCR
        if rapid_engine is None:
            rapid_engine = RapidOCR()
        res, _ = rapid_engine(img_path)
        return "\n".join([line[1] for line in res]) if res else ""
    except Exception:
        return ""

def find_code(text):
    digits = re.sub(r"\D", "", text)
    for c in PRODUCTS:
        if c in digits:
            return c
    for c in PRODUCTS:
        n = len(c)
        for i in range(max(0, len(digits) - n + 1)):
            if sum(a == b for a, b in zip(c, digits[i:i+n])) >= n - 3:
                return c
    for m in re.findall(r"(?:\d\s*){8,13}", text):
        clean = re.sub(r"\D", "", m)
        if 8 <= len(clean) <= 13:
            return clean
    return None

def read_photo(path):
    texts = []
    img = ImageOps.exif_transpose(Image.open(path)).convert("RGB")
    gray = ImageOps.autocontrast(ImageOps.grayscale(img)).convert("RGB")
    for im, ang in [(img, 0), (img, 90), (img, 270), (img, 180), (gray, 0), (gray, 90)]:
        rot = im.rotate(ang, expand=True) if ang else im
        with tempfile.NamedTemporaryFile(suffix=".jpg", delete=False) as t:
            tmp = t.name
        try:
            rot.save(tmp, "JPEG", quality=92)
            out = run_ocr(tmp)
            if out:
                texts.append(out)
                hit = find_code("\n".join(texts))
                if hit in PRODUCTS:
                    return hit, "\n".join(texts).strip()
        except Exception:
            pass
        finally:
            if os.path.exists(tmp):
                os.remove(tmp)
    all_t = "\n".join(texts).strip()
    return find_code(all_t), all_t

HTML = """<!DOCTYPE html><html lang="tr"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1.0">
<title>Akilli Kampus Atik</title><script src="https://cdn.tailwindcss.com"></script></head>
<body class="bg-slate-900 text-white min-h-screen font-sans"><div class="max-w-md mx-auto p-4">
<div class="flex justify-between items-center bg-slate-800/90 border border-slate-700 rounded-xl px-3 py-2 mb-3 text-xs">
<span id="conn" class="font-bold text-amber-400">Baglanti kontrol ediliyor...</span>
<span class="text-slate-400">Surum 2.2</span></div>
<div class="bg-slate-800 rounded-2xl p-4 mb-4 border border-slate-700">
<div class="flex justify-between items-center mb-3"><span class="text-xs font-bold text-emerald-400">KAMPUS DONGUSEL ATIK</span>
<span class="bg-emerald-500/20 text-emerald-300 text-xs px-2.5 py-1 rounded-full font-semibold" id="pts">0 Yesil Puan</span></div>
<div class="grid grid-cols-3 gap-2 text-center">
<div class="bg-slate-900 p-2 rounded-xl"><div class="text-lg font-bold text-emerald-400" id="g">0 g</div><div class="text-[11px] text-slate-400">Temiz Atik</div></div>
<div class="bg-slate-900 p-2 rounded-xl"><div class="text-lg font-bold text-sky-400" id="co2">0 g</div><div class="text-[11px] text-slate-400">CO2 Tasarrufu</div></div>
<div class="bg-slate-900 p-2 rounded-xl"><div class="text-lg font-bold text-amber-400" id="cnt">0</div><div class="text-[11px] text-slate-400">Dogru Ayrisma</div></div>
</div></div>
<div id="s1" class="bg-slate-800 rounded-2xl p-5 border border-slate-700">
<h2 class="text-lg font-bold mb-1">1. Adim: Barkod Numarasini Okut</h2>
<p class="text-sm text-slate-400 mb-4">Barkodun altindaki rakamlarin fotografini cekin veya numarasini yazin.</p>
<div id="st" class="hidden text-center text-xs font-bold text-amber-200 bg-amber-500/20 border border-amber-500/4
