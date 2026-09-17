from pathlib import Path
import re
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, Image, KeepTogether
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
base=Path(__file__).resolve().parents[1]
(base/'tmp/pdfs').mkdir(parents=True, exist_ok=True)
for name,file in [('Arial','arial.ttf'),('Arial-Bold','arialbd.ttf'),('Arial-Italic','ariali.ttf')]:
 pdfmetrics.registerFont(TTFont(name,'C:/Windows/Fonts/'+file))
pdfmetrics.registerFontFamily('Arial',normal='Arial',bold='Arial-Bold',italic='Arial-Italic',boldItalic='Arial-Bold')
styles=getSampleStyleSheet()
for name in ['Normal','BodyText','Title','Heading1','Heading2','Heading3']:
 styles[name].fontName='Arial'; styles[name].textColor=colors.HexColor('#172333')
styles['BodyText'].fontSize=11; styles['BodyText'].leading=15.8; styles['BodyText'].spaceAfter=8
styles['Title'].fontName='Arial-Bold'; styles['Title'].fontSize=30; styles['Title'].leading=35; styles['Title'].alignment=TA_LEFT
styles['Heading2'].fontName='Arial-Bold'; styles['Heading2'].fontSize=18; styles['Heading2'].leading=21; styles['Heading2'].spaceBefore=13; styles['Heading2'].spaceAfter=9
styles['Heading3'].fontName='Arial-Bold'; styles['Heading3'].fontSize=12; styles['Heading3'].leading=16
styles.add(ParagraphStyle(name='SmallText',fontName='Arial',fontSize=8.5,leading=12,spaceAfter=7,textColor=colors.HexColor('#506070')))
styles.add(ParagraphStyle(name='CellText',fontName='Arial',fontSize=9,leading=12))
def inline(s):
 s=s.replace('&','&amp;').replace('–','-').replace('—','-')
 s=re.sub(r'\[([^\]]+)\]\(([^)]+)\)',r'<a href="\2" color="#175b87">\1</a>',s)
 return re.sub(r'\*\*(.+?)\*\*',r'<b>\1</b>',s)
story=[]
def p(s,style='BodyText'): story.append(Paragraph(inline(s),styles[style]))
def heading(s): p(s,'Heading2')
def parse(text):
 lines=text.strip().splitlines(); i=0
 while i<len(lines):
  s=lines[i].strip(); i+=1
  if not s: continue
  if s.startswith('|'):
   rows=[s]
   while i<len(lines) and lines[i].strip().startswith('|'): rows.append(lines[i].strip()); i+=1
   data=[]
   for row in rows:
    if re.fullmatch(r'[| :\-]+',row): continue
    data.append([Paragraph(inline(c.strip()),styles['CellText']) for c in row.strip('|').split('|')])
   t=Table(data,colWidths=[64,177,111,139],repeatRows=1,hAlign='LEFT')
   t.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,0),colors.HexColor('#dfebf2')),('GRID',(0,0),(-1,-1),0.5,colors.HexColor('#d9d9d9')),('VALIGN',(0,0),(-1,-1),'MIDDLE'),('LEFTPADDING',(0,0),(-1,-1),7),('RIGHTPADDING',(0,0),(-1,-1),7),('TOPPADDING',(0,0),(-1,-1),8),('BOTTOMPADDING',(0,0),(-1,-1),8)])); story.append(t); story.append(Spacer(1,10))
  elif s.startswith('#### '): p(s[5:],'Heading3')
  elif s.startswith('### '): heading(s[4:])
  elif s.startswith('- '): p('• '+s[2:])
  else: p(s,'SmallText' if s.startswith('Zdroj:') else 'BodyText')
text=(base/'output/Sdeleni_CASPV_2026-09-01_navrh.md').read_text(encoding='utf-8')
p('Sdělení ČASPV','Title'); p('ZÁŘÍ 2026  /  INFORMACE PRO ČLENY','SmallText'); story.append(Spacer(1,14))

