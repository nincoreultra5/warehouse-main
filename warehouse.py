import streamlit as st

# =============================================
# PAGE CONFIG
# =============================================
st.set_page_config(
    page_title="Warehouse",
    page_icon="📦",
    layout="wide"
)

# =============================================
# FULL HTML/CSS/JS WEBSITE
# =============================================
html_content = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Warehouse - T-Shirt Inventory</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        body {
            font-family: Arial, sans-serif;
            background-color: #ffffff;
            color: #1f2937;
            padding: 20px;
        }
        .container {
            max-width: 1200px;
            margin: 0 auto;
        }
        .header {
            text-align: center;
            color: #dc2626;
            margin-bottom: 20px;
        }
        .sizes-row {
            display: flex;
            flex-wrap: wrap;
            gap: 10px;
            margin-bottom: 20px;
        }
        .size-item {
            flex: 1 1 20%;
            min-width: 80px;
            padding: 10px;
            border: 2px solid #e5e7eb;
            border-radius: 8px;
            background-color: #f9fafb;
            text-align: center;
        }
        .input-field {
            width: 100%;
            padding: 8px;
            margin-top: 5px;
            border: 2px solid #e5e7eb;
            border-radius: 6px;
        }
        .button {
            background-color: #dc2626;
            color: white;
            padding: 10px 20px;
            border: none;
            border-radius: 8px;
            cursor: pointer;
            font-weight: bold;
        }
        .button:hover {
            background-color: #b91c1c;
        }
        @media (max-width: 768px) {
            .size-item {
                flex: 1 1 20%;
                min-width: 80px;
            }
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>Warehouse - T-Shirt Inventory</h1>
        </div>
        
        <div class="sizes-row">
            <div class="size-item">
                <p>Size 26</p>
                <input type="number" class="input-field" placeholder="Quantity">
            </div>
            <div class="size-item">
                <p>Size 28</p>
                <input type="number" class="input-field" placeholder="Quantity">
            </div>
            <div class="size-item">
                <p>Size 30</p>
                <input type="number" class="input-field" placeholder="Quantity">
            </div>
            <div class="size-item">
                <p>Size 32</p>
                <input type="number" class="input-field" placeholder="Quantity">
            </div>
        </div>
        
        <div class="sizes-row">
            <div class="size-item">
                <p>Size 34</p>
                <input type="number" class="input-field" placeholder="Quantity">
            </div>
            <div class="size-item">
                <p>Size 36</p>
                <input type="number" class="input-field" placeholder="Quantity">
            </div>
            <div class="size-item">
                <p>Size 38</p>
                <input type="number" class="input-field" placeholder="Quantity">
            </div>
            <div class="size-item">
                <p>Size 40</p>
                <input type="number" class="input-field" placeholder="Quantity">
            </div>
            <div class="size-item">
                <p>Size 42</p>
                <input type="number" class="input-field" placeholder="Quantity">
            </div>
            <div class="size-item">
                <p>Size 44</p>
                <input type="number" class="input-field" placeholder="Quantity">
            </div>
            <div class="size-item">
                <p>Size 46</p>
                <input type="number" class="input-field" placeholder="Quantity">
            </div>
        </div>
        
        <button class="button">Submit</button>
    </div>
</body>
</html>
"""

# =============================================
# RENDER HTML
# =============================================
st.markdown(html_content, unsafe_allow_html=True)
