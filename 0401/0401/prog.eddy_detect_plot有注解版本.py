#!/usr/bin/env python3
# -*- coding: utf-8 -*-


# 导入datetime模块，用于处理日期和时间
import datetime as dt  
 # 导入RegularGridDataset类，用于处理网格数据
from py_eddy_tracker.dataset.grid import RegularGridDataset 
# 导入pyplot模块，用于创建图形和绘制图表
from matplotlib import pyplot as plt  
# 导入numpy模块，用于处理数值数组
import numpy as np  
 # 导入os模块，用于处理操作系统
import os 
 # 导入sys模块，用于处理系统
import sys 
# 导入netCDF4模块，用于处理netCDF4文件
from netCDF4 import Dataset  
# 导入time模块，用于获取当前时间
from time import ctime 

# 获取命令行参数，
dirin = sys.argv[1] # 输入目录。这是包含输入文件的目录的路径。
dirout = sys.argv[2] #  输出目录。这是结果文件和图像将要保存的目录的路径。
filepattern = np.str(sys.argv[3]) # 文件模式。用于匹配输入文件的文件名模式，通常是一个字符串，可能包含通配符。
fmt = np.str(sys.argv[4]) # 日期格式。指定日期的格式，例如"YYYY-MM-DD"。
vname = sys.argv[5]  # 变量名称。指定要处理的变量的名称，可以是"sla"或"adt"。
d1 = sys.argv[6]  # 起始日期。指定处理的起始日期。
d2 = sys.argv[7]  # 结束日期。指定处理的结束日期。
tile = sys.argv[8]  # 网格切片。可能是用于切割数据的网格切片的标识。
do_save_nc = np.int32(sys.argv[9])  # 是否保存NetCDF文件。一个整数值，如果为1，则表示将结果保存为NetCDF文件。
do_plot_fig = np.int32(sys.argv[10])  # 是否绘制图像。一个整数值，如果为1，则表示生成图像。
x_name = sys.argv[11]  # X轴名称。指定数据中X轴的名称。
y_name = sys.argv[12]  # Y轴名称。指定数据中Y轴的名称。
fp = sys.argv[13]  # 文件模式的占位符。在文件模式中指定日期的占位符。
wave_length = np.float32(sys.argv[14])  # 波长。用于高通滤波的波长。
radius_MIN = np.float32(sys.argv[15])  # 最小半径。指定较小的环流的最小半径。
amplitude_MIN = np.float32(sys.argv[16])  # 最小振幅。指定较小的环流的最小振幅。

if vname == 'sla':
    v1n, v2n = 'ugosa', 'vgosa'
elif vname == 'adt':
    v1n, v2n = 'ugos', 'vgos'
else:
    raise ValueError('check vname !!!')
    
# 获取当前日期时间
dt_now = dt.datetime.now()
# 将当前日期时间格式化为字符串, 例如："2024-04-12T0758" 表示2024年4月12日 07点58分, 用T分隔开
dt_now_str = dt_now.strftime('%Y-%m-%dT%H%M')
# 将输入的日期1格式化为日期时间
date_Start = dt.datetime.strptime(d1, fmt)
# 将输入的日期2格式化为日期时间  
date_End = dt.datetime.strptime(d2, fmt)
# 生成一个日期列表
datelist = np.arange(date_Start, 
                     date_End+dt.timedelta(days=1),
                     dt.timedelta(days=1),
                     dtype=dt.datetime)
# 生成AC目录
dirAC = dirout+'{:}.AC.{:}'.format(vname, tile)
# 生成CC目录
dirCC = dirout+'{:}.CC.{:}'.format(vname, tile)
# 生成图片目录
dirfig = dirout+'{:}.jpgs.{:}'.format(vname, tile)
# 生成临时文件名
filetmp = dirout+'tmp.{:}.nc'
# 生成临时文件名
filetmp = filetmp.format(dt.datetime.now().strftime('%y%m%dT%H%M'))

# 打印一些日志，输出的

