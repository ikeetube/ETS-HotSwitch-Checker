import numpy as np
import freader
import json 
#import file_def

file_name = freader.file_name
log_file = freader.log_file

file=open(log_file,"w")
class Resource(object):
    
    def __init__(self,name):
        self.name = name
        self.fvalue = 0
        self.mode = "NaN"
        self.relays = []

    def addRelay(self,relay):
        self.relays.append(relay)
        #Feedback to user linked relays
        print(relay, " linked to ", self.name, file=open(log_file,"a"))

    def setMode(self, mode):
        self.mode = mode
        print(self.name, "set to", self.mode, file=open(log_file,"a"))

    def setValue(self, value):
        self.fvalue = value
        print(self.name, "value = ", self.fvalue, file=open(log_file,"a"))
        

#sys.stdout = open(file_name.strip(".cpp"), "w")

############################## Stage 1 ##############################
#               Link relays to forcing resources                    #
#####################################################################
#Start of Program
print("\nReading cpp file to get all cbits and forcing used..\n")
print("\nReading cpp file to get all cbits and forcing used..\n", file=open(log_file,"a"))
forcing_res = freader.getAllForcing(file_name).tolist()
cbits_list = freader.getAllCbits(file_name).tolist()
#choices = np.concatenate((["None"],cbits_list)).tolist()
choices = ["None"] + cbits_list
print("Reources: ", forcing_res)
print("Reources: ", forcing_res, file=open(log_file,"a"))
print("Cbits: ", cbits_list, "\n")
print("Cbits: ", cbits_list, "\n", file=open(log_file,"a"))

#Create objects from forcing_res
resources_obj = []
for i in forcing_res:
    resources_obj.append(Resource(i))

for res in resources_obj:
    res_name = res.name
    res_rels = res.relays

    loop = 1
    while loop==1:
        if loop==1:
            print(res_name)
            print(res_name, file=open(log_file,"a"))
            print("Which relays are connnected to this resource?")
            print("Which relays are connnected to this resource?", file=open(log_file,"a"))
            print("(separate each relay with a comma)")
            print("(separate each relay with a comma)", file=open(log_file,"a"))

            #Prints relay/cbit choices
            for rel in choices:
                rel_index = choices.index(rel)
                print("[", rel_index, "] ", rel)
                print("[", rel_index, "] ", rel, file=open(log_file,"a"))

            #Gets user input
            rel_input = input("input: ")
            #Converts input to list
            relays_sel = np.unique(rel_input.split(",")).tolist()
            #Remove empty values
            relays_sel = list(filter(lambda x: x != "", relays_sel))
            print("You selected: ",relays_sel)
            print("You selected: ",relays_sel, file=open(log_file,"a"))

            #Check if inputs are valid by comparing inputs to choices index
            invalid = 0
            for relay_num in relays_sel:
                if relay_num.isnumeric()==True:
                    if int(relay_num) > len(choices)-1 or int(relay_num) < 0:
                        print("Input [",relay_num, "] is invalid.")
                        print("Input [",relay_num, "] is invalid.", file=open(log_file,"a"))
                        invalid = 1
                elif relay_num.isnumeric()==False:
                    print("Input [",relay_num, "] is invalid.")
                    print("Input [",relay_num, "] is invalid.", file=open(log_file,"a"))
                    invalid = 1
            if len(relays_sel)==0:
                print("No input detected.")
                print("No input detected.", file=open(log_file,"a"))
                relay_num=0
                invalid = 1      

            if invalid==1:
                print("\nTry again...")
                print("\nTry again...", file=open(log_file,"a"))
                loop=1
            else:
                if '0' in relays_sel:
                    res.addRelay("None")
                    print("NO RELAY linked to ",res_name)
                    print("NO RELAY linked to ",res_name, file=open(log_file,"a"))
                else:
                    for relay_num in relays_sel:
                        rel_linked = choices[int(relay_num)]
                        #Store relays selected in resource object
                        res.addRelay(rel_linked)
                    #res.initRelays()
                loop=0    
            print("\n")
            print("\n", file=open(log_file,"a"))

#print(resources_obj)
print("Done scanning", file_name, "for all forcing and cbits")
print("Done scanning", file_name, "for all forcing and cbits", file=open(log_file,"a"))

config = {}
for res in resources_obj:
    config['resources'] = []
    config['resources'].append({
        'name': res.name,
        'relays': res.relays
    })

config_file = MEDIA_ROOT + '/config/' + file_name + '_config.txt'
print(config_file)

with open(config_file, 'w') as outfile:
    json.dump(config, outfile)

with open(config_file) as json_file:
    data = json.load(json_file)
    for res in data['resources']:
        print('Name: ' + res['name'])
        print('Relays: ' + str(res['relays']))
        print('')
############################## Stage 2 #############################
#                     Scan cpp file for cbitclose/open                    #
####################################################################
print("\n\nScanning file per line to check for forcing and cbitclose/open", file=open(log_file,"a"))
f = open(file_name, "r")
for num, line in enumerate(f):
    line = line.partition("//")[0]
    num += 1
 
    #Check for Forcing
    res_name = freader.checkForcing(line)
    if res_name != None:
        print("\nScanning line: ", num, file=open(log_file,"a"))
        for res in resources_obj:
            if res_name==res.name:
                res.setMode(freader.getMode(line))
                res.setValue(freader.getFValue(line))

    #Monitor cbitclose/open
    cbit_names = freader.checkCbit(line)
    if cbit_names != None: 
        print("\nScanning line: ", num, file=open(log_file,"a"))
        valid = True
        if "cbitclose" in line or "cbitopen" in line:
            for cbit in cbit_names:
                for res in resources_obj:
                    if cbit in res.relays:
                        try:
                            float(res.fvalue)
                        except ValueError:
                            print("Not a float:", res.fvalue)
                            valid = False
                        if valid:
                            if float(res.fvalue) > 0.01 or float(res.fvalue) < -0.01:
                                print("***{Please check", res.name, "during cbitclose/open @ line [",num,"] }***")
                                print("***{Please check", res.name, "during cbitclose/open @ line [",num,"] }***", file=open(log_file,"a"))
                            else:
                                print("PASS", line, file=open(log_file,"a"))

#sys.stdout.close()