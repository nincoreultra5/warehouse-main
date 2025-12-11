import streamlit as st
from supabase import create_client
import pandas as pd
from datetime import datetime
import time

# =============================================
# PAGE CONFIG
# =============================================
st.set_page_config(
    page_title="Warehouse - T-Shirt Inventory",
    page_icon="📦",
    layout="wide"
)

# =============================================
# SUPABASE CREDENTIALS
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
    st.markdown("""
    <div style="text-align:center; padding:20px;">
        <h1 style="color:#dc2626;">📦 Warehouse - T-Shirt Inventory</h1>
    </div>
    """, unsafe_allow_html=True)
    
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
    st.markdown("""
    <div style="text-align:center; padding:20px;">
        <h2 style="color:#dc2626;">Stock IN</h2>
    </div>
    """, unsafe_allow_html=True)
    
    # Stock summary
    kids_total = sum([get_stock(size) for size in KIDS_SIZES])
    adults_total = sum([get_stock(size) for size in ADULT_SIZES])
    grand_total = kids_total + adults_total
    
    st.markdown(f"""
    <div style="display: flex; justify-content: space-around; margin: 20px 0; text-align: center;">
        <div style="flex: 1; padding: 10px; border: 2px solid #e5e7eb; border-radius: 8px; background-color: #f9fafb;">
            <h3 style="color:#dc2626;">Kids</h3>
            <p style="color:#6b7280;">{kids_total:,}</p>
        </div>
        <div style="flex: 1; padding: 10px; border: 2px solid #e5e7eb; border-radius: 8px; background-color: #f9fafb;">
            <h3 style="color:#dc2626;">Adults</h3>
            <p style="color:#6b7280;">{adults_total:,}</p>
        </div>
        <div style="flex: 1; padding: 10px; border: 2px solid #e5e7eb; border-radius: 8px; background-color: #f9fafb;">
            <h3 style="color:#dc2626;">Total</h3>
            <p style="color:#6b7280;">{grand_total:,}</p>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Reason input
    reason = st.text_area("Reason (required)", placeholder="e.g., New shipment", key="reason_in")
    
    # Kids section - Horizontal layout for phone
    st.markdown("""
    <div style="text-align:center; padding:20px;">
        <h3 style="color:#dc2626;">Kids</h3>
    </div>
    """, unsafe_allow_html=True)
    
    kids_quantities = {}
    st.markdown('<div style="display: flex; flex-wrap: wrap; justify-content: space-around; margin-bottom: 20px;">', unsafe_allow_html=True)
    for size in KIDS_SIZES:
        current_stock = get_stock(size)
        st.markdown(f'''
        <div style="flex: 1; min-width: 80px; max-width: 100px; padding: 8px; margin: 4px; border: 2px solid #e5e7eb; border-radius: 8px; background-color: #f9fafb; text-align: center; font-size: 14px;">
            <p style="color:#6b7280; margin: 0;">{current_stock}</p>
            <p style="margin: 0;">{size}</p>
            <input type="number" min="0" value="0" style="width: 100%; padding: 6px; border: 2px solid #e5e7eb; border-radius: 6px; font-size: 14px;" id="kids_in_{size}">
        </div>
        ''', unsafe_allow_html=True)
        kids_quantities[size] = st.number_input("", min_value=0, value=0, step=1, key=f"kids_in_{size}", label_visibility="collapsed")
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Adults section - Horizontal layout for phone
    st.markdown("""
    <div style="text-align:center; padding:20px;">
        <h3 style="color:#dc2626;">Adults</h3>
    </div>
    """, unsafe_allow_html=True)
    
    adults_quantities = {}
    st.markdown('<div style="display: flex; flex-wrap: wrap; justify-content: space-around; margin-bottom: 20px;">', unsafe_allow_html=True)
    for size in ADULT_SIZES:
        current_stock = get_stock(size)
        st.markdown(f'''
        <div style="flex: 1; min-width: 80px; max-width: 100px; padding: 8px; margin: 4px; border: 2px solid #e5e7eb; border-radius: 8px; background-color: #f9fafb; text-align: center; font-size: 14px;">
            <p style="color:#6b7280; margin: 0;">{current_stock}</p>
            <p style="margin: 0;">{size}</p>
            <input type="number" min="0" value="0" style="width: 100%; padding: 6px; border: 2px solid #e5e7eb; border-radius: 6px; font-size: 14px;" id="adult_in_{size}">
        </div>
        ''', unsafe_allow_html=True)
        adults_quantities[size] = st.number_input("", min_value=0, value=0, step=1, key=f"adult_in_{size}", label_visibility="collapsed")
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Submit button
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
    st.markdown("""
    <div style="text-align:center; padding:20px;">
        <h2 style="color:#dc2626;">Stock OUT</h2>
    </div>
    """, unsafe_allow_html=True)
    
    # Stock summary
    kids_total = sum([get_stock(size) for size in KIDS_SIZES])
    adults_total = sum([get_stock(size) for size in ADULT_SIZES])
    grand_total = kids_total + adults_total
    
    st.markdown(f"""
    <div style="display: flex; justify-content: space-around; margin: 20px 0; text-align: center;">
        <div style="flex: 1; padding: 10px; border: 2px solid #e5e7eb; border-radius: 8px; background-color: #f9fafb;">
            <h3 style="color:#dc2626;">Kids</h3>
            <p style="color:#6b7280;">{kids_total:,}</p>
        </div>
        <div style="flex: 1; padding: 10px; border: 2px solid #e5e7eb; border-radius: 8px; background-color: #f9fafb;">
            <h3 style="color:#dc2626;">Adults</h3>
            <p style="color:#6b7280;">{adults_total:,}</p>
        </div>
        <div style="flex: 1; padding: 10px; border: 2px solid #e5e7eb; border-radius: 8px; background-color: #f9fafb;">
            <h3 style="color:#dc2626;">Total</h3>
            <p style="color:#6b7280;">{grand_total:,}</p>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Reason input
    reason = st.text_area("Reason (required)", placeholder="e.g., Sent to Org A", key="reason_out")
    
    # Kids section - Horizontal layout for phone
    st.markdown("""
    <div style="text-align:center; padding:20px;">
        <h3 style="color:#dc2626;">Kids</h3>
    </div>
    """, unsafe_allow_html=True)
    
    kids_quantities = {}
    st.markdown('<div style="display: flex; flex-wrap: wrap; justify-content: space-around; margin-bottom: 20px;">', unsafe_allow_html=True)
    for size in KIDS_SIZES:
        current_stock = get_stock(size)
        st.markdown(f'''
        <div style="flex: 1; min-width: 80px; max-width: 100px; padding: 8px; margin: 4px; border: 2px solid #e5e7eb; border-radius: 8px; background-color: #f9fafb; text-align: center; font-size: 14px;">
            <p style="color:#6b7280; margin: 0;">{current_stock}</p>
            <p style="margin: 0;">{size}</p>
            <input type="number" min="0" max="{current_stock}" value="0" style="width: 100%; padding: 6px; border: 2px solid #e5e7eb; border-radius: 6px; font-size: 14px;" id="kids_out_{size}">
        </div>
        ''', unsafe_allow_html=True)
        kids_quantities[size] = st.number_input("", min_value=0, max_value=current_stock, value=0, step=1, key=f"kids_out_{size}", label_visibility="collapsed")
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Adults section - Horizontal layout for phone
    st.markdown("""
    <div style="text-align:center; padding:20px;">
        <h3 style="color:#dc2626;">Adults</h3>
    </div>
    """, unsafe_allow_html=True)
    
    adults_quantities = {}
    st.markdown('<div style="display: flex; flex-wrap: wrap; justify-content: space-around; margin-bottom: 20px;">', unsafe_allow_html=True)
    for size in ADULT_SIZES:
        current_stock = get_stock(size)
        st.markdown(f'''
        <div style="flex: 1; min-width: 80px; max-width: 100px; padding: 8px; margin: 4px; border: 2px solid #e5e7eb; border-radius: 8px; background-color: #f9fafb; text-align: center; font-size: 14px;">
            <p style="color:#6b7280; margin: 0;">{current_stock}</p>
            <p style="margin: 0;">{size}</p>
            <input type="number" min="0" max="{current_stock}" value="0" style="width: 100%; padding: 6px; border: 2px solid #e5e7eb; border-radius: 6px; font-size: 14px;" id="adult_out_{size}">
        </div>
        ''', unsafe_allow_html=True)
        adults_quantities[size] = st.number_input("", min_value=0, max_value=current_stock, value=0, step=1, key=f"adult_out_{size}", label_visibility="collapsed")
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Submit button
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
