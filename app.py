import streamlit as st
import qrcode
import pandas as pd
from io import BytesIO
from datetime import datetime

# --- Ρυθμίσεις Σελίδας ---
st.set_page_config(page_title="Team UTM Tool", page_icon="📊")

# --- Password Logic (Κρατάμε το ίδιο) ---
def check_password():
    password_actual = "team2026" 
    if "password_correct" not in st.session_state:
        st.session_state["password_correct"] = False
    if st.session_state["password_correct"]:
        return True
    st.title("🔒 Login Required")
    pwd_input = st.text_input("Enter Password:", type="password")
    if st.button("Login"):
        if pwd_input == password_actual:
            st.session_state["password_correct"] = True
            st.rerun()
        else:
            st.error("❌ Λάθος κωδικός")
    return False

if not check_password():
    st.stop()

# --- Initialize History in Session State ---
# Εδώ δημιουργούμε τον "πίνακα" στη μνήμη αν δεν υπάρχει ήδη
if 'history' not in st.session_state:
    st.session_state.history = pd.DataFrame(columns=['Date', 'Campaign Name', 'Source', 'Medium', 'Short URL'])

# --- Main App ---
st.title("🚀 UTM Builder & Tracker")

col1, col2 = st.columns(2)
with col1:
    base_url = st.text_input("Base URL", "https://myshop.gr")
    source = st.text_input("Source", "newsletter")
with col2:
    medium = st.text_input("Medium", "email")
    name = st.text_input("Campaign Name", "summer_sale")

# Logic
final_url = f"{base_url}?utm_source={source}&utm_medium={medium}&utm_campaign={name}"

if st.button("Generate Link & QR"):
    # 1. Δείξε το Link
    st.success("✅ Link Generated!")
    st.code(final_url)

    # 2. Φτιάξε QR Code
    qr = qrcode.QRCode(box_size=10, border=4)
    qr.add_data(final_url)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    
    buf = BytesIO()
    img.save(buf)
    byte_im = buf.getvalue()
    
    col_img, col_dl = st.columns([1,2])
    with col_img:
        st.image(byte_im, width=150)
    with col_dl:
        st.download_button("Download QR Image", data=byte_im, file_name="qr_code.png", mime="image/png")

    # 3. ΑΠΟΘΗΚΕΥΣΗ ΣΤΟ ΙΣΤΟΡΙΚΟ
    new_row = {
        'Date': datetime.now().strftime("%Y-%m-%d %H:%M"),
        'Campaign Name': name,
        'Source': source,
        'Medium': medium,
        'Short URL': final_url
    }
    # Προσθήκη της νέας εγγραφής στο dataframe
    st.session_state.history = pd.concat([pd.DataFrame([new_row]), st.session_state.history], ignore_index=True)

# --- Εμφάνιση Ιστορικού ---
st.divider()
st.subheader("📜 Session History (Recent Links)")

if not st.session_state.history.empty:
    st.dataframe(st.session_state.history, use_container_width=True)
    
    # Κουμπί για Download Excel/CSV
    csv = st.session_state.history.to_csv(index=False).encode('utf-8')
    st.download_button(
        "📥 Download History as CSV",
        data=csv,
        file_name='campaign_history.csv',
        mime='text/csv',
    )
else:
    st.info("Δεν έχεις δημιουργήσει links ακόμα σε αυτή τη συνεδρία.")