info = []
info.append('======= {:} ======='.format(ctime()))
info.append('{:16s}: {:}'.format('Input Dir',dirin))
info.append('{:16s}: {:}'.format('Output Dir', dirout))
info.append('{:16s}: {:}'.format('File Pattern', filepattern))
info.append('{:16s}: {:}'.format('Tile', tile))
info.append('{:16s}: {:}'.format('fmt', fmt))
info.append('{:16s}: {:}'.format('Variable', vname))
info.append('{:16s}: {:}'.format('X name', x_name))
info.append('{:16s}: {:}'.format('Y name', y_name))
info.append('{:16s}: from {:} to {:}'.format('Dates',
                                             date_Start.strftime(fmt),
                                             date_End.strftime(fmt)))
info.append('{:16s}: {:}'.format('Save NC', do_save_nc==1))
info.append('{:16s}: {:}'.format('Plot Figs', do_plot_fig==1))
info.append('{:16s}: {:}'.format('Tmp NC', filetmp))
info.append('{:16s}: {:}km'.format('Wave Length', wave_length))
info.append('{:16s}: {:}km'.format('Radius MIN', radius_MIN))
info.append('{:16s}: {:}m'.format('Amplitude MIN', amplitude_MIN))
for i in info:
    print(i)
    
while(True):
    print('!!! NOTE !!! Please confirm the above information.')
    in_content = input('Continue/Exit [Y/N]: ')
    if in_content == 'N':
        print('{:} Exit'.format(ctime()))
        exit(0)
    elif in_content == 'Y':
        if do_save_nc == 1:  # 如果需要保存数据
            jAC = os.path.exists(dirAC) # 检查目录是否存在
            if jAC:  # 如果目录存在
                print('!!! WARNING !!! {:} exists'.format(dirAC))  # 打印警告信息，目录已存在
                while(True):
                    dirAC_ic = input('Overwrite/Exit [Y/N]: ')  # 提示用户是否覆盖或退出
                    if dirAC_ic == 'N': # 如果用户选择不覆盖
                        print('{:} Exit'.format(ctime())) # 打印退出消息
                        exit(0) # 退出
                    elif dirAC_ic == 'Y':
                        os.system('rm -r {:}'.format(dirAC)) # 删除已存在的目录及其内容
                        os.system('mkdir {:}'.format(dirAC)) # 创建新目录
                        print('{:12s}: {:}'.format('Dir Re-Created', dirAC)) # 打印目录已重新创建的消息
                        break # 跳出循环
                    else: # 如果用户输入无效
                        print('Wrong input, Y/N only')
            else:  # 如果目录不存在
                os.system('mkdir {:}'.format(dirAC)) # 创建新目录
                print('{:12s}: {:}'.format('Dir Created', dirAC)) # 打印目录已创建的消息

             # 这段代码与上述的代码几乎完全相同，只是针对不同的目录进行了相同的操作。
            jCC = os.path.exists(dirCC)
            if jCC:
                print('!!! WARNING !!! {:} exists'.format(dirCC))
                while(True):
                    dirCC_ic = input('Overwrite/Exit [Y/N]: ')
                    if dirCC_ic == 'N':
                        print('{:} Exit'.format(ctime()))
                        exit(0)
                    elif dirCC_ic == 'Y':
                        os.system('rm -r {:}'.format(dirCC))
                        os.system('mkdir {:}'.format(dirCC))
                        print('{:12s}: {:}'.format('Dir Re-Created', dirCC))
                        break
                    else:
                        print('Wrong input, Y/N only')
            else:
                os.system('mkdir {:}'.format(dirCC))
                print('{:12s}: {:}'.format('Dir Created', dirCC))
            # ------------------------------------------------------------------------------------

        if do_plot_fig == 1: # 如果需要绘制图形
            jfg = os.path.exists(dirfig)  # 检查目录是否存在
            if jfg: # 如果目录存在
                print('!!! WARNING !!! {:} exists'.format(dirfig)) # 打印警告信息，目录已存在
                while(True): 
                    dirfig_ic = input('Overwrite/Exit [Y/N]: ') # 提示用户是否覆盖或退出
                    if dirfig_ic == 'N': # 如果用户选择不覆盖
                        print('{:} Exit'.format(ctime())) # 打印退出消息
                        exit(0) # 退出程序
                    elif dirfig_ic == 'Y': # 如果用户选择覆盖
                        os.system('rm -r {:}'.format(dirfig))  # 删除已存在的目录及其内容
                        os.system('mkdir {:}'.format(dirfig))  # 创建新目录
                        print('{:12s}: {:}'.format('Dir Re-Created', dirfig)) # 打印目录已重新创建的消息
                        break  # 跳出循环
                    else: # 如果用户输入无效
                        print('Wrong input, Y/N only')
            else:  # 如果目录不存在
                os.system('mkdir {:}'.format(dirfig))  # 创建新目录
                print('{:12s}: {:}'.format('Dir Created', dirfig))  # 打印目录已创建的消息
        break # 跳出循环
    else: 
        print('Wrong input, Y/N only')

