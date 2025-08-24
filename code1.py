import streamlit as st
import pandas as pd
import numpy as np
import math
from fuzzywuzzy import process

st.set_page_config(page_title="🧵 Wilton Weavers Bobbin Plan Calculator", layout="centered")

st.title("🧶 Bobbin Plan Calculator")

# Upload files
frame_file = st.file_uploader("Upload Frame Master Excel", type=["xlsx"])
plan_file = st.file_uploader("Upload Material-wise Planning Excel", type=["xlsx"])

# Clean Description Function
def clean_desc(desc):
    if isinstance(desc, str):
        if '-' in desc:
            parts = desc.rsplit('-', 1)
            last = parts[1].strip()
            if last.isalpha() and len(last) <= 4:
                return parts[0].strip()
        return desc.strip()
    return desc

# Bobbin Calculation Function
def compute_bobbins_from_planned(row):
    if pd.isna(row.get('Planned KG')) or row.get('Planned KG', 0) == 0 or pd.isna(row.get('Frame Needed')):
        return 0
    frame_needed = row['Frame Needed']
    planned_kg = row['Planned KG']
    if frame_needed == 1:
        return math.ceil(planned_kg / 1300)
    elif frame_needed == 2:
        return math.ceil(planned_kg / 2600)
    return 0

if frame_file and plan_file:
    df_frame = pd.read_excel(frame_file)
    df_plan = pd.read_excel(plan_file)

    # Clean Descriptions
    df_frame['Clean Description'] = df_frame['Description'].apply(clean_desc)
    df_plan['Clean Description'] = df_plan['Item Description'].apply(clean_desc)

    # Determine Frames Needed
    frame_counts = df_frame.groupby('Clean Description')['Item Type'].nunique().reset_index()
    frame_counts['Frame Needed'] = frame_counts['Item Type'].apply(lambda x: 2 if x > 1 else 1)
    frame_info = pd.merge(df_frame[['Clean Description', 'Item No.', 'Description']].drop_duplicates(),
                          frame_counts[['Clean Description', 'Frame Needed']],
                          on='Clean Description', how='left')

    # Fuzzy Match Plan Descriptions with Frame Descriptions
    frame_descriptions = frame_info['Clean Description'].tolist()
    def find_best_match(description):
        if pd.isna(description):
            return None, 0
        best_match = process.extractOne(description, frame_descriptions)
        if best_match and best_match[1] >= 80:
            return best_match[0], best_match[1]
        return None, 0

    df_plan[['Best_Match_Description', 'Match_Score']] = df_plan['Clean Description'].apply(
        lambda x: pd.Series(find_best_match(x))
    )

    # Merge on Best Match
    merged = pd.merge(df_plan, frame_info, left_on='Best_Match_Description', right_on='Clean Description', how='left')

    # Calculate Planned KG
    plan_cols_to_sum = ["Over_Due", "Current Week", "Column1", "Week 2"]
    for col in plan_cols_to_sum:
        if col not in merged.columns:
            merged[col] = 0
    merged['Planned KG'] = merged[plan_cols_to_sum].apply(pd.to_numeric, errors='coerce').sum(axis=1)

    # Stock and Stock Balance
    merged['Stock'] = pd.to_numeric(merged.get('Total Stock', 0), errors='coerce').fillna(0)
    merged['Stock Balance'] = merged['Stock'] - merged['Planned KG']

    # Bobbins Required
    merged['Frame Needed'] = pd.to_numeric(merged['Frame Needed'], errors='coerce')
    merged['Planned KG'] = pd.to_numeric(merged['Planned KG'], errors='coerce')
    merged['Bobbins Required'] = merged.apply(compute_bobbins_from_planned, axis=1)

    # Final Result Table
    final_result = merged[['Item No.', 'Item Description', 'Frame Needed', 'Planned KG', 'Bobbins Required']]

    st.subheader("📊 Bobbin Plan Summary")
    st.dataframe(final_result)

    # Download Button
    csv = final_result.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="📥 Download Bobbin Plan as CSV",
        data=csv,
        file_name='bobbin_plan_output.csv',
        mime='text/csv'
    )
else:
    st.info("Please upload both the Frame Master and Planning files to proceed.")
