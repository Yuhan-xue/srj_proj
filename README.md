# SRJ_Proj

## 项目描述

本项目是一个海洋涡流检测和跟踪系统，使用卫星海面高度异常（Sea Level Anomaly, SLA）数据来识别和分析海洋中的涡流（eddies）。项目基于PyEddyTracker库，处理全球卫星数据，检测反气旋涡流（Anticyclonic Eddies）和气旋涡流（Cyclonic Eddies），并生成可视化图表和统计分析。

### 主要功能
- **数据预处理**：使用CDO工具裁剪卫星数据到指定区域（70°E-100°E, -5°N-23°N）
- **涡流检测**：基于海面高度异常和高通滤波识别涡流
- **涡流跟踪**：跟踪涡流的时间演变和运动轨迹
- **可视化**：生成涡流分布图、统计直方图和时间序列图
- **数据输出**：保存涡流数据为NetCDF格式

### 数据流程
1. 输入全球卫星SLA数据（dt_global_twosat_phy_l4_*.nc）
2. 裁剪到研究区域
3. 应用高通滤波去除大尺度信号
4. 检测涡流（AC和CC）
5. 过滤满足半径和振幅阈值的涡流
6. 生成输出文件和图表
7. 跟踪涡流并进行统计分析

## 安装和依赖

### 系统要求
- Python 3.7+
- Linux/Windows (支持CDO工具)

### 依赖包
- py-eddy-tracker
- matplotlib
- cartopy
- numpy
- netCDF4
- numba

### 安装步骤
1. 克隆项目：
   ```bash
   git clone https://git.hxlab.tech/yuhanxue/srj_proj.git
   cd srj_proj
   ```

2. 安装Python依赖：
   ```bash
   pip install py-eddy-tracker matplotlib cartopy numpy netCDF4 numba
   ```

3. 安装CDO工具（用于数据预处理）：
   - Linux: `sudo apt install cdo`
   - Windows: 使用WSL或Miniconda安装

## 使用方法

### 数据准备
将原始卫星数据放置在 `Data/original/` 目录下。

### 运行涡流检测
使用 `0401/prog.eddy_detect_plot.py` 脚本：

```bash
python 0401/0401/prog.eddy_detect_plot.py \
  ./Data/original/ \          # 输入目录
  ./Data/output/ \            # 输出目录
  dt_global_twosat_phy_l4_{}.vDT2021.nc \  # 文件模式
  %Y%m%d \                    # 日期格式
  sla \                       # 变量名
  19930101 \                  # 起始日期
  19930131 \                  # 结束日期
  t001 \                      # 网格标识
  1 \                         # 保存NC文件 (1=是)
  1 \                         # 生成图表 (1=是)
  longitude \                  # X轴名称
  latitude \                   # Y轴名称
  {} \                        # 日期占位符
  400 \                       # 波长 (km)
  10 \                        # 最小半径 (km)
  0.01                        # 最小振幅 (m)
```

### 涡流跟踪和分析
运行 `main.ipynb` Jupyter Notebook：
1. 加载检测到的涡流数据
2. 执行涡流跟踪
3. 生成统计图表和可视化

## 输出文件结构
```
Data/output/
├── sla.AC.t001/          # 反气旋涡流数据
│   ├── AC.all.19930101.nc    # 所有检测到的AC涡流
│   └── AC.req.19930101.nc    # 满足阈值的AC涡流
├── sla.CC.t001/          # 气旋涡流数据
│   ├── CC.all.19930101.nc
│   └── CC.req.19930101.nc
└── sla.jpgs.t001/        # 可视化图表
    └── PET.sla.19930101.jpg
```

## 参数说明
- **波长 (wave_length)**: 高通滤波的截止波长，单位km
- **最小半径 (radius_MIN)**: 涡流最小半径阈值，单位km
- **最小振幅 (amplitude_MIN)**: 涡流最小振幅阈值，单位m
- **区域**: 70°E-100°E, -5°N-23°N (印度洋北部)

## 后期维护

### 数据更新
1. 下载新的卫星SLA数据
2. 放置在 `Data/original/` 目录
3. 更新脚本中的日期范围
4. 重新运行检测脚本

### 参数调整
根据研究需要调整涡流检测参数：
- 修改 `wave_length` 以改变滤波尺度
- 调整 `radius_MIN` 和 `amplitude_MIN` 阈值
- 更改研究区域坐标

### 代码维护
1. 定期更新依赖包版本
2. 测试新版本PyEddyTracker的兼容性
3. 优化性能和内存使用

### 常见问题
- **CDO命令失败**: 确保CDO已正确安装，路径正确
- **内存不足**: 对于大时间范围，考虑分批处理
- **坐标系统**: 确保输入数据的坐标系统与脚本匹配

### 贡献
欢迎提交问题报告和改进建议。请在提交PR前测试代码。

## 许可证
[请指定许可证]

## 联系
[请添加联系信息]