p('Zpětný návrh k 1. září, doplněný příspěvkem metodické rady ze 17. září 2026. Přihlašovací termíny jsou uvedeny v historickém kontextu.','SmallText')
parse(text.split('V září zahajujeme',1)[1].split('### Aktivní září')[0].join(['V září zahajujeme','']))
parse('### Aktivní září'+text.split('### Aktivní září',1)[1].split('### Rozhodnutí')[0])
story.append(PageBreak())
parse('### Rozhodnutí'+text.split('### Rozhodnutí',1)[1].split('### Inspirace')[0])
story.append(PageBreak())
heading('Informace z metodické rady')
p('Doplnění dodané 17. září 2026','SmallText')
p('Metodická rada ČASPV se částečně obměnila a některé odborné komise zaznamenaly změny ve složení. Svou práci ve vedení rady ukončila Radka Mothejzíková. Děkujeme jí za veškerou práci, kterou pro ČASPV vykonala. Novou předsedkyní Metodické rady ČASPV se stala Mgr. Martina Mlýnková. Složení komisí bude průběžně aktualizováno na [webu metodické rady](https://www.caspv.cz/cz/metodicka-rada/).')
p('Termínové listiny a příprava roku 2027','Heading3')
p('Termínová listina centrálních akcí na rok 2026 je zveřejněna na webu ČASPV a průběžně se aktualizuje. Podrobnosti k jednotlivým akcím jsou dostupné v [kalendáři akcí](https://www.caspv.cz/cz/kalendar-akci/), kde lze využít i vyhledávání.')
p('Podle podkladu metodické rady jsou termínová listina centrálních akcí pro rok 2027 a vyhlášení republikových akcí pro rok 2027 ve schvalovacím procesu. Zveřejnění termínové listiny je plánováno do konce září 2026 a vyhlášení republikových soutěží do konce října 2026. Následovat má příprava termínových listin jednotlivých KASPV.')
p('Víkend v pohybu s ČASPV','Heading3')
p('**13.-15. listopadu 2026, Sportcentrum Brandýs nad Labem.** Metodická rada zve na víkend vzdělávání, praktických workshopů a sdílení zkušeností. Program má zahrnout 13 hodin přednášek a pohybových aktivit: práci s chybou, funkční pohyb, psychomotoriku, práci s hudbou a respektující sportovní prostředí.')
p('Akce je určena instruktorům, lektorům, pedagogům, pedagogům volného času a trenérům napříč sportovními odvětvími i generacemi. Členové ČASPV mají zvýhodněnou cenu. [Program a přihlášení](https://www.caspv.cz/cz/kalendar-akci/2454-vikend-v-pohybu-s-caspv.html).')

