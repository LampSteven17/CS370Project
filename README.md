# Multithreaded Sonar Ruler
# Cade, Steve, AJ

[ USAGE ]

This code is written to be run on a Raspberry Pi, in Python 3.

To run from command line:

  python3 Driver.py [OPTIONAL ARGUMENTS]
  
  * This can be interrupted at ANY time, by pressing the RETURN key.*
  
 The standard no-argument run has 
  * 10 iterations
  * 1  second apart
  * writes all data to a CSV file called data.csv
      
 [ COMMAND LINE ARGUMENTS ]
 
 -h           : Help - lists the options for running the program then exits.
 
 -i [ARG]     : Interval - DEFAULT is 1 second, accepts any floating point number for interval between measurements
 
 -n [ARG]     : Number of measurements - DEFAULT is 10, accepts positive integers. [ ex: -i 100 ]
 
 -A           : Changes measurement unit to inchs. By default, program runs in centimeters.
 
 
 Once the inital Driver.py has finished running, pressing RETURN will close the CSV file data.csv, then call check.py
 to analyze the CSV file and find basic statistic information on the measurements.
 
 [ OTHER ]
 
 The data sensor used in this project [ HC-Sr04 ] is by nature unreliable. This code accounts for irregular measurements,
 outside the distance sensors range and subsequently replaces all measurements over 200cm with a [ -1 ]. Misfires of this
 instrument or bad readings usually result in measurements far outside of the devices range (usually around 6500-8500cm).
 This would corrupt any data interpritation, and therefore these measurements are not included in the calculations.
 
 These bad measurements are however - 
 
 * Noted in standard output
    
 * Counted and reported at end of measurement process
    
 * Subtracted from usable data points, reported at end of CSV (check.py) analysis, in the from of how many data points used.
      
 check.py also creates a list of python "datetime" objects. These arn't fully used. I overestimated the capabilities of 
 the sensor and the datetime objects can't be used for much more than finding time between pulses, and total time. 
 Kept in the code for future sensor implementation.
