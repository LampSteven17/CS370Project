### Thread library for python
import threading 
import time
import datetime
import sys
import RPi.GPIO as GPIO
import getopt
import check


# This variable keeps track of whether the intrument is still reading or not
is_curr_reading = True # will be global



# HELPER  to get current time 
# PARMAM: takes previous time
# RETURNS: current time
def get_time(prev):
    #gettime 
    curr = datetime.datetime.now()
    if not prev:
        print("\n")
        return curr
    else:
        print("[TIME SINCE PREVIOUS RUN]  ", curr-prev, "\n")
    return curr




def collect_data(between, iterations, inch): 
    # data members
    global is_curr_reading # keep global for all access
    prev = 0
    start_time = datetime.datetime.now() # use to keep track of total time
    error_count = 0

    # open up a csv file to write to, write only
    data_file = open("data.csv", "w+")
    
    suffix = " cm"
    
    if inch:
        suffix = " inches"


    while(is_curr_reading):
        
        # start of using driver code template 
        try: 
            # set up sensor
            GPIO.setmode(GPIO.BOARD)

            # the pins being used
            TRIGGER = 7
            ECHO = 11

            GPIO.setup(TRIGGER, GPIO.OUT)
            GPIO.setup(ECHO, GPIO.IN)

            GPIO.output(TRIGGER, GPIO.LOW)

            
            GPIO.output(TRIGGER, GPIO.HIGH)

            time.sleep(0.00001)
            
            GPIO.output(TRIGGER, GPIO.LOW)


            while GPIO.input(ECHO)==0:
                starttime = time.time()
            while GPIO.input(ECHO)==1:
                endtime = time.time()

            pulse = endtime - starttime
            distance = round(pulse * 17150, 2)
        finally:
            # cleanup no matter what
            GPIO.cleanup()
        #end of driver code
        
        # get current time 
        curr = datetime.datetime.now()
        
        # inches or cm
        if inch:
            distance = distance * 0.3937
        
        # check distance 
        if distance > 200:
            print("[ERROR IN SENSOR] erroneous measurement: ", round(distance, 0))
            distance = -1.0
            error_count += 1

        # write to csv data file
        data_file.write("%f,%s\n" % (distance, curr))

        print("[CURRENT DISTANCE]         ", round(distance, 3), suffix)
        print("[TOTAL TIME ELAPSED]       ", curr - start_time)
        
        # get time
        prev = get_time(prev)
        
        #decrement iterations to count down
        iterations -= 1
        # stop iterating
        if iterations == 0:
            is_curr_reading = False
        time.sleep(between) #TODO set between in call
    # save total time
    finish_time = datetime.datetime.now() - start_time
    
    print("TOTAL TIME                    | ", finish_time)
    print("NUMBER ERRONEOUS MEASUREMENTS | ", error_count)
    print("\nPress RETURN to finish writing CSV file, preform calculations and exit program.\n")
    
    
    # close csv, done
    data_file.close()
    
    



def keyboard_input(): 
    # Set to global for one instance, apparently cannot do at init declaration
    global is_curr_reading
    
    # Get user input
    input("\n==================================\n[USAGE] press RETURN to quit\n[USAGE] -h for HELP\n==================================\n")
    is_curr_reading = False # waits for input and stops reading upon recieving
    time.sleep(.5)
    check.main()




# MAIN MAIN MAIN
def main():

    # this defaults the time check period to 1 second
    # but a different time period can be provided via argument 1
    interval = 1
    iterations = 10
    inch = False # if true, uses inches
    yes_d = False
    
    
    # getting command line args    
    args = sys.argv
    arglist = args[1:]
    
    # setting options
    options = "i:n:hAs"
    
    try:
        arguments = getopt.getopt(arglist, options)
    except getopt.error as err:
        print(str(err))
        sys.exit(2)
        

    
    for a in arguments[0]:
        if a[0] == "-i":
            interval = float(a[1])
        elif a[0] == "-n":
            iterations = int(a[1])
        elif a[0] == "-A": # for American lol
            inch = True
        elif a[0] == "-h":
            print("==========\n   HELP\n==========\n")
            print("-i [arg]   interval of time between measurements. Default is 1 second.\n")
            print("-n [arg]   number of iterations. Default is 10.\n")
            print("-A         use INCHES as standard measurement, not CM\n")
            sys.exit(0)
    

    # sensor needs to settle 
    print("\n[ SENSOR SETTLING FOR (2 SECONDS)] ")
    time.sleep(2)

    # start the keyboard input thread
    keyboard = threading.Thread(target = keyboard_input)
    keyboard.start()

    # Start the thread that interacts with the instrument
    read_thread = threading.Thread(target = collect_data(interval, iterations, inch))
    read_thread.start()





# Call main 
if __name__ == "__main__":
    main()
