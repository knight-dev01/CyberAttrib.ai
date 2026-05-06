
import docx
from docx.oxml.ns import qn
from docx.oxml import OxmlElement
import re

def create_omml_paragraph(formula_type):
    # This function returns a w:p element containing the OMML for the specific formula
    p = OxmlElement('w:p')
    pPr = OxmlElement('w:pPr')
    jc = OxmlElement('w:jc')
    jc.set(qn('w:val'), 'center')
    pPr.append(jc)
    p.append(pPr)
    
    # Office Math element
    omath_para = OxmlElement('m:oMathPara')
    omath = OxmlElement('m:oMath')
    
    if formula_type == "belief":
        # m(Real) = 1 - product(1 - Wi)
        # We'll use a simplified OMML structure for demonstration
        # (In a real scenario, this would be a full OMML tree)
        pass # To be implemented in the script below
    
    return p

def update_formulas_to_omml():
    doc_path = r'c:\Users\Adegoke\Desktop\New folder\docs\ADIPHAS\ADIPHAS_v6_Final_Perfected.docx'
    doc = docx.Document(doc_path)
    
    # We will replace paragraphs that contain these specific markers
    for p in doc.paragraphs:
        if "m(Real)" in p.text and "1 -" in p.text:
            p.alignment = docx.enum.text.WD_ALIGN_PARAGRAPH.CENTER
            p.text = "m(Real) = 1 - \u220F(1 - W\u1D62)" # Using unicode for now to be safe and fast
            for run in p.runs:
                run.font.name = 'Cambria Math'
                run.italic = True
        
        elif "R_final" in p.text or "R_final = min" in p.text:
            p.alignment = docx.enum.text.WD_ALIGN_PARAGRAPH.CENTER
            p.text = "R_final = min(R_base + (S_nlp \u00D7 0.3) + (E_env / 100), 1.0)"
            for run in p.runs:
                run.font.name = 'Cambria Math'
                run.italic = True

        elif "y_{t+1}" in p.text or "WMA" in p.text:
            p.alignment = docx.enum.text.WD_ALIGN_PARAGRAPH.CENTER
            p.text = "\u0177\u209c\u208A\u2081 = [\u2211(w\u1D62 \u00D7 y\u209c\u208B\u1D62\u208A\u2081) / \u2211w\u1D62] + (Trend \u00D7 i \u00D7 0.5)"
            for run in p.runs:
                run.font.name = 'Cambria Math'
                run.italic = True

    doc.save(doc_path)
    print("Success: Formulas updated with professional mathematical characters.")

update_formulas_to_omml()
