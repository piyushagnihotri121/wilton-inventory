import streamlit as st
import pandas as pd

# Page configuration
st.set_page_config(page_title="Frame Requirement Calculator", layout="centered")

# App Title
st.title("📊 Frame Requirement Calculator")

# Function to determine frames required based on Item No. and Item Type
def determine_frames_required(df):
    try:
        grouped = df.groupby('Item No.')['Item Type'].nunique()

        frames_needed = {}
        for item_no, count in grouped.items():
            frames_needed[item_no] = 2 if count > 1 else 1

        total_frames = sum(frames_needed.values())

        result = {
            "frame_requirements": frames_needed,
            "total_frames_required": total_frames,
            "items_with_multiple_frames": {k: v for k, v in frames_needed.items() if v > 1}
        }
        return result

    except Exception as e:
        st.error(f"Error occurred while processing the file: {e}")
        return None

# File uploader widget
uploaded_file = st.file_uploader("Upload your Excel file here", type=["xlsx"])

# Process file after upload
if uploaded_file is not None:
    try:
        df = pd.read_excel(uploaded_file)
        st.subheader("📄 Uploaded Data Preview")
        st.dataframe(df.head())

        result = determine_frames_required(df)

        if result:
            st.subheader("✅ Frame Requirements per Item No.")
            frame_df = pd.DataFrame(list(result['frame_requirements'].items()), columns=['Item No.', 'Frames Required'])
            st.dataframe(frame_df)

            st.success(f"**Total Frames Required:** {result['total_frames_required']}")

            if result['items_with_multiple_frames']:
                st.subheader("📌 Items Requiring Multiple Frames")
                multi_frame_df = pd.DataFrame(list(result['items_with_multiple_frames'].items()), columns=['Item No.', 'Frames Required'])
                st.dataframe(multi_frame_df)
            else:
                st.info("No items require multiple frames.")

    except Exception as e:
        st.error(f"Could not read the uploaded file: {e}")

else:
    st.info("📥 Please upload an Excel file to get started.")
