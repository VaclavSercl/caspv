# Sdělení ČASPV

Měsíční redakční příprava Sdělení České asociace Sport pro všechny.

Aktuální výstup: `Sdeleni_CASPV_zari_2026_v4.pdf` (6 stran, redakční návrh).
Zářijové číslo je zpětný návrh k 1. 9. 2026 s odděleně datovaným doplněním metodické rady ze 17. 9. 2026.

## Obsah repozitáře
- `output/`: zdrojový text vydání.
- `scripts/build_pdf.py`: úplná sazba aktuálního vydání včetně metodické rady a stálých stránek.
- `assets/`: použité logo a fotografie z webu ČASPV.
- `Analyza_grafiky_a_zdroju.md`: grafická koncepce a zdroje.

## Sestavení PDF
Windows, Python 3, systémové fonty Arial:

```powershell
python -m pip install -r requirements.txt
python scripts/build_pdf.py
```

Skript vytvoří PDF v kořeni repozitáře a náhledy v `tmp/pdfs/`. Před odevzdáním zkontrolujte všech šest stran. Část textu je v Markdownu, doplňující rubriky přímo v sazbovém skriptu.

## Měsíční postup
Interní redakční koncepce zůstává v místní složce mimo veřejný repozitář. Ověřte aktuálnost zdrojů, připravte text, sestavte PDF a vizuálně zkontrolujte stránky. Každé dokončené vydání zaznamenejte samostatným commitem. GitHub zde slouží ke spolupráci a historii návrhů; vydání určené členům musí být označeno jako schválené až po skutečném schválení.

Původní e-mail, interní podklady, pracovní soubory a starší pracovní PDF zůstávají místně mimo Git. Logo a fotografie jsou materiály ČASPV; repozitář jim neuděluje novou licenci.