fw = 190
nlef, nrig = 10, 15
ntop, nbot = 10, 5
nha = (fw - nlef*2 - nrig)/2
nva = nha * 28 / 30
fh = nbot + ntop + nva
ha, va = nha/fw, nva/fh
xloc = [nlef/fw, (nlef*2+nha)/fw]
cloc = [(fw-nrig+2)/fw, nbot/fh, 2/fw, va]

# 定义一个函数plotax1，用于在二维图中绘制等值线，并显示矢量场
# 参数ax：子图的坐标轴
# 参数h：数据对象
# 参数xlim：x轴的范围
# 参数ylim：y轴的范围
# 参数vmin：矢量场的最小值
# 参数vmax：矢量场的最大值
# 参数var：要显示的变量
# 参数uname：u轴的变量名
# 参数vname：v轴的变量名
# 参数title：图标题
# 参数cmap：图的颜色映射
# 参数scale：矢量场的大小
# 参数sstep：显示矢量场的步长
def plotax1(ax, h,
            xlim=[70, 100],
            ylim=[-5, 23],
            vmin=-0.3, vmax=0.3,
            var='sla',
            uname='u',
            vname='v',
            title='date',
            cmap='coolwarm',
            scale=10,
            sstep=2):
    
    # 显示等值线
    im = h.display(ax, var, vmin=vmin, vmax=vmax, cmap=cmap)
    # 获取x轴和y轴的值
    u, v = h.grid(uname).T, h.grid(vname).T
    # 显示矢量场
    ax.quiver(h.x_c[::sstep], h.y_c[::sstep], 
              u[::sstep,::sstep], 
              v[::sstep,::sstep], 
              scale=scale, pivot='mid', color='gray')
    # 设置图标题
    ax.text(0.01, 1.02, title, transform=ax.transAxes)
    # 设置x轴和y轴的范围
    ax.set_xlim(xlim)
    ax.set_ylim(ylim)
    # 设置坐标轴标签的间距和长度
    ax.tick_params(axis='both',pad=0.5,length=2)

    return im

# 定义一个函数plotax2，用于绘制地图
def plotax2(ax, h, a, c,
            # 设置x轴和y轴的范围
            xlim=[70, 100],
            ylim=[-5, 23],
            # 设置颜色的最小值和最大值
            vmin=-0.3, vmax=0.3,
            # 设置要显示的变量
            var='sla',
            # 设置标题
            title='date',
            # 设置颜色方案
            cmap='coolwarm',
            # 设置是否显示圆圈
            show_circle=False):
    
    # 设置AC和CC的参数
    kwargs_a = dict(lw=0.5, 
                    label="AC ({nb_obs})", 
                    color="b")
    kwargs_c = dict(lw=0.5, 
                    label="CC ({nb_obs})", 
                    color="r")
    
    # 显示图像
    im = h.display(ax, var, vmin=vmin, vmax=vmax, cmap=cmap)
    if show_circle:
        # 显示圆圈
        a.circle_contour()
        c.circle_contour()
    # 显示AC和CC
    a.display(ax, **kwargs_a)
    c.display(ax, **kwargs_c)
    # 显示图例
    ax.legend(loc='upper left')
    ax.text(0.01, 1.02, title, transform=ax.transAxes)
    # 设置x轴和y轴的范围
    ax.set_xlim(xlim)
    ax.set_ylim(ylim)
    # 设置坐标轴的长度和标签
    ax.tick_params(axis='both',pad=0.5,length=2)

    return im

