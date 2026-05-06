
import os
import re
from lxml import etree

W_NS = "http://schemas.openxmlformats.org/wordprocessingml/2006/main"
NSMAP = {'w': W_NS}

def clean_text(text):
    # Remove senior info and replace with Titus
    text = text.replace("TANIMOWO, EMMANUEL OLUWADARASIMI", "IFET GREAT TITUS")
    text = text.replace("Tanimowo Emmanuel Oluwadarasimi", "Ifet Great Titus")
    text = text.replace("2101110048", "2201110075")
    # Clean up project title if necessary
    text = text.replace("ARTIFICIAL INTELLIGENCE ENHANCED JOB PLATFORM", "ADIPHAS: AUTONOMOUS DISEASE INTELLIGENCE AND PUBLIC HEALTH ADVISORY SYSTEM")
    return text

def create_run(text, bold=False, italic=False, size=24):
    r = etree.Element(f"{{{W_NS}}}r")
    rPr = etree.SubElement(r, f"{{{W_NS}}}rPr")
    rFonts = etree.SubElement(rPr, f"{{{W_NS}}}rFonts")
    rFonts.set(f"{{{W_NS}}}ascii", "Times New Roman")
    rFonts.set(f"{{{W_NS}}}hAnsi", "Times New Roman")
    sz = etree.SubElement(rPr, f"{{{W_NS}}}sz")
    sz.set(f"{{{W_NS}}}val", str(size))
    if bold: etree.SubElement(rPr, f"{{{W_NS}}}b")
    if italic: etree.SubElement(rPr, f"{{{W_NS}}}i")
    t = etree.SubElement(r, f"{{{W_NS}}}t")
    t.text = text
    return r

def total_consolidation():
    senior_xml = r'c:\Users\Adegoke\Desktop\New folder\docs\ADIPHAS\unpacked_senior\word\document.xml'
    adiphas_xml = r'c:\Users\Adegoke\Desktop\New folder\docs\ADIPHAS\unpacked_v6_final_attempt\word\document.xml'
    
    # Load and clean Senior Template (Prelims only)
    with open(senior_xml, 'r', encoding='utf-8') as f:
        s_content = f.read()
    s_content = clean_text(s_content)
    s_tree = etree.fromstring(s_content.encode('utf-8'))
    s_body = s_tree.find(f"{{{W_NS}}}body")
    s_paragraphs = s_body.xpath(".//w:p", namespaces=NSMAP)
    
    prelims = []
    for p in s_paragraphs:
        text = "".join(p.xpath(".//w:t/text()", namespaces=NSMAP))
        if "CHAPTER ONE" in text.upper(): break
        prelims.append(p)

    # Load and clean ADIPHAS content
    with open(adiphas_xml, 'r', encoding='utf-8') as f:
        a_content = f.read()
    a_content = clean_text(a_content)
    a_tree = etree.fromstring(a_content.encode('utf-8'))
    a_body = a_tree.find(f"{{{W_NS}}}body")
    a_paragraphs = a_body.xpath(".//w:p", namespaces=NSMAP)
    
    content = []
    start_collecting = False
    for p in a_paragraphs:
        text = "".join(p.xpath(".//w:t/text()", namespaces=NSMAP))
        if "CHAPTER ONE" in text.upper(): start_collecting = True
        if start_collecting:
            # Avoid repetitions by checking if already added
            if text.strip() and any(text.strip() == "".join(c.xpath(".//w:t/text()", namespaces=NSMAP)).strip() for c in content):
                continue
            content.append(p)

    # Rebuild Body
    new_body = etree.Element(f"{{{W_NS}}}body")
    for p in prelims: new_body.append(p)
    for p in content: new_body.append(p)
    
    # Add Section Properties (Keep original)
    sectPr = a_body.find(f"{{{W_NS}}}sectPr")
    if sectPr is not None: new_body.append(sectPr)
    
    a_tree.replace(a_body, new_body)
    
    with open(adiphas_xml, 'wb') as f:
        f.write(etree.tostring(a_tree, encoding='UTF-8', xml_declaration=True))
    
    print("Success: Wholistic consolidation and metadata scrub complete.")

total_consolidation()
