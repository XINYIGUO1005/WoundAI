import streamlit as st
import pandas as pd
import numpy as np
import re
from PIL import Image

from analysis import (
    get_scratch_mask,
    get_area,
    calculate_migration,
    make_overlay
)

from plot import draw_barplot


st.set_page_config(
    page_title="WoundAI",
    layout="wide"
)

st.title("🔬 WoundAI")
st.subheader("Cell Migration Analyzer")

uploaded_files = st.file_uploader(
    "Upload images",
    accept_multiple_files=True,
    type=["tif", "tiff", "png", "jpg"]
)

if uploaded_files:

    pairs = {}

    for file in uploaded_files:

        name = file.name

        if "0h" in name.lower():

            sample = re.sub(
                r'[-_]?0h.*',
                '',
                name,
                flags=re.I
            )

            if sample not in pairs:
                pairs[sample] = {}

            pairs[sample]["0h"] = file

        elif "24h" in name.lower():

            sample = re.sub(
                r'[-_]?24h.*',
                '',
                name,
                flags=re.I
            )

            if sample not in pairs:
                pairs[sample] = {}

            pairs[sample]["24h"] = file

    results = []

    for sample, imgs in pairs.items():

        if "0h" in imgs and "24h" in imgs:

            img0 = np.array(
                Image.open(
                    imgs["0h"]
                ).convert("RGB")
            )

            img24 = np.array(
                Image.open(
                    imgs["24h"]
                ).convert("RGB")
            )

            mask0 = get_scratch_mask(img0)
            mask24 = get_scratch_mask(img24)

            area0 = get_area(mask0)
            area24 = get_area(mask24)

            migration = calculate_migration(
                area0,
                area24
            )

            results.append(
                {
                    "Sample": sample,
                    "Area_0h": area0,
                    "Area_24h": area24,
                    "Migration_%": migration
                }
            )

            overlay0 = make_overlay(
                img0,
                mask0
            )

            overlay24 = make_overlay(
                img24,
                mask24
            )

            st.write("---")
            st.subheader(sample)

            col1, col2 = st.columns(2)

            with col1:
                st.image(
    mask0,
    caption="0h mask"
)

            with col2:
                st.image(
                    overlay24,
                    caption="24h"
                )

    if len(results) > 0:

        df = pd.DataFrame(results)

        st.write("## Results")

        st.dataframe(df)

        fig = draw_barplot(df)

        st.pyplot(fig)

        csv = df.to_csv(
            index=False
        )

        st.download_button(
            "Download CSV",
            csv,
            "results.csv",
            "text/csv"
        )

else:

    st.info(
        "Please upload images."
    )
