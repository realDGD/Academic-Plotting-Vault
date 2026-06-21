"""
图表：桑基图与堆叠柱状图组合图 / 流向与组分占比联动图
依赖：matplotlib, numpy, pandas, scipy
数据输入：data.csv 包含 Source/Target/Value；data2.csv 包含 Pairings 与 S/SP/W/WP 列
"""

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib.path import Path as MplPath
from matplotlib.patches import PathPatch, Rectangle
from scipy.interpolate import PchipInterpolator


BASE_DIR = Path(__file__).resolve().parent


C_LIST = np.array(
    [
        [86, 112, 156],
        [151, 181, 138],
        [227, 206, 139],
        [216, 139, 131],
        [204, 204, 204],
        [172, 41, 52],
        [224, 189, 133],
        [106, 188, 161],
        [79, 145, 187],
        [180, 98, 96],
        [226, 210, 151],
        [128, 158, 173],
        [75, 106, 150],
        [192, 198, 132],
        [224, 190, 133],
        [171, 213, 165],
        [205, 193, 174],
        [110, 187, 161],
        [82, 146, 186],
        [192, 198, 130],
        [156, 189, 141],
        [179, 179, 181],
        [223, 153, 124],
        [182, 167, 131],
    ],
    dtype=float,
) / 255.0


def unique_stable(values):
    seen = set()
    result = []
    for value in values:
        if value not in seen:
            seen.add(value)
            result.append(value)
    return result


def build_adjacency(data, node_list):
    node_to_idx = {node: idx for idx, node in enumerate(node_list)}
    adj = np.zeros((len(node_list), len(node_list)), dtype=float)
    for row in data.itertuples(index=False):
        adj[node_to_idx[row.Source], node_to_idx[row.Target]] = float(row.Value)
    return adj, node_to_idx


def infer_layers(adj):
    bool_mat = np.abs(adj) > 0
    node_count = adj.shape[0]
    layers = np.zeros(node_count, dtype=int)
    layers[bool_mat.sum(axis=0) == 0] = 1
    start_mat = np.diag(layers)

    reach = bool_mat.astype(int)
    for step in range(1, node_count):
        layer_candidates = (start_mat @ reach).sum(axis=0) > 0
        layers = np.maximum(layers, layer_candidates.astype(int) * (step + 1))
        reach = reach @ bool_mat
    return layers


def compute_layer_positions(adj, layers, sep=0.2, block_scale=0.05):
    total_len = np.maximum(adj.sum(axis=0), adj.sum(axis=1))
    if np.any(total_len == 0):
        total_len[total_len == 0] = total_len.mean() / 2
    sep_len = total_len.max() * sep

    layer_pos = np.zeros((len(layers), 4), dtype=float)
    for layer in range(1, layers.max() + 1):
        block_indices = np.flatnonzero(layers == layer)
        block_len = np.concatenate([[0.0], np.cumsum(total_len[block_indices])])
        offsets = np.arange(len(block_indices)) * sep_len
        layer_pos[block_indices, 2] = block_len[:-1] + offsets
        layer_pos[block_indices, 3] = block_len[1:] + offsets

    layer_pos[:, 0] = layers
    layer_pos[:, 1] = layers + block_scale
    return layer_pos, total_len, sep_len


def pchip_link_path(source_box, target_box, source_span, target_span, samples=220):
    x_points = np.array([source_box[0], source_box[1], target_box[0], target_box[1]])
    x_curve = np.linspace(source_box[0], target_box[1], samples)

    y1_points = np.array([source_span[0], source_span[0], target_span[0], target_span[0]])
    y2_points = np.array([source_span[1], source_span[1], target_span[1], target_span[1]])
    y_lower = PchipInterpolator(x_points, y1_points)(x_curve)
    y_upper = PchipInterpolator(x_points, y2_points)(x_curve)

    vertices = np.column_stack([x_curve, y_lower]).tolist()
    vertices.extend(np.column_stack([x_curve[::-1], y_upper[::-1]]).tolist())
    vertices.append(vertices[0])
    codes = [MplPath.MOVETO] + [MplPath.LINETO] * (len(vertices) - 2) + [MplPath.CLOSEPOLY]
    return MplPath(vertices, codes)


