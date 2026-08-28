# Owner: mousamdas156@gmail.com
# ================================================================================
# FILE: apps/invoiceGenerator/app.py — GST Invoice Generator (Streamlit UI)
# ================================================================================
# Why this file is used:
#   - This is the Streamlit frontend for the invoice generator.
#   - Collects customer, products, and discounts to create PDF billing forms.
# ================================================================================
import streamlit as st          # Streamlit UI banane ke liye
import pandas as pd             # CSV file read aur data handle karne ke liye
import base64                   # PDF preview ke liye Base64 encoding
import os                       # File exist karti hai ya nahi check karne ke liye
import tempfile                 # Temporary PDF file create karne ke liye
from generateInvoice import generateInvoice   # PDF invoice generate karne wala custom function

# ───────────────────────────────────────────────────────────────
# Load customer and product data from CSV files
# ───────────────────────────────────────────────────────────────
customers = pd.read_csv("customers.csv")   # Customer details load
products  = pd.read_csv("products.csv")    # Product details load

# ───────────────────────────────────────────────────────────────
# Configure Streamlit Page
# ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="GST Invoice Generator",   # Browser tab title
    page_icon="🧾",                       # Browser tab icon
    layout="wide"                        # Full width layout
)

st.title("🧾 GST Tax Invoice Generator")
st.caption("Karobarone Pvt. Ltd. — Professional Invoice System")

# ───────────────────────────────────────────────────────────────
# Sidebar Section
# Sidebar me user invoice ki sari details fill karega
# ───────────────────────────────────────────────────────────────
with st.sidebar:

    st.header("📋 Invoice Details")

    # ---------------- Customer Selection ----------------
    st.subheader("Customer")

    # Customer dropdown
    selected_customer = st.selectbox(
        "Select Customer",
        customers["customer_name"].tolist()
    )

    # Selected customer ka complete row fetch karna
    customer_row = customers[
        customers["customer_name"] == selected_customer
    ].iloc[0]

    # ---------------- Invoice Information ----------------
    st.subheader("Invoice Info")

    # Invoice Number
    inv_number = st.text_input(
        "Invoice Number",
        value="Inv-1"
    )

    # Invoice Date
    inv_date = st.text_input(
        "Invoice Date",
        value="24-06-26"
    )

    # Payment Mode
    pay_mode = st.selectbox(
        "Payment Mode",
        ["UPI", "Cash", "NEFT", "RTGS", "Cheque"]
    )

    # Reverse Charge GST
    rev_charge = st.selectbox(
        "Reverse Charge",
        ["NO", "YES"]
    )

    # ---------------- Optional Details ----------------
    st.subheader("Optional Fields")

    buyer_order = st.text_input("Buyer's Order No.")
    supplier_ref = st.text_input("Supplier's Ref.")
    vehicle_no = st.text_input("Vehicle Number")

    # ---------------- Product Selection ----------------
    st.subheader("Products")

    # Multiple products select kar sakte hain
    selected_products = st.multiselect(
        "Select Products",
        products["product_name"].tolist()
    )

    # Dictionaries to store product information
    quantities = {}   # Product quantity
    gst_rates = {}    # GST percentage
    units_map = {}    # Product unit

    # Har selected product ke liye inputs
    for pname in selected_products:

        # Quantity aur GST ko side-by-side dikhana
        col1, col2 = st.columns(2)

        with col1:
            qty = st.number_input(
                f"Qty – {pname}",
                min_value=1,
                max_value=1000,
                value=1
            )

        with col2:
            gst = st.selectbox(
                f"GST% – {pname}",
                [5,12,18,28],
                index=1
            )

        # Product Unit
        unit = st.text_input(
            f"Unit – {pname}",
            value="Nos",
            key=f"unit_{pname}"
        )

        # Store user inputs
        quantities[pname] = qty
        gst_rates[pname] = gst
        units_map[pname] = unit

    # Generate Button
    generate_btn = st.button(
        "🚀 Generate Invoice",
        type="primary",
        use_container_width=True
    )

# ───────────────────────────────────────────────────────────────
# Main Screen
# Customer aur selected products display karna
# ───────────────────────────────────────────────────────────────

col1, col2 = st.columns(2)

# Customer Information
with col1:

    st.subheader("👤 Customer Info")

    st.write(f"**Name:** {customer_row['customer_name']}")
    st.write(f"**Address:** {customer_row['address']}")
    st.write(f"**Mobile:** {customer_row['mobile']}")
    st.write(f"**Email:** {customer_row['email']}")