p('Podzimní republikové soutěže','Heading3')
p('Odborné komise připravují na říjen a listopad soutěže Mölkky - Kubb - Woodball OPEN, TeamGym, sportovní gymnastiku jednotlivců a florbal. Podle metodické rady je u většiny přihlašování již aktivní. Konkrétní uzávěrky a propozice sledujte v [kalendáři soutěží](https://www.caspv.cz/cz/kalendar-akci/?s=19).')
p('Zápolení na dálku','Heading3')
p('Projekt funguje od roku 2019. Vedle odborů SPV se do něj zapojují také základní a střední školy. Zájemci najdou podmínky účasti a přihlášení na [stránce podzimního kola](https://www.caspv.cz/cz/kalendar-akci/2449-zapoleni-na-dalku-podzimni-kolo.html) a v [informacích o projektu](https://www.caspv.cz/cz/projekty/zapoleni-na-dalku/).')
p('Zdroj: Podklady pro Sdělení 26-09.docx, zaslané Martinou Mlýnkovou 17. září 2026. Údaje této části nejsou dokladem stavu k 1. září.','SmallText')
story.append(PageBreak())
parse('### Inspirace'+text.split('### Inspirace',1)[1])
heading('Pohyb napříč generacemi')
p('Hry, společný pohyb a setkávání patří k činnosti ČASPV. Při představování nových hodin pomůže konkrétní nabídka: pro koho jsou určeny, kdy a kde probíhají a koho kontaktovat.')
photos=Table([[Image(str(base/'assets/sport-21.jpg'),width=231,height=173.25),Image(str(base/'assets/sport-36.jpg'),width=231,height=173.25)]],colWidths=[245.5,245.5])
photos.setStyle(TableStyle([('VALIGN',(0,0),(-1,-1),'TOP'),('LEFTPADDING',(0,0),(-1,-1),0),('RIGHTPADDING',(0,0),(-1,-1),14),('TOPPADDING',(0,0),(-1,-1),4),('BOTTOMPADDING',(0,0),(-1,-1),8)]))
story.append(photos)
p('Ilustrační archivní fotografie z webu ČASPV. Nejde o reportáž ze září 2026.','SmallText')
heading('O tomto vydání')
p('Redakční návrh pro Českou asociaci Sport pro všechny. Zpracováno 17. září 2026. Historická část vychází z usnesení valné hromady, veřejných pozvánek a informací dostupných před zářím. Příspěvek metodické rady je datován samostatně. Podrobné zdroje jsou dostupné prostřednictvím odkazů v textu.','SmallText')
story.append(PageBreak())
heading('Stálé informace')
p('Kontakty a praktický servis pro členy a pořadatele • Ověřeno 17. září 2026','SmallText')
p('Kontakt na ČASPV','Heading3')
p('**Česká asociace Sport pro všechny, z.s.**<br/>Ohradské náměstí 1628/7, 155 00 Praha 5 • IČO 00551368<br/>**Web:** [www.caspv.cz](https://www.caspv.cz/) • **E-mail:** [sekretariat@caspv.cz](mailto:sekretariat@caspv.cz)<br/>**Ústřední telefon:** +420 242 480 301<br/>**Sekretariát a potvrzení úrazů:** Alena Čechová, +420 242 480 303, +420 777 700 489.')
p('Úrazové pojištění a hlášení úrazu','Heading3')
p('**UNIQA pojišťovna, a.s. • smlouva č. 3558001543 • od 1. února 2025.** Skupinové pojištění sjednal Český olympijský výbor. Za smluvních podmínek zahrnuje členy při organizovaných sportovních aktivitách a organizovaných cestách na ně i nečleny během účasti na akcích pojištěných subjektů. Nevztahuje se na profesionální sportovce ani neorganizovanou soukromou činnost.')
p('**Postup:** zaznamenejte datum, okolnosti a pořadatele akce, uchovejte lékařské zprávy. Hlášení zašlete sekretariátu ČASPV k potvrzení; škodu oznamte UNIQA s číslem smlouvy. Formuláře a aktuální podmínky: [Úrazové pojištění ČASPV](https://www.caspv.cz/cz/caspv/dokumenty/smlouvy/urazove-pojisteni/). Rozsah plnění určují pojistné podmínky; nejde o automatické odškodnění každého drobného úrazu.')
p('Cesty do zahraničí','Heading3')
p('Cestovní pojištění se sjednává samostatně. ČASPV zveřejňuje nabídku **Generali České pojišťovny** pro členy a rodinné příslušníky. Aktuální cenu, rozsah sportů a délku výjezdu ověřte před sjednáním u makléře **Pavla Školníka: 608 317 942, fidesplus@gmail.com**. [Informace ČASPV](https://www.caspv.cz/cz/caspv/dokumenty/smlouvy/cestovni-pojisteni/).')
p('Hudba při cvičení a na akcích','Heading3')
p('**OSA** zastupuje autory hudby; **INTERGRAM** výkonné umělce a výrobce záznamů. ČASPV a její organizační články využívají příslušné kolektivní smlouvy přes **ČOV**, který hradí sjednané centrální odměny. Pro užití zahrnuté ve smlouvách se neplatí další individuální licence za tutéž produkci. Rozsah je nutné posoudit podle konkrétní akce.')
p('**Kdy ověřit zvláštní licenci:** například podnikatelské lekce OSVČ, taneční zábavy či koncerty, některé akce s externím spolupořadatelem a užití nad rámec smluv. Před objednáním licence nebo úhradou výzvy kontaktujte sekretariát; u nepokrytého užití pořadatel sjedná licenci a uhradí odměnu příslušnému správci podle smlouvy či faktury. OSA v čl. 4.1 stanoví také předání playlistu do 15 dnů po produkcích vymezených tímto článkem.')
p('Podmínky a výjimky: [aktuální smlouvy ČOV s OSA a INTERGRAM](https://www.olympijskytym.cz/osa-integram) • [informace ČASPV](https://www.caspv.cz/cz/caspv/dokumenty/smlouvy/osa-intergram/). Licence pro cvičení není automatickým oprávněním k použití hudby ve videu na internetu.','SmallText')
p('Při změně kontaktů nebo smluv se tato stránka aktualizuje. Přehled nenahrazuje úplné pojistné a licenční podmínky.','SmallText')

