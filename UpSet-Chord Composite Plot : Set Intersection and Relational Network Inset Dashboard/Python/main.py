"""
图表：UpSet-弦图复合图 / 集合交集与关系网络画中画组合图
依赖：matplotlib, numpy, pandas
数据输入：data.csv 为集合成员0/1矩阵；adjMat.csv 首列为弦图源节点，后续列为目标节点权重
"""

from __future__ import annotations

from pathlib import Path

import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib.patches import Polygon


ROOT = Path(__file__).resolve().parent


def rgb(values: list[list[float]] | list[float]) -> np.ndarray:
    return np.asarray(values, dtype=float) / 255.0


def bezier_curve(points: np.ndarray, n: int = 200) -> np.ndarray:
    t = np.linspace(0, 1, n)[:, None]
    return (1 - t) ** 2 * points[0] + 2 * (1 - t) * t * points[1] + t**2 * points[2]


def calc_upset(set_df: pd.DataFrame) -> dict[str, np.ndarray]:
    set_mat = set_df.to_numpy(dtype=float) > 0
    set_mat = set_mat[set_mat.any(axis=1)]
    set_num = set_mat.shape[1]

    full_bool = np.array(
        [list(map(int, format(i, f"0{set_num}b"))) for i in range(1, 2**set_num)],
        dtype=int,
    )
    dec_list = 2 ** np.arange(set_num - 1, -1, -1)
    set_size = set_mat.sum(axis=0)
    ori_index = set_mat.astype(int) @ dec_list

    unique_codes, code_counts = np.unique(ori_index, return_counts=True)
    bin_count = np.zeros(2**set_num, dtype=int)
    bin_count[unique_codes] = code_counts

    nz_index = np.flatnonzero(bin_count[1:] > 0) + 1
    nz_count = bin_count[nz_index]
    nz_bool = full_bool[nz_index - 1]

    order = np.lexsort((nz_index, nz_bool.sum(axis=1)))
    return {
        "set_size": set_size,
        "full_bool": full_bool,
        "nz_index": nz_index[order],
        "nz_count": nz_count[order],
        "sort_set_index": np.arange(set_num),
    }


