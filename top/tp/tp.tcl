#vivado
set bin_file 1
set _ip_dir_ "../../IP"

### FPGA and Vivado strategies and flows

set FPGA xcvu37p-fsvh2892-3-e

set SYNTH_STRATEGY "Flow_AreaOptimized_High"

set SYNTH_FLOW "Vivado Synthesis 2019"

set IMPL_STRATEGY "Performance_ExplorePostRoutePhysOpt"

set IMPL_FLOW "Vivado Implementation 2019"

set DESIGN "[file rootname [file tail [info script]]]"

set path_repo "[file normalize [file dirname [info script]]]/../../"

set SIMULATOR "modelsim"

source $path_repo/Hog/Tcl/create-project.tcl

set_property "ip_repo_paths" "${_ip_dir_}" [current_project]
set_property target_language Verilog [current_project]

set_property "questa.simulate.runtime" "1ms" [get_filesets b2b_sim]
update_ip_catalog 
