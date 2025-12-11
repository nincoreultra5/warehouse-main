"""
==============================================
T-SHIRT INVENTORY - WAREHOUSE APP
==============================================
Parallel Sizes on Mobile | HTML/CSS for Phone
==============================================
"""

import streamlit as st
from supabase import create_client
import pandas as pd
from datetime import datetime
import time

# =============================================
# PAGE CONFIG
# =============================================
st.set_page_config(
    page_title="Warehouse",
    page_icon="📦",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =============================================
# CUSTOM CSS - MOBILE PARALLEL LAYOUT
# =============================================
st.markdown("""
<style>
    /* Main Background - Pure White */
    .stApp {
        background-color: #ffffff;
        color: #1f2937;
    }
    
    /* Headers - Red */
    h1, h2, h3, h4, h5, h6 {
        color: #dc2626 !important;
        font-weight: 700;
    }
    
    /* Text - Dark Grey */
    p, div, span, label {
        color: #374151 !important;
    }
    
    /* Buttons - Red */
    .stButton>button {
        background: #dc2626;
        color: #ffffff !important;
        border: 2px solid #dc2626;
        border-radius: 8px;
        padding: 0.6rem 1.2rem;
        font-weight: 600;
    }
    
    /* Input Fields */
    .stTextInput>div>div>input,
    .stSelectbox>div>div>select,
    .stNumberInput>div>div>input,
    .stTextArea>div>div>textarea {
        background-color: #f9fafb !important;
        color: #1f2937 !important;
        border: 2px solid #e5e7eb !important;
        border-radius: 6px;
    }
    
    /* Sidebar - Light Grey */
    [data-testid="stSidebar"] {
        background-color: #f3f4f6 !important;
        border-right: 2px solid #e5e7eb;
    }
    
    /* Metrics */
    [data-testid="stMetricValue"] {
        color: #dc2626 !important;
        font-size: 1.5rem !important;
        font-weight: 700;
    }
    
    /* Loading spinner */
    .stSpinner > div {
        color: #dc2626 !important;
    }
    
    /* Mobile parallel layout */
    .size-row {
        display: flex;
        flex-wrap: wrap;
        gap: 10px;
        margin-bottom: 1rem;
    }
    
    .size-item {
        flex: 1 1 20%;
        min-width: 100px;
        padding: 10px;
        border: 2px solid #e5e7eb;
        border-radius: 8px;
        background-color: #f9fafb;
    }
    
    @media (max-width: 768px) {
        .size-row {
            flex-direction: row;
            justify-content: space-between;
        }
        
        .size-item {
            flex: 1 1 20%;
            min-width: 80px;
        }
    }
</style>
""", unsafe_allow_html=True)

# =============================================
# ✅ YOUR CREDENTIALS
# =============================================
SUPABASE_URL = "https://ylrfinilcktpmaslaytn.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InlscmZpbmlsY2t0cG1hc2xheXRuIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NjU0Mzg5NTAsImV4cCI6MjA4MTAxNDk1MH0.GrVMQVfED2xiyZk25XhZSBY5pHwilH7NixedsvlhEME"

# =============================================
# SUPABASE CONNECTION
# =============================================
@st.cache_resource
def init_supabase():
    try:
        return create_client(SUPABASE_URL, SUPABASE_KEY)
    except Exception as e:
        st.error(f"❌ Failed to connect to database: {str(e)}")
        st.stop()

supabase = init_supabase()

# =============================================
# SIZE DEFINITIONS
# =============================================
KIDS_SIZES = ['26', '28', '30', '32']
ADULT_SIZES = ['34', '36', '38', '40', '42', '44', '46']

# =============================================
# AUTHENTICATION FUNCTIONS
# =============================================
def verify_login(username, password):
    try:
        user = supabase.table("users").select("*").eq("username", username).eq("password", password).eq("organization", "Warehouse").execute()
        return user.data[0] if user.data else None
    except Exception as e:
        st.error(f"Login error: {str(e)}")
        return None

# =============================================
# GET CURRENT STOCK
# =============================================
def get_stock(size):
    try:
        result = supabase.table("stock").select("quantity").eq("organization", "Warehouse").eq("size", size).execute()
        return result.data[0]['quantity'] if result.data else 0
    except:
        return 0

# =============================================
# UPDATE STOCK
# =============================================
def update_stock(size, category, quantity, operation):
    try:
        current = get_stock(size)
        new_quantity = current + quantity if operation == "IN" else max(0, current - quantity)
        
        # Check if record exists
        check = supabase.table("stock").select("id").eq("organization", "Warehouse").eq("size", size).execute()
        
        if check.data:
            supabase.table("stock").update({"quantity": new_quantity}).eq("organization", "Warehouse").eq("size", size).execute()
        else:
            supabase.table("stock").insert({
                "organization": "Warehouse",
                "size": size,
                "category": category,
                "quantity": new_quantity
            }).execute()
        
        return True
    except Exception as e:
        st.error(f"Error updating stock: {str(e)}")
        return False

# =============================================
# RECORD TRANSACTION
# =============================================
def record_transaction(size, quantity, operation, reason, user_name):
    try:
        supabase.table("transactions").insert({
            "organization": "Warehouse",
            "size": size,
            "quantity": quantity,
            "type": operation,
            "reason": reason,
            "user_name": user_name,
            "created_at": datetime.now().isoformat()
        }).execute()
        return True
    except Exception as e:
        st.error(f"Error recording transaction: {str(e)}")
        return False

# =============================================
# LOGIN PAGE
# =============================================
def login_page():
    st.markdown("<h1 style='text-align:center;color:#dc2626;'>📦 Warehouse</h1>", unsafe_allow_html=True)
    st.markdown("---")
    
    username = st.text_input("Username", placeholder="warehouse1", key="username_input")
    password = st.text_input("Password", type="password", placeholder="Enter password", key="password_input")
    
    if st.button("Login"):
        if username and password:
            user = verify_login(username, password)
            if user:
                st.session_state.logged_in = True
                st.session_state.user = user
                st.session_state.login_time = datetime.now()
                st.success(f"Welcome {user['name']}!")
                st.rerun()
            else:
                st.error("Invalid credentials!")
        else:
            st.warning("Please enter both username and password")

# =============================================
# STOCK IN PAGE
# =============================================
def stock_in_page():
    st.markdown("<h2 style='color:#dc2626;'>Stock IN</h2>", unsafe_allow_html=True)
    st.markdown("---")
    
    # Stock summary
    kids_total = sum([get_stock(size) for size in KIDS_SIZES])
    adults_total = sum([get_stock(size) for size in ADULT_SIZES])
    grand_total = kids_total + adults_total
    
    col1, col2, col3 = st.columns(3)
    col1.metric("Kids", f"{kids_total:,}")
    col2.metric("Adults", f"{adults_total:,}")
    col3.metric("Total", f"{grand_total:,}")
    
    st.markdown("---")
    
    # Reason input
    reason = st.text_area("Reason (required)", placeholder="e.g., New shipment", key="reason_in")
    
    st.markdown("---")
    
    # Kids section - Parallel on mobile
    st.markdown("<h3 style='color:#dc2626;'>Kids</h3>", unsafe_allow_html=True)
    st.markdown('<div class="size-row">', unsafe_allow_html=True)
    kids_quantities = {}
    for size in KIDS_SIZES:
        current_stock = get_stock(size)
        st.markdown(f'<div class="size-item"><p style="color:#6b7280;">Current: {current_stock}</p><p>Size {size}</p><input type="number" min="0" value="0" id="kids_in_{size}" style="width:100%;"></div>', unsafe_allow_html=True)
        kids_quantities[size] = st.number_input("", min_value=0, value=0, step=1, key=f"kids_in_{size}", label_visibility="collapsed")
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Adults section - Parallel on mobile
    st.markdown("<h3 style='color:#dc2626;'>Adults</h3>", unsafe_allow_html=True)
    st.markdown('<div class="size-row">', unsafe_allow_html=True)
    adults_quantities = {}
    for size in ADULT_SIZES:
        current_stock = get_stock(size)
        st.markdown(f'<div class="size-item"><p style="color:#6b7280;">Current: {current_stock}</p><p>Size {size}</p><input type="number" min="0" value="0" id="adult_in_{size}" style="width:100%;"></div>', unsafe_allow_html=True)
        adults_quantities[size] = st.number_input("", min_value=0, value=0, step=1, key=f"adult_in_{size}", label_visibility="collapsed")
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Submit button with loading
    if st.button("Submit Stock IN"):
        if not reason.strip():
            st.error("Please enter a reason!")
            return
        
        all_items = []
        for size in KIDS_SIZES:
            if kids_quantities[size] > 0:
                all_items.append(("Kids", size, kids_quantities[size]))
        
        for size in ADULT_SIZES:
            if adults_quantities[size] > 0:
                all_items.append(("Adults", size, adults_quantities[size]))
        
        if not all_items:
            st.warning("No quantities entered!")
            return
        
        # Show loading spinner
        with st.spinner("Processing stock IN..."):
            time.sleep(2)  # Simulate processing
            success_count = 0
            for category, size, qty in all_items:
                if update_stock(size, category, qty, "IN"):
                    if record_transaction(size, qty, "IN", reason, st.session_state.user['name']):
                        success_count += 1
            
            if success_count == len(all_items):
                st.success("Stock IN completed!")
                st.balloons()
                st.rerun()
            else:
                st.warning(f"Partial completion: {success_count}/{len(all_items)} items processed")

# =============================================
# STOCK OUT PAGE
# =============================================
def stock_out_page():
    st.markdown("<h2 style='color:#dc2626;'>Stock OUT</h2>", unsafe_allow_html=True)
    st.markdown("---")
    
    # Stock summary
    kids_total = sum([get_stock(size) for size in KIDS_SIZES])
    adults_total = sum([get_stock(size) for size in ADULT_SIZES])
    grand_total = kids_total + adults_total
    
    col1, col2, col3 = st.columns(3)
    col1.metric("Kids", f"{kids_total:,}")
    col2.metric("Adults", f"{adults_total:,}")
    col3.metric("Total", f"{grand_total:,}")
    
    st.markdown("---")
    
    # Reason input
    reason = st.text_area("Reason (required)", placeholder="e.g., Sent to Org A", key="reason_out")
    
    st.markdown("---")
    
    # Kids section - Parallel on mobile
    st.markdown("<h3 style='color:#dc2626;'>Kids</h3>", unsafe_allow_html=True)
    st.markdown('<div class="size-row">', unsafe_allow_html=True)
    kids_quantities = {}
    for size in KIDS_SIZES:
        current_stock = get_stock(size)
        st.markdown(f'<div class="size-item"><p style="color:#6b7280;">Available: {current_stock}</p><p>Size {size}</p><input type="number" min="0" max="{current_stock}" value="0" id="kids_out_{size}" style="width:100%;"></div>', unsafe_allow_html=True)
        kids_quantities[size] = st.number_input("", min_value=0, max_value=current_stock, value=0, step=1, key=f"kids_out_{size}", label_visibility="collapsed")
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Adults section - Parallel on mobile
    st.markdown("<h3 style='color:#dc2626;'>Adults</h3>", unsafe_allow_html=True)
    st.markdown('<div class="size-row">', unsafe_allow_html=True)
    adults_quantities = {}
    for size in ADULT_SIZES:
        current_stock = get_stock(size)
        st.markdown(f'<div class="size-item"><p style="color:#6b7280;">Available: {current_stock}</p><p>Size {size}</p><input type="number" min="0" max="{current_stock}" value="0" id="adult_out_{size}" style="width:100%;"></div>', unsafe_allow_html=True)
        adults_quantities[size] = st.number_input("", min_value=0, max_value=current_stock, value=0, step=1, key=f"adult_out_{size}", label_visibility="collapsed")
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Submit button with loading
    if st.button("Submit Stock OUT"):
        if not reason.strip():
            st.error("Please enter a reason!")
            return
        
        all_items = []
        for size in KIDS_SIZES:
            if kids_quantities[size] > 0:
                all_items.append(("Kids", size, kids_quantities[size]))
        
        for size in ADULT_SIZES:
            if adults_quantities[size] > 0:
                all_items.append(("Adults", size, adults_quantities[size]))
        
        if not all_items:
            st.warning("No quantities entered!")
            return
        
        # Show loading spinner
        with st.spinner("Processing stock OUT..."):
            time.sleep(2)  # Simulate processing
            success_count = 0
            for category, size, qty in all_items:
                if update_stock(size, category, qty, "OUT"):
                    if record_transaction(size, qty, "OUT", reason, st.session_state.user['name']):
                        success_count += 1
            
            if success_count == len(all_items):
                st.success("Stock OUT completed!")
                st.balloons()
                st.rerun()
            else:
                st.warning(f"Partial completion: {success_count}/{len(all_items)} items processed")

# =============================================
# MAIN APP
# =============================================
def main():
    if 'logged_in' not in st.session_state:
        st.session_state.logged_in = False
    
    if not st.session_state.logged_in:
        login_page()
        return
    
    with st.sidebar:
        st.markdown("<h2 style='color:#dc2626;'>Warehouse</h2>", unsafe_allow_html=True)
        st.markdown(f"👤 {st.session_state.user['name']}")
        st.markdown("---")
        
        operation = st.radio("Operation", ["Stock IN", "Stock OUT"], label_visibility="collapsed")
        
        st.markdown("---")
        
        if st.button("Logout"):
            st.session_state.logged_in = False
            st.session_state.user = None
            st.rerun()
    
    if operation == "Stock IN":
        stock_in_page()
    else:
        stock_out_page()

if __name__ == "__main__":
    main()
