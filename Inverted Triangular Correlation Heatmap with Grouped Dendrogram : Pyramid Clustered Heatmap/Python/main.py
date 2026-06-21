"""
图表：带分组树状图的倒三角相关性热图 / 分类金字塔聚类热图
依赖：matplotlib, numpy, pandas, scipy
数据输入：data.csv，首列为变量名，后续列为同名变量的方阵相关系数矩阵
"""

from __future__ import annotations

import math
from dataclasses import dataclass
from pathlib import Path

import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib.collections import PatchCollection
from matplotlib.colors import ListedColormap, Normalize
from matplotlib.patches import Polygon
from scipy.cluster.hierarchy import dendrogram, fcluster, linkage


DF_COLOR_2 = np.array([
    [0.6196, 0.0039, 0.2588], [0.6892, 0.0811, 0.2753],
    [0.7588, 0.1583, 0.2917], [0.8283, 0.2354, 0.3082],
    [0.8706, 0.2966, 0.2961], [0.9098, 0.3561, 0.2810],
    [0.9490, 0.4156, 0.2658], [0.9660, 0.4932, 0.2931],
    [0.9774, 0.5755, 0.3311], [0.9887, 0.6577, 0.3690],
    [0.9930, 0.7266, 0.4176], [0.9943, 0.7899, 0.4707],
    [0.9956, 0.8531, 0.5238], [0.9968, 0.9020, 0.5846],
    [0.9981, 0.9412, 0.6503], [0.9994, 0.9804, 0.7161],
    [0.9842, 0.9937, 0.7244], [0.9526, 0.9810, 0.6750],
    [0.9209, 0.9684, 0.6257], [0.8721, 0.9486, 0.6022],
    [0.7975, 0.9183, 0.6173], [0.7228, 0.8879, 0.6325],
    [0.6444, 0.8564, 0.6435], [0.5571, 0.8223, 0.6448],
    [0.4698, 0.7881, 0.6460], [0.3868, 0.7461, 0.6531],
    [0.3211, 0.6727, 0.6835], [0.2553, 0.5994, 0.7139],
    [0.2016, 0.5261, 0.7378], [0.2573, 0.4540, 0.7036],
    [0.3130, 0.3819, 0.6694], [0.3686, 0.3098, 0.6353],
])

CLUSTER_COLORS = np.array([
    [0.1490, 0.4039, 0.4980],
    [0.3882, 0.3608, 0.4471],
    [0.5373, 0.2157, 0.3098],
    [0.7686, 0.4353, 0.2431],
])

DEMO1_TERMINAL_COLORS = np.array([
    [0x3B / 255, 0x76 / 255, 0x8B / 255],
    [0x72 / 255, 0x6C / 255, 0x80 / 255],
    [0x93 / 255, 0x4B / 255, 0x60 / 255],
])


@dataclass
class TreeResult:
    z: np.ndarray
    order: np.ndarray
    classes: np.ndarray
    class_values: list[int]
    wticks: np.ndarray


def configure_matplotlib() -> None:
    mpl.rcParams.update({
        "font.family": "serif",
        "font.serif": ["Times New Roman", "Times", "DejaVu Serif"],
        "axes.unicode_minus": False,
        "savefig.facecolor": "white",
        "figure.facecolor": "white",
    })


def load_matrix_csv(path: str | Path) -> tuple[np.ndarray, list[str]]:
    frame = pd.read_csv(path, index_col=0)
    return frame.to_numpy(dtype=float), list(frame.columns)


def corr_linkage(data: np.ndarray) -> np.ndarray:
    return linkage(data, method="average", metric="euclidean")


def scale_values(values: np.ndarray, original: tuple[float, float], target: tuple[float, float]) -> np.ndarray:
    lo, hi = original
    tlo, thi = target
    return (values - lo) / (hi - lo) * (thi - tlo) + tlo


def rotate_xy(x: np.ndarray, y: np.ndarray, angle: float) -> tuple[np.ndarray, np.ndarray]:
    ca = math.cos(angle)
    sa = math.sin(angle)
    return ca * x - sa * y, sa * x + ca * y