def draw_upset(fig: plt.Figure, data: dict[str, np.ndarray], set_names: list[str]) -> None:
    set_num = len(set_names)
    max_bars = len(data["nz_index"])

    padding = np.array([0.04, 0.08, 0.02, 0.28], dtype=float)
    spacing = np.array([0.01, 0.01], dtype=float)
    w_ratio = np.array([8.0, 1.0, 0.15], dtype=float)
    h_ratio = np.array([1.0, 0.8], dtype=float)

    total_w = 2 * spacing[0] + padding[0] + padding[2]
    total_h = spacing[1] + padding[1] + padding[3]
    w_ratio = w_ratio / w_ratio.sum() * (1 - total_w)
    h_ratio = h_ratio / h_ratio.sum() * (1 - total_h)

    pos_s = [1 - w_ratio[1] - padding[2], padding[1], w_ratio[1], h_ratio[0]]
    pos_c = [padding[0] + w_ratio[2] + spacing[0], padding[1], w_ratio[0], h_ratio[0]]
    pos_i = [
        padding[0] + w_ratio[2] + spacing[0],
        padding[1] + h_ratio[0] + spacing[1],
        w_ratio[0],
        h_ratio[1],
    ]

    font = "Times New Roman"
    font_weight = "bold"
    text_size = 14
    label_size = 18
    set_name_size = 15
    upset_dot_size = 12.5
    upset_line_width = 3.0
    x = np.arange(1, max_bars + 1)
    y = np.arange(1, set_num + 1)
    counts = data["nz_count"]
    set_sizes = data["set_size"]

    ax_i = fig.add_axes(pos_i, facecolor="none")
    ax_i.bar(x, counts, width=0.8, color="black", edgecolor="none")
    label_offset = 8
    for xi, ci in zip(x, counts, strict=True):
        ax_i.text(
            xi,
            ci + label_offset,
            f"{int(ci)}",
            rotation=90,
            rotation_mode="anchor",
            ha="left",
            va="center_baseline",
            fontsize=text_size,
            fontname=font,
            fontweight=font_weight,
            color="black",
            clip_on=False,
            zorder=5,
        )
    ax_i.set_xlim(max_bars + 1, 0)
    ax_i.set_ylim(0, 500)
    ax_i.set_ylabel("Shared genes", fontsize=label_size, fontname=font, fontweight=font_weight)
    ax_i.set_xticks([])
    ax_i.set_yticks(np.arange(0, 501, 100))
    ax_i.tick_params(axis="y", labelsize=text_size, width=1.2, length=8, direction="out")
    ax_i.tick_params(axis="x", length=0)
    ax_i.spines["left"].set_linewidth(1.2)
    ax_i.spines["bottom"].set_visible(False)
    ax_i.spines["right"].set_visible(False)
    ax_i.spines["top"].set_visible(False)
    for label in ax_i.get_yticklabels():
        label.set_fontname(font)
        label.set_fontweight(font_weight)

    ax_c = fig.add_axes(pos_c, facecolor="none")
    stripe_colors = rgb(
        [
            [230, 75, 53],
            [77, 187, 213],
            [0, 160, 135],
            [60, 84, 136],
            [132, 145, 180],
            [145, 209, 194],
            [176, 156, 133],
        ]
    )
    for row in y:
        ax_c.axhspan(row - 0.5, row + 0.5, color=stripe_colors[row - 1], alpha=0.5, lw=0)

    xx, yy = np.meshgrid(x, y)
    dot_color = rgb([201, 203, 203])
    ax_c.plot(
        xx.ravel(),
        yy.ravel(),
        "o",
        color=dot_color,
        markerfacecolor=dot_color,
        markeredgecolor=dot_color,
        markersize=upset_dot_size,
        linestyle="none",
    )
    for idx, code in enumerate(data["nz_index"], start=1):
        active = np.flatnonzero(data["full_bool"][code - 1, data["sort_set_index"]]) + 1
        ax_c.plot(
            np.full(active.size, idx),
            active,
            "-o",
            color="black",
            markerfacecolor="black",
            markeredgecolor="none",
            markersize=upset_dot_size,
            linewidth=upset_line_width,
        )

    ax_c.set_xlim(max_bars + 1, 0)
    ax_c.set_ylim(set_num + 0.5, 0.5)
    ax_c.set_xticks([])
    ax_c.set_yticks([])
    for spine in ax_c.spines.values():
        spine.set_visible(False)

    label_x = pos_c[0] - 0.016
    for i, name in enumerate(set_names, start=1):
        y_fig = pos_c[1] + pos_c[3] * (set_num - i + 0.5) / set_num
        fig.text(
            label_x,
            y_fig,
            name,
            ha="right",
            va="center",
            fontsize=set_name_size,
            fontname=font,
            fontweight=font_weight,
            color="0.2",
        )

    ax_s = fig.add_axes(pos_s, facecolor="none")
    ax_s.barh(y, set_sizes, height=0.6, color="black", edgecolor="none")
    for yi, size in zip(y, set_sizes, strict=True):
        ax_s.text(
            size + 8,
            yi,
            f"{int(size)}",
            ha="left",
            va="center",
            fontsize=text_size,
            fontname=font,
            fontweight=font_weight,
            color="black",
            clip_on=False,
        )
    ax_s.set_xlim(0, 600)
    ax_s.set_ylim(set_num + 0.5, 0.5)
    ax_s.set_xlabel("Set Size", fontsize=label_size, fontname=font, fontweight=font_weight)
    ax_s.set_yticks([])
    ax_s.set_xticks([0, 200, 400, 600])
    ax_s.tick_params(axis="x", labelsize=text_size, width=1.2, length=4, direction="out")
    ax_s.spines["bottom"].set_linewidth(1.2)
    ax_s.spines["left"].set_visible(False)
    ax_s.spines["right"].set_visible(False)
    ax_s.spines["top"].set_visible(False)
    for label in ax_s.get_xticklabels():
        label.set_fontname(font)
        label.set_fontweight(font_weight)


