import os

import matplotlib.patches as mpatches
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

# Set paths
base_dir = os.path.dirname(os.path.abspath(__file__))
csv_path = os.path.join(base_dir, "data.csv")

# Read data
df = pd.read_csv(csv_path)

# MATLAB reads the table with preserve names, so pandas will append .1 to duplicates.
# Original Columns:
# 0: treat
# 1: Day
# 2: value1
# 3: value2
# 4: value3
# 5: Non_SMK
# 6: SMK
# 7: Non_SMK+abx
# 8: SMK+abx
# 9: Non_SMK.1
# 10: SMK.1
# 11: Non_SMK+abx.1
# 12: SMK+abx.1

treat_names = ["Non_SMK", "SMK", "Non_SMK+abx", "SMK+abx"]
color_list = (
    np.array([[84, 148, 206], [255, 130, 131], [13, 137, 138], [249, 204, 82]]) / 255.0
)

fig = plt.figure(figsize=(7.5, 7.25))

# Main plot
ax1 = fig.add_axes([0.12, 0.11, 0.83, 0.82])
legend_patches = []

for i, treat in enumerate(treat_names):
    temp_df = df[df["treat"] == treat].copy()
    day = temp_df["Day"].values
    val_cols = ["value1", "value2", "value3"]
    values = temp_df[val_cols].values

    mean_val = np.nanmean(values, axis=1)
    # MATLAB std(value, 1, 2) specifies weight=1 which is population standard deviation (N instead of N-1)
    std_val = np.nanstd(values, axis=1, ddof=0)
    # MATLAB size(value, 2) is always 3 here
    n_val = values.shape[1]
    se_val = std_val / np.sqrt(n_val)

    # Error bar (black lines)
    ax1.errorbar(
        day,
        mean_val,
        yerr=se_val,
        fmt="none",
        ecolor="black",
        elinewidth=1.8,
        capsize=6,
        capthick=2.0,
        zorder=3,
    )

    # Thick line
    ax1.plot(day, mean_val, color=color_list[i], linewidth=6, zorder=2)

    # Markers (white face initially, wait MATLAB says MarkerFaceColor is colorList(i,:))
    ax1.plot(
        day,
        mean_val,
        "o",
        markeredgecolor="black",
        markeredgewidth=1.7,
        markerfacecolor=color_list[i],
        markersize=12,
        zorder=4,
    )

    patch = mpatches.Patch(facecolor=color_list[i], edgecolor="black", linewidth=1.2)
    legend_patches.append(patch)

# Legend
legend_labels = ["Non_SMK", "SMK", "Non_SMK+abx", "SMK+abx"]
# To emulate 'northoutside', place it above the axes
ax1.legend(
    legend_patches,
    legend_labels,
    loc="lower center",
    bbox_to_anchor=(0.5, 1.02),
    ncol=4,
    frameon=False,
    prop={"size": 14},
    handletextpad=0.4,
    columnspacing=1.0,
    handlelength=1.4,
    handleheight=1.2,
)

# Axes configuration
ax1.set_xlim([0, 40])
ax1.set_ylim([0, 60])
ax1.set_xticks(np.arange(0, 41, 10))
ax1.set_yticks(np.arange(0, 61, 20))

ax1.set_xlabel("Day", fontsize=14, fontweight="bold")
ax1.set_ylabel("Weight change(%)", fontsize=14, fontweight="bold")

for spine in ax1.spines.values():
    spine.set_linewidth(1.5)
ax1.spines["top"].set_visible(False)
ax1.spines["right"].set_visible(False)
ax1.tick_params(direction="out", width=1.5, labelsize=12)

# Background lines and patches
ax1.plot([21, 21], [0, 60], linestyle="--", color="black", linewidth=1.8, zorder=0.5)
ax1.fill_between(
    [21, 40],
    [0, 0],
    [60, 60],
    color=np.array([229, 229, 229]) / 255.0,
    edgecolor="none",
    zorder=0,
)

# Significance lines and text on ax1
ax1.plot([36.2, 36.2], [18, 26], color="black", linewidth=2.5, zorder=5)
ax1.plot([38, 38], [18, 40], color="black", linewidth=2.5, zorder=5)
ax1.text(
    37.3,
    22,
    "***",
    rotation=90,
    fontsize=17,
    ha="center",
    va="center",
    fontweight="bold",
    zorder=5,
)
ax1.text(
    39.3,
    29,
    "****",
    rotation=90,
    fontsize=17,
    ha="center",
    va="center",
    fontweight="bold",
    zorder=5,
)

# ==================== Inset 1 ====================
ax2 = fig.add_axes([0.14, 0.725, 0.35, 0.17])
bar_data_1 = df.iloc[:, 5:9].values
bar_data_1 = bar_data_1[~np.isnan(bar_data_1[:, 0])]  # Drop NaN rows

