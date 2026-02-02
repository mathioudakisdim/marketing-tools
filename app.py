import streamlit as st
import qrcode
from io import BytesIO

# --- Ρυθμίσεις Σελίδας ---
st.set_page_config(page_title="Team UTM Tool", page_icon="🔒")

# --- Λειτουργία Κωδικού ---
def check_password():
    """Returns `True` if the user had the correct password."""
    
    # Ο ΚΩΔΙΚΟΣ ΣΟΥ:
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
            st.rerun() # Κάνει refresh τη σελίδα μόλις βάλεις τον σωστό κωδικό
        else:
            st.error("❌ Λάθος κωδικός")

    return False

if not check_password():
    st.stop()  # ΣΤΑΜΑΤΑΕΙ ΕΔΩ αν δεν βάλεις κωδικό

# --- Η Κυρίως Εφαρμογή (Τρέχει μόνο μετά το Login) ---
st.title("🚀 UTM Builder & QR Generator")
st.success("Είσοδος επιτυχής! Καλώς ήρθες.")

# Layout
col1, col2 = st.columns(2)
with col1:
    base_url = st.text_input("Base URL", "https://myshop.gr")
    source = st.text_input("Source (utm_source)", "newsletter")
with col2:
    medium = st.text_input("Medium (utm_medium)", "email")
    name = st.text_input("Name (utm_campaign)", "summer_sale")

# Logic
final_url = f"{base_url}?utm_source={source}&utm_medium={medium}&utm_campaign={name}"
st.code(final_url)

# QR Code Logic
if st.button("Generate QR"):
    qr = qrcode.QRCode(box_size=10, border=4)
    qr.add_data(final_url)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    
    buf = BytesIO()
    img.save(buf)
    byte_im = buf.getvalue()
    
    st.image(byte_im, width=200)