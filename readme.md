# 🐟 FischFinder Deutschland

Eine KI-gestützte Streamlit-App zur Erkennung von Fischarten in Deutschland – inklusive Schonzeit und Mindestmaß je Bundesland.

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://share.streamlit.io)

---

## Features

- 📸 **Fischerkennung** per Foto-Upload (EfficientNet-B2, vortrainiert auf ImageNet)
- 🗓️ **Schonzeiten** für alle wichtigen deutschen Süßwasserfischarten
- 📏 **Mindestmaße** bundeslandspezifisch
- 🗺️ **Alle 16 Bundesländer** abgedeckt
- ⚠️ Hinweise zu geschützten/gefährdeten Arten (Aal, Stör, Äsche)

---

## Erkannte Fischarten

| Art | Schonzeit (default) | Mindestmaß |
|-----|---------------------|------------|
| Hecht | Feb – Apr | 50 cm |
| Zander | Mär – Mai | 50 cm |
| Barsch | variiert | 15–20 cm |
| Forelle | Okt – Feb | 25–35 cm |
| Lachs | Sep – Dez | 50–60 cm |
| Karpfen | Mai – Jun | 35 cm |
| Schleie | Mai – Jun | 25 cm |
| Brassen | Mai – Jun | 25 cm |
| Aal | variiert | 45 cm |
| Wels | Mai – Jun | 70 cm |
| Äsche | Mär – Apr/Mai | 30 cm |
| Rotauge | Mai – Jun | 15 cm |
| Stör | **ganzjährig geschont** | – |

---

## Lokale Installation

```bash
# 1. Repository klonen
git clone https://github.com/DEIN-USERNAME/fischfinder.git
cd fischfinder

# 2. Virtuelle Umgebung (empfohlen)
python -m venv venv
source venv/bin/activate      # Linux/Mac
venv\Scripts\activate         # Windows

# 3. Abhängigkeiten installieren
pip install -r requirements.txt

# 4. App starten
streamlit run app.py
```

Die App öffnet sich automatisch unter `http://localhost:8501`.

---

## Deployment auf Streamlit Community Cloud

1. Dieses Repository auf GitHub pushen (public oder private).
2. Auf [share.streamlit.io](https://share.streamlit.io) einloggen (kostenlos).
3. **New app** → Repository auswählen → `app.py` als Main file → **Deploy**.

Die App ist nach wenigen Minuten öffentlich erreichbar.

---

## Technologie

| Komponente | Details |
|---|---|
| Framework | [Streamlit](https://streamlit.io) |
| KI-Modell | EfficientNet-B2 (torchvision, ImageNet-Gewichte) |
| Mapping | ImageNet-Labels → deutsche Fischnamen (custom) |
| Daten | Manuelle Datenbank basierend auf Länder-Fischereigesetzen |

### Warum EfficientNet-B2?

Das Modell ist auf ImageNet mit ~1000 Klassen vortrainiert und enthält mehrere Fischkategorien (Tench, Eel, Coho Salmon, Sturgeon u. a.). Es wird **kein eigenes Fine-Tuning** benötigt – die App mappt die erkannten ImageNet-Labels direkt auf deutsche Fischnamen.

> **Tipp für höhere Genauigkeit:** Ein eigenes Fine-Tuning auf einem Datensatz mit deutschen Süßwasserfischen (z. B. [Fish4Knowledge](http://homepages.inf.ed.ac.uk/rbf/Fish4Knowledge/)) würde die Erkennungsrate deutlich verbessern.

---

## Haftungsausschluss

Die Schonzeiten und Mindestmaße basieren auf öffentlich zugänglichen Quellen (Stand 2024). Sie können sich jährlich ändern. **Bitte prüfen Sie immer die aktuell gültigen Regelungen der zuständigen Fischereibehörde Ihres Bundeslandes.**

---

## Lizenz

MIT License – frei verwendbar und erweiterbar.
