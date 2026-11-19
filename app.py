import os, sys, re, json, tempfile, subprocess
from flask import Flask, request, jsonify, render_template_string
from PIL import Image, ImageOps

app = Flask(__name__)
DB_FILE = "products.json"
PRODUCTS = {
    "8681413502057": {"name": "Mila Su 0.5L", "bin": "SARI", "type": "Plastik (PET)", "tip": "Kapagi ayirip siseyi ezerek atin.", "grams": 18, "co2": 45},
    "8690504016502": {"name": "Ulker Cikolatali Gofret", "bin": "SARI", "type": "Plastik Ambalaj", "tip": "Icinde gida artigi birakmadan atin.", "grams": 5, "co2": 12},
    "5449000000996": {"name": "Coca-Cola Kutu 330ml", "bin": "SARI", "type": "Metal / Aluminyum", "tip": "Siviyi bosaltip kutuyu sikistirin.", "grams": 14, "co2": 110},
    "8690624101011": {"name": "Meyve Suyu Karton 200ml", "bin": "MAVI", "type": "Kagit / Kompozit", "tip": "Pipeti cikarip Mavi kutuya atin.", "grams": 12, "co2": 22},
}
if os.path.exists(DB_FILE):
    try: PRODUCTS.update(json.load(open(DB_FILE, encoding="utf-8")))
    except Exception: pass

