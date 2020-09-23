import numpy as np
import matplotlib.pyplot as plt
import csv
#from math import sin, pi
#import sys

#Simple function to visualize 4 arrays that are given to it
def visualize_data(timestamps, x_arr,y_arr,z_arr,s_arr):
  #Plotting accelerometer readings
  plt.figure(1)
  plt.plot(timestamps, x_arr, color = "blue",linewidth=1.0)
  plt.plot(timestamps, y_arr, color = "red",linewidth=1.0)
  plt.plot(timestamps, z_arr, color = "green",linewidth=1.0)
  plt.show()
  #magnitude array calculation
  m_arr = []
  for i, x in enumerate(x_arr):
    m_arr.append(magnitude(x_arr[i],y_arr[i],z_arr[i]))
  plt.figure(2)
  #plotting magnitude and steps
  plt.plot(timestamps, s_arr, color = "black",linewidth=1.0)
  plt.plot(timestamps, m_arr, color = "red",linewidth=1.0)
  plt.show()

#Function to read the data from the log file
#Read the measurements into row by row. Record value of each item into
# corresponding array variables and return them
def read_data(filename):
  timestamps=[]
  x_array=[]
  y_array=[]
  z_array=[]
  with open(filename,'r')as f :
      data = csv.reader(f)
      for row in data:
        timestamps.append(row[0])
        x_array.append(row[1])
        y_array.append(row[2])
        z_array.append(row[3])
  return timestamps,x_array,y_array,z_array

#Function to calculate tresholds
def treshold (buff, size):
    total = 0.0
    i=0
    #print (len(buff))
    while i < len(buff):
        total = total+buff[i]
        #print (i, total)
        i=i+1
    total = total/size
    #print ("total:", total)
    return total
#Function to count steps.
#Takes in arrays and buffer size
#Returns an array of timestamps from when steps were detected
#Each value in this arrray represent the time that step was made.
def count_steps(timestamps, x_arr, y_arr, z_arr, buff_size):
  rv = []
  marginal=1
  time_between_steps = 3
  #create a sum vector
  sum_arr=[]
  c = 0
  pass_mean = False
  wait_delay = 0
  for a in enumerate(x_arr):
    tot = abs(float(x_arr[c]))+abs(float(y_arr[c]))+abs(float(z_arr[c]))
    #print (tot)
    sum_arr.append(tot)
    c=c+1
  buffer=[]
  for i, time in enumerate(timestamps):
#create buffer
    if int(i)<=buff_size:
        buffer.append(sum_arr[i])
        #print(i, buffer[i])
    else:
        #calculate dynamic treshold
        treshold_level = treshold(buffer, buff_size)
        #add new value to buffer and remove old
        buffer.append(sum_arr[i])
        del buffer[0]
        #detect step
        #print (treshold_level)
        if sum_arr[i]>(treshold_level+marginal):
            pass_mean=True
            wait_delay=time_between_steps
        elif pass_mean==True:
            if wait_delay <= 0:
                rv.append(time)
                pass_mean=False
                print(time)
            else:
                wait_delay=wait_delay-1
  return rv

#Calculate the magnitude of the given vector
def magnitude(x,y,z):
  return np.linalg.norm((x,y,z))

#Function to convert array of times where steps happened into array to give into graph visualization
#Takes timestamp-array and array of times that step was detected as an input
#Returns an array where each entry is either zero if corresponding timestamp has no step detected or 50000 if the step was detected
def generate_step_array(timestamps, step_time):
  s_arr = []
  ctr = 0
  for i, time in enumerate(timestamps):
    if(ctr<len(step_time) and step_time[ctr]<=time):
      ctr += 1
      s_arr.append( 50000 )
    else:
      s_arr.append( 0 )
  while(len(s_arr)<len(timestamps)):
    s_arr.append(0)
  return s_arr

#Check that the sizes of arrays match
def check_data(t,x,y,z):
  if( len(t)!=len(x) or len(y)!=len(z) or len(x)!=len(y) ):
    print("Arrays of incorrect length")
    return False
  print("The amount of data read from accelerometer is "+str(len(t))+" entries")
  return True

def main():
  #read data from a measurement file, change the inoput file name if needed
  timestamps, x_array, y_array, z_array = read_data("test1.csv")
  #Chek that the data does not produce errors
  if(not check_data(timestamps, x_array,y_array,z_array)):
    return
  #Count the steps based on array of measurements from accelerometer
  buffer_size = 30
  st = count_steps(timestamps, x_array, y_array, z_array, buffer_size)
  #Print the result
  print("This data contains "+str(len(st))+" steps according to current algorithm")
  #convert array of step times into graph-compatible format
  s_array = generate_step_array(timestamps, st)
  #visualize data and steps
  visualize_data(timestamps, x_array,y_array,z_array,s_array)

main()
