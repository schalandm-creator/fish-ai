import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import streamlit as st
from PIL import Image
import numpy as np
import requests
import json
from fish_data import FISH_REGULATIONS, BUNDESLAENDER

st.set_page_config(page_title="FischFinder Deutschland", page_icon="🐟", layout="centered")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@700&family=Source+Sans+3:wght@300;400;600&display=swap');
html, body, [class*="css"] { font-family: 'Source Sans 3', sans-serif; }
.main-title { font-family:'Playfair Display',serif; font-size:2.8rem; color:#0a3d62; text-align:center; margin-bottom:0.2rem; }
.subtitle   { text-align:center; color:#5f7f96; font-size:1.1rem; margin-bottom:2.5rem; font-weight:300; }
.result-card { background:linear-gradient(135deg,#eaf4fb,#f0f9e8); border-left:5px solid #0a3d62; border-radius:12px; padding:1.5rem 2rem; margin:1rem 0; }
.fish-name   { font-family:'Playfair Display',serif; font-size:1.8rem; color:#0a3d62; margin-bottom:0.2rem; }
.bar-wrap    { background:#dce8f0; border-radius:20px; height:10px; margin-top:0.5rem; overflow:hidden; }
.reg-box     { border-radius:12px; padding:1.4rem 1.6rem; margin-top:1rem; }
.reg-warn    { background:#fff8e1; border-left:5px solid #f9a825; }
.reg-info    { background:#e3f2fd; border-left:5px solid #1565c0; }
.reg-ok      { background:#e8f5e9; border-left:5px solid #2e7d32; }
.reg-title   { font-size:1.1rem; font-weight:600; margin-bottom:0.4rem; }
.small-note  { font-size:0.8rem; color:#777; margin-top:1.5rem; text-align:center; }
</style>
""", unsafe_allow_html=True)

MODEL_URL  = "https://github.com/onnx/models/raw/main/validated/vision/classification/efficientnet-lite4/model/efficientnet-lite4-11.onnx"
MODEL_PATH = "/tmp/efficientnet_lite4.onnx"
LABELS_URL = "https://raw.githubusercontent.com/anishathalye/imagenet-simple-labels/master/imagenet-simple-labels.json"

@st.cache_resource(show_spinner="KI-Modell wird geladen …")
def load_model():
    import onnxruntime as ort
    if not os.path.exists(MODEL_PATH):
        r = requests.get(MODEL_URL, timeout=120)
        r.raise_for_status()
        with open(MODEL_PATH, "wb") as f:
            f.write(r.content)
    return ort.InferenceSession(MODEL_PATH, providers=["CPUExecutionProvider"])

@st.cache_data(show_spinner=False)
def load_labels():
    return requests.get(LABELS_URL, timeout=10).json()

def preprocess(image):
    img = image.resize((224, 224), Image.BILINEAR)
    arr = np.array(img, dtype=np.float32) / 255.0
    arr = (arr - [0.485,0.456,0.406]) / [0.229,0.224,0.225]
    return arr.transpose(2,0,1)[np.newaxis,...].astype(np.float32)

IMAGENET_TO_FISH = {
    "tench":"Schleie","goldfish":"Karpfen","coho":"Lachs","eel":"Aal",
    "sturgeon":"Stör","gar":"Hecht","trout":"Forelle","pike":"Hecht",
    "perch":"Barsch","carp":"Karpfen","bream":"Brassen","catfish":"Wels",
    "roach":"Rotauge","zander":"Zander","rudd":"Rotfeder","grayling":"Äsche",
    "salmon":"Lachs","bass":"Barsch",
}

def match_fish(label):
    ll = label.lower()
    for kw, fish in IMAGENET_TO_FISH.items():
        if kw in ll:
            return fish
    return None

st.markdown('<div class="main-title">🐟 FischFinder</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Fischerkennung & Schonzeitauskunft für Deutschland</div>', unsafe_allow_html=True)

uploaded = st.file_uploader("Bild hochladen (JPG / PNG)", type=["jpg","jpeg","png"], label_visibility="collapsed")

if uploaded:
    image = Image.open(uploaded).convert("RGB")
    st.image(image, use_container_width=True, caption="Hochgeladenes Bild")

    with st.spinner("Fisch wird analysiert …"):
        try:
            session = load_model()
            labels  = load_labels()
            tensor  = preprocess(image)
            inp     = session.get_inputs()[0].name
            out     = session.get_outputs()[0].name
            logits  = session.run([out], {inp: tensor})[0][0]
            e = np.exp(logits - logits.max()); probs = e / e.sum()
            top5    = probs.argsort()[-5:][::-1]
            ok = True
        except Exception as ex:
            st.error(f"Modellfehler: {ex}"); ok = False

    if ok:
        top_label = labels[top5[0]]; top_prob = float(probs[top5[0]])
        fish_key  = match_fish(top_label)
        if not fish_key:
            for i in top5[1:]:
                alt = match_fish(labels[i])
                if alt:
                    fish_key = alt; top_label = labels[i]; top_prob = float(probs[i]); break

        st.markdown("---")
        if fish_key:
            st.markdown(f"""
            <div class="result-card">
                <div class="fish-name">🎣 {fish_key}</div>
                <div style="color:#5f7f96;font-size:.9rem;">Erkannt: <em>{top_label}</em></div>
                <div style="margin-top:.6rem;font-size:.9rem;color:#333;">Konfidenz: <strong>{top_prob*100:.1f} %</strong></div>
                <div class="bar-wrap"><div style="width:{top_prob*100:.0f}%;height:100%;background:linear-gradient(90deg,#0a3d62,#1e90ff);border-radius:20px;"></div></div>
            </div>""", unsafe_allow_html=True)

            st.markdown("#### 📍 Aus welchem Bundesland kommen Sie?")
            bl = st.selectbox("Bundesland", ["– bitte wählen –"] + BUNDESLAENDER, label_visibility="collapsed")
            if bl != "– bitte wählen –":
                regs = FISH_REGULATIONS.get(fish_key, {})
                d    = regs.get(bl) or regs.get("default", {})
                if d:
                    st.markdown(f'<div class="reg-box reg-warn"><div class="reg-title">🗓️ Schonzeit</div>{d.get("schonzeit","–")}</div>', unsafe_allow_html=True)
                    if d.get("mindestmass"):
                        st.markdown(f'<div class="reg-box reg-info"><div class="reg-title">📏 Mindestmaß</div>{d["mindestmass"]}</div>', unsafe_allow_html=True)
                    if d.get("hinweis"):
                        st.markdown(f'<div class="reg-box reg-ok"><div class="reg-title">ℹ️ Hinweis</div>{d["hinweis"]}</div>', unsafe_allow_html=True)
                    st.markdown('<div class="small-note">⚠️ Angaben ohne Gewähr – bitte Fischereibehörde Ihres Bundeslandes konsultieren.</div>', unsafe_allow_html=True)
                else:
                    st.info("Keine Daten für diese Kombination vorhanden.")
        else:
            st.markdown(f"""
            <div class="result-card" style="border-left-color:#c0392b;">
                <div class="fish-name" style="color:#c0392b;">❓ Kein Fisch erkannt</div>
                <div style="color:#555;margin-top:.4rem;">Erkannt: <em>{top_label}</em> ({top_prob*100:.1f} %) – kein bekannter Süßwasserfisch.</div>
                <div style="margin-top:.8rem;color:#555;">Tipp: Seitliche Aufnahme, scharf, guter Kontrast zum Hintergrund.</div>
            </div>""", unsafe_allow_html=True)

            st.markdown("#### 🔍 Manuell suchen")
            c1, c2 = st.columns(2)
            mf = c1.selectbox("Fischart",   ["– wählen –"] + list(FISH_REGULATIONS.keys()))
            mb = c2.selectbox("Bundesland", ["– wählen –"] + BUNDESLAENDER)
            if mf != "– wählen –" and mb != "– wählen –":
                d = FISH_REGULATIONS.get(mf,{}).get(mb) or FISH_REGULATIONS.get(mf,{}).get("default",{})
                if d:
                    st.markdown(f"**Schonzeit:** {d.get('schonzeit','–')}")
                    if d.get("mindestmass"): st.markdown(f"**Mindestmaß:** {d['mindestmass']}")
else:
    st.markdown('<div style="text-align:center;padding:3rem 1rem;color:#5f7f96;"><div style="font-size:4rem;">📸</div><div style="font-size:1.1rem;margin-top:.5rem;">Laden Sie ein Foto Ihres Fangs hoch.</div></div>', unsafe_allow_html=True)
