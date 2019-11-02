from random import randrange, shuffle
import csv
import json
from datetime import date


# assign staff to the site/shift/roster. 
# calls get_staff to get the staff list from the switchboard file.
# calls build_vacant_roster which creates a vacant roster based on off the site
# and shift policies. 
# 
def build_roster(site, staff, sitePolicy):
    staffFileName = staff
    for items in sitePolicy['shifts']:
        # get shift so we can build the staff list
        shift = items["name"]
        staff, callOffList = get_staff(staffFileName, shift, site)
        numberOfStaff = len(staff)

        mustFillRoster = build_vacant_roster(shift, sitePolicy, 1)
        overFlowRoster = build_vacant_roster(shift, sitePolicy, 2)

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
        fileName = site + " " + shift  
        write_roster(fileName, fullRoster, callOffList, numberOfStaff, staff, 'csv')
    
    
    return fullRoster, staff, callOffList


# called by build_roster
# builds the roster based on the policy for that site and shift.
# returns an empty roster ready for assignments. 
def build_vacant_roster(shift_roster, roster, priority):
    blank_roster = []
    if priority == 1:
        fill = "mustFillPosts"
    else:
        fill = "overflowPosts"
    
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


# create a list of staff and a list of call offs from Shift Board input file.
# These lists will be used as input to build_roaster 

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
        if len(callOffList) == 0:
            callOffList.insert(0,"No Call Offs")
        else:
            callOffList.insert(0,"Call Offs:")

    return staffList, callOffList


# write the filled in roster to either a csv or tab file. 
def write_roster(roster_file, roster, callOffList, numberOfStaff, staff, rosterType='csv'):
    shiftName = roster_file
    today = date.today()
    d = today.strftime("%m/%d/%y")
    # create either a csv or tabbed file
    if rosterType == 'csv':
        fileType = "{}, {}\n"
        fileExtension = '.csv'
    else:
        fileType = "{}\t{}\n"
        fileExtension = '.txt'

    roster_file = "./output-files/" + roster_file + fileExtension
    with open(roster_file, 'w') as f:
        f.write("{} - {}\n".format("Computer generated roster for: " + shiftName, d ))
        f.write("{}\n".format("Number Of Available Staff: " + str(numberOfStaff)))
        
        i=0
        for name in callOffList:
            if i == 0:
                f.write("{}\n".format(name))
            else:
                f.write("{}. {}\n".format(i, name))
            i+=1
        f.write(fileType.format("POST","NAME" ))
        for position in roster:
            f.write(fileType.format(position[0],position[1]))

        if len(staff) > 0:
            f.write(fileType.format("Unassinged Staff: "))
            for name in staff:
               f.write("{}\n".format(name)) 


 
# Generate the shift roasters by placing the staff randomly in positions.
# This will eliminate any bias as to where the staff is posted.
# skb

def main():
    print("*** Start ***")

    # staff list 
    staff = "./input-files/ShiftboardShifts-74.csv" 

    # get the policies
    with open('./input-files/policy.json') as json_file:
        roster_policies = json.load(json_file)           
    
    policies =  roster_policies[0]["sites"]

    for sitePolicy in policies:
        build_roster(sitePolicy['name'], staff, sitePolicy) 
        
    print("*** End ***")
if __name__ == "__main__":
  main()
