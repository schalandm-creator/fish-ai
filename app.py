import sys
import os

# Sicherstellen, dass das App-Verzeichnis im Python-Pfad ist (wichtig für Streamlit Cloud)
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import streamlit as st
from PIL import Image
import torch
from torchvision import models, transforms
import requests
import json
from fish_data import FISH_REGULATIONS, BUNDESLAENDER

# ─── Page config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="FischFinder Deutschland",
    page_icon="🐟",
    layout="centered",
    initial_sidebar_state="collapsed",
)

# ─── Custom CSS ───────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@700&family=Source+Sans+3:wght@300;400;600&display=swap');

html, body, [class*="css"] {
    font-family: 'Source Sans 3', sans-serif;
}

.main-title {
    font-family: 'Playfair Display', serif;
    font-size: 2.8rem;
    color: #0a3d62;
    text-align: center;
    margin-bottom: 0.2rem;
    letter-spacing: -1px;
}

.subtitle {
    text-align: center;
    color: #5f7f96;
    font-size: 1.1rem;
    margin-bottom: 2.5rem;
    font-weight: 300;
}

.result-card {
    background: linear-gradient(135deg, #eaf4fb 0%, #f0f9e8 100%);
    border-left: 5px solid #0a3d62;
    border-radius: 12px;
    padding: 1.5rem 2rem;
    margin: 1rem 0;
}

.fish-name {
    font-family: 'Playfair Display', serif;
    font-size: 1.8rem;
    color: #0a3d62;
    margin-bottom: 0.2rem;
}

.confidence-bar-wrapper {
    background: #dce8f0;
    border-radius: 20px;
    height: 10px;
    margin-top: 0.5rem;
    overflow: hidden;
}

.regulation-box {
    border-radius: 12px;
    padding: 1.4rem 1.6rem;
    margin-top: 1rem;
}

.reg-ok    { background: #e8f5e9; border-left: 5px solid #2e7d32; }
.reg-warn  { background: #fff8e1; border-left: 5px solid #f9a825; }
.reg-info  { background: #e3f2fd; border-left: 5px solid #1565c0; }

.reg-title {
    font-size: 1.1rem;
    font-weight: 600;
    margin-bottom: 0.4rem;
}

.small-note {
    font-size: 0.8rem;
    color: #777;
    margin-top: 1.5rem;
    text-align: center;
}

.divider {
    border: none;
    border-top: 1px solid #d0dfe8;
    margin: 1.5rem 0;
}

/* Upload area */
[data-testid="stFileUploadDropzone"] {
    border: 2px dashed #5f7f96 !important;
    border-radius: 12px !important;
    background: #f7fbfe !important;
}
</style>
""", unsafe_allow_html=True)


# ─── Load model (cached) ──────────────────────────────────────────────────────
@st.cache_resource(show_spinner="Modell wird geladen …")
def load_model():
    model = models.efficientnet_b2(weights="IMAGENET1K_V1")
    model.eval()
    return model


@st.cache_data(show_spinner=False)
def load_imagenet_labels():
    url = "https://raw.githubusercontent.com/anishathalye/imagenet-simple-labels/master/imagenet-simple-labels.json"
    resp = requests.get(url, timeout=10)
    return resp.json()


def preprocess(image: Image.Image):
    transform = transforms.Compose([
        transforms.Resize(256),
        transforms.CenterCrop(224),
        transforms.ToTensor(),
        transforms.Normalize([0.485, 0.456, 0.406],
                             [0.229, 0.224, 0.225]),
    ])
    return transform(image).unsqueeze(0)


# Mapping: ImageNet label keywords → German fish name key used in FISH_REGULATIONS
IMAGENET_TO_FISH = {
    "tench":          "Schleie",
    "goldfish":       "Karpfen",
    "great white shark": None,
    "tiger shark":    None,
    "hammerhead":     None,
    "electric ray":   None,
    "stingray":       None,
    "coho":           "Lachs",
    "eel":            "Aal",
    "rock beauty":    None,
    "anemone fish":   None,
    "sturgeon":       "Stör",
    "gar":            "Hecht",
    "lionfish":       None,
    "puffer":         None,
    "barracouta":     "Makrele",
    "trout":          "Forelle",
    "pike":           "Hecht",
    "perch":          "Barsch",
    "carp":           "Karpfen",
    "bream":          "Brassen",
    "catfish":        "Wels",
    "roach":          "Rotauge",
    "zander":         "Zander",
    "rudd":           "Rotfeder",
    "grayling":       "Äsche",
    "salmon":         "Lachs",
    "bass":           "Barsch",
}


def match_fish(label: str):
    """Return German fish key if the ImageNet label maps to a known fish."""
    label_lower = label.lower()
    for keyword, fish_key in IMAGENET_TO_FISH.items():
        if keyword in label_lower:
            return fish_key
    return None


# ─── UI ───────────────────────────────────────────────────────────────────────
st.markdown('<div class="main-title">🐟 FischFinder</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Fischerkennung & Schonzeitauskunft für Deutschland</div>', unsafe_allow_html=True)

uploaded = st.file_uploader(
    "Bild hochladen (JPG / PNG)",
    type=["jpg", "jpeg", "png"],
    label_visibility="collapsed",
)

if uploaded:
    image = Image.open(uploaded).convert("RGB")
    st.image(image, use_container_width=True, caption="Hochgeladenes Bild")

    with st.spinner("Fisch wird analysiert …"):
        model = load_model()
        labels = load_imagenet_labels()
        tensor = preprocess(image)
        with torch.no_grad():
            outputs = model(tensor)
        probs = torch.nn.functional.softmax(outputs[0], dim=0)
        top5_probs, top5_idx = torch.topk(probs, 5)

    top_label = labels[top5_idx[0].item()]
    top_prob  = top5_probs[0].item()
    fish_key  = match_fish(top_label)

    # Also check other top-5 labels for a fish match
    if fish_key is None:
        for idx, prob in zip(top5_idx[1:], top5_probs[1:]):
            alt_label = labels[idx.item()]
            alt_fish  = match_fish(alt_label)
            if alt_fish:
                fish_key = alt_fish
                top_label = alt_label
                top_prob  = prob.item()
                break

    st.markdown('<hr class="divider">', unsafe_allow_html=True)

    if fish_key:
        st.markdown(f"""
        <div class="result-card">
            <div class="fish-name">🎣 {fish_key}</div>
            <div style="color:#5f7f96; font-size:0.9rem;">
                Erkanntes Objekt: <em>{top_label}</em>
            </div>
            <div style="margin-top:0.6rem; font-size:0.9rem; color:#333;">
                Modell-Konfidenz: <strong>{top_prob*100:.1f} %</strong>
            </div>
            <div class="confidence-bar-wrapper">
                <div style="width:{top_prob*100:.0f}%; height:100%;
                            background: linear-gradient(90deg,#0a3d62,#1e90ff);
                            border-radius:20px;"></div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        # ── Bundesland picker ──────────────────────────────────────────────
        st.markdown("#### 📍 Aus welchem Bundesland kommen Sie?")
        bundesland = st.selectbox(
            "Bundesland wählen",
            ["– bitte wählen –"] + BUNDESLAENDER,
            label_visibility="collapsed",
        )

        if bundesland != "– bitte wählen –":
            regs = FISH_REGULATIONS.get(fish_key, {})
            bl_regs = regs.get(bundesland) or regs.get("default", {})

            if bl_regs:
                schonzeit  = bl_regs.get("schonzeit",    "Keine Angabe")
                mindestmass = bl_regs.get("mindestmass",  None)
                hinweis    = bl_regs.get("hinweis",      None)

                # Schonzeit
                st.markdown(f"""
                <div class="regulation-box reg-warn">
                    <div class="reg-title">🗓️ Schonzeit</div>
                    <div>{schonzeit}</div>
                </div>
                """, unsafe_allow_html=True)

                # Mindestmaß
                if mindestmass:
                    st.markdown(f"""
                    <div class="regulation-box reg-info">
                        <div class="reg-title">📏 Mindestmaß</div>
                        <div>{mindestmass}</div>
                    </div>
                    """, unsafe_allow_html=True)

                # Hinweis
                if hinweis:
                    st.markdown(f"""
                    <div class="regulation-box reg-ok">
                        <div class="reg-title">ℹ️ Hinweis</div>
                        <div>{hinweis}</div>
                    </div>
                    """, unsafe_allow_html=True)

                st.markdown("""
                <div class="small-note">
                    ⚠️ Angaben ohne Gewähr. Bitte prüfen Sie die aktuell gültigen Regelungen
                    der zuständigen Fischereibehörde Ihres Bundeslandes.
                </div>
                """, unsafe_allow_html=True)
            else:
                st.info("Für diesen Fisch und dieses Bundesland liegen keine Daten vor.")

    else:
        # Kein Fisch erkannt
        st.markdown(f"""
        <div class="result-card" style="border-left-color:#c0392b;">
            <div class="fish-name" style="color:#c0392b;">❓ Kein Fisch erkannt</div>
            <div style="color:#555; margin-top:0.4rem;">
                Das Modell hat <em>{top_label}</em> mit {top_prob*100:.1f} % Konfidenz erkannt –
                aber keinen bekannten deutschen Süßwasserfisch.
            </div>
            <div style="margin-top:0.8rem; color:#555;">
                Tipps für bessere Ergebnisse:
                <ul>
                    <li>Fisch vollständig und scharf abgelichtet</li>
                    <li>Guter Kontrast zum Hintergrund</li>
                    <li>Seitliche Aufnahme bevorzugt</li>
                </ul>
            </div>
        </div>
        """, unsafe_allow_html=True)

        # Trotzdem Bundesland anzeigen zum Stöbern
        st.markdown("#### 🔍 Fisch manuell suchen")
        col1, col2 = st.columns(2)
        with col1:
            manual_fish = st.selectbox("Fischart", ["– wählen –"] + list(FISH_REGULATIONS.keys()))
        with col2:
            manual_bl = st.selectbox("Bundesland", ["– wählen –"] + BUNDESLAENDER)

        if manual_fish != "– wählen –" and manual_bl != "– wählen –":
            regs = FISH_REGULATIONS.get(manual_fish, {})
            bl_regs = regs.get(manual_bl) or regs.get("default", {})
            if bl_regs:
                st.markdown(f"**Schonzeit:** {bl_regs.get('schonzeit','–')}")
                if bl_regs.get('mindestmass'):
                    st.markdown(f"**Mindestmaß:** {bl_regs['mindestmass']}")

else:
    st.markdown("""
    <div style="text-align:center; padding: 3rem 1rem; color:#5f7f96;">
        <div style="font-size:4rem;">📸</div>
        <div style="font-size:1.1rem; margin-top:0.5rem;">
            Laden Sie ein Foto Ihres Fangs hoch, um Fischart, Schonzeit und Mindestmaß zu ermitteln.
        </div>
    </div>
    """, unsafe_allow_html=True)
