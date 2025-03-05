import json
from fpdf import FPDF
import unicodedata

def remove_unicode(text):
    return ''.join(c if ord(c) < 128 else unicodedata.normalize('NFKD', c).encode('ascii', 'ignore').decode('ascii') for c in text)

def convert_json_to_pdf(json_file, output_pdf):
    with open(json_file, 'r', encoding='utf-8') as f:
        data = json.load(f)

    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    pdf.cell(0, 10, txt="This PDF was automatically generated.", ln=True)
    pdf.ln(10)

    for course in data:
        pdf.cell(0, 10, txt=f"Course Title: {remove_unicode(course.get('Course Number and Title', ''))}", ln=True)
        pdf.cell(0, 10, txt=f"Lecturers: {remove_unicode(course.get('Lecturers', ''))}", ln=True)
        # pdf.cell(0, 10, txt=f"Weekday: {remove_unicode(course.get('Weekday', ''))}", ln=True)
        # pdf.cell(0, 10, txt=f"Time: {remove_unicode(course.get('Time', ''))}", ln=True)
        # pdf.cell(0, 10, txt=f"Where: {remove_unicode(course.get('Where', ''))}", ln=True)
        pdf.multi_cell(0, 10, txt=f"Short Description: {remove_unicode(course.get('Short Description', ''))}")
        pdf.ln(5)

    pdf.output(output_pdf)

convert_json_to_pdf("course_data.json", "course_data.pdf")
print("PDF generation completed. Output saved to course_data.pdf.")
