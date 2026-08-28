# Owner: mousamdas156@gmail.com
# ================================================================================
# FILE: apps/invoiceGenerator/generateInvoice.py — PDF Invoice Generator (ReportLab)
# ================================================================================
# Why this file is used:
#   - Implements custom canvas draws to generate PDF invoice layouts.
#
# What components are inside:
#   - drect(), dtext(), drawField(), hline() -> Canvas drawing helper algorithms.
#   - generateInvoice() -> Draws company headers, product grids, and GST summaries.
# ================================================================================
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import mm
from reportlab.pdfgen import canvas
from reportlab.platypus import Table, TableStyle
import math

# ─── COLOR PALETTE ────────────────────────────────────────────────────────────
# Yeh saare colors pure invoice mein use ho rahe hain — header, table, borders sab yahin se aate hain
HEADER_BLUE  = colors.HexColor("#B8D4E8")   # "Bill To" / "Ship To" ke header strip aur summary header mein use
DARK_BLUE    = colors.HexColor("#2E4057")   # Company name aur footer text ke liye accent color
TABLE_HEADER = colors.HexColor("#A0BED4")   # Product table ka header row background
LIGHT_GRAY   = colors.HexColor("#F5F5F5")   # Table ke alternate (zebra) rows aur QR placeholder box ka background
WHITE        = colors.white                 # Saare boxes/sections ka default fill
BLACK        = colors.black                 # Default text color
BORDER       = colors.HexColor("#888888")   # Saari rectangle borders aur grid lines ka color

W, H   = A4                 # Page ki full width/height (A4 size)
MARGIN = 12 * mm            # Page ke chaaron taraf ka margin
IW     = W - 2 * MARGIN     # Inner usable width (margin minus karke)


# ─── HELPERS ──────────────────────────────────────────────────────────────────
# Neeche diye gaye 4 helper functions pure file mein repeatedly use hote hain —
# inhi ki madad se har section (header, table, summary, etc.) draw hota hai.

def drect(c, x, y, w, h, fill=None, stroke=BORDER, lw=0.5):
    # Generic rectangle draw karne wala function. y = top-left corner (top se measure hota hai).
    # Har section ka "box/background" yahi function banata hai — e.g. header box, bill-to box, table box, summary box.
    bottom = y - h
    c.saveState()
    c.setLineWidth(lw)
    if fill:
        c.setFillColor(fill)
        c.setStrokeColor(stroke)
        c.rect(x, bottom, w, h, fill=1, stroke=1)
    else:
        c.setStrokeColor(stroke)
        c.rect(x, bottom, w, h, fill=0, stroke=1)
    c.restoreState()


def dtext(c, x, y, txt, size=8, bold=False, color=BLACK, align="left"):
    # Generic text draw karne wala function — saari labels, values, headings yahi se print hoti hain.
    c.saveState()
    c.setFillColor(color)
    c.setFont("Helvetica-Bold" if bold else "Helvetica", size)
    if align == "center":
        c.drawCentredString(x, y, str(txt))
    elif align == "right":
        c.drawRightString(x, y, str(txt))
    else:
        c.drawString(x, y, str(txt))
    c.restoreState()


def hline(c, x1, y, x2, lw=0.4):
    # Horizontal divider line — sirf "Summary" section ke rows ke beech separator banane ke liye use hota hai.
    c.saveState(); c.setStrokeColor(BORDER); c.setLineWidth(lw)
    c.line(x1, y, x2, y); c.restoreState()