def unique_stable(values: np.ndarray) -> list[int]:
    seen: list[int] = []
    for value in values:
        ivalue = int(value)
        if ivalue not in seen:
            seen.append(ivalue)
    return seen


def label_anchor_kwargs(rotation: float) -> dict[str, str]:
    if abs(rotation) < 1e-9:
        return {"va": "center"}
    return {"va": "center_baseline", "rotation_mode": "anchor"}


def build_tree(
    data: np.ndarray,
    max_clusters: int,
    *,
    optimal_ordering: bool = False,
) -> TreeResult:
    z = linkage(data, method="average", metric="euclidean", optimal_ordering=optimal_ordering)
    den = dendrogram(z, no_plot=True)
    order = np.array(den["leaves"], dtype=int)
    classes = fcluster(z, max_clusters, criterion="maxclust")[order]
    return TreeResult(z=z, order=order, classes=classes, class_values=unique_stable(classes), wticks=np.arange(1, len(order) + 1, dtype=float))


def _tree_segments(tree: TreeResult) -> tuple[list[np.ndarray], list[np.ndarray], np.ndarray, float]:
    den = dendrogram(tree.z, no_plot=True)
    w_segments = [np.asarray(xs, dtype=float) / 10.0 + 0.5 for xs in den["icoord"]]
    h_segments = [np.asarray(ys, dtype=float) for ys in den["dcoord"]]
    max_h = max(float(np.max(h)) for h in h_segments)
    cutoff = 0.0
    n_clusters = len(tree.class_values)
    if n_clusters > 1:
        cutoff = float(np.median([tree.z[-(n_clusters - 1), 2], tree.z[-n_clusters, 2]]))
    else:
        cutoff = max_h * 0.5
    return w_segments, h_segments, np.array(den["leaves"], dtype=int), cutoff


def _apply_class_gap_to_positions(values: np.ndarray, classes: np.ndarray) -> np.ndarray:
    out = values.copy()
    gaps = np.where(np.diff(classes) != 0)[0] + 1.5
    for gap in gaps[::-1]:
        out[out > gap] += 1
    return out


def _class_for_segment(w: np.ndarray, h: np.ndarray, classes: np.ndarray, cutoff: float) -> int | None:
    if not np.all(h < cutoff):
        return None
    center = int(np.clip(round(float((w[1] + w[2]) / 2.0)), 1, len(classes))) - 1
    return int(classes[center])


def _branch_highlight_heights(
    w_segments: list[np.ndarray],
    h_segments: list[np.ndarray],
    classes: np.ndarray,
    cutoff: float,
    class_values: list[int],
    fallback: float,
) -> dict[int, float]:
    heights: dict[int, float] = {}
    for w, h in zip(w_segments, h_segments):
        w_pairs = [(w[0], w[1]), (w[2], w[3])]
        h_pairs = [(h[0], h[1]), (h[2], h[3])]
        for (w0, _), (h0, h1) in zip(w_pairs, h_pairs):
            if (h0 - cutoff) * (h1 - cutoff) < 0:
                idx = int(np.clip(round(float(w0)), 1, len(classes))) - 1
                cls = int(classes[idx])
                heights[cls] = float((h0 + h1) / 2.0)
    return {cls: heights.get(cls, fallback) for cls in class_values}


