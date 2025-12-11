"""
==============================================
T-SHIRT INVENTORY - WAREHOUSE APP
==============================================
Simple IN/OUT Management | White/Red/Grey Theme
==============================================
"""

import streamlit as st
from supabase import create_client
import pandas as pd
from datetime import datetime

# =============================================
# PAGE CONFIG
# =============================================
st.set_page_config(
    page_title="Warehouse - T-Shirt Inventory",
    page_icon="📦",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =============================================
# CUSTOM CSS - WHITE/RED/GREY THEME
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
        background: linear-gradient(135deg, #dc2626 0%, #b91c1c 100%);
        color: #ffffff !important;
        border: 2px solid #dc2626;
        border-radius: 8px;
        padding: 0.6rem 1.2rem;
        font-weight: 600;
        transition: all 0.3s;
    }
    
    .stButton>button:hover {
        background: linear-gradient(135deg, #b91c1c 0%, #991b1b 100%);
        border-color: #b91c1c;
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(220, 38, 38, 0.4);
    }
    
    /* Input Fields - Light Grey Border */
    .stTextInput>div>div>input,
    .stSelectbox>div>div>select,
    .stNumberInput>div>div>input,
    .stTextArea>div>div>textarea {
        background-color: #f9fafb !important;
        color: #1f2937 !important;
        border: 2px solid #e5e7eb !important;
        border-radius: 6px;
    }
    
    .stTextInput>div>div>input:focus,
    .stSelectbox>div>div>select:focus,
    .stNumberInput>div>div>input:focus,
    .stTextArea>div>div>textarea:focus {
        border-color: #dc2626 !important;
    }
    
    /* Number input - smaller width */
    .stNumberInput {
        max-width: 150px;
    }
    
    /* Sidebar - Light Grey */
    [data-testid="stSidebar"] {
        background-color: #f3f4f6 !important;
        border-right: 2px solid #e5e7eb;
    }
    
    /* Metrics - Red */
    [data-testid="stMetricValue"] {
        color: #dc2626 !important;
        font-size: 2rem !important;
        font-weight: 700;
    }
    
    [data-testid="stMetricLabel"] {
        color: #6b7280 !important;
    }
    
    /* Info/Success/Error boxes */
    .stAlert {
        background-color: #fef2f2 !important;
        border: 2px solid #fecaca !important;
        color: #991b1b !important;
    }
    
    /* Radio buttons */
    .stRadio > label {
        color: #374151 !important;
    }
    
    /* Divider */
    hr {
        border-color: #e5e7eb !important;
    }
    
    /* Section boxes */
    .section-box {
        background-color: #f9fafb;
        border: 2px solid #e5e7eb;
        border-radius: 8px;
        padding: 1.5rem;
        margin-bottom: 1rem;
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
    """Initialize Supabase client"""
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
    """Simple password verification"""
    try:
        user = supabase.table("users").select("*").eq("username", username).eq("password", password).eq("organization", "Warehouse").execute()
        
        if user.data and len(user.data) > 0:
            return user.data[0]
                
        return None
    except Exception as e:
        st.error(f"Login error: {str(e)}")
        return None

# =============================================
# GET CURRENT STOCK
# =============================================
def get_stock(size):
    """Get current stock for a size"""
    try:
        result = supabase.table("stock").select("quantity").eq("organization", "Warehouse").eq("size", size).execute()
        if result.data and len(result.data) > 0:
            return result.data[0]['quantity']
        return 0
    except:
        return 0

# =============================================
# UPDATE STOCK
# =============================================
def update_stock(size, category, quantity, operation):
    """Update stock - add or subtract"""
    try:
        current = get_stock(size)
        
        if operation == "IN":
            new_quantity = current + quantity
        else:  # OUT
            new_quantity = current - quantity
            if new_quantity < 0:
                st.error(f"❌ Size {size}: Not enough stock! Current: {current}, Requested: {quantity}")
                return False
        
        # Check if record exists
        check = supabase.table("stock").select("id").eq("organization", "Warehouse").eq("size", size).execute()
        
        if check.data and len(check.data) > 0:
            # Update existing
            supabase.table("stock").update({"quantity": new_quantity, "updated_at": datetime.now().isoformat()}).eq("organization", "Warehouse").eq("size", size).execute()
        else:
            # Insert new
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
    """Record transaction in database"""
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
    """Simple login page"""
    st.markdown("<h1 style='text-align:center;color:#dc2626;'>📦 WAREHOUSE</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align:center;color:#6b7280;'>T-Shirt Stock Management</p>", unsafe_allow_html=True)
    st.markdown("---")
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown("<h3 style='color:#dc2626;'>Warehouse Login</h3>", unsafe_allow_html=True)
        
        username = st.text_input("👤 Username", placeholder="warehouse1", key="username_input")
        password = st.text_input("🔑 Password", type="password", placeholder="Enter password", key="password_input")
        
        if st.button("🚀 Login", use_container_width=True):
            if username and password:
                user = verify_login(username, password)
                if user:
                    st.session_state.logged_in = True
                    st.session_state.user = user
                    st.session_state.login_time = datetime.now()
                    st.success(f"✅ Welcome {user['name']}!")
                    st.rerun()
                else:
                    st.error("❌ Invalid credentials!")
            else:
                st.warning("⚠️ Please enter both username and password")
    
    st.markdown("---")
    st.markdown("<p style='text-align:center;color:#9ca3af;font-size:0.9rem;'>Warehouse App v1.0</p>", unsafe_allow_html=True)

# =============================================
# STOCK IN PAGE
# =============================================
def stock_in_page():
    """Stock IN - Receiving new stock"""
    st.markdown("<h2 style='color:#dc2626;'>📥 Stock IN - Receive New Stock</h2>", unsafe_allow_html=True)
    st.markdown("---")
    
    # Show current stock summary at top
    st.markdown("<h3 style='color:#dc2626;'>📊 Current Stock Summary</h3>", unsafe_allow_html=True)
    
    kids_total = sum([get_stock(size) for size in KIDS_SIZES])
    adults_total = sum([get_stock(size) for size in ADULT_SIZES])
    grand_total = kids_total + adults_total
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("👶 Kids Total", f"{kids_total:,}")
    with col2:
        st.metric("👔 Adults Total", f"{adults_total:,}")
    with col3:
        st.metric("🎽 Grand Total", f"{grand_total:,}")
    
    st.markdown("---")
    
    # Reason input (single reason for all sizes)
    st.markdown("<h3 style='color:#dc2626;'>📝 Reason for Stock IN</h3>", unsafe_allow_html=True)
    reason = st.text_area("Enter reason (required)", placeholder="e.g., New shipment from supplier", key="reason_in", height=100)
    
    st.markdown("---")
    
    # Kids Section
    st.markdown("<h3 style='color:#dc2626;'>👶 Kids Sizes</h3>", unsafe_allow_html=True)
    
    kids_quantities = {}
    cols = st.columns(4)
    for idx, size in enumerate(KIDS_SIZES):
        with cols[idx]:
            current_stock = get_stock(size)
            st.markdown(f"<p style='color:#6b7280;font-size:0.9rem;'>Current: {current_stock}</p>", unsafe_allow_html=True)
            kids_quantities[size] = st.number_input(
                f"Kids Size {size}",
                min_value=0,
                value=0,
                step=1,
                key=f"kids_in_{size}"
            )
    
    st.markdown("---")
    
    # Adults Section
    st.markdown("<h3 style='color:#dc2626;'>👔 Adult Sizes</h3>", unsafe_allow_html=True)
    
    adults_quantities = {}
    cols = st.columns(4)
    for idx, size in enumerate(ADULT_SIZES):
        with cols[idx % 4]:
            current_stock = get_stock(size)
            st.markdown(f"<p style='color:#6b7280;font-size:0.9rem;'>Current: {current_stock}</p>", unsafe_allow_html=True)
            adults_quantities[size] = st.number_input(
                f"Adult Size {size}",
                min_value=0,
                value=0,
                step=1,
                key=f"adult_in_{size}"
            )
    
    st.markdown("---")
    
    # Submit button
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("✅ STOCK IN - Receive All Items", use_container_width=True, type="primary"):
            if not reason.strip():
                st.error("❌ Please enter a reason for stock IN!")
                return
            
            # Collect all non-zero quantities
            all_items = []
            for size in KIDS_SIZES:
                if kids_quantities[size] > 0:
                    all_items.append(("Kids", size, kids_quantities[size]))
            
            for size in ADULT_SIZES:
                if adults_quantities[size] > 0:
                    all_items.append(("Adults", size, adults_quantities[size]))
            
            if not all_items:
                st.warning("⚠️ No quantities entered!")
                return
            
            # Process all items
            success_count = 0
            for category, size, qty in all_items:
                if update_stock(size, category, qty, "IN"):
                    if record_transaction(size, qty, "IN", reason, st.session_state.user['name']):
                        success_count += 1
            
            if success_count == len(all_items):
                st.success(f"✅ Successfully received {len(all_items)} items into stock!")
                st.balloons()
                st.rerun()
            else:
                st.warning(f"⚠️ Partially completed: {success_count}/{len(all_items)} items processed")

# =============================================
# STOCK OUT PAGE
# =============================================
def stock_out_page():
    """Stock OUT - Sending stock to destinations"""
    st.markdown("<h2 style='color:#dc2626;'>📤 Stock OUT - Send to Destinations</h2>", unsafe_allow_html=True)
    st.markdown("---")
    
    # Show current stock summary at top
    st.markdown("<h3 style='color:#dc2626;'>📊 Current Stock Summary</h3>", unsafe_allow_html=True)
    
    kids_total = sum([get_stock(size) for size in KIDS_SIZES])
    adults_total = sum([get_stock(size) for size in ADULT_SIZES])
    grand_total = kids_total + adults_total
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("👶 Kids Total", f"{kids_total:,}")
    with col2:
        st.metric("👔 Adults Total", f"{adults_total:,}")
    with col3:
        st.metric("🎽 Grand Total", f"{grand_total:,}")
    
    st.markdown("---")
    
    # Reason input (single reason for all sizes)
    st.markdown("<h3 style='color:#dc2626;'>📝 Reason for Stock OUT</h3>", unsafe_allow_html=True)
    reason = st.text_area("Enter reason (required)", placeholder="e.g., Sent to Org A for event", key="reason_out", height=100)
    
    st.markdown("---")
    
    # Kids Section
    st.markdown("<h3 style='color:#dc2626;'>👶 Kids Sizes</h3>", unsafe_allow_html=True)
    
    kids_quantities = {}
    cols = st.columns(4)
    for idx, size in enumerate(KIDS_SIZES):
        with cols[idx]:
            current_stock = get_stock(size)
            st.markdown(f"<p style='color:#6b7280;font-size:0.9rem;'>Available: {current_stock}</p>", unsafe_allow_html=True)
            kids_quantities[size] = st.number_input(
                f"Kids Size {size}",
                min_value=0,
                max_value=current_stock,
                value=0,
                step=1,
                key=f"kids_out_{size}"
            )
    
    st.markdown("---")
    
    # Adults Section
    st.markdown("<h3 style='color:#dc2626;'>👔 Adult Sizes</h3>", unsafe_allow_html=True)
    
    adults_quantities = {}
    cols = st.columns(4)
    for idx, size in enumerate(ADULT_SIZES):
        with cols[idx % 4]:
            current_stock = get_stock(size)
            st.markdown(f"<p style='color:#6b7280;font-size:0.9rem;'>Available: {current_stock}</p>", unsafe_allow_html=True)
            adults_quantities[size] = st.number_input(
                f"Adult Size {size}",
                min_value=0,
                max_value=current_stock,
                value=0,
                step=1,
                key=f"adult_out_{size}"
            )
    
    st.markdown("---")
    
    # Submit button
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("✅ STOCK OUT - Send All Items", use_container_width=True, type="primary"):
            if not reason.strip():
                st.error("❌ Please enter a reason for stock OUT!")
                return
            
            # Collect all non-zero quantities
            all_items = []
            for size in KIDS_SIZES:
                if kids_quantities[size] > 0:
                    all_items.append(("Kids", size, kids_quantities[size]))
            
            for size in ADULT_SIZES:
                if adults_quantities[size] > 0:
                    all_items.append(("Adults", size, adults_quantities[size]))
            
            if not all_items:
                st.warning("⚠️ No quantities entered!")
                return
            
            # Process all items
            success_count = 0
            for category, size, qty in all_items:
                if update_stock(size, category, qty, "OUT"):
                    if record_transaction(size, qty, "OUT", reason, st.session_state.user['name']):
                        success_count += 1
            
            if success_count == len(all_items):
                st.success(f"✅ Successfully sent {len(all_items)} items out of stock!")
                st.balloons()
                st.rerun()
            else:
                st.warning(f"⚠️ Partially completed: {success_count}/{len(all_items)} items processed")

# =============================================
# MAIN APP
# =============================================
def main():
    """Main application"""
    
    # Initialize session state
    if 'logged_in' not in st.session_state:
        st.session_state.logged_in = False
    
    # Check login status
    if not st.session_state.logged_in:
        login_page()
        return
    
    # Sidebar navigation
    with st.sidebar:
        st.markdown("<h2 style='color:#dc2626;'>📦 Warehouse</h2>", unsafe_allow_html=True)
        st.markdown(f"<p style='color:#374151;'>👤 {st.session_state.user['name']}</p>", unsafe_allow_html=True)
        st.markdown("---")
        
        # Operation selection
        st.markdown("<h3 style='color:#dc2626;'>Select Operation</h3>", unsafe_allow_html=True)
        operation = st.radio(
            "Operation",
            ["📥 Stock IN", "📤 Stock OUT"],
            label_visibility="collapsed"
        )
        
        st.markdown("---")
        
        # Session info
        login_time = st.session_state.get('login_time', datetime.now())
        session_duration = datetime.now() - login_time
        st.markdown(f"<p style='color:#9ca3af;font-size:0.8rem;'>Session: {int(session_duration.total_seconds() / 60)} min</p>", unsafe_allow_html=True)
        
        # Logout button
        if st.button("🚪 Logout", use_container_width=True):
            st.session_state.logged_in = False
            st.session_state.user = None
            st.rerun()
        
        st.markdown("---")
        st.markdown("<p style='color:#9ca3af;font-size:0.8rem;text-align:center;'>Warehouse v1.0</p>", unsafe_allow_html=True)
    
    # Main content based on operation
    if operation == "📥 Stock IN":
        stock_in_page()
    else:
        stock_out_page()

# =============================================
# RUN APP
# =============================================
if __name__ == "__main__":
    main()
