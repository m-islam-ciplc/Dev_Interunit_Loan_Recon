from core.database import get_unmatched_data_by_companies
from core.matching import extract_po, extract_lc

# Get January 2025 data
data = get_unmatched_data_by_companies('GeoTex', 'Steel', 'January', '2025')

# Find records with PO and LC patterns
po_records = []
lc_records = []

for record in data:
    particulars = record.get('Particulars', '')
    po = extract_po(particulars)
    lc = extract_lc(particulars)
    
    if po:
        po_records.append((record, po))
    if lc:
        lc_records.append((record, lc))

print(f"Records with PO patterns: {len(po_records)}")
print(f"Records with LC patterns: {len(lc_records)}")

print("\nPO Records:")
for record, po in po_records:
    print(f"  UID: {record['uid']}, Amount: {record.get('Debit', record.get('Credit'))}, PO: {po}")
    print(f"  Particulars: {record.get('Particulars', '')[:100]}")

print("\nLC Records:")
for record, lc in lc_records:
    print(f"  UID: {record['uid']}, Amount: {record.get('Debit', record.get('Credit'))}, LC: {lc}")
    print(f"  Particulars: {record.get('Particulars', '')[:100]}")

# Check if these records are part of amount matches
lenders = [r for r in data if r.get('Debit') and r['Debit'] > 0]
borrowers = [r for r in data if r.get('Credit') and r['Credit'] > 0]

print(f"\nChecking if PO/LC records are in amount matches:")
for lender in lenders:
    for borrower in borrowers:
        if float(lender['Debit']) == float(borrower['Credit']):
            lender_po = extract_po(lender.get('Particulars', ''))
            borrower_po = extract_po(borrower.get('Particulars', ''))
            lender_lc = extract_lc(lender.get('Particulars', ''))
            borrower_lc = extract_lc(borrower.get('Particulars', ''))
            
            if lender_po or borrower_po or lender_lc or borrower_lc:
                print(f"Amount match: {lender['Debit']} == {borrower['Credit']}")
                print(f"  Lender UID: {lender['uid']}, PO: {lender_po}, LC: {lender_lc}")
                print(f"  Borrower UID: {borrower['uid']}, PO: {borrower_po}, LC: {borrower_lc}") 