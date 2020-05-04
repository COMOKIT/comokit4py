#!/usr/bin/env Rscript
args = commandArgs(trailingOnly=TRUE)

load_matrix_from_array_ages <- function(mat,id_category,arr,step){
  
  mat[1,step] <- mean(arr[id_category,,step])
  mat[2,step] <- median(arr[id_category,,step])
  mat[3,step] <- min(arr[id_category,,step])
  mat[4,step] <- max(arr[id_category,,step])
  mat[5,step] <- quantile(arr[id_category,,step],probs=0.05)
  mat[6,step] <- quantile(arr[id_category,,step],probs=0.95)
  mat[7,step] <- quantile(arr[id_category,,step],probs=0.025)
  mat[8,step] <- quantile(arr[id_category,,step],probs=0.975)
  return(mat)
}

read_folder <- function(path_input, path_output, age_categories,building_types,nb_steps){
  print(path_input)
  print(path_output)
  print(nb_steps)
  
  files <- list.files(path_input,all.files = F,full.names = T,recursive = F, pattern = "*_building.csv")
  nb_simulation <- length(files)
  
  
  array_incidence_ages <- array(0,dim=c(length(age_categories),nb_simulation,nb_steps))
  array_hospitalisation_ages <- array(0,dim=c(length(age_categories),nb_simulation,nb_steps))
  array_ICU_ages <- array(0,dim=c(length(age_categories),nb_simulation,nb_steps))
  array_susceptible_ages <- array(0,dim=c(length(age_categories),nb_simulation,nb_steps))
  array_latent_ages <- array(0,dim=c(length(age_categories),nb_simulation,nb_steps))
  array_asymptomatic_ages <- array(0,dim=c(length(age_categories),nb_simulation,nb_steps))
  array_presymptomatic_ages <- array(0,dim=c(length(age_categories),nb_simulation,nb_steps))
  array_symptomatic_ages <- array(0,dim=c(length(age_categories),nb_simulation,nb_steps))
  array_recovered_ages <- array(0,dim=c(length(age_categories),nb_simulation,nb_steps))
  array_dead_ages <- array(0,dim=c(length(age_categories),nb_simulation,nb_steps))
  array_building <- array(0,dim=c(length(building_types),nb_simulation,nb_steps))
  
  files <- list.files(path_input,all.files = F,full.names = T,recursive = F)
  
  ##LOADING ARRAYS
  for(aFile in files){
    file_name <- unlist(strsplit(aFile,"/",fixed=TRUE))
    file_name <- file_name[length(file_name)]
    file_name_no_extension <- gsub(".csv","",file_name,fixed=TRUE)
    age_category <- unlist(strsplit(file_name_no_extension,"_",fixed=TRUE))
    age_category <- age_category[length(age_category)]
    id_simulation <- unlist(strsplit(file_name_no_extension,"_",fixed=TRUE))
    id_simulation <- unlist(strsplit(id_simulation[1],"-",fixed=TRUE))
    id_simulation <- as.numeric(id_simulation[length(id_simulation)])
    tmp_df <- read.csv(aFile,stringsAsFactors = F)
    
    if(age_category=="building"){
      #FOR BUILDINGS
      for(a_column in 1:ncol(tmp_df)){
        id_building <- which(building_types==colnames(a_column))
        max_nb_row <- min(nb_steps,nrow(tmp_df))
        array_building[id_building,id_simulation,1:max_nb_row] <- tmp_df[1:max_nb_row,a_column]
      }
    }else{
      age_category <- unlist(strsplit(age_category,"-",fixed=TRUE))
      age_category <- age_category[1]
      age_category <- which(age_categories==age_category)
      if(is.na(age_category)==FALSE){
        #FOR AGES
        max_nb_row <- min(nb_steps,nrow(tmp_df))
        array_incidence_ages[age_category,id_simulation,1:max_nb_row] <- tmp_df[1:max_nb_row,1]
        array_hospitalisation_ages[age_category,id_simulation,1:max_nb_row] <- tmp_df[1:max_nb_row,2]
        array_ICU_ages[age_category,id_simulation,1:max_nb_row] <- tmp_df[1:max_nb_row,3]
        array_susceptible_ages[age_category,id_simulation,1:max_nb_row] <- tmp_df[1:max_nb_row,4]
        array_latent_ages[age_category,id_simulation,1:max_nb_row] <- tmp_df[1:max_nb_row,5]
        array_asymptomatic_ages[age_category,id_simulation,1:max_nb_row] <- tmp_df[1:max_nb_row,6]
        array_presymptomatic_ages[age_category,id_simulation,1:max_nb_row] <- tmp_df[1:max_nb_row,7]
        array_symptomatic_ages[age_category,id_simulation,1:max_nb_row] <- tmp_df[1:max_nb_row,8]
        array_recovered_ages[age_category,id_simulation,1:max_nb_row] <- tmp_df[1:max_nb_row,9]
        array_dead_ages[age_category,id_simulation,1:max_nb_row] <- tmp_df[1:max_nb_row,10]
      }
    }
  }
  
  for(an_age_category in age_categories){
    mat_incidence <- matrix(0,nrow=8,ncol=nb_steps)
    mat_hospitalisation <- matrix(0,nrow=8,ncol=nb_steps)
    mat_ICU <- matrix(0,nrow=8,ncol=nb_steps)
    mat_susceptible <- matrix(0,nrow=8,ncol=nb_steps)
    mat_latent <- matrix(0,nrow=8,ncol=nb_steps)
    mat_presymptomatic <- matrix(0,nrow=8,ncol=nb_steps)
    mat_asymptomatic <- matrix(0,nrow=8,ncol=nb_steps)
    mat_symptomatic <- matrix(0,nrow=8,ncol=nb_steps)
    mat_recovered <- matrix(0,nrow=8,ncol=nb_steps)
    mat_dead <- matrix(0,nrow=8,ncol=nb_steps)
    id_age_category <- which(age_categories==an_age_category)
    for(a_step in 1:nb_steps){
      mat_incidence <- load_matrix_from_array_ages(mat_incidence,id_age_category,array_incidence_ages,a_step)
      mat_hospitalisation <- load_matrix_from_array_ages(mat_hospitalisation,id_age_category,array_hospitalisation_ages,a_step)
      mat_ICU <- load_matrix_from_array_ages(mat_ICU,id_age_category,array_ICU_ages,a_step)
      mat_susceptible <- load_matrix_from_array_ages(mat_susceptible,id_age_category,array_susceptible_ages,a_step)
      mat_latent <- load_matrix_from_array_ages(mat_latent,id_age_category,array_latent_ages,a_step)
      mat_presymptomatic <- load_matrix_from_array_ages(mat_presymptomatic,id_age_category,array_presymptomatic_ages,a_step)
      mat_asymptomatic <- load_matrix_from_array_ages(mat_asymptomatic,id_age_category,array_asymptomatic_ages,a_step)
      mat_symptomatic <- load_matrix_from_array_ages(mat_symptomatic,id_age_category,array_symptomatic_ages,a_step)
      mat_recovered <- load_matrix_from_array_ages(mat_recovered,id_age_category,array_recovered_ages,a_step)
      mat_dead <- load_matrix_from_array_ages(mat_dead,id_age_category,array_dead_ages,a_step)
    }
    
    write.csv(mat_incidence,paste(path_output,"Incidence_",an_age_category,".csv",sep=""))
    write.csv(mat_hospitalisation,paste(path_output,"Hospitalisation_",an_age_category,".csv",sep=""))
    write.csv(mat_ICU,paste(path_output,"ICU_",an_age_category,".csv",sep=""))
    write.csv(mat_susceptible,paste(path_output,"Susceptible_",an_age_category,".csv",sep=""))
    write.csv(mat_latent,paste(path_output,"Latent_",an_age_category,".csv",sep=""))
    write.csv(mat_presymptomatic,paste(path_output,"Presymptomatic_",an_age_category,".csv",sep=""))
    write.csv(mat_asymptomatic,paste(path_output,"Asymptomatic_",an_age_category,".csv",sep=""))
    write.csv(mat_symptomatic,paste(path_output,"Symptomatic_",an_age_category,".csv",sep=""))
    write.csv(mat_recovered,paste(path_output,"Recovered_",an_age_category,".csv",sep=""))
    write.csv(mat_dead,paste(path_output,"Dead_",an_age_category,".csv",sep=""))
  }
  
  for(a_building_type in building_types){
    mat_incidence_building <- matrix(0,nrow=8,ncol=nb_steps)
    id_building_type <- which(building_types==a_building_type)
    for(a_step in 1:nb_steps){
      mat_incidence_building <- load_matrix_from_array_ages(mat_incidence_building,id_building_type,array_building,a_step)
    }
    write.csv(mat_incidence_building,paste(path_output,"Building_",a_building_type,".csv",sep=""))
  }
  
}
param_age_categories <- seq(0,95,by = 5)
param_building_categories <- c("","school","shop","place_of_worship","meeting","restaurant","coffee","supermarket","playground","supplypoint","market","industry","hotel","karaoke")
#read_folder("/Users/damie/Downloads/batch_output_building2_0-80/batch_output/","/Users/damie/Downloads/batch_aggregated/",seq(0,95,by = 5),c("","school","shop","place_of_worship","meeting","restaurant","coffee","supermarket","playground","supplypoint","market","industry","hotel","karaoke"),90)
read_folder(args[1],args[2],param_age_categories,param_building_categories,as.numeric(args[3]))
