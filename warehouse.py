<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Warehouse - T-Shirt Inventory</title>
    <script src="https://cdn.jsdelivr.net/npm/@supabase/supabase-js@2"></script>
    <style>
        /* Reset and base styles */
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            font-family: Arial, sans-serif;
            background-color: #ffffff;
            color: #1f2937;
            padding: 10px;
            font-size: 14px;
        }

        .container {
            max-width: 366px;
            margin: 0 auto;
        }

        .header {
            text-align: center;
            color: #dc2626;
            margin-bottom: 15px;
            font-size: 18px;
            font-weight: bold;
        }

        .section {
            margin-bottom: 20px;
            padding: 10px;
            border: 2px solid #e5e7eb;
            border-radius: 8px;
            background-color: #f9fafb;
        }

        .section-title {
            color: #dc2626;
            font-size: 16px;
            font-weight: bold;
            margin-bottom: 10px;
            text-align: center;
        }

        .sizes-row {
            display: flex;
            flex-wrap: wrap;
            gap: 5px;
            justify-content: space-between;
            margin-bottom: 10px;
        }

        .size-item {
            flex: 1 1 calc(20% - 5px);
            min-width: 60px;
            padding: 8px;
            border: 2px solid #e5e7eb;
            border-radius: 8px;
            background-color: #ffffff;
            text-align: center;
            font-size: 12px;
        }

        .size-item p {
            margin: 2px 0;
            color: #6b7280;
        }

        .input-field {
            width: 100%;
            padding: 6px;
            margin-top: 2px;
            border: 2px solid #e5e7eb;
            border-radius: 6px;
            font-size: 12px;
        }

        .button {
            background-color: #dc2626;
            color: white;
            padding: 10px 15px;
            border: none;
            border-radius: 8px;
            cursor: pointer;
            font-weight: bold;
            font-size: 14px;
            width: 100%;
        }

        .button:hover {
            background-color: #b91c1c;
        }

        .reason {
            width: 100%;
            padding: 8px;
            margin: 10px 0;
            border: 2px solid #e5e7eb;
            border-radius: 6px;
            font-size: 12px;
        }

        @media (max-width: 366px) {
            .size-item {
                flex: 1 1 calc(20% - 5px);
                min-width: 60px;
            }
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>Warehouse - T-Shirt Inventory</h1>
        </div>
        
        <div class="section">
            <div class="section-title">Kids</div>
            <div class="sizes-row">
                <div class="size-item">
                    <p>26</p>
                    <input type="number" class="input-field" placeholder="Qty">
                </div>
                <div class="size-item">
                    <p>28</p>
                    <input type="number" class="input-field" placeholder="Qty">
                </div>
                <div class="size-item">
                    <p>30</p>
                    <input type="number" class="input-field" placeholder="Qty">
                </div>
                <div class="size-item">
                    <p>32</p>
                    <input type="number" class="input-field" placeholder="Qty">
                </div>
            </div>
        </div>
        
        <div class="section">
            <div class="section-title">Adults</div>
            <div class="sizes-row">
                <div class="size-item">
                    <p>34</p>
                    <input type="number" class="input-field" placeholder="Qty">
                </div>
                <div class="size-item">
                    <p>36</p>
                    <input type="number" class="input-field" placeholder="Qty">
                </div>
                <div class="size-item">
                    <p>38</p>
                    <input type="number" class="input-field" placeholder="Qty">
                </div>
                <div class="size-item">
                    <p>40</p>
                    <input type="number" class="input-field" placeholder="Qty">
                </div>
                <div class="size-item">
                    <p>42</p>
                    <input type="number" class="input-field" placeholder="Qty">
                </div>
                <div class="size-item">
                    <p>44</p>
                    <input type="number" class="input-field" placeholder="Qty">
                </div>
                <div class="size-item">
                    <p>46</p>
                    <input type="number" class="input-field" placeholder="Qty">
                </div>
            </div>
        </div>
        
        <div class="section">
            <div class="section-title">Reason</div>
            <textarea class="reason" placeholder="Enter reason"></textarea>
        </div>
        
        <button class="button">Submit</button>
    </div>

    <script>
        // Initialize Supabase client
        const supabaseUrl = 'https://ylrfinilcktpmaslaytn.supabase.co';
        const supabaseKey = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InlscmZpbmlsY2t0cG1hc2xheXRuIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NjU0Mzg5NTAsImV4cCI6MjA4MTAxNDk1MH0.GrVMQVfED2xiyZk25XhZSBY5pHwilH7NixedsvlhEME';
        const supabase = supabase.createClient(supabaseUrl, supabaseKey);

        // Example: Read stock data
        async function getStock() {
            const { data, error } = await supabase
                .from('stock')
                .select('*')
                .eq('organization', 'Warehouse');
            
            if (error) {
                console.error('Error fetching stock:', error);
            } else {
                console.log('Stock data:', data);
            }
        }

        // Example: Update stock
        async function updateStock(size, quantity) {
            const { data, error } = await supabase
                .from('stock')
                .upsert({
                    organization: 'Warehouse',
                    size: size,
                    quantity: quantity
                });
            
            if (error) {
                console.error('Error updating stock:', error);
            } else {
                console.log('Stock updated:', data);
            }
        }

        // Example: Record transaction
        async function recordTransaction(organization, size, quantity, type, reason, userName) {
            const { data, error } = await supabase
                .from('transactions')
                .insert({
                    organization: organization,
                    size: size,
                    quantity: quantity,
                    type: type,
                    reason: reason,
                    user_name: userName
                });
            
            if (error) {
                console.error('Error recording transaction:', error);
            } else {
                console.log('Transaction recorded:', data);
            }
        }

        // Call getStock on page load
        getStock();
    </script>
</body>
</html>
