## Conversion of Boeing Aircraft Performance Files
## for Analysis with Column-based Analytical Tools
## nils.clausen@tuifly.com / mail@clausenn.de
## 2019-05-07 17:20
import pandas as pd
from pathlib import Path
from datetime import datetime

# date setting and file locations
today = datetime.today()
apm_folder = "code/aircraft-performance/data/raw/apm/TXT/"
apm_file = ""
outfile = "code/aircraft-performance/data/output/outfile.txt"

# main routine
# open output file and write header
outfile_handle = open(outfile,"w")
outfile_handle.write("apm_file,aircraft,date,flight,pct_n1_reqd,pct_thrst_reqd,pct_fuelflow,pct_fm\r\n")
outfile_handle.close()
# cycle through complete file list in above folder
file_list = [f for f in Path(apm_folder).glob('**/*') if f.is_file()]
for f in file_list:
    apm_file = f.stem+f.suffix
    # open outfile again in append mode to prevent possible buffer overflow
    outfile_handle = open(outfile,"a+")
    # grab aircraft registration from intermediate headers
    # then put as qualifying column in front and read all other columns
    # modify encoding in open function accordingly based on the OS origin of the files
    with open(apm_folder+apm_file, "r", encoding='windows-1252') as ins:
        print(apm_file+" opened.")
        aircraft = ""
        date = ""
        for line in ins:
            if "PERFORMANCE ANALYSIS FOR AIRPLANE" in line:
                aircraft = line[45:].strip()
            # find and mingle the other columns together
            if ((line[1:2] == "0") or (line[1:2] == "1") or (line[1:2] == "2") or (line[1:2] == "3")) and (line[3:4] == "-") and (line[6:7] == "-") and (line[74:78].strip() != "*"):
                date = "20"+line[7:9]+"-"+line[4:6]+"-"+line[1:3]
                flight = line[10:19].strip()
                pct_n1_reqd = line[54:60].strip()
                pct_thrst_reqd = line[61:66].strip()
                pct_fuelflow = line[67:72].strip()
                pct_fm = line[72:78].strip()
                # print(apm_file+","+aircraft+","+date+","+flight+","+pct_n1_reqd+","+pct_thrst_reqd+","+pct_fuelflow+","+pct_fm)
                outfile_handle.write(apm_file+","+aircraft+","+date+","+flight+","+pct_n1_reqd+","+pct_thrst_reqd+","+pct_fuelflow+","+pct_fm+"\r\n")
    print(apm_file+" done.")
    # walk away clean after piping one input file at a time into the output file
outfile_handle.close()