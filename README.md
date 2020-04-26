# COVID-19-CHALLENGE

## CsvTable class

The csv class has two ways of initializing, one that consists of reading the csv and the other where the csv has already
been read. We also added some magic methods to represent the instance and facilitate its manipulation.

### Filter 

- At first we create a named tuple that will contain the sample information needed for both sorting and filtering.
- We go through the CSV table once to create a dictionary as a key we will have the region and as a value a list where 
we will add those values registered in the named tuple.
- When we already have the dictionary, we pass the list to the function get_average_row that will return the sample 
line that has the average value in the samples of each region.
- Finally the list comprehension will filter the csv with our samples.