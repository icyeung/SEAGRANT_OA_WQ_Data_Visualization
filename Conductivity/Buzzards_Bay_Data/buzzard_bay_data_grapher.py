import pandas as pd
import matplotlib.pyplot as plt
import csv
import os

__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))

with open(os.path.join(__location__, 'bbcdata1992to2020-ver07May2021.csv'),'r') as csvfile:
    lines = csv.reader(csvfile, delimiter=',')
    for row in lines:
      
        # Checks if time entry has corresponding Time and Verified Measurement
        # If not, does not include data point in graph
        if not row[0] == "-" and not row[1] == "-" and not row[2] == "-" and not row[0] == "" and not row[1] == "" and not row[2] == "" and numofLinesS > 0:
           
            numofLinesS += 1
        elif numofLinesS <= 0:
            numofLinesS += 1