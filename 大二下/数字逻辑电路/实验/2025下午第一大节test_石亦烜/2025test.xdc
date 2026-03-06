#CLK input
set_property -dict {PACKAGE_PIN J19 IOSTANDARD LVCMOS33} [get_ports CLK];     #CLK接插孔

#RST input
set_property -dict {PACKAGE_PIN K18 IOSTANDARD LVCMOS33} [get_ports RST];     #IO0接插孔

# Code input
set_property -dict {PACKAGE_PIN M21 IOSTANDARD LVCMOS33} [get_ports num[7]];     #IO1接插孔
set_property -dict {PACKAGE_PIN N20 IOSTANDARD LVCMOS33} [get_ports num[6]];     #IO1接插孔
set_property -dict {PACKAGE_PIN N22 IOSTANDARD LVCMOS33} [get_ports num[5]];     #IO1接插孔
set_property -dict {PACKAGE_PIN P21 IOSTANDARD LVCMOS33} [get_ports num[4]];     #IO1接插孔
set_property -dict {PACKAGE_PIN P22 IOSTANDARD LVCMOS33} [get_ports num[3]];     #IO1接插孔
set_property -dict {PACKAGE_PIN T21 IOSTANDARD LVCMOS33} [get_ports num[2]];     #IO1接插孔
set_property -dict {PACKAGE_PIN U21 IOSTANDARD LVCMOS33} [get_ports num[1]];     #IO1接插孔
set_property -dict {PACKAGE_PIN R21 IOSTANDARD LVCMOS33} [get_ports num[0]];     #IO1接插孔

# Mode input
set_property -dict {PACKAGE_PIN W21 IOSTANDARD LVCMOS33} [get_ports mode];     #IO11接插孔

# Unlock output
set_property -dict {PACKAGE_PIN AA18 IOSTANDARD LVCMOS33} [get_ports led];     #IO16接插孔

# required if touch button used as manual clock source
set_property CLOCK_DEDICATED_ROUTE FALSE [get_nets CLK_IBUF]

set_property CFGBVS VCCO [current_design]
set_property CONFIG_VOLTAGE 3.3 [current_design]