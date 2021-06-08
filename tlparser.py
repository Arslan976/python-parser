"""
author: Arslan Faisal
CSUID: 2809340
"""
from datetime import datetime
import sys
import re

# UTILITY FUNCTIONS
def find_date(line, line_count):
    time_regx = re.compile(r'\b((1[0-2]|0?[0-9]):([0-5][0-9])([AaPp][Mm]) - (1[0-2]|0?[0-9]):([0-5][0-9])([AaPp][Mm]))')
    try:
        date = time_regx.search(line)
        time_set = date.group()
    except:
          print("Format issue in line number:", line_count)
    else:
        return time_set
def data_cleaning(dataset):
    cleaned_data=[]
    FMT = '%H:%M:%S'
    for x in range(len(dataset)):            
        value = str(dataset[x]).split(',')
        if len(value) == 1:
            cleaned_data.append(value[0])
        elif len(value) == 2:
            temp = value[1].strip()
            cleaning_difference = datetime.strptime(temp, FMT) - datetime.strptime('12:00:00', FMT)
            cleaned_data.append(str(cleaning_difference))
    return cleaned_data
# TIME EXTRACTION FUNCTION 
def extractTime(line, line_count):
    FMT = '%H:%M%p'
    time_set = find_date(line, line_count)
    new_time = time_set.split('-')
    t1 = new_time[0].strip()
    t2 = new_time[1].strip()
    time_difference = datetime.strptime(t2, FMT) - datetime.strptime(t1, FMT)
    return time_difference
# GENERAL INFORMATION EXTRACTION FUNCTION
def informationExtraction(line, line_count):
    extract_date_list = []
    extract_time_item = ''
    try:
        newLine = line.split('\: [0-9]\gm')
        if len(newLine) == 2:
            extract_date_list.append(newLine[0])
            extract_time_item = extractTime(newLine[1], line_count)
        else : extract_time_item = extractTime(newLine[0], line_count)
    except:
        return print("Format issue in line number:", line_count)
    return extract_time_item
# FINAL REPORT EXTRACTION
def final_report(timeList):
    totalSecs = 0
    for tm in timeList:
        if tm == 'None':
            continue
        else:
            timeParts = [int(s) for s in tm.split(':')]
            totalSecs += (timeParts[0] * 60 + timeParts[1]) * 60 + timeParts[2]
    totalSecs, sec = divmod(totalSecs, 60)
    hr, min = divmod(totalSecs, 60)
    print (str(hr) + ":" + str(min) + ":" + str(sec) + " hours:minutes:seconds")
    
# MAIN PROGRAM
def main():
    # INITIAL VARIABLE DECLARATION
    activate = False
    extracted_list = []
    line_count = 0
    # READING THE FILE
    file = open(str(sys.argv[1]), "r")
    lines = file.readlines()
    file.close()
    # LOOKING INTO THE FILE
    for line in lines:
        line_count = line_count + 1
        line = line.strip()
        if activate == False and line == 'Time Log:':
            activate = True
            continue
        if  activate == True and line.strip()[0] == '-':
            continue
        if activate == True:
            extracted_list.append(informationExtraction(line, line_count))
    if activate == False:
        print("NO TIME LOG ON TOP OF THE FILE")
    else:
        cleaned_data = data_cleaning(extracted_list)
        final_report(cleaned_data)
print("Welcome to the parser program!\n")
if __name__ == '__main__':
    main()
