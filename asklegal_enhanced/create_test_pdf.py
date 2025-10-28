from fpdf import FPDF

# Create instance of FPDF class
pdf = FPDF()

# Add a page
pdf.add_page()

# Set font
pdf.set_font("Arial", size=12)

# Add a title
pdf.set_font("Arial", 'B', 16)
pdf.cell(200, 10, txt="Test Legal Document", ln=True, align='C')

# Add some content
pdf.set_font("Arial", size=12)
content = [
    "",
    "This is a test legal document for the AskLegal Enhanced system.",
    "",
    "CONTRACT AGREEMENT",
    "",
    "This Agreement is made on this 1st day of January, 2024 between:",
    "",
    "Party A: ABC Corporation",
    "Address: 123 Business Street, New York, NY 10001",
    "",
    "Party B: XYZ Services",
    "Address: 456 Service Avenue, Los Angeles, CA 90001",
    "",
    "1. SCOPE OF WORK",
    "Party B agrees to provide consulting services to Party A for a period of 12 months.",
    "",
    "2. PAYMENT TERMS",
    "Party A shall pay Party B a monthly fee of $5,000 for the services rendered.",
    "",
    "3. TERMINATION",
    "Either party may terminate this agreement with 30 days written notice.",
    "",
    "4. GOVERNING LAW",
    "This agreement shall be governed by the laws of the State of New York.",
    "",
    "IN WITNESS WHEREOF, the parties have executed this Agreement as of the date first above written.",
    "",
    "Party A: _________________________    Party B: _________________________",
    "         (Signature)                           (Signature)",
    "",
    "Date: _________________           Date: _________________"
]

for line in content:
    pdf.cell(200, 10, txt=line, ln=True)

# Save the PDF
pdf.output("test_document.pdf")
print("Test PDF created successfully!")