story.append(PageBreak())
heading('Jak se zapojit do ČASPV')
p('Členství jednotlivců a vlastní sportovní klub • Praktický postup','SmallText')
p('1. Chci se stát členem','Heading3')
p('**Najděte si místní odbor SPV.** Vyberte si oddíl či skupinu podle místa bydliště a nabídky pohybových aktivit. S vyhledáním vhodného odboru pomůže [sekretariat@caspv.cz](mailto:sekretariat@caspv.cz). Členem se může stát občan ČR i cizinec.')
p('**Podejte přihlášku.** Vyplňte požadované údaje a přihlášku předejte místnímu odboru. U zájemce mladšího 18 let je nutný podpis zákonného zástupce. [Vzor přihlášky jednotlivce](https://www.caspv.cz/download/sites/vzor-prihlasky-do-caspv-clen-2019-2716.doc) je dostupný na webu; před použitím si ověřte aktuální verzi.')
p('**Dohodněte příspěvek a začněte cvičit.** Výši členského příspěvku, splatnost a platební údaje vám sdělí místní odbor. Ověřte si, že vás zařadil do členské evidence. Samotná registrace účtu na webu nenahrazuje přihlášení za člena.')
p('2. Máme klub a chceme vstoupit do ČASPV','Heading3')
p('**Obraťte se na sekretáře krajské asociace SPV** v kraji, kde klub působí. Kontakt zprostředkuje i ústřední sekretariát. S KASPV dohodněte podmínky přijetí, evidenci členů a odvádění příspěvků.')
p('Použijte [přihlášku právnické osoby / odboru](https://www.caspv.cz/download/sites/vzor-prihlasky-do-caspv-odbor-2019-2717.doc). Pro jednání doporučujeme připravit název a IČO klubu, stanovy, kontakt na oprávněného zástupce a stručný přehled činnosti. Přesné přílohy a aktuální formulář potvrdí KASPV. Zápis spolku ve veřejném rejstříku sám o sobě členství v ČASPV nezakládá.')
p('3. Chceme založit vlastní klub','Heading3')
p('**Zvolte způsob fungování.** Skupina může po dohodě působit v existující tělovýchovné jednotě či klubu. Pokud chcete samostatnou právnickou osobu, obvyklou cestou je založení spolku.')
p('**Připravte spolek alespoň se třemi zakladateli.** Dohodněte stanovy: název a sídlo, účel, práva a povinnosti členů a statutární orgán. Ustavte vedení a písemně zachyťte zakladatelská rozhodnutí. Právní základ stanoví občanský zákoník, zejména § 214 a následující.')
p('**Podejte návrh na zápis do spolkového rejstříku.** Použijte formulář Ministerstva spravedlnosti a přiložte listiny dokládající zapisované skutečnosti. Návrh se podává příslušnému rejstříkovému soudu. Spolek vzniká zápisem do rejstříku; podrobný postup a způsob podání uvádí [Portál veřejné správy](https://portal.gov.cz/sluzby-vs/zapis-do-spolkoveho-rejstriku-S15505).')
p('**Následně dohodněte vstup do ČASPV s KASPV.** Nastavte členskou evidenci, příspěvky, účetnictví, odpovědnosti vedení a pravidla bezpečného cvičení. Před zahájením činnosti ověřte také rozsah pojištění a podmínky užívání hudby uvedené na předchozí stránce.')
p('Přihlášky a podmínky: [Jak se stát členem ČASPV](https://www.caspv.cz/cz/caspv/jak-se-stat-clenem/). Právní základ: [občanský zákoník](https://e-sbirka.gov.cz/sb/2012/89/2026-01-01). Ověřeno 17. září 2026.','SmallText')

def footer(c,d):
 c.saveState()
 navy=colors.HexColor('#151e68'); blue=colors.HexColor('#6cc0f2')
 if d.page==1:
  c.drawImage(str(base/'assets/identita/2025_Logo_SPV/SPV_Logo_color.png'),A4[0]-122,A4[1]-112,70,70,mask='auto')
 else:
  c.drawImage(str(base/'assets/identita/2025_Logo_SPV/SPV_Logo_color.png'),52,A4[1]-53,28,28,mask='auto')
  c.setFont('Arial-Bold',8); c.setFillColor(navy); c.drawString(91,A4[1]-37,'ČESKÁ ASOCIACE SPORT PRO VŠECHNY')
  c.setFont('Arial',8); c.drawRightString(A4[0]-52,A4[1]-37,'SDĚLENÍ  /  ZÁŘÍ 2026')
 c.setFillColor(navy); c.rect(52,43,A4[0]-104,1,fill=1,stroke=0)
 c.setFont('Arial',8); c.setFillColor(colors.HexColor('#506070'))
 c.drawString(52,28,'ČASPV  •  Září 2026  •  Redakční návrh')
 c.drawRightString(A4[0]-52,28,f'{d.page} / 6')
 c.restoreState()
out=base/'Sdeleni_CASPV_zari_2026_v4.pdf'
SimpleDocTemplate(str(out),pagesize=A4,rightMargin=52,leftMargin=52,topMargin=68,bottomMargin=60,title='Sdělení ČASPV září 2026',author='ČASPV - redakční návrh').build(story,onFirstPage=footer,onLaterPages=footer)
import pypdfium2 as pdfium
pdf=pdfium.PdfDocument(str(out))
for i,page in enumerate(pdf): page.render(scale=1.3).to_pil().save(base/f'tmp/pdfs/v4-page-{i+1}.png')
print(out); print('PAGES',len(pdf))
