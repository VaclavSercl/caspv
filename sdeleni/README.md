# Sdělení ČASPV

Měsíční redakční příprava Sdělení České asociace Sport pro všechny.

Aktuální výstup: `Sdeleni_CASPV_zari_2026.pdf` (rozšířené zářijové vydání, aktualizováno 17. 9. 2026).
Vydání zahrnuje aktuální informace dostupné k 17. 9. 2026, včetně zpráv zveřejněných po 1. září.

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

Skript vytvoří PDF v kořeni repozitáře a náhledy v `tmp/pdfs/`. Před odevzdáním zkontrolujte všechny strany. Úplný text je v `output/Sdeleni_CASPV_2026-09.md`; přehled ověřených zdrojů a rozporů v `output/Overeni_webu_2026-09-17.md`. Starší soubor s příponou `_navrh.md` je archivní.

## Měsíční postup
Interní redakční koncepce zůstává v místní složce mimo veřejný repozitář. Ověřte aktuálnost zdrojů, připravte text, sestavte PDF a vizuálně zkontrolujte stránky. Každé dokončené vydání zaznamenejte samostatným commitem. GitHub zde slouží ke spolupráci a historii návrhů; vydání určené členům musí být označeno jako schválené až po skutečném schválení.

Původní e-mail, interní podklady, pracovní soubory a starší pracovní PDF zůstávají místně mimo Git. Logo a fotografie jsou materiály ČASPV; repozitář jim neuděluje novou licenci.

Pravidelné externí zdroje: ČUS, NSA, ministrsportu.cz, DZS a příručka Erasmus+. Vydání rozlišuje platné povinnosti, otevřené příležitosti a připravované změny.

Rubrika Z krajů - Praha: pravidelně kontrolovat https://www.spvpraha.cz/ včetně kalendáře a odkazovaných propozic; rozlišovat pozvánky a předběžnou termínovou listinu.
