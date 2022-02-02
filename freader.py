import numpy as np
import file_def

#forcing_list = ["apu12set", "sp100set","sp100set", "sp500set", "dpinviset" ]
forcing_list = ["sp100set","sp100set", "sp500set"]
file_name = file_def.file_name
log_file = file_def.log_file

#User Defined Functions
def getCbitName(s):
    start = s.find("(")+1
    stop = s.find(")")
    names = s[start:stop].split(",")
    names = [x.strip(' ') for x in names]
    return names

def getForcingName(s):
    start = s.find("(")+1
    stop = s.find(",")
    name = s[start:stop].split(",")[0].strip().strip('"')
    return name

def getForcingMode(s):
    start = s.find("(")+1
    stop = s.find(")")
    name = s[start:stop].split(",")[1].strip().strip('"')
    return name

#gets all resources depending on type: "cbit" or "force" 
def getAllResources(fname, rtype):
    f = open(file_name, "r")
    #f = open("SPM7_S_01_SP_ETS_A0_FSB70250_DS.cpp", "r")
    all_resources = []
    all_resources.clear()
    for r in f:
        #ignore comments
        r = r.partition("//")[0]    
        if rtype == "forcing" and any(x in r for x in forcing_list):
            name = []
            name = [getForcingName(r)]
            f_res = np.concatenate((all_resources, name))
            all_resources = np.unique(f_res)
        #elif rtype =="cbit" and "cbitclose" in r:
        elif rtype =="cbit" and ("cbitclose" in r or "cbitopen" in r):
            name = []
            name = getCbitName(r)
            cbits = np.concatenate((all_resources, name))
            all_resources = np.unique(cbits)
    map(str.strip, all_resources)
    return all_resources

def getAllCbits(fname):
    all_cbits = []
    all_cbits = getAllResources(file_name, "cbit")
    return all_cbits

def getAllForcing(fname):
    all_forcing = []
    all_forcing = getAllResources(file_name, "forcing")
    return all_forcing

def checkForcing(line):
    if any(x in line for x in forcing_list):
        forced_val = line.split(",")[2]
        #print("Checking forcing ", getForcingName(line)[0],":", forced_val, file=open(log_file,"a"))
        return getForcingName(line)

def getMode(line):
    if any(x in line for x in forcing_list):
        mode = line.split(",")[1]
        return mode

def getFValue(line):
    if any(x in line for x in forcing_list):
        fvalue = line.split(",")[2]
        return fvalue

def checkCbit(line):
    if "cbitclose" in line or "cbitopen" in line:
        cbit_names = getCbitName(line)
        return cbit_names


