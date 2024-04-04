# ------------
# Introduction
# ------------

## Here you can include a brief description of the main purpose of this file.

NAME <- 'start_template_R' ## Name of the R file goes here (without the file extension!)
PROJECT <- '<[{PROJECT}]>'
PROJECT_DIR <- 'C:/' ## Change this to the directory in which your project folder is located, make sure to avoid using single backslashes (i.e. \)!

# ------------
# Preamble
# ------------

## -------
## Imports
## -------
### All the library imports go here

## --------
## Settings
## --------
### Any settings go here


## ---------------------
## Set working directory
## ---------------------
### The code below will traverse the path upwards until it finds the root folder of the project.

setwd(file.path(PROJECT_DIR, PROJECT))

## ----------------------------------
## Set  up pipeline folder if missing
## ----------------------------------
### The code below will automatically create a pipeline folder for this code file if it does not exist.

if (dir.exists(file.path('empirical', '2_pipeline'))){
  pipeline <- file.path('empirical', '2_pipeline', NAME)
} else {
  pipeline <- file.path('2_pipeline', NAME)
}

if (!dir.exists(pipeline)) {
  dir.create(pipeline)
  for (folder in c('out', 'store', 'tmp')){
    dir.create(file.path(pipeline, folder))
  }
}

# ---------
# Main code
# ---------

# Reference examples on how to save and load data
#
## -- Load data from 0_data folder --
#
# auto_df <- read_excel(file.path('empirical', '0_data', 'external', 'auto.xls'))
#
## -- Save data to pipeline folder -- 
#
# auto_df['log_weight'] <- log(auto_df['weight'])
# saveRDS(auto_df, file = file.path(pipeline, 'out', 'auto.rds'))
#
## -- Load data from another pipeline folder --
#
# auto_df <- readRDS(file.path('empirical', '2_pipeline', '0_load_data', 'out', 'auto.rds'))


# ----------
# Leftovers
# ----------
## Here you leave any code snippets or temporary code that you don't need but don't want to delete just yet


