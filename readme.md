Technologie
KomponenteDetailsFrameworkStreamlitKI-ModellEfficientNet-B2 (torchvision, ImageNet-Gewichte)MappingImageNet-Labels → deutsche Fischnamen (custom)DatenManuelle Datenbank basierend auf Länder-Fischereigesetzen
Warum EfficientNet-B2?
Das Modell ist auf ImageNet mit ~1000 Klassen vortrainiert und enthält mehrere Fischkategorien (Tench, Eel, Coho Salmon, Sturgeon u. a.). Es wird kein eigenes Fine-Tuning benötigt – die App mappt die erkannten ImageNet-Labels direkt auf deutsche Fischnamen.

Tipp für höhere Genauigkeit: Ein eigenes Fine-Tuning auf einem Datensatz mit deutschen Süßwasserfischen (z. B. Fish4Knowledge) würde die Erkennungsrate deutlich verbessern.


Haftungsausschluss
Die Schonzeiten und Mindestmaße basieren auf öffentlich zugänglichen Quellen (Stand 2024). Sie können sich jährlich ändern. Bitte prüfen Sie immer die aktuell gültigen Regelungen der zuständigen Fischereibehörde Ihres Bundeslandes.

Lizenz
MIT License – frei verwendbar und erweiterbar.
