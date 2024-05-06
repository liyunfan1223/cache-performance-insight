import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches

# 生成 x 值
x = np.linspace(0, 10, 100)

# 生成 y=1 和 y=(1/2)^x 的值
y1 = np.ones_like(x)
y2 = (1/2)**x
y3 = (1/2)**(0.45*x)
y4 = (1/2)**(0.22*x)
y5 = (1/2)**(0.08*x)
# 绘制图形
fig, ax = plt.subplots(dpi=150, figsize=(6 / 1.1, 2.5 * 3 / 2 / 1.1))
ax.plot(x, y1, label='$y=1$', color='black')
ax.plot(x, y2, label='$y=(1/2)^x$', color='black')
ax.plot(x, y3, '--',label='$y=(1/2)^(0.5*x)$', color='grey')
ax.plot(x, y4, '--',label='$y=(1/2)^(0.2*x)$', color='grey')
ax.plot(x, y5, '--',label='$y=(1/2)^(0.08*x)$', color='grey')
# 填充阴影区域
ax.fill_between(x, y1, y2, where=(y1 > y2), color='lightgrey', alpha=0.5, interpolate=True)

# 隐藏 x 轴刻度标签
ax.set_xticks([])

# 设置 y 轴刻度标签
ax.set_yticks([0, 1])

# 显示 x 和 y 轴标签
ax.set_xlabel('$x=t^{cur}-t_b^i$ (time since accessed)', fontsize=15)
ax.set_ylabel('$F(x)$', fontsize=15)

# 设置坐标轴范围和显示刻度
ax.set_xlim(0, 5)
ax.set_ylim(0, 1.2)
ax.set_yticks([0, 1])

# 显示图例
# ax.legend()

# 在曲线周围标注算式
ax.text(2, 1.05, '$F(x)=1$ ($\lambda=0$)', fontsize=15, ha='center', va='center')
ax.text(1.5, 0.15, r'$F(x)=(\frac{1}{2})^x$ ($\lambda=1$)', fontsize=15, ha='center', va='center')
ax.text(3.4, 0.42, r'$\lambda=0.5$', fontsize=15, ha='center', va='center')
ax.text(3.7, 0.63, r'$\lambda=0.2$', fontsize=15, ha='center', va='center')
ax.text(4.1, 0.85, r'$\lambda=0.08$', fontsize=15, ha='center', va='center')

# ax.text(2.9, 0.25, r'LRU Extreme', fontsize=15, ha='center', va='center')
# ax.text(4.1, 1.05, r'LFU Extreme', fontsize=15, ha='center', va='center')
plt.tight_layout()
# ax.text(2.8, 0.6, 'Spectrum\n(Recency/Frequency)', fontsize=17, ha='center', va='center')
plt.savefig('plots/D2.2/lrfu_para2.png')
plt.savefig('plots/D2.2/lrfu_para2.eps')
plt.savefig('plots/D2.2/lrfu_para2.svg')
# 显示图形
# plt.show()