def annular_sector(
    ax: plt.Axes,
    theta1: float,
    theta2: float,
    inner_r: float,
    outer_r: float,
    color: np.ndarray,
    zorder: int,
) -> None:
    theta = np.linspace(theta1, theta2, 100)
    x = np.cos(theta)
    y = np.sin(theta)
    points = np.column_stack(
        [
            np.r_[inner_r * x, outer_r * x[::-1]],
            np.r_[inner_r * y, outer_r * y[::-1]],
        ]
    )
    ax.add_patch(Polygon(points, closed=True, facecolor=color, edgecolor="none", zorder=zorder))


def draw_chord(
    fig: plt.Figure,
    adj_df: pd.DataFrame,
    pos: list[float] | tuple[float, float, float, float],
) -> None:
    ax = fig.add_axes(pos, facecolor="none")
    ax.set_xlim(-1.15, 1.15)
    ax.set_ylim(-1.15, 1.15)
    ax.set_aspect("equal", adjustable="box")
    ax.axis("off")

    data = adj_df.iloc[:, 1:].to_numpy(dtype=float)
    row_names = adj_df.iloc[:, 0].astype(str).tolist()
    col_names = adj_df.columns[1:].astype(str).tolist()
    num_f, num_t = data.shape
    num_m = max(num_f, num_t)

    sep = 1 / 40
    group_sep = 1 / 16
    if sep * (num_m - 1) > 1:
        sep = 1 / (2 * (num_m - 1))
    square_radius = np.array([1.025, 1.15], dtype=float)
    label_radius = 1.09
    total = data.sum()

    ratio_f = np.r_[0, data.sum(axis=1) / total]
    ratio_t = np.r_[0, data.sum(axis=0) / total]
    sep_len = np.pi * (1 - group_sep) * sep
    base_len_f = np.pi * (1 - group_sep) - num_f * sep_len
    base_len_t = np.pi * (1 - group_sep) - num_t * sep_len

    row_colors = rgb([[177, 156, 132], [144, 209, 196], [131, 146, 179]])
    col_colors = rgb([[232, 72, 51], [76, 187, 214], [0, 160, 136], [59, 83, 137]])

    row_mid = []
    row_rot = []
    for i in range(num_f):
        theta1 = 2 * np.pi - np.pi * group_sep / 2 - ratio_f[: i + 1].sum() * base_len_f - (i + 0.5) * sep_len
        theta2 = 2 * np.pi - np.pi * group_sep / 2 - ratio_f[: i + 2].sum() * base_len_f - (i + 0.5) * sep_len
        annular_sector(ax, theta1, theta2, square_radius[0], square_radius[1], row_colors[i], zorder=3)
        theta3 = (theta1 + theta2) / 2 % (2 * np.pi)
        rotation = theta3 / np.pi * 180 % 360
        if 0 < rotation < 180:
            text_rotation = -((0.5 * np.pi - theta3) / np.pi * 180)
        else:
            text_rotation = -((1.5 * np.pi - theta3) / np.pi * 180)
        row_mid.append(theta3)
        row_rot.append(text_rotation)

    col_mid = []
    col_rot = []
    for j in range(num_t):
        theta1 = np.pi - np.pi * group_sep / 2 - ratio_t[: j + 1].sum() * base_len_t - (j + 0.5) * sep_len
        theta2 = np.pi - np.pi * group_sep / 2 - ratio_t[: j + 2].sum() * base_len_t - (j + 0.5) * sep_len
        annular_sector(ax, theta1, theta2, square_radius[0], square_radius[1], col_colors[j], zorder=3)
        theta3 = (theta1 + theta2) / 2 % (2 * np.pi)
        rotation = theta3 / np.pi * 180
        if 0 < rotation < 180:
            text_rotation = -((0.5 * np.pi - theta3) / np.pi * 180)
        else:
            text_rotation = -((1.5 * np.pi - theta3) / np.pi * 180)
        col_mid.append(theta3)
        col_rot.append(text_rotation)

    for i in range(num_f):
        row_vector = np.r_[0, data[i, ::-1] / data[i].sum()]
        theta1 = 2 * np.pi - np.pi * group_sep / 2 - ratio_f[: i + 1].sum() * base_len_f - (i + 0.5) * sep_len
        theta2 = 2 * np.pi - np.pi * group_sep / 2 - ratio_f[: i + 2].sum() * base_len_f - (i + 0.5) * sep_len
        for j in range(num_t - 1, -1, -1):
            if data[i, j] == 0:
                continue
            col_vector = np.r_[0, data[:, j] / data[:, j].sum()]
            theta3 = np.pi - np.pi * group_sep / 2 - ratio_t[: j + 1].sum() * base_len_t - (j + 0.5) * sep_len
            theta4 = np.pi - np.pi * group_sep / 2 - ratio_t[: j + 2].sum() * base_len_t - (j + 0.5) * sep_len

            theta5 = (theta2 - theta1) * row_vector[: num_t - j].sum() + theta1
            theta6 = (theta2 - theta1) * row_vector[: num_t + 1 - j].sum() + theta1
            theta7 = (theta3 - theta4) * col_vector[: i + 1].sum() + theta4
            theta8 = (theta3 - theta4) * col_vector[: i + 2].sum() + theta4

            p1 = np.array([np.cos(theta5), np.sin(theta5)])
            p2 = np.array([np.cos(theta6), np.sin(theta6)])
            p3 = np.array([np.cos(theta7), np.sin(theta7)])
            p4 = np.array([np.cos(theta8), np.sin(theta8)])

            line1 = bezier_curve(np.vstack([p1, [0, 0], p3]))
            line2 = bezier_curve(np.vstack([p2, [0, 0], p4]))
            line3_theta = np.linspace(theta6, theta5, 100)
            line4_theta = np.linspace(theta7, theta8, 100)
            line3 = np.column_stack([np.cos(line3_theta), np.sin(line3_theta)])
            line4 = np.column_stack([np.cos(line4_theta), np.sin(line4_theta)])
            points = np.vstack([line1, line4, line2[::-1], line3])
            ax.add_patch(
                Polygon(
                    points,
                    closed=True,
                    facecolor=row_colors[i],
                    edgecolor="none",
                    alpha=0.4,
                    zorder=1,
                )
            )

    for theta, rotation, name in zip(row_mid, row_rot, row_names, strict=True):
        ax.text(
            np.cos(theta) * label_radius,
            np.sin(theta) * label_radius,
            name,
            fontsize=14,
            fontname="Arial",
            fontweight="bold",
            color="white",
            ha="center",
            va="center",
            rotation=rotation,
            rotation_mode="anchor",
            zorder=4,
        )

    for theta, rotation, name in zip(col_mid, col_rot, col_names, strict=True):
        ax.text(
            np.cos(theta) * label_radius,
            np.sin(theta) * label_radius,
            name,
            fontsize=14,
            fontname="Arial",
            fontweight="bold",
            color="white",
            ha="center",
            va="center",
            rotation=rotation,
            rotation_mode="anchor",
            zorder=4,
        )


def main() -> None:
    mpl.rcParams["axes.unicode_minus"] = False
    mpl.rcParams["font.family"] = ["Times New Roman", "Arial", "DejaVu Sans"]
    mpl.rcParams["font.weight"] = "bold"
    mpl.rcParams["axes.labelweight"] = "bold"

    set_df = pd.read_csv(ROOT / "data.csv")
    adj_df = pd.read_csv(ROOT / "adjMat.csv")

    fig = plt.figure(figsize=(22.93, 12.14), dpi=100, facecolor="white")
    draw_upset(fig, calc_upset(set_df), set_df.columns.tolist())
    draw_chord(fig, adj_df, [0.07, 0.47, 0.295, 0.52])

    fig.savefig(ROOT / "result.png", dpi=100, facecolor="white")
    plt.close(fig)


if __name__ == "__main__":
    main()