def num_to_words(n):
    # Total amount ko words mein convert karta hai (e.g. 1500 -> "One Thousand Five Hundred Only")
    # Yeh sirf Section 6 "TOTAL IN WORDS" mein use hota hai.
    ones = ['','One','Two','Three','Four','Five','Six','Seven','Eight','Nine',
            'Ten','Eleven','Twelve','Thirteen','Fourteen','Fifteen','Sixteen',
            'Seventeen','Eighteen','Nineteen']
    tens = ['','','Twenty','Thirty','Forty','Fifty','Sixty','Seventy','Eighty','Ninety']

    def b100(x):
        return ones[x] if x < 20 else tens[x//10]+(' '+ones[x%10] if x%10 else '')
    def b1000(x):
        return (ones[x//100]+' Hundred'+(' '+b100(x%100) if x%100 else '')) if x>=100 else b100(x)

    n = int(round(n))
    if n == 0: return 'Zero'
    parts = []
    for div, label in [(10000000,'Crore'),(100000,'Lakh'),(1000,'Thousand')]:
        if n >= div:
            parts.append(b1000(n//div)+' '+label); n %= div
    if n: parts.append(b1000(n))
    return ' '.join(parts) + ' Only'


# ══════════════════════════════════════════════════════════════════════════════
def generateInvoice(data: dict, filename: str = "invoice.pdf"):
    # Yeh main function hai jo pura invoice PDF banata hai.
    # "cur" variable ek running Y-coordinate hai jo top se neeche ki taraf chalta hai —
    # har section draw hone ke baad cur ko us section ki height se ghata diya jaata hai (cur -= height),
    # taaki next section uske theek neeche aa jaaye.
    c   = canvas.Canvas(filename, pagesize=A4)
    x0  = MARGIN
    cur = H - MARGIN

    # data dictionary se alag-alag parts nikal rahe hain — yeh saare keys caller ko pass karne padte hain
    co  = data["company"]    # Company info (GSTIN, name, address, contact) -> Section 2 mein use
    bil = data["bill_to"]    # Bill To customer info -> Section 3a mein use
    shi = data["ship_to"]    # Ship To customer info -> Section 3b mein use
    inv = data["invoice"]    # Invoice meta details (number, date, payment mode etc.) -> Section 3c mein use
    bnk = data["bank"]       # Bank account details -> Section 5 (left box) mein use

    # ══ 1. TOP STRIP ══════════════════════════════════════════════════════════
    # Sabse upar "Tax Invoice" title wali patti
    sh = 14
    drect(c, x0, cur, IW, sh, fill=WHITE, lw=0.8)
    # Vertically centered: strip center = cur - sh/2
    strip_mid = cur - sh / 2
    dtext(c, x0 + IW/2,    strip_mid - 4,  "Tax Invoice",              size=11, bold=True, align="center")

    cur -= sh

    # ══ 2. COMPANY HEADER ═════════════════════════════════════════════════════
    # Logo + company ka naam, GSTIN, address, contact number wala header block
    hdr_h = 40 * mm
    drect(c, x0, cur, IW, hdr_h, fill=WHITE, lw=0.8)

    # Logo — vertically centered in header
    logo_w = logo_h = 22 * mm
    logo_x = x0 + 3
    logo_y_bot = cur - hdr_h/2 - logo_h/2      # centered vertically
    logo_y_top = logo_y_bot + logo_h
    try:
        # Agar data mein logo_path diya hai to actual logo image draw hoga
        if not data.get("logo_path"): raise FileNotFoundError
        c.drawImage(data["logo_path"], logo_x, logo_y_bot,
                    width=logo_w, height=logo_h, preserveAspectRatio=True, mask='auto')
    except Exception:
        # Logo na milne par placeholder blue box with "LOGO" text dikhta hai
        drect(c, logo_x, logo_y_top, logo_w, logo_h, fill=colors.HexColor("#3B8BBE"))
        dtext(c, logo_x + logo_w/2, logo_y_bot + logo_h/2 - 4,
              "LOGO", size=9, bold=True, color=WHITE, align="center")

    # Company text — vertically centered block (GSTIN, Name, Address lines, Contact)
    tx     = logo_x + logo_w + 5
    # 5 lines total: GSTIN, Name, addr1, addr2, contact
    # total height of text block ≈ 9+13+10+10+10 = 52 pts spacing
    text_block_h = 52
    ty = cur - (hdr_h - text_block_h) / 2  # start so block is centered
    dtext(c, tx, ty,           f"GSTIN : {co['gstin']}",               size=8)
    dtext(c, tx, ty - 13,       co["name"],                             size=15, bold=True, color=DARK_BLUE)
    dtext(c, tx, ty - 27,       co.get("address1",""),                  size=8.5)
    dtext(c, tx, ty - 37,       co.get("address2",""),                  size=8.5)
    dtext(c, tx, ty - 47,      f"Contact No. : {co.get('contact','')}",size=8.5)
    cur -= hdr_h

    # ══ 3. BILL-TO / SHIP-TO  +  INVOICE DETAILS ══════════════════════════════
    # Yeh poora section 2 columns mein bata hai: LEFT (Bill To + Ship To stacked) aur RIGHT (Invoice details)
    LEFT_W  = IW * 0.55
    RIGHT_W = IW - LEFT_W
    rx      = x0 + LEFT_W

    BILL_H   = 30 * mm
    SHIP_H   = 26 * mm
    DETAIL_H = BILL_H + SHIP_H   # Right column ki total height = Bill + Ship dono ki height ke barabar
    LINE_H   = 9

    # ── 3a. Bill To ── (customer ka naam/address/state/GSTIN jisko bill jaa raha hai)
    drect(c, x0, cur, LEFT_W, BILL_H, fill=WHITE)
    drect(c, x0, cur, LEFT_W, 9, fill=HEADER_BLUE)
    dtext(c, x0 + 3, cur - 7, "Bill To", size=9, bold=True)

    # 4 data lines; total = 4 * LINE_H = 36 pts
    bill_data_h = 4 * LINE_H
    bill_content_h = BILL_H - 9   # space below header strip
    bly = cur - 9 - (bill_content_h - bill_data_h) / 2 - 2
    for label, val in [
        ("Name :",    bil["name"]),
        ("Address :", bil["address"]),
        ("State :",   bil.get("state","")),
        ("GSTIN :",   bil.get("gstin","")),
    ]:
        dtext(c, x0 + 3,          bly, label, size=8.5)
        dtext(c, x0 + 3 + 18*mm,  bly, val,   size=8.5)
        bly -= LINE_H

    # ── 3b. Ship To ── (jahan goods deliver honge uska address — Bill To ke neeche)
    sy_top = cur - BILL_H
    drect(c, x0, sy_top, LEFT_W, SHIP_H, fill=WHITE)
    drect(c, x0, sy_top, LEFT_W, 9, fill=HEADER_BLUE)
    dtext(c, x0 + 3, sy_top - 7, "Ship To", size=9, bold=True)

    ship_data_h = 4 * LINE_H
    ship_content_h = SHIP_H - 9
    sly = sy_top - 9 - (ship_content_h - ship_data_h) / 2 - 2
    for label, val in [
        ("Name :",    shi["name"]),
        ("Address :", shi["address"]),
        ("State :",   shi.get("state","")),
        ("GSTIN :",   shi.get("gstin","")),
    ]:
        dtext(c, x0 + 3,          sly, label, size=8.5)
        dtext(c, x0 + 3 + 18*mm,  sly, val,   size=8.5)
        sly -= LINE_H

    # ── 3c. Invoice details (right column) ── (Invoice number, date, payment mode, transport etc.)
    drect(c, rx, cur, RIGHT_W, DETAIL_H, fill=WHITE)

    MID = rx + RIGHT_W * 0.54
    RH  = 8.5
    inv_rows = [
        ("# Inv. No. :",        inv.get("number","")),
        ("Inv. Date :",         inv.get("date","")),
        ("Payment Mode :",      inv.get("payment_mode","")),
        ("Reverse Charge :",    inv.get("reverse_charge","")),
        ("",""),
        ("Buyer's Order No :",  inv.get("buyer_order","")),
        ("Supplier's Ref. :",   inv.get("supplier_ref","")),
        ("Vehicle Number :",    inv.get("vehicle","")),
        ("Delivery Date :",     inv.get("delivery_date","")),
        ("Transport Details :", inv.get("transport","")),
        ("Terms Of Delivery :", inv.get("terms_of_delivery","")),
    ]
    # Vertically center all rows in DETAIL_H
    total_rows_h = len(inv_rows) * RH
    iy = cur - (DETAIL_H - total_rows_h) / 2 - RH * 0.3
    for label, val in inv_rows:
        dtext(c, rx + 3,  iy, label, size=8)
        dtext(c, MID,     iy, str(val), size=8, bold=True)
        iy -= RH

    cur -= DETAIL_H

    # ══ 4. PRODUCT TABLE ══════════════════════════════════════════════════════
    # Yahan saare items (products/services) ki list table format mein print hoti hai,
    # ReportLab ke Table/TableStyle ka use karke (yeh ek alag platypus component hai, canvas wale draw se different)
    items = data["items"]

    cw = [
        7*mm, 50*mm, 13*mm, 15*mm, 16*mm, 19*mm, 10*mm, 19*mm,
    ]
    cw.append(IW - sum(cw))   # Last column ki width = bachi hui width (Total column)

    headers = ["Sr", "Goods & Service\nDiscription", "HSN", "Quantity",
               "Rate", "Taxable", "GST\n%", "GST\nAmt.", "Total"]

    rows    = [headers]
    tot_qty = tot_tax = tot_gst = grand = 0.0

    # Har item ke liye taxable amount, GST amount, line total calculate karte hain — aur grand totals mein add karte hain
    for it in items:
        qty     = it["qty"]
        rate    = it["rate"]
        gp      = it["gst_pct"]
        taxable = round(qty * rate, 2)
        gst_amt = round(taxable * gp / 100, 2)
        ltot    = round(taxable + gst_amt, 2)
        tot_qty += qty; tot_tax += taxable; tot_gst += gst_amt; grand += ltot
        rows.append([
            str(it["sr"]), it["description"], str(it["hsn"]),
            f"{qty} {it.get('unit','')}", f"{rate:.2f}",
            f"{taxable:.2f}", f"{gp}%", f"{gst_amt:.2f}", f"{ltot:.2f}",
        ])

    # Agar items kam hain to table ko minimum 11 rows tak empty rows se fill karte hain (consistent layout ke liye)
    while len(rows) < 11:
        rows.append([""] * 9)

    # Last row mein Sub-Total ke totals print hote hain
    rows.append(["", "Sub-Total:", "", str(int(tot_qty)),
                 "", f"{tot_tax:.2f}", "", f"{tot_gst:.2f}", f"{grand:.2f}"])

    tbl = Table(rows, colWidths=cw)
    tbl.setStyle(TableStyle([
        ("BACKGROUND",    (0,0),(-1,0), TABLE_HEADER),     # Header row background
        ("FONTNAME",      (0,0),(-1,0), "Helvetica-Bold"),
        ("FONTSIZE",      (0,0),(-1,0), 8),
        ("ALIGN",         (0,0),(-1,0), "CENTER"),
        ("VALIGN",        (0,0),(-1,0), "MIDDLE"),
        ("BACKGROUND",    (0,-1),(-1,-1), HEADER_BLUE),    # Sub-Total row background
        ("FONTNAME",      (0,-1),(-1,-1), "Helvetica-Bold"),
        ("FONTSIZE",      (0,-1),(-1,-1), 8.5),
        ("ROWBACKGROUNDS",(0,1),(-1,-2), [WHITE, LIGHT_GRAY]),  # Zebra striping for item rows
        ("FONTSIZE",      (0,1),(-1,-1), 8.5),
        ("GRID",          (0,0),(-1,-1), 0.4, BORDER),     # Saari cells ke around grid lines
        ("ALIGN",         (0,0),(0,-1),  "CENTER"),        # Sr No column center align
        ("ALIGN",         (2,1),(3,-1),  "CENTER"),        # HSN + Quantity columns center align
        ("ALIGN",         (4,1),(-1,-1), "RIGHT"),         # Rate/Taxable/GST/Total columns right align
        ("ALIGN",         (6,1),(6,-1),  "CENTER"),        # GST% column center align
        ("TOPPADDING",    (0,0),(-1,-1), 3),
        ("BOTTOMPADDING", (0,0),(-1,-1), 3),
        ("LEFTPADDING",   (0,0),(-1,-1), 3),
        ("RIGHTPADDING",  (0,0),(-1,-1), 3),
    ]))

    tw, th = tbl.wrapOn(c, IW, H)
    tbl.drawOn(c, x0, cur - th)
    cur -= th

    # ══ 5. BANK + SUMMARY ═════════════════════════════════════════════════════
    # Left side: Bank account details. Right side: CGST/SGST/IGST/Round off/Total Amount summary box
    # Inter-state vs Intra-state GST determination
    co_state = (co.get("state") or co.get("address2") or "").lower().strip()
    bill_state = (bil.get("state") or bil.get("address") or "").lower().strip()
    co_gst_code = (co.get("gstin") or "")[:2]
    bill_gst_code = (bil.get("gstin") or "")[:2]

    is_interstate = False
    if co_gst_code and bill_gst_code and co_gst_code != bill_gst_code:
        is_interstate = True
    elif co_state and bill_state and co_state != bill_state and not (co_state in bill_state or bill_state in co_state):
        is_interstate = True

    if is_interstate:
        igst = round(tot_gst, 2)
        cgst = 0.0
        sgst = 0.0
    else:
        cgst = round(tot_gst / 2, 2)
        sgst = round(tot_gst / 2, 2)
        igst = 0.0

    total_amt = round(grand)
    round_off = round(total_amt - grand, 2)

    BNK_W = IW * 0.50
    SUM_W = IW - BNK_W
    SUM_X = x0 + BNK_W
    BOX_H = 24 * mm

    drect(c, x0,    cur, BNK_W, BOX_H, fill=WHITE)
    drect(c, SUM_X, cur, SUM_W, BOX_H, fill=WHITE)

    # ── Bank (left) — vertically centered ──
    bank_lines = [
        ("Bank Name :", bnk.get("name","")),
        ("Branch :",    bnk.get("branch","")),
        ("Account No :",bnk.get("account","")),
        ("IFSC Code :", bnk.get("ifsc","")),
        ("UPI ID :",    bnk.get("upi","")),
    ]
    # Title (9pt) + 5 lines (8pt each ~8px) = 9 + 5*8 = 49 pts
    bank_block_h = 9 + len(bank_lines) * 8
    bx = x0 + 3
    # center the whole block (title + lines) in BOX_H
    by = cur - (BOX_H - bank_block_h) / 2
    dtext(c, bx, by, "Our Bank Details", size=9, bold=True)
    by -= 9
    LABEL_W = 24 * mm
    for lbl, val in bank_lines:
        dtext(c, bx,           by, lbl, size=8.5)
        dtext(c, bx + LABEL_W, by, val, size=8.5, bold=True)
        by -= 8

    # ── Summary (right) ── (CGST, SGST, IGST, Round off, Total Amount ki list, har row ke neeche divider line)
    SH  = 9
    sy  = cur
    summary_rows = [
        ("SUMMARY",                   "AMOUNT",           True),   # True = header/highlighted style
        ("CGST Amt :",                f"{cgst:.2f}" if cgst else "",      False),
        ("SGST Amt :",                f"{sgst:.2f}" if sgst else "",      False),
        ("IGST Amt :",                f"{igst:.2f}" if igst else "",      False),
        ("Freight Packing Charges :", "",                 False),
        ("Round off :",               f"{round_off:.2f}", False),
        ("Total Amount :",            f"{total_amt:.2f}", True),
    ]
    for lbl, val, is_hdr in summary_rows:
        row_top = sy
        if is_hdr:
            drect(c, SUM_X, row_top, SUM_W, SH, fill=HEADER_BLUE)
            dtext(c, SUM_X + SUM_W*0.28, row_top - SH + 1.5, lbl, size=8.5, bold=True)
            dtext(c, SUM_X + SUM_W - 3,  row_top - SH + 1.5, val, size=8.5, bold=True, align="right")
        else:
            dtext(c, SUM_X + 3,          row_top - SH + 1.5, lbl, size=8)
            dtext(c, SUM_X + SUM_W - 3,  row_top - SH + 1.5, val, size=8,   bold=True, align="right")
        hline(c, SUM_X, row_top - SH, SUM_X + SUM_W)   # Har row ke neeche divider line
        sy -= SH

    drect(c, x0,    cur, BNK_W, BOX_H)   # Outer border for bank box
    drect(c, SUM_X, cur, SUM_W, BOX_H)   # Outer border for summary box
    cur -= BOX_H

    # ══ 6. TOTAL IN WORDS ═════════════════════════════════════════════════════
    # "Invoice Total in Word" — total amount ko words mein likha jaata hai (num_to_words function ka use yahin hota hai)
    WH = 18 * mm
    drect(c, x0, cur, IW, WH, fill=WHITE)
    # 2 lines: title (9pt) + content (9pt) ≈ 20 pts total
    word_block_h = 20
    wy = cur - (WH - word_block_h) / 2
    dtext(c, x0 + 3, wy,      "Invoice Total in Word",          size=9, bold=True)
    dtext(c, x0 + 3, wy - 11, f"Rupees {num_to_words(total_amt)}", size=9)
    cur -= WH

    # ══ 7. DECLARATION + QR + SIGNATURE ══════════════════════════════════════
    # Left half: Declaration terms (data["declaration"] list se aate hain) + "E. & O.E." note
    # Right half: Company name, QR code placeholder, Authorised Signatory text
    DH   = 32 * mm
    drect(c, x0, cur, IW, DH, fill=WHITE)

    HALF = IW / 2

    # ── Left: Declaration — vertically centered ──
    decl_lines = data.get("declaration", [])
    # title + lines + E&OE
    decl_total_lines = 1 + len(decl_lines) + 1
    decl_block_h = 9 + len(decl_lines) * 7 + 8   # title(9) + lines(7 each) + E&OE(8)
    dy = cur - (DH - decl_block_h) / 2
    dtext(c, x0 + 3, dy, "Declaration", size=9, bold=True); dy -= 9
    for line in decl_lines:
        dtext(c, x0 + 3, dy, line, size=7.5); dy -= 7
    dtext(c, x0 + 3, dy, "E. & O.E.", size=8)

    # ── Right: Company name + QR + Signatory — vertically distributed ──
    rx3 = x0 + HALF

    # "For, Company" at top of right half
    dtext(c, x0 + IW - 3, cur - 9, f"For, {co['name']}", size=9, bold=True, align="right")

    # QR — centered horizontally in right half, vertically centered in DH (abhi placeholder gray box hai)
    qr_size  = 20 * mm
    qr_x     = rx3 + (HALF - qr_size) / 2
    qr_y_top = cur - (DH - qr_size) / 2        # vertically centered in section
    drect(c, qr_x, qr_y_top, qr_size, qr_size, fill=LIGHT_GRAY)
    dtext(c, qr_x + qr_size / 2, qr_y_top - qr_size / 2 - 4,
          "QR", size=8, bold=True, color=DARK_BLUE, align="center")

    # "Authorised Signatory" at bottom of right half
    dtext(c, x0 + IW - 3, cur - DH + 6, "Authorised Signatory", size=8.5, align="right")
    cur -= DH

    # ══ 8. FOOTER ═════════════════════════════════════════════════════════════
    # Sabse neeche thank-you message
    cur -= 8 * mm   # extra gap before footer
    dtext(c, x0 + IW/2, cur - 9,
          "Thank You For Business With US!", size=10, bold=True,
          color=DARK_BLUE, align="center")

    c.save()   # PDF file disk par save hoti hai
    print(f"Invoice saved → {filename}")
    return filename

