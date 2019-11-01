from random import randrange, shuffle
import csv
import json

# Generate the shift roasters by placing the staff randomly in positions.
# This will eliminate any bias as to where the staff is posted.
# skb

# ds consdier standardizing on format for variable names
# ds and function names. Industry standard seems to be camelCase


# dgs this seems out of place here
# dgs consider moving to inside of main and pass to fuctions
must_fill = []

def get_blank_rosters(shift_roster, roster, priority):
    if priority == 1:
        fill = "mustFillPosts"
    else:
        fill = "overflowPosts"
    blank_roster = []

    for policy in roster['shifts']:
        i = 0
        if policy["name"] == shift_roster:
            posts = policy["groups"]
            for post in posts:
                mustFillPosts = post[fill]
                size = len(mustFillPosts)
                if size != 0:
                    blank_roster.append([]) # create a roster row
                    size -= 1

                for unit in mustFillPosts:
                    blank_roster[i].append(unit) # add unit column to the row
                    blank_roster[i].append("Vacant") # add name column to the row
                    i += 1
                    if size != 0:
                        blank_roster.append([])
                        size -= 1
    return blank_roster

def get_staff(filename, shift, site):
    staffList = []
    callOffList = []
    callOff = "CALL OFF"
    with open(filename, newline='') as csvfile:
        shiftsRoaster = csv.reader(csvfile, delimiter=',', quotechar='|')
        for row in shiftsRoaster:

            # strip out the quotes

            roleFromFile        = row[4].strip('\"')
            shiftFromFile       = row[5].strip('\"')
            firstNameFromFile   = row[7].strip('\"')
            lastNameFromFile    = row[8].strip('\"')
            subjectFromFile     = row[9].strip('\"')

            if roleFromFile == site:
                if len(firstNameFromFile) > 0:
                    # print("4-{} 5-{} 7-{} 8-{} 9-{}".format(name[4],name[5],name[7],name[8],name[9]))
                    fullName = firstNameFromFile + " " + lastNameFromFile

                if shiftFromFile == shift:
                    if subjectFromFile == callOff:
                        callOffList.append(fullName)
                    elif subjectFromFile != callOff:
                        staffList.append(fullName)


        shuffle(staffList)

    return staffList, callOffList

# -------------------------
# ds need pramble to tell what this funciton is doing
# ds preable should be no more than 1 line
# ds also preable should describe inputs and outputs
def write_roster(roster_file, roster, callOffList):
    shiftName = roster_file
    roster_file = "./output-files/" + roster_file + ".txt"
    with open(roster_file, 'w') as f:
        f.write("%s\n" % ("Shift: " + shiftName ))
        f.write("%s\t%s\n" % ("POST","NAME" ))
        for position in roster:
            f.write("%s\t%s\n" % (position[0],position[1]))
        f.write("%s\n" % ("Call Off List"))
        for name in callOffList:
            f.write("%s\t%s\n" % (" ",name))
            # print("call name {}".format(name))

    
def build_roster(site, staff, sitePolicy):
    staffFileName = staff
    for items in sitePolicy['shifts']:
        # get shift so we can build the staff list
        shift = items["name"]
        staff, callOffList = get_staff(staffFileName, shift, site)

        mustFillRoster = get_blank_rosters(shift, sitePolicy, 1)
        shuffle(mustFillRoster)
        overFlowRoster = get_blank_rosters(shift, sitePolicy, 2)
        shuffle(overFlowRoster)
        
        row            = 0
        fullRoster     = []
        sizeOfMustFill = len(mustFillRoster)
        sizeOfOverFlow = len(overFlowRoster)
        combined       = sizeOfMustFill + sizeOfOverFlow
    
        if len(staff) <= len(mustFillRoster): # More positions to fill than staff so we'll fill the must-fill first
            while len(staff) > 0:
                mustFillRoster[row][1] = staff.pop()
                row += 1
            fullRoster = mustFillRoster + overFlowRoster

        elif len(staff) <= combined: # leftover staff so let's fill overflow
                while sizeOfMustFill > 0:
                    mustFillRoster[row][1] = staff.pop()
                    row += 1
                    sizeOfMustFill -= 1
                row = 0 
        
                if len(staff) >= 0:
                    while sizeOfOverFlow > 0 and len(staff) > 0:
                        overFlowRoster[row][1] = staff.pop()
                        row += 1
                        sizeOfOverFlow -= 1    
                fullRoster = mustFillRoster + overFlowRoster
        else:
            # We have more staff than positions so let's fill them all
            fullRoster = mustFillRoster + overFlowRoster 
            shuffle(fullRoster)
            sizeOfFullRoster = len(fullRoster)
            while sizeOfFullRoster > 0:
                fullRoster[row][1] = staff.pop()
                row += 1
                sizeOfFullRoster -= 1   
    fullRoster.sort() 
    return fullRoster, staff, callOffList


# -------------------------
# ds need pramble to tell what this funciton is doing
# ds preable should be no more than 1 line
# ds also preable should describe inputs and outputs
def main():
    print("*** Start ***")
    leftoverStaff = []
    staff = "./input-files/ShiftboardShifts-8.csv" 

  
    # get the policies
    with open('./input-files/policy.json') as json_file:
        roster_policies = json.load(json_file)           

#     #TODO grab from json
#     #TODO add site to json
#     #TODO rework 141
    
    policies =  roster_policies[0]["sites"]

    for sitePolicy in policies:
        if sitePolicy['name'] == 'Apple Park':
            (roster, leftoverStaff, callOffList) = build_roster(sitePolicy['name'], staff, sitePolicy) 

            # write_roster(shift, roster, callOffList)    

#         # Check to see if there's any leftover staff
#         if len(leftoverStaff) > 0:
#             print("Over Staff")
#             for name in leftoverStaff:
#                 print("  {} ".format(name))  
                

    print("*** End ***")
if __name__ == "__main__":
  main()
