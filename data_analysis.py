"""
The purpose of this program is to analyze the air quality data from:
   https://aqicn.org/data-platform/covid19/
in order to see the effect of 19 on air polution.

The program reads and combines multiple csv files, and used a plynomial curve
fit as a projection based on the data from before 2020. This curve fit
projection is then compared to the actual data from 2020.

Control of the program is done using the global variables in order to change the
area, and what type of pollution is being looked at. The degrees of the
polynomials can also be altered for better data fit and projection.
"""

import sys
import csv
from datetime import date
import numpy as np
import matplotlib.pyplot as plt


# What data is being looked for from which place:
COUNTRY = "CN"
CITY = "Wuhan"
SPECIE = "no2"

# Plynomial Degree for each curve fit:
DEG_PROJ = 2
DEG_ACTUAL = 1

# Paths to all of the files to search:
a_FILE_PATHS = ["raw data/waqi-covid19-airqualitydata-2015H1.csv",
                "raw data/waqi-covid19-airqualitydata-2016H1.csv",
                "raw data/waqi-covid19-airqualitydata-2017H1.csv",
                "raw data/waqi-covid19-airqualitydata-2018H1.csv",
                "raw data/waqi-covid19-airqualitydata-2019Q1.csv",
                "raw data/waqi-covid19-airqualitydata-2019Q2.csv",
                "raw data/waqi-covid19-airqualitydata-2019Q3.csv",
                "raw data/waqi-covid19-airqualitydata-2019Q4.csv",
                "raw data/waqi-covid19-airqualitydata-2020Q1.csv",
                "raw data/waqi-covid19-airqualitydata-2020Q2.csv",
                "raw data/waqi-covid19-airqualitydata-2020Q3.csv",
                "raw data/waqi-covid19-airqualitydata-2020Q4.csv"]

# Dates will be converted into an x vale for a plot by calculating the number of
# days past 1/1/2010 the date is.
# Date of 1/1/2010:
START_DATE = date(2010, 1, 1)
# Corresponding number to mark the start of 2020:
DAYS_TO_20 = 3652

# Array indexes of the data:
iDATE = 0
iDAYS = 1
iCOUNTRY = 2
iCITY = 3
iSPECIE = 4
iCOUNT = 5
iMIN = 6
iMAX = 7
iMED = 8
iVAR = 9

# The index of the value that will be plotted/curve fit
VALUE = iMAX


"""
Function: list_str_to_float(lst)
   Takes a list of strings and converts the values which can be converted to
   floating point.
Input:
        lst - a list
Return:
        out - a list
"""
def list_str_to_float(lst):
   out = []
   except_flag = False
   for i in lst:
      try:
         out.append(float(i))
      except:
         if (except_flag):
            except_flag = "DONE"
         elif (not except_flag):
            except_flag = True
         out.append(i)
   if (except_flag):
      print("Some values not converted to float", end="\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b")
   elif (not except_flag):
      print("OK", end="\b\b")
   return out


"""
Function: read_csvs(paths)
   Reads and combines multiple csv files with the same format(same fields).
Input:
        paths - a list of file paths to read
Return:
        fields - a list of the fields of the csv files
        out_array - a 2D list of the combined csv viles
"""
def read_csvs(paths):
   out_array = []
   fields = []

   count = 0
   for path in paths:
      count += 1
      print("Reading File # ", count, end=" - ")
      with open(path, 'r', encoding='utf-8') as csvfile:
         reader = csv.reader(csvfile)
         row = 0
         for r in reader:
            if (('#' in r[0])):
               pass
            elif (row == 1 and (COUNTRY in r) and (CITY in r) and (SPECIE in r)):
                out_array.append(list_str_to_float(r))
            elif(row == 0):
               fields = r
               row = 1
         print("")
   print("Done Reading\n")
   return fields, out_array


"""
Function: write_csv(fields, data, file_name)
   Writes a new csv file.
Input:
        fields - a list of the fields for the csv file
        data - a 2D list of the data for the csv file which corresponds to the
               fields
        file_name - a string which is to be the name of the csv file
Output:
        A csv file
"""
def write_csv(fields, data, file_name):
   with open(file_name, 'w') as csvfile:
      csvwriter = csv.writer(csvfile)
      csvwriter.writerow(fields)
      csvwriter.writerows(data)