def draw_sankey(ax, data):
    node_list = unique_stable(data["Source"].tolist() + data["Target"].tolist())
    adj, node_to_idx = build_adjacency(data, node_list)
    layers = infer_layers(adj)
    layer_pos, _, _ = compute_layer_positions(adj, layers, sep=0.2, block_scale=0.05)
    colors = C_LIST.copy()
    if len(node_list) > len(colors):
        rng = np.random.default_rng(0)
        colors = np.vstack([colors, rng.random((len(node_list) - len(colors), 3)) * 0.7])

    source_idx, target_idx = np.where(adj.T != 0)
    link_pairs = list(zip(target_idx, source_idx))
    for source, target in link_pairs:
        source_box = layer_pos[source, [0, 1]]
        target_box = layer_pos[target, [0, 1]]
        source_top = layer_pos[source, 2] + adj[source, :target].sum()
        source_bottom = layer_pos[source, 2] + adj[source, : target + 1].sum()
        target_top = layer_pos[target, 2] + adj[:source, target].sum()
        target_bottom = layer_pos[target, 2] + adj[: source + 1, target].sum()

        path = pchip_link_path(
            source_box,
            target_box,
            (source_top, source_bottom),
            (target_top, target_bottom),
        )
        ax.add_patch(
            PathPatch(
                path,
                facecolor=colors[source],
                edgecolor="none",
                alpha=0.7,
                zorder=1,
            )
        )

    for idx, node in enumerate(node_list):
        x0, x1, y0, y1 = layer_pos[idx]
        ax.add_patch(
            Rectangle(
                (x0, y0),
                x1 - x0,
                y1 - y0,
                facecolor=colors[idx],
                edgecolor="none",
                zorder=3,
            )
        )
        if layers[idx] == 3:
            ax.text(
                x1,
                (y0 + y1) / 2,
                f" {node} ",
                ha="left",
                va="center",
                fontsize=15,
                fontname="Arial",
                zorder=4,
            )
        else:
            ax.text(
                x0,
                (y0 + y1) / 2,
                f" {node} ",
                ha="right",
                va="center",
                fontsize=15,
                fontname="Arial",
                zorder=4,
            )

    ax.set_xlim(layer_pos[:, 0].min(), layer_pos[:, 1].max())
    ax.set_ylim(layer_pos[:, 3].max(), layer_pos[:, 2].min())
    ax.axis("off")
    return node_list, colors, node_to_idx


def draw_stacked_bar(ax, bar_data, node_list, colors):
    bar_types = bar_data.columns[1:].tolist()
    pairings = bar_data["Pairings"].tolist()
    node_to_color = {node: colors[idx] for idx, node in enumerate(node_list)}

    x = np.arange(1, len(bar_types) + 1)
    bottoms = np.zeros(len(bar_types))
    for pairing in pairings:
        values = bar_data.loc[bar_data["Pairings"] == pairing, bar_types].iloc[0].to_numpy(float)
        ax.bar(
            x,
            values,
            bottom=bottoms,
            width=0.6,
            color=node_to_color.get(pairing, (0.7, 0.7, 0.7)),
            edgecolor="none",
            alpha=0.9,
            zorder=2,
        )
        bottoms += values

    ax.set_facecolor("none")
    ax.set_xlim(0, 5)
    ax.set_ylim(0, 90)
    ax.set_yticks([0, 30, 60, 90])
    ax.set_xticks(x)
    ax.set_xticklabels(bar_types, fontname="Arial", fontsize=15)
    ax.set_ylabel("Pairings", fontname="Arial", fontsize=15)

    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.spines["left"].set_linewidth(1.5)
    ax.spines["bottom"].set_linewidth(1.5)
    ax.tick_params(axis="both", width=1.5, length=5, direction="in", labelsize=15)
    ax.tick_params(axis="x", pad=10)
    for label in ax.get_yticklabels():
        label.set_fontname("Arial")


def main():
    data = pd.read_csv(BASE_DIR / "data.csv")
    bar_data = pd.read_csv(BASE_DIR / "data2.csv")

    fig = plt.figure(figsize=(12.91, 9.85), dpi=100)
    ax1 = fig.add_axes([0.2, 0.1, 0.6, 0.8])
    node_list, colors, _ = draw_sankey(ax1, data)

    ax2 = fig.add_axes([0.2, 0.1, 0.4, 0.38])
    draw_stacked_bar(ax2, bar_data, node_list, colors)

    fig.savefig(
        BASE_DIR / "result.png",
        dpi=118,
        facecolor="white",
        bbox_inches="tight",
        pad_inches=0.02,
    )
    plt.close(fig)


if __name__ == "__main__":
    main()
