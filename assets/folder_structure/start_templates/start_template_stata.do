clear all

/*
# ------------
# Introduction
# ------------

Here you can include a brief description of the main purpose of this do file.
*/

local NAME "template_stata" // <-- Change this to the name of the file (without the file extension!)
local PROJECT "<[{PROJECT}]>"
local STATA_VERSION "14.0"
local PROJECT_DIR "C:/" // <-- Change this to the directory in which your project folder is located 


/*
# --------
# Settings
# --------

Any setings go here, for example:
*/

set more off

/*
# ---------------------
# Set working directory
# ---------------------

Make sure to set the NAME and PROJECT_DIR above!
*/

local full_dir "`PROJECT_DIR'/`PROJECT'"
cd "`full_dir'"

/*
# ---------------------------------
# Set up pipeline folder if missing
# ---------------------------------

Make sure to set the NAME and PROJECT_DIR above!
*/

capture mkdir "empirical/2_pipeline"
if _rc != 0 {
	local pipeline "empirical/2_pipeline/`NAME'"
} 
else if {
	local pipeline "2_pipeline/`NAME'"
}

capture mkdir "`pipeline'"
if _rc == 0 {
	foreach folder in "out" "store" "tmp" {
		capture mkdir "`pipeline'/`folder'"
	}
} 

/*
# ---------
# Main code
# ---------
*/

/* Reference examples on how to save and load data: 

	-- Load data from 0_data folder --
	
	use "empirical/0_data/external/auto.dta"
	
	-- Save data to pipeline folder -- 
	
	generate log_weight = log(weight)
	save "`pipeline'/out/auto.dta"
	
	-- Load data from another pipeline folder --
	
	use "empirical/2_pipeline/0_load_data/out/auto.dta"
*/



/*
# ---------
# Leftovers
# ---------

Here you leave any code snippets or temporary code that you don't need but don't want to delete just yet
*/

