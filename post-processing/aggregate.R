#!/usr/bin/env Rscript


#Function to determine information of the file from its name
get_file_info <- function(filename){
  info_file <- c()
  split_name <- unlist(strsplit(filename, "_", fixed=TRUE))
  if(split_name[length(split_name)]=="building.csv"){
    info_file <- c(info_file,BUILDINGS)
    split_name <- unlist(strsplit(split_name[length(split_name)-1],"-",fixed=TRUE))
    info_file <- c(split_name[length(split_name)],info_file)
  }else{
    info_file <- c(info_file,INDIVIDUALS)
    info_file <- c(info_file, as.numeric(unlist(strsplit(gsub(".csv","",split_name[length(split_name)],fixed=TRUE),"-",fixed=TRUE))[1]))
    split_name <- unlist(strsplit(split_name[length(split_name)-1],"-",fixed=TRUE))
    info_file <- c(split_name[length(split_name)],info_file)
  }
  return(info_file)
}

#Function to take care of a folder of results
do_folder <- function(path_folder, path_output, nb_steps){
  subfolders <- list.dirs(path_folder,full.names = TRUE,recursive = F)
  
  #One subfolder is expected to contain the results of all simulations from a same experiment
  for(aSubfolder in subfolders){
    dir.create(gsub(path_folder,path_output,aSubfolder,fixed = T),showWarnings = F, recursive = T)
    nb_simulations <- length(list.files(aSubfolder,pattern="*building.csv",include.dirs = F,recursive = F))
    array_individuals <- array(0,dim=c(INDIVIDUAL_VARIABLES,nb_simulations,length(INDIVIDUAL_AGE_CATEGORIES),nb_steps))
    array_buildings <- array(0,dim=c(BUILDING_TYPES,nb_simulations,nb_steps))
    v_simulations <- c()
    building_names <- c()
    files <- list.files(aSubfolder, pattern="*.csv", full.names = TRUE, include.dirs = F, recursive = F)
    for(aFile in files){
      file_info <- get_file_info(aFile)
      if((file_info[1] %in% v_simulations) == FALSE){
        v_simulations <- c(v_simulations,file_info[1])
      }
      tmp_df <- read.csv(aFile, stringsAsFactors = F)
      max_steps <- min(nrow(tmp_df),nb_steps)
      if(file_info[2]==BUILDINGS){
        if(length(building_names)==0){
          building_names <- colnames(tmp_df)
        }
        for(aColumn in 1:BUILDING_TYPES){
          array_buildings[aColumn,which(v_simulations==file_info[1]),1:max_steps] <- tmp_df[1:max_steps,aColumn]
          if(max_steps<nb_steps){
            array_buildings[aColumn,which(v_simulations==file_info[1]),(max_steps+1):nb_steps] <- rep(array_buildings[aColumn,which(v_simulations==file_info[1]),max_steps],nb_steps-max_steps)
          }
          
        }
      }else{
        if(file_info[2]==INDIVIDUALS){
          for(aColumn in 1:INDIVIDUAL_VARIABLES){
            array_individuals[aColumn,which(v_simulations==file_info[1]),which(INDIVIDUAL_AGE_CATEGORIES==as.numeric(file_info[3])),1:max_steps] <- tmp_df[1:max_steps,aColumn]
            if((max_steps<nb_steps)&(aColumn %in% c(1,4,9,10))){
              array_individuals[aColumn,which(v_simulations==file_info[1]),which(INDIVIDUAL_AGE_CATEGORIES==as.numeric(file_info[3])),(max_steps+1):nb_steps] <- rep(array_individuals[aColumn,which(v_simulations==file_info[1]),which(INDIVIDUAL_AGE_CATEGORIES==file_info[3]),max_steps],nb_steps-max_steps)
            }
          }
        }
      }
    }
    #SAVING FILES
    
    #This is to save the cumulative incidence for each type of building
    for(aColumn in 1:BUILDING_TYPES){
      mat_info <- matrix(0,ncol=nb_steps,nrow=8)
      for(aStep in 1:nb_steps){
        mat_info[1,aStep] <- mean(array_buildings[aColumn,,aStep])
        mat_info[2,aStep] <- min(array_buildings[aColumn,,aStep])
        mat_info[3,aStep] <- max(array_buildings[aColumn,,aStep])
        mat_info[4,aStep] <- median(array_buildings[aColumn,,aStep])
        mat_info[5,aStep] <- quantile(array_buildings[aColumn,,aStep],probs = 0.05)
        mat_info[6,aStep] <- quantile(array_buildings[aColumn,,aStep],probs = 0.95)
        mat_info[7,aStep] <- quantile(array_buildings[aColumn,,aStep],probs = 0.025)
        mat_info[8,aStep] <- quantile(array_buildings[aColumn,,aStep],probs = 0.975)
      }
      write.csv(mat_info,file.path(gsub(path_folder,path_output,aSubfolder,fixed = T),paste(building_names[aColumn],".csv",sep="")))
    }
    for(aColumn in 1:INDIVIDUAL_VARIABLES){
      
      #This is for the total matrix, doing the sum, for each simulation, of the age categories for the different variables
      mat_total <- matrix(0, ncol=nb_steps, nrow=8)
      for(aStep in 1:nb_steps){
        mat_total[1,aStep] <- mean(rowSums(array_individuals[aColumn,,,aStep]))
        mat_total[2,aStep] <- min(rowSums(array_individuals[aColumn,,,aStep]))
        mat_total[3,aStep] <- max(rowSums(array_individuals[aColumn,,,aStep]))
        mat_total[4,aStep] <- median(rowSums(array_individuals[aColumn,,,aStep]))
        mat_total[5,aStep] <- quantile(rowSums(array_individuals[aColumn,,,aStep]),probs = 0.05)
        mat_total[6,aStep] <- quantile(rowSums(array_individuals[aColumn,,,aStep]),probs = 0.95)
        mat_total[7,aStep] <- quantile(rowSums(array_individuals[aColumn,,,aStep]),probs = 0.025)
        mat_total[8,aStep] <- quantile(rowSums(array_individuals[aColumn,,,aStep]),probs = 0.975)
      }
      write.csv(mat_total,file.path(gsub(path_folder,path_output,aSubfolder,fixed = T),paste(INDIVIDUAL_VARIABLES_NAMES[aColumn],"_Total.csv",sep="")))
      
      #This is for the matrix for each age category of a variable
      for(aCategory in 1:length(INDIVIDUAL_AGE_CATEGORIES)){
        mat_info <- matrix(0,ncol=nb_steps,nrow=8)
        for(aStep in 1:nb_steps){
          mat_info[1,aStep] <- mean(array_individuals[aColumn,,aCategory,aStep])
          mat_info[2,aStep] <- min(array_individuals[aColumn,,aCategory,aStep])
          mat_info[3,aStep] <- max(array_individuals[aColumn,,aCategory,aStep])
          mat_info[4,aStep] <- median(array_individuals[aColumn,,aCategory,aStep])
          mat_info[5,aStep] <- quantile(array_individuals[aColumn,,aCategory,aStep],probs = 0.05)
          mat_info[6,aStep] <- quantile(array_individuals[aColumn,,aCategory,aStep],probs = 0.95)
          mat_info[7,aStep] <- quantile(array_individuals[aColumn,,aCategory,aStep],probs = 0.025)
          mat_info[8,aStep] <- quantile(array_individuals[aColumn,,aCategory,aStep],probs = 0.975)
        }
        write.csv(mat_info,file.path(gsub(path_folder,path_output,aSubfolder,fixed = T),paste(INDIVIDUAL_VARIABLES_NAMES[aColumn],"_",INDIVIDUAL_AGE_CATEGORIES[aCategory],".csv",sep="")))
      }
    }
  }
}

args = commandArgs(trailingOnly=TRUE)
number_args <- 3
INDIVIDUALS <- "Individuals"
BUILDINGS <- "Buildings"
INDIVIDUAL_VARIABLES <- 10
INDIVIDUAL_VARIABLES_NAMES <- c("Cumulative Incidence","Hospitalisations","ICU","Susceptible","Latent","Asymptomatic","Presymptomatic","Symptomatic","Recovered","Dead")
INDIVIDUAL_AGE_CATEGORIES <- seq(0,95,5)
BUILDING_TYPES <- 14

if(length(args)>number_args){
  print("Too many arguments")
}else{
  if(length(args)<number_args){
    print("Too few arguments")
  }else{
    main_folder <- as.character(args[1])
    output_folder <- as.character(args[2])
    nb_steps <- as.numeric(args[3])
    do_folder(main_folder,output_folder,nb_steps)
  }
}