state = {"sensor_active": False, "expected_bin": None, "last_product": None, "last_result": None, "points": 0, "total_grams": 0, "total_co2": 0, "contaminated_prevented": 0}
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
<span class="text-slate-400">Surum 2.0</span></div>
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
<p class="text-sm text-slate-400 mb-4">Barkodun altindaki rakamlarin fotografini cekin.</p>
<div id="st" class="hidden text-center text-xs font-bold text-amber-200 bg-amber-500/20 border border-amber-500/40 rounded-xl p-3 mb-3"></div>
<label class="block w-full bg-amber-500 hover:bg-amber-400 active:scale-95 text-slate-950 font-bold py-3.5 rounded-xl text-sm text-center cursor-pointer mb-3">
<span id="pbtn">Fotograf Cek (Rakamları Oku)</span>
<input type="file" accept="image/*" capture="environment" class="hidden" onchange="sendPhoto(this)">
</label>
<div class="flex gap-2 mb-3"><input id="man" inputmode="numeric" placeholder="Barkod no yaz (8681413502057)" class="flex-1 bg-slate-900 border border-slate-700 rounded-xl px-3 py-2 text-sm">
<button onclick="pick(document.getElementById('man').value)" class="bg-slate-700 font-bold px-4 py-2 rounded-xl text-sm">Sorgula</button></div>
<details class="bg-slate-900 border border-slate-700 rounded-xl p-3 mb-3"><summary class="text-xs font-bold text-emerald-400 cursor-pointer">+ Yeni Urun Barkodu Tanimla</summary>
<div class="mt-2 space-y-2"><input id="nc" inputmode="numeric" placeholder="Barkod No" class="w-full bg-slate-800 border border-slate-700 rounded-lg px-3 py-2 text-xs">
<input id="nn" placeholder="Urun Adi" class="w-full bg-slate-800 border border-slate-700 rounded-lg px-3 py-2 text-xs">
<select id="nb" class="w-full bg-slate-800 border border-slate-700 rounded-lg px-3 py-2 text-xs"><option value="SARI">SARI KUTU</option><option value="MAVI">MAVI KUTU</option></select>
<button onclick="addP()" class="w-full bg-emerald-600 text-xs font-bold py-2 rounded-lg">Kaydet</button></div></details>
<div class="border-t border-slate-700 pt-3 grid grid-cols-2 gap-2">
<button onclick="pick('8681413502057')" class="bg-slate-700 text-xs py-2 rounded-lg">Mila Su (Sari)</button>
<button onclick="pick('8690624101011')" class="bg-slate-700 text-xs py-2 rounded-lg">Karton Kutu (Mavi)</button></div></div>
<div id="s2" class="hidden bg-slate-800 rounded-2xl p-5 border border-slate-700">
<div id="ban" class="p-4 rounded-xl mb-4 text-center font-bold"><div class="text-xs uppercase opacity-80" id="pn"></div><div class="text-2xl my-1" id="tb"></div><div class="text-xs font-normal" id="pt"></div></div>
<h2 class="text-base font-bold mb-2">2. Adim: Kutudaki QR Kodu Okut</h2>
<button onclick="arm('KUTU_01')" class="w-full bg-sky-600 font-bold py-3 rounded-xl">Kutu QR Okutuldu / Sensoru Baslat</button></div>
<div id="s3" class="hidden bg-slate-800 rounded-2xl p-5 border border-emerald-500/50 text-center">
<h2 class="text-lg font-bold text-emerald-400 mb-2">Kutu Sensoru Aktif!</h2>
<p class="text-sm text-slate-300 mb-4">Atigi <strong id="wb"></strong> bolmeye birakin.</p>
<div class="grid grid-cols-2 gap-2"><button onclick="drop(cur.bin)" class="bg-emerald-600 text-xs font-bold py-2.5 rounded-lg">Dogru Kutuya Atildi</button>
<button onclick="drop('YANLIS')" class="bg-rose-600 text-xs font-bold py-2.5 rounded-lg">Yanlis Kutuya Atildi</button></div></div>
<div id="s4" class="hidden bg-slate-800 rounded-2xl p-6 border border-slate-700 text-center">
<h2 id="rt" class="text-xl font-bold mb-2"></h2><p id="rd" class="text-sm text-slate-300 mb-5"></p>
<button onclick="go(1)" class="w-full bg-emerald-600 font-bold py-3 rounded-xl">Yeni Atik Okut</button></div></div>
<script>
let cur=null,tmr=null;
const go=n=>{[1,2,3,4].forEach(i=>document.getElementById('s'+i).classList.add('hidden'));document.getElementById('s'+n).classList.remove('hidden')};
const msg=t=>{const e=document.getElementById('st');e.innerText=t;e.classList.toggle('hidden',!t)};
async function ping(){try{const r=await fetch('/api/status');if(r.ok){document.getElementById('conn').innerText='Sunucu Bagli';document.getElementById('conn').className='font-bold text-emerald-400';return}}catch(e){}document.getElementById('conn').innerText='Baglanti Koptu! Terminal linkini yenile';document.getElementById('conn').className='font-bold text-rose-400'}
ping();setInterval(ping,5000);
function shrink(f){return new Promise(r=>{const rd=new FileReader();rd.onload=e=>{const im=new Image();im.onload=()=>{const s=Math.min(1,1000/Math.max(im.width,im.height)),c=document.createElement('canvas');c.width=im.width*s;c.height=im.height*s;c.getContext('2d').drawImage(im,0,0,c.width,c.height);c.toBlob(b=>r(b),'image/jpeg',0.88)};im.src=e.target.result};rd.readAsDataURL(f)})}
async function sendPhoto(inp){if(!inp.files||!inp.files.length)return;const b=document.getElementById('pbtn');b.innerText='Sunucuda okunuyor...';msg('Foto sunucuya gonderildi, rakamlar taraniyor...');try{const fd=new FormData();fd.append('photo',await shrink(inp.files[0]),'p.jpg');const d=await(await fetch('/api/scan_photo',{method:'POST',body:fd})).json();if(d.code){msg('Tanindi: '+d.code);await pick(d.code)}else{msg('Rakam secilemedi (Gorulen: '+(d.raw||'bos')+'). Yakindan tekrar cekin.')}}catch(e){msg('Sunucu baglantisi koptu! Terminaldeki yeni linki acin.')}b.innerText='Fotograf Cek (Rakamları Oku)';inp.value=''}
async function addP(){try{const code=document.getElementById('nc').value.trim(),name=document.getElementById('nn').value.trim(),bin=document.getElementById('nb').value;if(!code||!name)return;await fetch('/api/products',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({code,name,bin})});alert('Kaydedildi: '+name)}catch(e){alert('Baglanti koptu')}}
async function pick(c){c=(c||'').trim();if(!c)return;try{cur=await(await fetch('/api/product/'+encodeURIComponent(c))).json();document.getElementById('pn').innerText=cur.name+' ['+c+']';document.getElementById('tb').innerText=cur.bin+' KUTUYA ATIN';document.getElementById('pt').innerText=cur.tip;document.getElementById('ban').className='p-4 rounded-xl mb-4 text-center font-bold '+(cur.bin==='SARI'?'bg-amber-500 text-slate-950':'bg-sky-500 text-slate-950');go(2)}catch(e){msg('Sunucu baglantisi koptu! Terminaldeki yeni linki acin.')}}
async function arm(id){try{await fetch('/api/activate',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({bin_id:id,product:cur})});document.getElementById('wb').innerText=cur.bin;go(3);if(tmr)clearInterval(tmr);tmr=setInterval(async()=>{const d=await(await fetch('/api/status')).json();document.getElementById('pts').innerText=d.points+' Yesil Puan';document.getElementById('g').innerText=d.total_grams+' g';document.getElementById('co2').innerText=d.total_co2+' g';document.getElementById('cnt').innerText=d.contaminated_prevented;if(!d.sensor_active&&d.last_result){clearInterval(tmr);const ok=d.last_result==='SUCCESS';document.getElementById('rt').innerText=ok?'Dogru Ayristirma! +10 Puan':'Yanlis Kutuya Atildi!';document.getElementById('rt').className='text-xl font-bold mb-2 '+(ok?'text-emerald-400':'text-rose-400');document.getElementById('rd').innerText=ok?cur.grams+'g atik kurtarildi, '+cur.co2+'g CO2 onlendi.':'Kontaminasyon olustu, puan yuklenmedi.';go(4)}},1000)}catch(e){alert('Baglanti koptu')}}
const drop=b=>fetch('/api/sensor_trigger?bin='+b);
</script></body></html>"""

@app.route("/")
def index(): return render_template_string(HTML)

@app.route("/api/scan_photo", methods=["POST"])
def scan_photo():
    f = request.files.get("photo")
    if not f: return jsonify({"code": None, "raw": "bos"})
    with tempfile.NamedTemporaryFile(suffix=".jpg", delete=False) as t: p = t.name
    try:
        f.save(p)
        c, raw = read_photo(p)
        return jsonify({"code": c, "raw": raw[:60]})
    finally:
        if os.path.exists(p): os.remove(p)

@app.route("/api/product/<code>")
def get_product(code):
    return jsonify(PRODUCTS.get(code.strip(), {"name": f"Tanimsiz ({code})", "bin": "SARI", "type": "Ambalaj", "tip": "Sari kutuya atin.", "grams": 10, "co2": 25}))

@app.route("/api/products", methods=["POST"])
def add_product():
    d = request.json
    c, b = d["code"].strip(), d["bin"].upper()
    PRODUCTS[c] = {"name": d["name"].strip(), "bin": b, "type": b, "tip": f"{b} kutuya atin.", "grams": 15, "co2": 35}
    json.dump(PRODUCTS, open(DB_FILE, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
    return jsonify({"ok": True})

@app.route("/api/activate", methods=["POST"])
def activate():
    d = request.json
    state.update({"sensor_active": True, "expected_bin": d["product"]["bin"], "last_product": d["product"], "last_result": None})
    return jsonify({"status": "armed"})

@app.route("/api/esp32/check")
def esp32_check(): return jsonify({"active": state["sensor_active"], "expected_bin": state["expected_bin"]})

@app.route("/api/sensor_trigger")
def sensor_trigger():
    b = request.args.get("bin", "").upper()
    if not state["sensor_active"]: return jsonify({"status": "ignored"})
    p = state["last_product"]
    if b == state["expected_bin"]:
        state["points"] += 10; state["total_grams"] += p["grams"]; state["total_co2"] += p["co2"]; state["contaminated_prevented"] += 1; state["last_result"] = "SUCCESS"
    else: state["last_result"] = "WRONG_BIN"
    state["sensor_active"] = False
    return jsonify({"status": "recorded"})

@app.route("/api/status")
def status(): return jsonify(state)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5001)), debug=False)
