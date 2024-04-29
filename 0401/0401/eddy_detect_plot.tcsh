#! /bin/tcsh

set cenv        = pet
# set dirin       = /Users/shiruijia/Downloads/AVISOvDT2021/
set dirin       = /Volumes/U/AVISOvDT2021/
# set dirout      = /Users/shiruijia/Downloads/eddy_output/
set dirout      = /Volumes/U/eddy_output/
set pattern     = XXXXXXXX
set filepattern = dt_global_twosat_phy_l4_${pattern}_vDT2021.nc
set fmt         = %Y%m%d
set vname       = sla # sla/adt
set d1          = 19930101
set d2          = 20221231
set tile        = t001
set do_save_nc  = 1 # 1==yes
set do_plot_fig = 0 # 1==yes
set x_name      = longitude
set y_name      = latitude
set wavelength  = 800 # km, cut-off wavelength used in the bessel high filter
set radius_MIN  = 50 # km, minimum effective radius required
set amp_MIN     = 0.04 # m, minimum applitude required

######################################################################################
conda activate $cenv # activate the virtual environment where you have py-eddy-tracking

python3 prog.eddy_detect_plot.py $dirin $dirout $filepattern $fmt $vname $d1 $d2 $tile $do_save_nc $do_plot_fig $x_name $y_name $pattern $wavelength $radius_MIN $amp_MIN
######################################################################################