# 循环遍历日期列表
for date in datelist:
    # 将日期格式化为字符串
    datestr = date.strftime(fmt)
    # 打印正在处理的日期
    print('-- processing {:}'.format(datestr))
    # 构建输入文件路径
    filein = dirin+'{:}/{:}'.format(date.year,
                                    filepattern.replace(fp, datestr))
    # 构建临时输出文件路径                                
    filetmp = dirout+'tmp.{:}.nc'
    filetmp = filetmp.format(dt.datetime.now().strftime('%y%m%dT%H%M'))
    # 使用Cmd命令处理文件
    cmd = ('cdo -s -b 32 -f nc copy -sellonlatbox,70,100,-5,23 ' +
           '{:} '.format(filein) +
           '{:}'.format(filetmp))
    os.system(cmd)
    # 读取数据集
    h = RegularGridDataset(filetmp,
                           x_name,
                           y_name,
                           centered=True)
    
    # 复制变量vname，并将副本命名为vname_high
    h.copy(vname, vname+'_high')
    # 对vname_high进行贝塞尔高程过滤器
    h.bessel_high_filter(vname+'_high',
                         wave_length=wave_length,
                         order=1)
    # 识别eddy
    a, c = h.eddy_identification(vname+'_high', v1n, v2n, date,
                                  # step：步长，用于eddy识别
                                  step=0.002,
                                  # shape_error：形状误差，用于eddy识别
                                  shape_error=55)
    # 提取满足条件的a
    a_req = a.extract_with_mask(a.radius_e > radius_MIN)
    # 提取满足条件的a
    a_req = a_req.extract_with_mask(a_req.amplitude > amplitude_MIN)
    # 提取满足条件的c
    c_req = c.extract_with_mask(c.radius_e > radius_MIN)
    # 提取满足条件的c
    c_req = c_req.extract_with_mask(c_req.amplitude > amplitude_MIN)

    savename = '{:}/PET.{:}.{:}.jpg'.format(dirfig,
                                            vname,
                                            datestr)
    # do_plot_fig为1时，
    if do_plot_fig == 1:
        # 创建一个新的图，设置宽度和高度
        fig = plt.figure(figsize=(fw/25.4, fh/25.4))
        # 在图中添加一个新的轴，设置x轴的位置，y轴的位置，宽度和高度
        ax1 = fig.add_axes([xloc[0], nbot/fh, ha, va])
        # 调用plotax1函数，绘制第一个图表
        im = plotax1(ax1, h,
                     var=vname,
                     uname=v1n,
                     vname=v2n,
                     title=vname,
                     cmap='coolwarm')
        # 在图中添加一个新的轴，设置x轴的位置，y轴的位置，宽度和高度
        ax2 = fig.add_axes([xloc[1], nbot/fh, ha, va])
        # 调用plotax2函数，绘制第二个图表
        im = plotax2(ax2, h, a_req, c_req,
                     var=vname+'_high',
                     title=vname+'_high',
                     show_circle=True,
                     cmap='coolwarm')
        # 在第二个图表上添加日期，设置字体大小
        ax2.text(1, 1.02, datestr, ha='right', transform=ax2.transAxes,
                fontsize='x-large')
        # 添加颜色条
        cax = plt.axes(cloc)
        cbar = plt.colorbar(im, cax=cax,)
        # 设置颜色条的刻度
        cbar.ax.tick_params(direction='in')
        # 保存图片
        plt.savefig(savename, dpi=600)
        # 关闭图片
        plt.close()
    if do_save_nc == 1:
        # 创建一个新的NetCDF文件，将a的数据写入
 with Dataset('{:}/AC.all.{:}.nc'.format(dirAC, datestr), 'w') as nc:
            a.to_netcdf(nc)
 # 创建一个新的NetCDF文件，将a_req的数据写入
 with Dataset('{:}/AC.req.{:}.nc'.format(dirAC, datestr), 'w') as nc:
            a_req.to_netcdf(nc)
 # 创建一个新的NetCDF文件，将c的数据写入
 with Dataset('{:}/CC.all.{:}.nc'.format(dirCC, datestr), 'w') as nc:
            c.to_netcdf(nc)
 # 创建一个新的NetCDF文件，将c_req的数据写入
 with Dataset('{:}/CC.req.{:}.nc'.format(dirCC, datestr), 'w') as nc:
            c_req.to_netcdf(nc)
print('======= {:} DONE ======='.format(ctime()))
