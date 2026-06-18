import matplotlib.pyplot as plt
import pandas as pd


def draw_barplot(df):

    fig, ax = plt.subplots(figsize=(6,4))

    ax.bar(
        df["Sample"],
        df["Migration_%"]
    )

    ax.set_ylabel("Migration (%)")

    ax.set_title("Cell migration")

    plt.xticks(rotation=45)

    plt.tight_layout()

    return fig
