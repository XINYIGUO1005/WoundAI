import streamlit as st
import pandas as pd
import numpy as np
import cv2
import re
from PIL import Image

st.set_page_config(page_title="WoundAI", layout="wide")

st.title("🔬 WoundAI")
st.subheader("Cell Migration Analyzer")


def get_mask(img):

    gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)

    # Otsu threshold
    _, mask = cv2.threshold(
        gray,
        0,
        255,
        cv2.THRESH_BINARY + cv2.THRESH_OTSU
    )

    # invert
    mask = 255 - mask

    kernel = np.ones((5,5), np.uint8)

    mask = cv2.morphologyEx(
        mask,
        cv2.MORPH_CLOSE,
        kernel
    )

    return mask


def area(mask):

    return np.sum(mask > 0)


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

            pairs[sample]["0h"] = file

        elif "24h" in name.lower():

            sample = re.sub(r'[-_]?24h.*', '', name, flags=re.I)

            if sample not in pairs:
                pairs[sample] = {}

            pairs[sample]["24h"] = file

    results = []

    for sample, imgs in pairs.items():

        if "0h" in imgs and "24h" in imgs:

            img0 = np.array(
                Image.open(imgs["0h"]).convert("RGB")
            )

            img24 = np.array(
                Image.open(imgs["24h"]).convert("RGB")
            )

            mask0 = get_mask(img0)
            mask24 = get_mask(img24)

            a0 = area(mask0)
            a24 = area(mask24)

            migration = (a0 - a24) / a0 * 100

            results.append(
                {
                    "Sample": sample,
                    "Area_0h": a0,
                    "Area_24h": a24,
                    "Migration_%": round(migration, 2)
                }
            )

            st.write("---")
            st.subheader(sample)

            col1, col2 = st.columns(2)

            with col1:
                st.image(mask0, caption="0h mask")

            with col2:
                st.image(mask24, caption="24h mask")

    if len(results) > 0:

        df = pd.DataFrame(results)

        st.write("## Results")

        st.dataframe(df)

        csv = df.to_csv(index=False)

        st.download_button(
            "Download CSV",
            csv,
            "results.csv",
            "text/csv"
        )

else:

    st.info("Please upload images.")
