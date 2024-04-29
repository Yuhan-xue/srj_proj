#!/bin/bash

# 检查是否提供了两个参数
if [ "$#" -ne 2 ]; then
    echo "Usage: $0 arg1 arg2"
    exit 1
fi

# conda init
# 执行 cdo 命令
~/miniconda3/bin/cdo -s -b 32 -f nc copy -sellonlatbox,70,100,-5,23 $1 $2