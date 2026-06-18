import streamlit as st

st.set_page_config(page_title="WoundAI", layout="wide")

st.title("🔬 WoundAI")
st.subheader("Cell Migration Analyzer")

uploaded_files = st.file_uploader(
    "Upload images (0h and 24h)",
    accept_multiple_files=True,
    type=["tif", "tiff", "png", "jpg"]
)

if uploaded_files:

    st.success(f"{len(uploaded_files)} images uploaded!")

    st.write("### Uploaded files")

    for file in uploaded_files:
        st.write(file.name)

else:

    st.info("Please upload images.")
