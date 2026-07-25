import matplotlib.pyplot as plt
from io import BytesIO
import numpy as np
import pandas as pd


class HabitVisualization:

    @staticmethod
    def create_heatmap(matrix):

        fig, ax = plt.subplots(figsize=(16, 3))

        cmap = plt.cm.Greens
        max_val = max(1, matrix.values.max())

        for y in range(7):
            for x in range(52):
                val = matrix.iloc[y, x]

                rect = plt.Rectangle(
                    (x, y),
                    1,
                    1,
                    facecolor=cmap(val / max_val),
                    edgecolor="#d0d7de",
                    linewidth=0.5
                )
                ax.add_patch(rect)

        ax.set_xlim(0, 52)
        ax.set_ylim(0, 7)
        ax.invert_yaxis()

        ax.set_yticks(range(7))
        ax.set_yticklabels(
            ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
        )

        ax.set_xticks([])

        start = pd.Timestamp.today().normalize() - pd.Timedelta(days=364)

        month_starts = []
        month_labels = []

        for i in range(12):
            d = (start + pd.DateOffset(months=i)).normalize()
            week_index = (d - start).days // 7

            if 0 <= week_index < 52:
                month_starts.append(week_index)
                month_labels.append(d.strftime("%b"))

        for x, label in zip(month_starts, month_labels):
            ax.text(
                x,
                -0.7,
                label,
                fontsize=9,
                ha="center",
                color="#24292f"
            )

        ax.set_title("Habit Heatmap", fontsize=12, pad=40)

        plt.tight_layout()

        buf = BytesIO()
        plt.savefig(buf, format="png", dpi=150, bbox_inches="tight")
        plt.close(fig)

        buf.seek(0)
        return buf