def draw_tree(
    ax: plt.Axes,
    tree: TreeResult,
    *,
    orientation: str,
    xlim: tuple[float, float],
    ylim: tuple[float, float],
    angle: float = 0.0,
    clust_gap: bool = False,
    branch_color: bool = False,
    branch_highlight: bool = False,
    class_highlight: bool = False,
    colors: np.ndarray = CLUSTER_COLORS,
    terminal_colors: np.ndarray | None = None,
    class_highlight_span: tuple[float, float] = (0.20, 0.31),
    lw: float = 0.8,
) -> None:
    w_segments, h_segments, _, cutoff = _tree_segments(tree)
    class_values = tree.class_values
    max_h = max(float(np.max(h)) for h in h_segments)
    wticks = np.arange(1, len(tree.classes) + 1, dtype=float)

    if clust_gap:
        wticks = _apply_class_gap_to_positions(wticks, tree.classes)
        w_segments = [_apply_class_gap_to_positions(w.copy(), tree.classes) for w in w_segments]

    def orient(w: np.ndarray, h: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
        if orientation == "left":
            return max_h - h, w
        if orientation == "bottom":
            return w, -h
        return w, h

    oriented = [orient(w, h) for w, h in zip(w_segments, h_segments)]
    all_x = np.concatenate([xy[0] for xy in oriented])
    all_y = np.concatenate([xy[1] for xy in oriented])
    gap = 1.0 if clust_gap else 0.5
    if orientation in {"top", "bottom"}:
        oxlim = (float(np.min(all_x)) - gap, float(np.max(all_x)) + gap)
        oylim = (float(np.min(all_y)), float(np.max(all_y)))
    else:
        oxlim = (float(np.min(all_x)), float(np.max(all_x)))
        oylim = (float(np.min(all_y)) - gap, float(np.max(all_y)) + gap)

    def transform(w: np.ndarray, h: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
        x, y = orient(w, h)
        x = scale_values(x, oxlim, xlim)
        y = scale_values(y, oylim, ylim)
        if angle:
            x, y = rotate_xy(x, y, angle)
        return x, y

    for w, h in zip(w_segments, h_segments):
        cls = _class_for_segment(w, h, tree.classes, cutoff)
        if branch_color and cls in class_values:
            color = colors[class_values.index(cls) % len(colors)]
            width = lw
        else:
            color = "black"
            width = 0.7
        xs, ys = transform(w, h)
        ax.plot(xs, ys, color=color, lw=width, solid_capstyle="butt", zorder=6)

    branch_heights = _branch_highlight_heights(
        w_segments,
        h_segments,
        tree.classes,
        cutoff,
        class_values,
        fallback=min(max_h, max(cutoff, max_h * 0.30)),
    )
    terminal_colors = colors if terminal_colors is None else terminal_colors

    if branch_highlight or class_highlight:
        for i, cls in enumerate(class_values):
            cls_positions = wticks[tree.classes == cls]
            if len(cls_positions) == 0:
                continue
            w1 = float(np.min(cls_positions) - 0.5)
            w2 = float(np.max(cls_positions) + 0.5)
            h_top = branch_heights[int(cls)]
            if branch_highlight:
                w = np.r_[np.linspace(w1, w2, 50), np.full(50, w2), np.linspace(w2, w1, 50), np.full(50, w1)]
                h = np.r_[np.full(50, h_top), np.linspace(h_top, 0, 50), np.zeros(50), np.linspace(0, h_top, 50)]
                xs, ys = transform(w, h)
                ax.fill(xs, ys, color=colors[i % len(colors)], alpha=0.25, edgecolor="none", zorder=1)
            if class_highlight:
                h_inner = -max_h * class_highlight_span[0]
                h_outer = -max_h * class_highlight_span[1]
                w = np.r_[np.linspace(w1, w2, 50), np.full(50, w2), np.linspace(w2, w1, 50), np.full(50, w1)]
                h = np.r_[np.full(50, h_inner), np.linspace(h_inner, h_outer, 50), np.full(50, h_outer), np.linspace(h_outer, h_inner, 50)]
                xs, ys = transform(w, h)
                ax.fill(xs, ys, color=terminal_colors[i % len(terminal_colors)], alpha=0.95, edgecolor="none", zorder=5)


def _matrix_positions(n: int, classes: np.ndarray | None, clust_gap: bool) -> np.ndarray:
    values = np.arange(1, n + 1, dtype=float)
    if clust_gap and classes is not None:
        values = _apply_class_gap_to_positions(values, classes)
    return values


def _square_boundary() -> tuple[np.ndarray, np.ndarray]:
    bx = np.r_[np.linspace(-1, 1, 30), np.ones(30), np.linspace(1, -1, 30), -np.ones(30)] * 0.5
    by = np.r_[-np.ones(30), np.linspace(-1, 1, 30), np.ones(30), np.linspace(1, -1, 30)] * 0.5
    return bx, by


def draw_matrix(
    ax: plt.Axes,
    data: np.ndarray,
    labels: list[str],
    *,
    row_order: np.ndarray | None = None,
    col_order: np.ndarray | None = None,
    row_classes: np.ndarray | None = None,
    col_classes: np.ndarray | None = None,
    xlim: tuple[float, float] = (0, 1),
    ylim: tuple[float, float] = (0, 1),
    angle: float = 0.0,
    clust_gap: bool = False,
    mask: str = "upper",
    diagonal_half: bool = False,
    top_labels: bool = False,
    bottom_labels: bool = False,
    right_labels: bool = False,
    bottom_label_mode: str = "auto",
    top_label_offset: float = 0.0,
    bottom_label_offset: float = 0.0,
    right_label_offset: float = 0.0,
    label_size: float = 15,
) -> mpl.cm.ScalarMappable:
    n = data.shape[0]
    row_order = np.arange(n) if row_order is None else np.asarray(row_order, dtype=int)
    col_order = np.arange(n) if col_order is None else np.asarray(col_order, dtype=int)
    if row_classes is None:
        row_classes = np.ones(n, dtype=int)
    if col_classes is None:
        col_classes = np.ones(n, dtype=int)

    ordered = data[np.ix_(row_order, col_order)]
    x_pos = _matrix_positions(n, col_classes, clust_gap)
    y_pos = _matrix_positions(n, row_classes, clust_gap)
    gap = 1.0 if clust_gap else 0.5
    oxlim = (1 - gap, float(np.max(x_pos)) + gap)
    oylim = (1 - gap, float(np.max(y_pos)) + gap)
    xticks = np.r_[x_pos[0] - 0.75, x_pos, x_pos[-1] + 0.75]
    y_pad = 0.5 if angle else 0.75
    yticks = np.r_[y_pos[0] - y_pad, y_pos, y_pos[-1] + y_pad]

    bx, by = _square_boundary()
    patches: list[Polygon] = []
    colors: list[float] = []

    for r in range(n):
        for c in range(n):
            if mask == "upper" and r < c:
                continue
            if mask == "lower_equal" and r >= c:
                continue
            if mask == "lower_strict" and r > c:
                continue

            x = x_pos[c] + bx
            y = y_pos[r] + by
            x = scale_values(x, oxlim, xlim)
            y = scale_values(y, oylim, ylim)
            if angle:
                x, y = rotate_xy(x, y, angle)
            if diagonal_half and r == c:
                keep = y <= 0
                x = x[keep]
                y = y[keep]
                if len(x) < 3:
                    continue
            patches.append(Polygon(np.column_stack([x, y]), closed=True))
            colors.append(float(ordered[r, c]))

    cmap = ListedColormap(DF_COLOR_2)
    norm = Normalize(vmin=-1, vmax=1)
    collection = PatchCollection(
        patches,
        cmap=cmap,
        norm=norm,
        edgecolor="white",
        linewidth=0.5,
        antialiased=True,
        zorder=3,
    )
    collection.set_array(np.asarray(colors))
    ax.add_collection(collection)

    x_tick_scaled = scale_values(xticks, oxlim, xlim)
    y_tick_scaled = scale_values(yticks, oylim, ylim)
    xb, yb = rotate_xy(x_tick_scaled[1:-1], np.full(n, y_tick_scaled[0]), angle) if angle else (x_tick_scaled[1:-1], np.full(n, y_tick_scaled[0]))
    xt, yt = rotate_xy(x_tick_scaled[1:-1], np.full(n, y_tick_scaled[-1]), angle) if angle else (x_tick_scaled[1:-1], np.full(n, y_tick_scaled[-1]))
    xr, yr = rotate_xy(np.full(n, x_tick_scaled[-1]), y_tick_scaled[1:-1], angle) if angle else (np.full(n, x_tick_scaled[-1]), y_tick_scaled[1:-1])

    col_names = [labels[i] for i in col_order]
    row_names = [labels[i] for i in row_order]
    if top_labels:
        if top_label_offset:
            if angle:
                dx, dy = rotate_xy(np.zeros_like(xt), np.full_like(yt, top_label_offset), angle)
                xt = xt + dx
                yt = yt + dy
            else:
                yt = yt + top_label_offset
        for x, y, text in zip(xt, yt, col_names):
            ax.text(x, y, text, fontsize=label_size, rotation=45, ha="left", zorder=10, **label_anchor_kwargs(45))
    if bottom_labels:
        if bottom_label_mode == "flat":
            xb = xb * 2.0
            yb = np.full_like(yb, -0.09)
            rotation = 45
        elif bottom_label_mode == "zigzag_edge":
            step = math.sqrt(2) / n
            xb = (np.arange(n, dtype=float) + 0.25) * step
            yb = np.full(n, -0.25 * step)
            rotation = 45
        else:
            rotation = 45 if angle else 45
        if bottom_label_offset:
            if bottom_label_mode == "zigzag_edge":
                xb = xb - bottom_label_offset / math.sqrt(2)
                yb = yb - bottom_label_offset / math.sqrt(2)
            elif angle:
                dx, dy = rotate_xy(np.zeros_like(xb), np.full_like(yb, -bottom_label_offset), angle)
                xb = xb + dx
                yb = yb + dy
            else:
                yb = yb - bottom_label_offset
        for x, y, text in zip(xb, yb, col_names):
            ax.text(x, y, text, fontsize=label_size, rotation=rotation, ha="right", zorder=10, **label_anchor_kwargs(rotation))
    if right_labels:
        rotation = -45 if angle else 0
        if right_label_offset:
            if angle:
                dx, dy = rotate_xy(np.full_like(xr, right_label_offset), np.zeros_like(yr), angle)
                xr = xr + dx
                yr = yr + dy
            else:
                xr = xr + right_label_offset
        for x, y, text in zip(xr, yr, row_names):
            ax.text(x, y, text, fontsize=label_size, rotation=rotation, ha="left", zorder=10, **label_anchor_kwargs(rotation))

    return mpl.cm.ScalarMappable(norm=norm, cmap=cmap)


def add_colorbar(
    fig: plt.Figure,
    mappable: mpl.cm.ScalarMappable,
    *,
    orientation: str,
    rect: tuple[float, float, float, float],
    tick_size: float = 17,
    ticks: list[float] | None = None,
    tick_length: float = 7,
    keep_endpoint_labels_inside: bool = False,
) -> None:
    cax = fig.add_axes(rect)
    if ticks is None:
        ticks = [-1, -0.8, -0.6, -0.4, -0.2, 0, 0.2, 0.4, 0.6, 0.8, 1]
    cb = fig.colorbar(mappable, cax=cax, orientation=orientation, ticks=ticks)
    cb.ax.tick_params(labelsize=tick_size, width=0.8, length=tick_length, direction="in")
    cb.outline.set_linewidth(0.8)
    cb.ax.set_yticklabels([f"{t:g}" for t in cb.get_ticks()]) if orientation == "vertical" else cb.ax.set_xticklabels([f"{t:g}" for t in cb.get_ticks()])
    if keep_endpoint_labels_inside and orientation == "horizontal":
        labels = cb.ax.get_xticklabels()
        if labels:
            labels[0].set_ha("left")
            labels[-1].set_ha("right")


def finish_axes(ax: plt.Axes, xlim: tuple[float, float], ylim: tuple[float, float]) -> None:
    ax.set_xlim(*xlim)
    ax.set_ylim(*ylim)
    ax.set_aspect("equal", adjustable="box")
    ax.axis("off")


def render_demo0(data: np.ndarray, labels: list[str], output: str | Path) -> None:
    configure_matplotlib()
    fig = plt.figure(figsize=(12.70, 8.44), dpi=100)
    ax = fig.add_axes([0.01, 0.17, 0.98, 0.82])
    sm = draw_matrix(
        ax,
        data,
        labels,
        angle=-math.pi / 4,
        mask="upper",
        top_labels=True,
        top_label_offset=0.030,
        label_size=19,
    )
    finish_axes(ax, (0, 1.45), (-0.05, 0.78))
    add_colorbar(fig, sm, orientation="horizontal", rect=(0.012, 0.045, 0.976, 0.040), tick_size=18)
    fig.savefig(output, dpi=100)
    plt.close(fig)


def render_demo1(data: np.ndarray, labels: list[str], output: str | Path) -> None:
    configure_matplotlib()
    tree = build_tree(data, 3)
    fig = plt.figure(figsize=(12.61, 7.78), dpi=100)
    ax = fig.add_axes([0.01, 0.14, 0.98, 0.85])
    draw_tree(
        ax,
        tree,
        orientation="left",
        xlim=(-0.25, -0.05),
        ylim=(0, 1),
        angle=-math.pi / 4,
        clust_gap=True,
        branch_color=True,
        branch_highlight=True,
        class_highlight=True,
        colors=CLUSTER_COLORS,
        terminal_colors=DEMO1_TERMINAL_COLORS,
        class_highlight_span=(0.00, 0.16),
    )
    sm = draw_matrix(
        ax,
        data,
        labels,
        row_order=tree.order,
        col_order=tree.order,
        row_classes=tree.classes,
        col_classes=tree.classes,
        angle=-math.pi / 4,
        clust_gap=True,
        mask="upper",
        top_labels=True,
        top_label_offset=0.030,
        label_size=19,
    )
    finish_axes(ax, (-0.15, 1.45), (-0.05, 0.84))
    add_colorbar(fig, sm, orientation="horizontal", rect=(0.012, 0.045, 0.976, 0.043), tick_size=17)
    fig.savefig(output, dpi=100)
    plt.close(fig)


def render_demo2(data: np.ndarray, labels: list[str], output: str | Path) -> None:
    configure_matplotlib()
    tree = build_tree(data, 3)
    row_labels = labels.copy()
    col_labels = labels.copy()
    col_labels[tree.order[0]] = ""
    row_labels[tree.order[-1]] = ""
    fig = plt.figure(figsize=(10.00, 11.06), dpi=100)
    ax = fig.add_axes([0.010, 0.110, 0.940, 0.890])
    draw_tree(
        ax,
        tree,
        orientation="left",
        xlim=(-0.25, 0),
        ylim=(0, math.sqrt(2)),
        angle=-math.pi / 4,
        branch_color=False,
        branch_highlight=False,
        colors=CLUSTER_COLORS,
        lw=0.9,
    )
    sm = draw_matrix(
        ax,
        data,
        labels,
        row_order=tree.order,
        col_order=tree.order,
        xlim=(0, 1),
        ylim=(0, 1),
        angle=0,
        mask="lower_equal",
        bottom_labels=True,
        right_labels=True,
        label_size=19,
    )
    # Replace labels drawn from original order with the Matlab-style blanks.
    for text in ax.texts[-2 * len(labels):]:
        text.remove()
    ordered_cols = [col_labels[i] for i in tree.order]
    ordered_rows = [row_labels[i] for i in tree.order]
    n = len(labels)
    x_pos = np.arange(1, n + 1, dtype=float)
    oxlim = (0.5, n + 0.5)
    scaled = scale_values(x_pos, oxlim, (0, 1))
    for x, text in zip(scaled, ordered_cols):
        ax.text(x, -0.035, text, fontsize=19, rotation=45, ha="right", zorder=10, **label_anchor_kwargs(45))
    for y, text in zip(scale_values(x_pos, oxlim, (0, 1)), ordered_rows):
        ax.text(1.015, y, text, fontsize=19, rotation=0, ha="left", va="center", zorder=10)
    finish_axes(ax, (-0.12, 1.14), (-0.08, 1.10))
    fig.canvas.draw()
    cbar_left = fig.transFigure.inverted().transform(ax.transData.transform((1 / n, 0)))[0]
    cbar_right = fig.transFigure.inverted().transform(ax.transData.transform((1.0, 0)))[0]
    add_colorbar(
        fig,
        sm,
        orientation="horizontal",
        rect=(cbar_left, 0.033, cbar_right - cbar_left, 0.030),
        tick_size=18,
        keep_endpoint_labels_inside=True,
    )
    fig.savefig(output, dpi=100)
    plt.close(fig)


def render_demo3(data: np.ndarray, labels: list[str], output: str | Path) -> None:
    configure_matplotlib()
    tree = build_tree(data, 2)
    fig = plt.figure(figsize=(12.61, 8.07), dpi=100)
    ax = fig.add_axes([0.01, 0.13, 0.98, 0.86])
    sm = draw_matrix(
        ax,
        data,
        labels,
        row_order=tree.order,
        col_order=tree.order,
        row_classes=tree.classes,
        col_classes=tree.classes,
        angle=-math.pi / 4,
        mask="upper",
        bottom_labels=True,
        bottom_label_mode="zigzag_edge",
        bottom_label_offset=0.035,
        label_size=18,
    )
    num_n = len(tree.classes)
    num_a = int(np.sum(tree.classes == tree.classes[0]))
    num_b = int(np.sum(tree.classes == tree.classes[-1]))
    rt2 = math.sqrt(2)
    ax.plot(np.array([0, rt2 / 2, rt2]) * num_a / num_n, np.array([0, rt2 / 2, 0]) * num_a / num_n, color="black", lw=5.5, zorder=11)
    ax.plot(rt2 - np.array([0, rt2 / 2, rt2]) * num_b / num_n, np.array([0, rt2 / 2, 0]) * num_b / num_n, color="black", lw=5.5, zorder=11)
    xx = np.linspace(0, rt2, 2 * num_n + 1)
    yy = -rt2 / num_n / 2 * np.mod(np.arange(0, 2 * num_n + 1), 2)
    ax.plot(xx, yy, color="black", lw=5.5, zorder=11)
    ax.plot(np.array([0, rt2 / 2]) * num_a / num_n - 0.15 / num_n, np.array([0, rt2 / 2]) * num_a / num_n + 0.15 / num_n, color=(0.8, 0, 0), lw=8, zorder=12)
    ax.plot(rt2 - np.array([0, rt2 / 2]) * num_b / num_n + 0.15 / num_n, np.array([0, rt2 / 2]) * num_b / num_n + 0.15 / num_n, color=(0, 0, 0.8), lw=8, zorder=12)
    ax.text(rt2 / 4 * num_a / num_n - 0.50 / num_n, rt2 / 4 * num_a / num_n + 0.50 / num_n, "A", fontsize=50, ha="right", va="center", zorder=13)
    ax.text(rt2 - rt2 / 4 * num_b / num_n + 0.50 / num_n, rt2 / 4 * num_b / num_n + 0.50 / num_n, "B", fontsize=50, ha="left", va="center", zorder=13)
    finish_axes(ax, (-0.08, math.sqrt(2) + 0.02), (-0.15, 0.73))
    add_colorbar(fig, sm, orientation="horizontal", rect=(0.012, 0.046, 0.976, 0.040), tick_size=17)
    fig.savefig(output, dpi=100)
    plt.close(fig)


def render_demo4(data: np.ndarray, labels: list[str], output: str | Path) -> None:
    configure_matplotlib()
    tree = build_tree(data, 4)
    fig = plt.figure(figsize=(12.33, 8.00), dpi=100)
    ax = fig.add_axes([0.03, 0.02, 0.90, 0.975])
    draw_tree(
        ax,
        tree,
        orientation="top",
        xlim=(0, math.sqrt(2)),
        ylim=(0, 0.25),
        angle=0,
        branch_color=True,
        branch_highlight=True,
        colors=CLUSTER_COLORS,
    )
    sm = draw_matrix(
        ax,
        data,
        labels,
        row_order=tree.order,
        col_order=tree.order,
        row_classes=tree.classes,
        col_classes=tree.classes,
        angle=-math.pi / 4,
        mask="lower_strict",
        diagonal_half=True,
        bottom_labels=True,
        right_labels=True,
        bottom_label_offset=0.026,
        right_label_offset=0.026,
        label_size=18,
    )
    finish_axes(ax, (-0.15, 1.50), (-1.45 / 2, 0.26))
    add_colorbar(fig, sm, orientation="vertical", rect=(0.925, 0.075, 0.027, 0.32), tick_size=18, ticks=[-1, -0.5, 0, 0.5, 1], tick_length=4)
    fig.savefig(output, dpi=100)
    plt.close(fig)


def main() -> None:
    here = Path(__file__).resolve().parent
    data, labels = load_matrix_csv(here / "data.csv")
    render_demo1(data, labels, here / "result.png")


if __name__ == "__main__":
    main()
