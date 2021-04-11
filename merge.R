
# merge sampled dataset with shoe dataset
# Rscript sampled_csv shoe_csv output_csv

args <- commandArgs( trailingOnly = TRUE )
#args <- c("men_sampled.csv","men_shoe.csv","men_sampled_shoe.csv")

input_sampled <- 'women_sampled.csv'
input_shoe <- 'women_shoe.csv'
output_csv <- 'women_sampled_shoe.csv'

# read in the data
perf_data <- read.csv( input_sampled, as.is = TRUE)
shoe_data <- read.csv( input_shoe, as.is = TRUE)
#print(shoe_data$match_name)
# join them together
perf_data$vaporfly <- NA
for(j in 1:nrow(perf_data)){
    
    # find the right row in shoe data 
    ind_shoedata <- which( 
        shoe_data$match_name == perf_data$match_name[j] &
        shoe_data$marathon == perf_data$marathon[j] &
        shoe_data$year == perf_data$year[j] 
    )
    
    # assign vaporfly variable
    #hitting "int 0" at 440 for some reason
    if (length(shoe_data$vaporfly[ind_shoedata]) == 0 || is.na(shoe_data$vaporfly[ind_shoedata])){
        print('here')
        perf_data$vaporfly[j] <- FALSE
    }
    else{
        perf_data$vaporfly[j] <- shoe_data$vaporfly[ind_shoedata]
    }
    print(perf_data$vaporfly[j])

    # check for weirdness
    if( length(ind_shoedata) != 1 ){print(j)}
}

# write to csv
write.csv(perf_data, file = output_csv, row.names = FALSE )