"""
Function: create_date(string)
   Takes a date in string form and converts it into a date object.
Input:
        string - a string in the format: 15-12-2020
Return:
        date object containing the date represented in the string
"""
def create_date(string):
   s_date = string.split('-')
   return date(int(s_date[0]), int(s_date[1]), int(s_date[2]))


"""
Function: data_to_num(d_date)
   Calculates the number of days a date is past START_DATE
Input:
        d_date - date object
Return:
        number of days past START_DATE
"""
def date_to_num(d_date):
   return (d_date - START_DATE).days


"""
Main Program:
"""
if __name__ == "__main__":
    # Read the csv files:
   a_fields, a_data = read_csvs(a_FILE_PATHS)
   # Add extra column for number of days conversion to the fields:
   a_fields.insert(iDAYS, "Days")
   print(a_fields)

   # Add extra column with # of days from 1/1/2000(used as x value) to the data:
   for r in range(len(a_data)):
      s_date = a_data[r][iDATE]
      d_date = create_date(s_date)
      num = date_to_num(d_date)
      a_data[r].insert(iDAYS, num)

   # If early data is effecting projection:
   # Remove Days less than:
   LT = 0
   offset = 0
   for i in range(len(a_data)):
      if (a_data[i-offset][iDAYS] < LT):
         a_data.pop(i-offset)
         offset += 1

   # Initialize x, y arrays for before 2020 data, and for 2020 data:
   x_before_20 = []
   y_before_20 = []
   x_after_20 = []
   y_after_20 = []
   # Create x, y data:
   for i in a_data:
      if (int(i[iDAYS]) < DAYS_TO_20):
         x_before_20.append(i[iDAYS])
         y_before_20.append(i[VALUE])
      else:
         x_after_20.append(i[iDAYS])
         y_after_20.append(i[VALUE])

   # Create the plot:
   plt.figure()
   # add the points:
   plt.scatter(x_before_20, y_before_20, label="2015 - 2019 Data")
   plt.scatter(x_after_20, y_after_20, label="2020 Data")

   # Calculate polynomial curve fit coefficients for before 2020, and 2020 data:
   before_coefs = np.polyfit(x_before_20, y_before_20, DEG_PROJ)
   after_coefs = np.polyfit(x_after_20, y_after_20, DEG_ACTUAL)
   print("Projection Coefficients:", before_coefs)
   print("Actual Coefficients:", after_coefs)

   # create a function to turn the coefficients into a polynomial:
   def fx(x, coefs):
      sum = 0
      for i in range(len(coefs)):
         sum += coefs[i]*(x**(len(coefs)-1-i))
      return sum

   # Plot the curve fit functions:
   x_range = np.linspace(min(x_before_20), max(x_after_20), 3000)
   plt.plot(x_range, fx(x_range, before_coefs), color="g", label="'15 - '19 Projection, DEG " + str(DEG_PROJ))
   x_range = np.linspace(min(x_after_20), max(x_after_20), 1000)
   plt.plot(x_range, fx(x_range, after_coefs), color='m', label="Actual, DEG " + str(DEG_ACTUAL))

   # Add labels to the function:
   plt.ylabel("Max Count")
   plt.xlabel("# Days Past 1/1/2010")
   plt.title(CITY + " " + SPECIE)
   plt.legend()

   # Calculate Avgerage projected for 2020 and actual average for 2020:
   count = 0
   sum_proj = 0
   sum_actual = 0
   for x in range(min(x_after_20), max(x_after_20)):
      count += 1
      sum_proj += fx(x, before_coefs)
      sum_actual += fx(x, after_coefs)
   avg_proj = sum_proj/count
   avg_actual = sum_actual/count

   print("Proj. Avg. =", avg_proj)
   print("Actual Avg. =", avg_actual)
   print("Reduced By:", avg_proj-avg_actual)
   plt.show()