# Product Information
with col2:

    st.subheader("📦 Selected Products")

    if selected_products:

        for p in selected_products:

            row = products[
                products["product_name"] == p
            ].iloc[0]

            st.write(
                f"**{p}** — ₹{row['price']} × "
                f"{quantities[p]} {units_map[p]} "
                f"@ {gst_rates[p]}% GST"
            )

    else:
        st.info("No products selected yet.")

# ───────────────────────────────────────────────────────────────
# Invoice Generation
# Generate button click hone par execute hoga
# ───────────────────────────────────────────────────────────────

if generate_btn:

    # Agar product select nahi hua
    if not selected_products:
        st.error("⚠️ Please select at least one product.")

    else:

        # Invoice items list banana
        items = []

        for i, pname in enumerate(selected_products, start=1):

            row = products[
                products["product_name"] == pname
            ].iloc[0]

            items.append({

                # Serial Number
                "sr": i,

                # Product Name
                "description": pname,

                # HSN Code
                "hsn": row.get("hsn","0000"),

                # Quantity
                "qty": quantities[pname],

                # Unit
                "unit": units_map[pname],

                # Price
                "rate": float(row["price"]),

                # GST Percentage
                "gst_pct": gst_rates[pname],
            })

        # Complete invoice data dictionary
        invoice_data = {

            # Company Details
            "company": {

                "gstin": "27AADCK1234A1Z5",

                "name": "KAROBARONE PVT. LTD.",

                "address1": "Sector-5, Salt Lake, Kolkata - 700091",

                "address2": "West Bengal, India",

                "contact": "+91-1234567890",
            },

            # Billing Details
            "bill_to": {

                "name": customer_row["customer_name"],

                "address": customer_row["address"],

                "state": customer_row.get(
                    "state",
                    "West Bengal - 19"
                ),

                "gstin": customer_row.get(
                    "gstin",
                    ""
                ),
            },

            # Shipping Details
            "ship_to": {

                "name": customer_row["customer_name"],

                "address": customer_row["address"],

                "state": customer_row.get(
                    "state",
                    "West Bengal - 19"
                ),

                "gstin": customer_row.get(
                    "gstin",
                    ""
                ),
            },

            # Invoice Meta Data
            "invoice": {

                "number": inv_number,

                "date": inv_date,

                "payment_mode": pay_mode,

                "reverse_charge": rev_charge,

                "buyer_order": buyer_order,

                "supplier_ref": supplier_ref,

                "vehicle": vehicle_no,

                "delivery_date": "",

                "transport": "",

                "terms_of_delivery": "",
            },

            # Product List
            "items": items,

            # Bank Details
            "bank": {

                "name": "STATE BANK OF INDIA",

                "branch": "Salt Lake, Kolkata",

                "account": "XXXXXXXXXX",

                "ifsc": "SBIN0XXXXXX",

                "upi": "karobarone@sbi",
            },

            # Footer Declaration
            "declaration": [

                "1. Subject to Kolkata jurisdiction",

                "2. Terms & conditions are subject to our trade policy",

                "3. Our risk & responsibility ceases after delivery of goods."
            ],

            # Company Logo
            "logo_path": (
                "company_logo.png"
                if os.path.exists("company_logo.png")
                else None
            ),
        }

        # Temporary PDF create karna
        with tempfile.NamedTemporaryFile(
            suffix=".pdf",
            delete=False
        ) as tmp:

            tmp_path = tmp.name

        try:

            # PDF Generate
            generateInvoice(invoice_data, tmp_path)

            # PDF Read
            with open(tmp_path, "rb") as f:
                pdf_bytes = f.read()

            st.success("✅ Invoice generated successfully!")

            # Download Button
            st.download_button(

                label="⬇️ Download Invoice PDF",

                data=pdf_bytes,

                file_name=f"invoice_{inv_number}.pdf",

                mime="application/pdf",

                use_container_width=True,
            )

            # PDF Preview
            st.subheader("📄 Invoice Preview")

            b64 = base64.b64encode(pdf_bytes).decode("utf-8")

            pdf_display = f'''
            <iframe
            src="data:application/pdf;base64,{b64}"
            width="100%"
            height="900px"
            type="application/pdf">
            </iframe>
            '''

            st.markdown(
                pdf_display,
                unsafe_allow_html=True
            )

        except Exception as e:

            # Error Handling
            st.error(
                f"❌ Error generating invoice: {e}"
            )

        finally:

            # Temporary PDF delete karna
            if os.path.exists(tmp_path):
                os.remove(tmp_path)