mean_bar1 = np.nanmean(bar_data_1, axis=0)
# MATLAB std(barData1, 1) uses N for normalization
std_bar1 = np.nanstd(bar_data_1, axis=0, ddof=0)
se_bar1 = std_bar1 / np.sqrt(bar_data_1.shape[0])

y_pos = np.array([1, 2, 3, 4])
ax2.barh(
    y_pos,
    mean_bar1,
    height=0.8,
    facecolor="white",
    edgecolor="black",
    linewidth=1.2,
    zorder=2,
)
ax2.errorbar(
    mean_bar1,
    y_pos,
    xerr=se_bar1,
    fmt="none",
    ecolor="black",
    elinewidth=1.2,
    capsize=3.5,
    capthick=1.5,
    zorder=4,
)

np.random.seed(42)  # Ensure reproducible jitter
for i in range(4):
    y_jitter = y_pos[i] + np.random.uniform(-0.3, 0.3, size=bar_data_1.shape[0])
    ax2.scatter(
        bar_data_1[:, i],
        y_jitter,
        color=color_list[i],
        s=20,
        edgecolor="none",
        zorder=5,
    )

ax2.axvline(0, color="black", linewidth=1.2, zorder=1)  # Mimic bar BaseLine

ax2.plot([370, 370], [1, 2], color="black", linewidth=2.5, zorder=6)
ax2.plot([530, 530], [3, 4], color="black", linewidth=2.5, zorder=6)
ax2.text(
    410,
    1.5,
    "****",
    rotation=90,
    fontsize=17,
    ha="center",
    va="center",
    fontweight="bold",
    zorder=6,
)
ax2.text(
    570,
    3.5,
    "****",
    rotation=90,
    fontsize=17,
    ha="center",
    va="center",
    fontweight="bold",
    zorder=6,
)

ax2.set_xlim([-50, 600])
ax2.set_ylim([4.6, 0.4])
ax2.set_xticks(np.arange(0, 601, 200))
ax2.set_yticks([])
ax2.set_title("iAUC: Exposure", fontsize=15, fontweight="bold", pad=2)

for spine in ax2.spines.values():
    spine.set_linewidth(1.5)
ax2.spines["top"].set_visible(False)
ax2.spines["right"].set_visible(False)
ax2.tick_params(direction="out", width=1.5, labelsize=12)
ax2.patch.set_alpha(0)  # Transparent background

# ==================== Inset 2 ====================
ax3 = fig.add_axes([0.58, 0.725, 0.35, 0.17])
bar_data_2 = df.iloc[:, 9:13].values
bar_data_2 = bar_data_2[~np.isnan(bar_data_2[:, 0])]

mean_bar2 = np.nanmean(bar_data_2, axis=0)
std_bar2 = np.nanstd(bar_data_2, axis=0, ddof=0)
se_bar2 = std_bar2 / np.sqrt(bar_data_2.shape[0])

ax3.barh(
    y_pos,
    mean_bar2,
    height=0.8,
    facecolor="white",
    edgecolor="black",
    linewidth=1.2,
    zorder=2,
)
ax3.errorbar(
    mean_bar2,
    y_pos,
    xerr=se_bar2,
    fmt="none",
    ecolor="black",
    elinewidth=1.2,
    capsize=3.5,
    capthick=1.5,
    zorder=4,
)

for i in range(4):
    y_jitter = y_pos[i] + np.random.uniform(-0.3, 0.3, size=bar_data_2.shape[0])
    ax3.scatter(
        bar_data_2[:, i],
        y_jitter,
        color=color_list[i],
        s=20,
        edgecolor="none",
        zorder=5,
    )

ax3.axvline(0, color="black", linewidth=1.2, zorder=1)

ax3.plot([430, 430], [1, 2], color="black", linewidth=2.5, zorder=6)
ax3.plot([420, 420], [3, 4], color="black", linewidth=2.5, zorder=6)
ax3.text(
    465,
    1.5,
    "****",
    rotation=90,
    fontsize=17,
    ha="center",
    va="center",
    fontweight="bold",
    zorder=6,
)
ax3.text(
    455,
    3.5,
    "****",
    rotation=90,
    fontsize=17,
    ha="center",
    va="center",
    fontweight="bold",
    zorder=6,
)

ax3.set_xlim([0, 500])
ax3.set_ylim([4.6, 0.4])
ax3.set_xticks(np.arange(0, 501, 100))
ax3.set_yticks([])
ax3.set_title("iAUC: Cessation", fontsize=15, fontweight="bold", pad=2)

for spine in ax3.spines.values():
    spine.set_linewidth(1.5)
ax3.spines["top"].set_visible(False)
ax3.spines["right"].set_visible(False)
ax3.tick_params(direction="out", width=1.5, labelsize=12)
ax3.patch.set_alpha(0)

# Save figure matching Matlab output name result.png
out_file = os.path.join(base_dir, "result.png")
plt.savefig(out_file, dpi=300, bbox_inches="tight")
print(f"Plot successfully saved to {out_file}")
