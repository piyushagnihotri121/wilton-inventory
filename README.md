A Streamlit-based tool designed to assist in the barcode inventory system for Wilton Weavers by calculating bobbins required for material planning.
It helps production teams streamline planning by matching item descriptions from two different files (Frame Master and Material-wise Planning) and automatically computing bobbins needed, stock balances, and planned weights.


🚀 Features

📂 Upload Frame Master Excel and Material-wise Planning Excel files

🧹 Cleans item descriptions (handles hyphens, suffixes, etc.)

🔎 Fuzzy matching of item descriptions between planning and frame files (using fuzzywuzzy)

📊 Computes:

Frames needed per material

Planned KG (aggregating weekly & overdue quantities)

Stock and stock balance

Required bobbins (based on load capacity per frame)

📥 Download results as CSV

🖥️ Simple Streamlit web interface with one-click calculations
