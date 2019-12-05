import csv
import time
import sys
import math
from datetime import time


def get_csv():
    with open("data.csv", 'r') as csvfile:
        # opening reader
        reader = csv.reader(csvfile, delimiter = ',')
        # read into list
        data = []
        for row in reader:
            data.append(row)
        # return the data
        return data

# creates a datetime object
def get_datetime(data_str):
    vals = data_str.split()

    #get time string
    time_str = vals[1]

    # create datetime object
    hour = int(time_str[:2])
    minute = int(time_str[3:5])
    second = int(time_str[6:8])
    millisecond = int(time_str[9:])
    
    # return time object
    return time(hour, minute, second, millisecond)


# gets standard deviation, sum of squares and creats a 95% confidence interval for distance
def std_dev(mean, data, count):
	
    differences = []
    mean_square = 0
	
    for x in data:
         if x is -1:
             continue
         differences.append((mean - x)**2)
         
    for x in differences:
         mean_square += x
		
    print("SUM OF SQUARES                  |  ", round(mean_square, 2))
	
    dev = math.sqrt(mean_square)
	
    print("STANDARD DEVIATION              |  ", round(dev, 2))
    
    dev *= 2
    
    print("95% CONFIDENCE INTERVAL         |   (", round(mean - dev, 2), ", ", round(mean + dev, 2), ")") 
	
    return





def main(): 
    print("[GETTING CSV FILE]\n")

    # Data section
    data = get_csv()
    time_variables = []
    distance_variables = []
    mean = 0

    for dt in data:
        # get time object
        time_variables.append(get_datetime(dt[1]))
        distance_variables.append(float(dt[0]))
        
    count = len(distance_variables)
    for x in distance_variables:
        if x == -1:
            count -= 1
            continue
        mean += x
		
    mean /= count
    
    print("DATA\n----------------")
    print("DISTANCE MEAN                   |  ", round(mean, 3))
    std_dev(mean, distance_variables, count)
    print("NUMBER OF USABLE DATA POINTS    |  ", count)
    
    print("\nFINISHED\n----------------")


    # parse into separate data objects 
    

if __name__ == "__main__":
    main()
