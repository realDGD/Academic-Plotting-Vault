"""
图表：末端独立着色的双边弦图 / Multi-attribute Flow Chord Chart
依赖：pandas, numpy, matplotlib, pycirclize
数据输入：data.csv，包含 Source, Target, Value, Regulation 四列
"""
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.patches import Patch
from pycirclize import Circos

def main():
    # 1. 颜色配置 (Color mapping)
    CListT = {
        'Upregulated': (173/255, 70/255, 65/255),
        'Downregulated': (79/255, 135/255, 136/255)
    }

    CListF = {
        'Lung': (128/255, 108/255, 171/255),
        'Spleen': (222/255, 208/255, 161/255),
        'Liver': (180/255, 196/255, 229/255),
        'Heart': (209/255, 150/255, 146/255),
        'Renal cortex': (175/255, 201/255, 166/255),
        'Renal medulla': (134/255, 156/255, 118/255),
        'Thyroid': (175/255, 175/255, 173/255)
    }

    import os
    current_dir = os.path.dirname(os.path.abspath(__file__))
    data_path = os.path.join(current_dir, 'data.csv')
    df = pd.read_csv(data_path)

    colName = ['A2M', 'FGA', 'FGB', 'FGG', 'F11', 'KLKB1', 'SERPINE1', 'VWF',
               'THBD', 'TFPI', 'PLAT', 'SERPINA5', 'SERPIND1', 'F2', 'PLG', 'F12',
               'SERPINC1', 'SERPINA1', 'PROS1', 'SERPINF2', 'F13A1', 'PROC']
    rowName = ['Lung', 'Spleen', 'Liver', 'Heart',
               'Renal cortex', 'Renal medulla', 'Thyroid']

    # 3. 统计Sector大小 (Calculate sector sizes)
    temp_sectors = {}
    for t in colName:
        if t in df['Target'].values:
            temp_sectors[t] = df[df['Target'] == t]['Value'].sum()

    for s in rowName[::-1]: 
        if s in df['Source'].values:
            temp_sectors[s] = df[df['Source'] == s]['Value'].sum()

    # 插入两个空白分区 (GAP) 从而强制在左右两边断开，避免两端节点过近导致丝带畸形
    total_val = sum(temp_sectors.values())
    gap_size = total_val * 0.015  # 将留白的宽度改为 1.5% 的数据量
    
    sectors = {}
    for t in colName:
        if t in temp_sectors:
            sectors[t] = temp_sectors[t]
            
    sectors['GAP1'] = gap_size
    
    for s in rowName[::-1]:
        if s in temp_sectors:
            sectors[s] = temp_sectors[s]
            
    sectors['GAP2'] = gap_size

    # 4. 初始化 Circos 对象
    circos = Circos(sectors, space=1.5)

    # 5. 绘制源底色块和文本标签
    for s_name in sectors:
        if s_name.startswith('GAP'):
            continue
            
        sector = circos.get_sector(s_name)
        # 绘制外层方块
        track = sector.add_track((90, 100))
        if s_name in CListF:
            track.rect(0, sector.size, color=CListF[s_name])
        
        # 绘制旋转的文本标签
        sector.text(s_name, r=105, size=8, orientation="vertical")

    # 6. 计算最佳连线顺序以避免交叉 (缠绕)
    # Target 的角度从 0 (右) 到 180 (左)
    # Source 的角度从 180 (左) 到 360 (右)
    
    # 预计算每个 (s, t) 的起点和终点
    s_positions = {}
    t_positions = {}
    
    # 对于每个 Source，其内部坐标 0 是左边，size 是右边
    # 为了不交叉，应该优先把“靠左的 Target”分配到“靠左的坐标”
    # 靠左的 Target 是 colName 的反序 (PROC -> A2M)
    for s in rowName[::-1]: # 这里的 s 遍历没有特别要求，主要是为了把每个 s 里的 t 分配好
        current_s_ptr = 0
        for t in colName[::-1]:
            mask = (df['Source'] == s) & (df['Target'] == t)
            if mask.any():
                v = df[mask]['Value'].values[0]
                s_positions[(s, t)] = (current_s_ptr, current_s_ptr + v)
                current_s_ptr += v
                
    # 对于每个 Target，其内部坐标 0 是右边，size 是左边
    # 为了不交叉，应该优先把“靠右的 Source”分配到“靠右的坐标”
    # 靠右的 Source 是 rowName (Lung -> Thyroid)
    for t in colName:
        current_t_ptr = 0
        for s in rowName:
            mask = (df['Source'] == s) & (df['Target'] == t)
            if mask.any():
                v = df[mask]['Value'].values[0]
                t_positions[(s, t)] = (current_t_ptr, current_t_ptr + v)
                current_t_ptr += v

    # 7. 绘制弦和末端方块
    for _, row in df.iterrows():
        s = row['Source']
        t = row['Target']
        reg = row['Regulation']
        
        s_start, s_end = s_positions[(s, t)]
        t_start, t_end = t_positions[(s, t)]
        
        # 目标端的独立着色方块 (按上调/下调分类着色)
        track = circos.get_sector(t).add_track((90, 100))
        # 增加与填充色相同的描边 (ec=color, lw=0.5) 完美消除反锯齿白边缝隙
        track.rect(t_start, t_end, color=CListT[reg], ec=CListT[reg], lw=0.5)
        
        # 绘制半透明连接弦 (贝塞尔曲线带)
        # 完全不加任何 padding，让所有丝带在源节点和目标节点都严丝合缝
        circos.link(
            (s, s_start, s_end),
            (t, t_end, t_start),
            color=CListF.get(s, "grey"),
            alpha=0.45,
            r1=85, r2=85,
            direction=0
        )

    # 7. 绘制图例与保存
    fig = circos.plotfig()
    legend_elements = [
        Patch(facecolor=CListT['Upregulated'], edgecolor='none', label='Upregulated'),
        Patch(facecolor=CListT['Downregulated'], edgecolor='none', label='Downregulated')
    ]
    # 添加图例到右上角
    fig.legend(handles=legend_elements, loc='upper right', bbox_to_anchor=(0.95, 0.95), frameon=False, fontsize=10)

    result_path = os.path.join(current_dir, 'result.png')
    fig.savefig(result_path, dpi=300, bbox_inches='tight')
    print(f"Bipartite Chord Diagram successfully generated at {result_path}")

if __name__ == "__main__":
    main()
