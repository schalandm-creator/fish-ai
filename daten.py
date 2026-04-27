"""
fish_data.py – Schonzeiten & Mindestmaße für Süßwasserfische in Deutschland.
Quellen: Länder-Fischereigesetze und -verordnungen (Stand 2024).
Angaben ohne Gewähr – bitte immer die aktuelle Behördenauskunft einholen.
"""

BUNDESLAENDER = [
    "Baden-Württemberg",
    "Bayern",
    "Berlin",
    "Brandenburg",
    "Bremen",
    "Hamburg",
    "Hessen",
    "Mecklenburg-Vorpommern",
    "Niedersachsen",
    "Nordrhein-Westfalen",
    "Rheinland-Pfalz",
    "Saarland",
    "Sachsen",
    "Sachsen-Anhalt",
    "Schleswig-Holstein",
    "Thüringen",
]
  
# Struktur:
#   FISH_REGULATIONS[Fischart][Bundesland] = {schonzeit, mindestmass, hinweis}
# Falls kein bundeslandspezifischer Eintrag → "default" wird genutzt.

FISH_REGULATIONS = {
    "Hecht": {
        "default": {
            "schonzeit":   "01. Februar – 30. April",
            "mindestmass": "50 cm",
            "hinweis":     "Regional können abweichende Regelungen gelten.",
        },
        "Bayern": {
            "schonzeit":   "01. Februar – 30. April",
            "mindestmass": "50 cm",
        },
        "Brandenburg": {
            "schonzeit":   "01. Februar – 30. April",
            "mindestmass": "50 cm",
            "hinweis":     "In manchen Gewässern verlängert bis 15. Mai.",
        },
        "Mecklenburg-Vorpommern": {
            "schonzeit":   "01. Februar – 30. April",
            "mindestmass": "50 cm",
        },
        "Schleswig-Holstein": {
            "schonzeit":   "01. Februar – 31. März",
            "mindestmass": "50 cm",
        },
        "Nordrhein-Westfalen": {
            "schonzeit":   "01. März – 30. April",
            "mindestmass": "50 cm",
        },
        "Baden-Württemberg": {
            "schonzeit":   "01. Februar – 30. April",
            "mindestmass": "50 cm",
        },
    },

    "Zander": {
        "default": {
            "schonzeit":   "01. März – 31. Mai",
            "mindestmass": "50 cm",
        },
        "Bayern": {
            "schonzeit":   "01. März – 31. Mai",
            "mindestmass": "50 cm",
        },
        "Schleswig-Holstein": {
            "schonzeit":   "01. März – 31. Mai",
            "mindestmass": "45 cm",
        },
        "Mecklenburg-Vorpommern": {
            "schonzeit":   "01. März – 31. Mai",
            "mindestmass": "50 cm",
        },
        "Brandenburg": {
            "schonzeit":   "01. März – 31. Mai",
            "mindestmass": "50 cm",
        },
        "Nordrhein-Westfalen": {
            "schonzeit":   "01. März – 31. Mai",
            "mindestmass": "50 cm",
        },
    },

    "Barsch": {
        "default": {
            "schonzeit":   "Keine bundesweit einheitliche Schonzeit",
            "mindestmass": "Je nach Bundesland 15–20 cm",
            "hinweis":     "Viele Bundesländer haben keine oder nur kurze Schonzeiten für den Flussbarsch.",
        },
        "Bayern": {
            "schonzeit":   "Keine allgemeine Schonzeit",
            "mindestmass": "15 cm",
        },
        "Schleswig-Holstein": {
            "schonzeit":   "01. April – 31. Mai",
            "mindestmass": "18 cm",
        },
        "Brandenburg": {
            "schonzeit":   "01. April – 31. Mai",
            "mindestmass": "20 cm",
        },
        "Nordrhein-Westfalen": {
            "schonzeit":   "Keine allgemeine Schonzeit",
            "mindestmass": "15 cm",
        },
        "Baden-Württemberg": {
            "schonzeit":   "Keine allgemeine Schonzeit",
            "mindestmass": "15 cm",
        },
    },

    "Forelle": {
        "default": {
            "schonzeit":   "01. Oktober – 28. Februar (Bachforelle)",
            "mindestmass": "25 cm (Bachforelle) / 30 cm (Regenbogenforelle)",
            "hinweis":     "Regenbogenforelle meist ganzjährig angelbar. Meerforelle: eigene Regelung.",
        },
        "Bayern": {
            "schonzeit":   "01. Oktober – 28. Februar (Bach- & Seeforelle)",
            "mindestmass": "25 cm (Bach) / 35 cm (See)",
        },
        "Baden-Württemberg": {
            "schonzeit":   "01. November – 28. Februar",
            "mindestmass": "25 cm",
        },
        "Schleswig-Holstein": {
            "schonzeit":   "15. Oktober – 15. Januar",
            "mindestmass": "30 cm (Bach) / 45 cm (Meer)",
        },
        "Nordrhein-Westfalen": {
            "schonzeit":   "01. Oktober – 28. Februar",
            "mindestmass": "25 cm",
        },
        "Mecklenburg-Vorpommern": {
            "schonzeit":   "01. Oktober – 28. Februar",
            "mindestmass": "30 cm",
        },
    },

    "Lachs": {
        "default": {
            "schonzeit":   "15. September – 31. Dezember",
            "mindestmass": "50 cm",
            "hinweis":     "In vielen Bundesländern streng reguliert oder ganzjährig geschont. Bitte unbedingt lokale Vorschriften beachten.",
        },
        "Bayern": {
            "schonzeit":   "01. September – 28. Februar",
            "mindestmass": "50 cm",
        },
        "Schleswig-Holstein": {
            "schonzeit":   "01. September – 31. Dezember (Flüsse)",
            "mindestmass": "60 cm (Ostsee) / 50 cm (Süßwasser)",
        },
    },

    "Karpfen": {
        "default": {
            "schonzeit":   "01. Mai – 30. Juni",
            "mindestmass": "35 cm",
        },
        "Bayern": {
            "schonzeit":   "01. Mai – 30. Juni",
            "mindestmass": "35 cm",
        },
        "Brandenburg": {
            "schonzeit":   "01. Mai – 30. Juni",
            "mindestmass": "35 cm",
        },
        "Nordrhein-Westfalen": {
            "schonzeit":   "01. Mai – 30. Juni",
            "mindestmass": "35 cm",
        },
        "Baden-Württemberg": {
            "schonzeit":   "01. Mai – 30. Juni",
            "mindestmass": "35 cm",
        },
    },

    "Schleie": {
        "default": {
            "schonzeit":   "01. Mai – 30. Juni",
            "mindestmass": "25 cm",
        },
        "Bayern": {
            "schonzeit":   "01. Mai – 30. Juni",
            "mindestmass": "25 cm",
        },
        "Brandenburg": {
            "schonzeit":   "01. Mai – 30. Juni",
            "mindestmass": "25 cm",
        },
        "Schleswig-Holstein": {
            "schonzeit":   "01. Mai – 30. Juni",
            "mindestmass": "25 cm",
        },
    },

    "Brassen": {
        "default": {
            "schonzeit":   "01. Mai – 15. Juni",
            "mindestmass": "25 cm",
        },
        "Bayern": {
            "schonzeit":   "01. Mai – 15. Juni",
            "mindestmass": "25 cm",
        },
        "Brandenburg": {
            "schonzeit":   "01. Mai – 15. Juni",
            "mindestmass": "25 cm",
        },
        "Schleswig-Holstein": {
            "schonzeit":   "01. Mai – 15. Juni",
            "mindestmass": "20 cm",
        },
    },

    "Aal": {
        "default": {
            "schonzeit":   "Keine bundesweit einheitliche Schonzeit",
            "mindestmass": "45 cm",
            "hinweis":     "Der Aal ist stark gefährdet (IUCN: critically endangered). In einigen Bundesländern ist die Entnahme stark eingeschränkt oder verboten. Bitte unbedingt lokale Vorschriften prüfen.",
        },
        "Bayern": {
            "schonzeit":   "Keine allgemeine Schonzeit",
            "mindestmass": "45 cm",
            "hinweis":     "Besatzpflicht in vielen Gewässern.",
        },
        "Schleswig-Holstein": {
            "schonzeit":   "01. Oktober – 30. November (Blankaale)",
            "mindestmass": "45 cm",
        },
        "Mecklenburg-Vorpommern": {
            "schonzeit":   "15. September – 15. November",
            "mindestmass": "45 cm",
        },
        "Brandenburg": {
            "schonzeit":   "Keine allgemeine Schonzeit",
            "mindestmass": "45 cm",
        },
    },

    "Wels": {
        "default": {
            "schonzeit":   "01. Mai – 30. Juni",
            "mindestmass": "70 cm",
        },
        "Bayern": {
            "schonzeit":   "01. Mai – 30. Juni",
            "mindestmass": "70 cm",
        },
        "Brandenburg": {
            "schonzeit":   "01. Mai – 30. Juni",
            "mindestmass": "70 cm",
        },
        "Baden-Württemberg": {
            "schonzeit":   "01. Mai – 30. Juni",
            "mindestmass": "70 cm",
        },
        "Nordrhein-Westfalen": {
            "schonzeit":   "01. Mai – 30. Juni",
            "mindestmass": "70 cm",
        },
    },

    "Äsche": {
        "default": {
            "schonzeit":   "01. März – 30. April",
            "mindestmass": "30 cm",
            "hinweis":     "Die Äsche ist in Deutschland gefährdet. In manchen Bundesländern ganzjährig geschützt.",
        },
        "Bayern": {
            "schonzeit":   "01. März – 30. April",
            "mindestmass": "30 cm",
        },
        "Baden-Württemberg": {
            "schonzeit":   "01. März – 31. Mai",
            "mindestmass": "30 cm",
        },
        "Nordrhein-Westfalen": {
            "schonzeit":   "01. März – 30. April",
            "mindestmass": "30 cm",
        },
        "Schleswig-Holstein": {
            "schonzeit":   "15. Februar – 15. April",
            "mindestmass": "30 cm",
        },
    },

    "Rotauge": {
        "default": {
            "schonzeit":   "01. Mai – 15. Juni",
            "mindestmass": "15 cm",
        },
        "Bayern": {
            "schonzeit":   "Keine allgemeine Schonzeit",
            "mindestmass": "15 cm",
        },
        "Brandenburg": {
            "schonzeit":   "01. Mai – 15. Juni",
            "mindestmass": "15 cm",
        },
        "Schleswig-Holstein": {
            "schonzeit":   "01. Mai – 15. Juni",
            "mindestmass": "15 cm",
        },
    },

    "Rotfeder": {
        "default": {
            "schonzeit":   "01. Mai – 15. Juni",
            "mindestmass": "15 cm",
        },
    },

    "Stör": {
        "default": {
            "schonzeit":   "Ganzjährig geschont (streng geschützte Art)",
            "mindestmass": "Keine Entnahme erlaubt",
            "hinweis":     "Der Europäische Stör (Acipenser sturio) ist vom Aussterben bedroht und darf nicht entnommen werden. Sofortiger schonender Rückwurf ist Pflicht.",
        },
    },

    "Makrele": {
        "default": {
            "schonzeit":   "Keine allgemeine Schonzeit (Küstenmeer)",
            "mindestmass": "20 cm (Ostsee) / 30 cm (Nordsee)",
            "hinweis":     "Primär Meeresfisch. Für Binnengewässer nicht relevant.",
        },
    },
}
