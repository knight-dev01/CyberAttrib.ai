
import os
from lxml import etree
import re

W_NS = "http://schemas.openxmlformats.org/wordprocessingml/2006/main"
NSMAP = {'w': W_NS}

def update_xml_content(xml_string):
    # Replace names and project titles
    xml_string = xml_string.replace("ARTIFICIAL INTELLIGENCE ENHANCED JOB PLATFORM: A MACHINE LEARNING-DRIVEN RECOMMENDATIONS", "ADIPHAS: AUTONOMOUS DISEASE INTELLIGENCE AND PUBLIC HEALTH ADVISORY SYSTEM")
    xml_string = xml_string.replace("TANIMOWO, EMMANUEL OLUWADARASIMI", "IFET GREAT TITUS")
    xml_string = xml_string.replace("Tanimowo Emmanuel Oluwadarasimi", "Ifet Great Titus")
    xml_string = xml_string.replace("2101110048", "2201110075")
    return xml_string

def final_merge():
    senior_xml_path = r'c:\Users\Adegoke\Desktop\New folder\docs\ADIPHAS\unpacked_senior\word\document.xml'
    adiphas_xml_path = r'c:\Users\Adegoke\Desktop\New folder\docs\ADIPHAS\unpacked_v6_final_attempt\word\document.xml'
    
    # 1. READ SENIOR PRELIMS
    with open(senior_xml_path, 'r', encoding='utf-8') as f:
        senior_content = f.read()
    
    # Update names in the XML string
    senior_content = update_xml_content(senior_content)
    senior_tree = etree.fromstring(senior_content.encode('utf-8'))
    senior_body = senior_tree.find(f"{{{W_NS}}}body")
    senior_paragraphs = senior_body.xpath(".//w:p", namespaces=NSMAP)
    
    # Find start of Chapter 1 in senior doc to get prelims
    prelims = []
    for p in senior_paragraphs:
        text = "".join(p.xpath(".//w:t/text()", namespaces=NSMAP))
        if "CHAPTER ONE" in text.upper():
            break
        prelims.append(p)

    # 2. READ ADIPHAS CONTENT
    with open(adiphas_xml_path, 'r', encoding='utf-8') as f:
        adiphas_content = f.read()
    adiphas_tree = etree.fromstring(adiphas_content.encode('utf-8'))
    adiphas_body = adiphas_tree.find(f"{{{W_NS}}}body")
    adiphas_paragraphs = adiphas_body.xpath(".//w:p", namespaces=NSMAP)
    
    # Find start of Chapter 1 in ADIPHAS
    content_start_idx = 0
    for i, p in enumerate(adiphas_paragraphs):
        text = "".join(p.xpath(".//w:t/text()", namespaces=NSMAP))
        if "CHAPTER ONE" in text.upper():
            content_start_idx = i
            break
    
    # 3. MERGE
    # Remove old prelims from ADIPHAS
    for i in range(content_start_idx):
        adiphas_body.remove(adiphas_paragraphs[i])
        
    # Insert senior prelims at the beginning
    sectPr = adiphas_body.find(f"{{{W_NS}}}sectPr")
    for p in reversed(prelims):
        adiphas_body.insert(0, p)

    # 4. UNIVERSAL FORMATTING POLISH
    for p in adiphas_body.xpath(".//w:p", namespaces=NSMAP):
        pPr = p.find(f"{{{W_NS}}}pPr")
        if pPr is None:
            pPr = etree.Element(f"{{{W_NS}}}pPr")
            p.insert(0, pPr)
        
        # 1.5 Spacing
        spacing = pPr.find(f"{{{W_NS}}}spacing")
        if spacing is None: spacing = etree.SubElement(pPr, f"{{{W_NS}}}spacing")
        spacing.set(f"{{{W_NS}}}line", "360")
        spacing.set(f"{{{W_NS}}}lineRule", "auto")
        
        # Justification for body
        jc = pPr.find(f"{{{W_NS}}}jc")
        text = "".join(p.xpath(".//w:t/text()", namespaces=NSMAP)).upper()
        if not any(x in text for x in ["CHAPTER", "DEDICATION", "ACKNOWLEDGEMENT", "ABSTRACT", "CERTIFICATION"]):
            if jc is None: jc = etree.SubElement(pPr, f"{{{W_NS}}}jc")
            jc.set(f"{{{W_NS}}}val", "both")

    # 5. SAVE
    with open(adiphas_xml_path, 'wb') as f:
        f.write(etree.tostring(adiphas_tree, encoding='UTF-8', xml_declaration=True))
    
    print("Success: Final Standardization Complete.")

final_merge()
