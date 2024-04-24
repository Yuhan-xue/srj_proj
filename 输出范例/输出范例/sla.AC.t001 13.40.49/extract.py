import netCDF4 as nc

# 打开 NetCDF 文件
nc_file = nc.Dataset('CC.all.19930101.nc', 'r')

# 获取所有变量的名称
variable_names = nc_file.variables.keys()

# 遍历每个变量并获取单位属性
for variable_name in variable_names:
    # 获取变量对象
    variable = nc_file.variables[variable_name]
    
    # 检查是否存在单位属性
    if 'units' in variable.ncattrs():
        # 获取变量的单位属性
        units = variable.units
        print("Variable:", variable_name)
        print("Units:", units)
    else:
        print("Variable:", variable_name)
        print("Units: No units attribute found")

# 关闭文件
nc_file.close()