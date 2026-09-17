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
  if s=='<!-- PHOTOS -->':
   add_photos()
  elif s.startswith('<!-- SMALL -->'): p(s.removeprefix('<!-- SMALL -->'),'SmallText')
  elif s.startswith('|'):
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

def add_photos():
 photos=Table([[Image(str(base/'assets/sport-21.jpg'),width=231,height=173.25),Image(str(base/'assets/sport-36.jpg'),width=231,height=173.25)]],colWidths=[245.5,245.5])
 photos.setStyle(TableStyle([('VALIGN',(0,0),(-1,-1),'TOP'),('LEFTPADDING',(0,0),(-1,-1),0),('RIGHTPADDING',(0,0),(-1,-1),14),('TOPPADDING',(0,0),(-1,-1),4),('BOTTOMPADDING',(0,0),(-1,-1),8)]))
 story.append(photos)

text=(base/'output/Sdeleni_CASPV_2026-09.md').read_text(encoding='utf-8')
sections=text.split('<!-- PAGE -->')
for idx,section in enumerate(sections):
 if idx: story.append(PageBreak())
 else:
  p('Sdělení ČASPV','Title')
  p('ZÁŘÍ 2026  /  AKTUALIZOVÁNO 17. 9. 2026','SmallText')
  story.append(Spacer(1,10))
 parse(section)

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
 c.drawString(52,28,'ČASPV  •  Sdělení  •  Září 2026')
 c.drawRightString(A4[0]-52,28,f'{d.page} / {len(sections)}')
 c.restoreState()
out=base/'Sdeleni_CASPV_zari_2026.pdf'
SimpleDocTemplate(str(out),pagesize=A4,rightMargin=52,leftMargin=52,topMargin=68,bottomMargin=60,title='Sdělení ČASPV září 2026',author='Česká asociace Sport pro všechny').build(story,onFirstPage=footer,onLaterPages=footer)
import pypdfium2 as pdfium
pdf=pdfium.PdfDocument(str(out))
for i,page in enumerate(pdf): page.render(scale=1.3).to_pil().save(base/f'tmp/pdfs/final-page-{i+1}.png')
assert len(pdf)==len(sections), f'Unexpected overflow: {len(pdf)} pages for {len(sections)} sections'
print(out); print('PAGES',len(pdf))
