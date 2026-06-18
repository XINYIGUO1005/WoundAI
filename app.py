import streamlit as st
import pandas as pd
import re

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

    pairs = {}

    for file in uploaded_files:

        name = file.name

        if "0h" in name.lower():
            sample = re.sub(r'[-_]?0h.*', '', name, flags=re.I)

            if sample not in pairs:
                pairs[sample] = {}

            pairs[sample]["0h"] = name

        elif "24h" in name.lower():
            sample = re.sub(r'[-_]?24h.*', '', name, flags=re.I)

            if sample not in pairs:
                pairs[sample] = {}

            pairs[sample]["24h"] = name

    st.write("## Paired samples")

    results = []

    for sample, imgs in pairs.items():

        zero = imgs.get("0h", "Missing")
        day24 = imgs.get("24h", "Missing")

        results.append(
            {
                "Sample": sample,
                "0h image": zero,
                "24h image": day24
            }
        )

    df = pd.DataFrame(results)

    st.dataframe(df)

    csv = df.to_csv(index=False)

    st.download_button(
        "Download CSV",
        csv,
        "paired_samples.csv",
        "text/csv"
    )

else:

    st.info("Please upload images.")
