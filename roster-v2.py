from random import randrange, shuffle
import csv
import json
from datetime import date
import os
import re

# assign staff to the site/shift/roster. 
# calls get_staff to get the staff list from the switchboard file.
# calls build_vacant_roster which creates a vacant roster based on off the site
# and shift policies. 
# 
messageLog = []
# pathToHome = os.getenv("HOME") + "/"


def build_roster(pathToRosterFolder, site, shiftboard, shiftBoardDate, sitePolicy, rosterType='txt'):
    staffFileName = shiftboard
    staff = shiftboard
    write_to_log("Building Roster for: {}".format(site))
  
    for items in sitePolicy['shifts']:

        # get shift so we can build the staff list
        shift = items["name"]
        staff, callOffList = get_staff(staffFileName, shift, site)
        numberOfStaff = len(staff)
        write_to_log("\tAvailable staff for shift {} is: {}".format(shift, numberOfStaff))
        mustFillRoster = build_vacant_roster(shift, sitePolicy, 1)
        overFlowRoster = build_vacant_roster(shift, sitePolicy, 2)

        row            = 0
        fillRoster     = []
        sizeOfMustFill = len(mustFillRoster)
        sizeOfOverFlow = len(overFlowRoster)
        combined       = sizeOfMustFill + sizeOfOverFlow
        unassigned     = []
    
        if len(staff) <= len(mustFillRoster): # More positions to fill than staff so we'll fill the must-fill first
            while len(staff) > 0:
                mustFillRoster[row][1] = staff.pop()
                row += 1
            fillRoster = mustFillRoster + overFlowRoster

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
            fillRoster = mustFillRoster + overFlowRoster
        else: # We have more staff than positions so let's fill them all and report unassigned
            fillRoster = mustFillRoster + overFlowRoster 
            shuffle(fillRoster)
            sizeOfFillRoster = len(fillRoster)
            while sizeOfFillRoster > 0:
                fillRoster[row][1] = staff.pop()
                row += 1
                sizeOfFillRoster -= 1

            # collect staff that didn't get assigned to a post
            while len(staff): 
                unassigned.append(staff.pop())
                    

        fillRoster.sort() 
        fileName = site + " " + shift  
        write_roster(pathToRosterFolder, fileName, fillRoster, callOffList, numberOfStaff, unassigned, shiftBoardDate, rosterType)
    write_to_log("Completed roster for: {}.".format(site))  
    return 


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
                    blank_roster[i].append("SIS Assist") # add name column to the row
                    i += 1
                    if size != 0:
                        blank_roster.append([])
                        size -= 1
    return blank_roster

# called by build_roster
# create a list of staff and a list of call offs from Shift Board input file.
# These lists will be used as input to build_roaster 

def get_staff(shiftBoardRoster, shift, site):

    staffList = []
    callOffList = []
    callOff = "CALL OFF"
        
    for row in shiftBoardRoster:

        # strip out the quotes
        roleFromFile        = row[4].strip('\"')
        shiftFromFile       = row[5].strip('\"')
        firstNameFromFile   = row[7].strip('\"')
        lastNameFromFile    = row[8].strip('\"')
        subjectFromFile     = row[9].strip('\"')

        if roleFromFile == site:
            # see if we have a name otherwise skip to next record
            if len(firstNameFromFile) > 0:
                fullName = firstNameFromFile + " " + lastNameFromFile
                # if the shift from the file matches the shift we're processing    
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
   
    return staffList, callOffList, 

# DRY print helper     
def writeExceptionList (f, exceptionList):
    i=0
    for name in exceptionList:
        if i == 0:
            f.write("{}\n".format(name))
        else:
            f.write("{}. {}\n".format(i, name))
        i+=1
    return

# called by build_roster
# write the filled in roster to either a csv or tab file. 
def write_roster(pathToRosterFolder, shiftName, roster, callOffList, numberOfStaff, unassignedStaff, shiftBoardDate, rosterType='csv'):
    
    # today = date.today()
    # d = today.strftime("%m/%d/%y")


    # create either a csv or tabbed file
    if rosterType == 'csv':
        fileType = "{}, {}\n"
        fileExtension = '.csv'
    else:
        fileType = "{}\t{}\n"
        fileExtension = '.txt'

    writeableRoster = shiftName + fileExtension
    with open(pathToRosterFolder + "/" + writeableRoster, 'w') as f:
        f.write("{} , {}\n".format("Roster for " + shiftName, shiftBoardDate))
        f.write("{}\n".format("Number Of Available Staff: " + str(numberOfStaff)))
        
        # call print helper
        writeExceptionList(f, callOffList)
        # writeExceptionList(f, exceptions)

        f.write(fileType.format("POST","NAME" ))
        for position in roster:
            f.write(fileType.format(position[0],position[1]))

        if len(unassignedStaff) > 0:
            f.write("Unassigned Staff:\n".format())
            for name in unassignedStaff:
               f.write("{}\n".format(name)) 

# get the date out of the shiftboard file to display to 
# the user

def get_input_date(shiftBoardRoster):
    dateFromFile = "Date not found in shiftboard file"

    # look for the shiftboard date using regex
    p = re.compile(r'^\d\d\d\d-\d\d-\d\d')
    # p.match('2019-11-11')
    # print( p.match('2019-11-11,'))


    for row in shiftBoardRoster:
        dateFromFile = row[2].strip('\"')
        if p.match(dateFromFile):
            break
    return dateFromFile

# log console messages to file 
def write_to_log(message):
    print(message)
    messageLog.append(message)
    return messageLog

def create_output_folder(path):
    # create the output folder on the users desktop
    # path = pathToHome + "Desktop/Rosters"
    try:
        os.mkdir(path)
    except OSError:
        # pSass
        print ("Rosters directory already exists on users desktop")
    else:
        write_to_log("Successfully created the directory %s " % path)
   


# Generate the shift roasters by placing the staff randomly in positions.
# This will eliminate any bias as to where the staff is posted.
# skb

def load_input(filename, shiftBoardRoster, inputFolder = 'Downloads' ):

    savedPwd = os.getcwd()
    pathToHome = os.getenv("HOME") + "/"
    os.chdir(pathToHome + inputFolder)

    with open(filename, newline='') as csvfile:
        shiftsRoaster = csv.reader(csvfile, delimiter=',', quotechar='|')
    
        for row in shiftsRoaster:
            shiftBoardRoster.append(row)

    os.chdir(savedPwd)
    return shiftBoardRoster


def main():

    
    # get the policies from json
    with open('./input-files/policy.json') as json_file:
        roster_policies = json.load(json_file)

    pathToHome = os.getenv("HOME") + "/"
    pathToRosterFolder = pathToHome + "Desktop/Rosters/"
    create_output_folder(pathToRosterFolder)

    shiftBoardRoster = []
    write_to_log("*** Auto generate rosters started ***")
    shiftBoardInput = 'ShiftboardShifts.csv'
    shiftBoardRoster = load_input(shiftBoardInput, shiftBoardRoster)
    shiftBoardDate = get_input_date(shiftBoardRoster)
  
    userInput = input("Process shiftboard " + shiftBoardDate + " [y/n]? >")
    if userInput.lower() != 'y':
        write_to_log("*** Auto generate rosters ended ***")
        return  

    # contains the policies for fulling posts at each site
    policies =  roster_policies[0]["sites"]

    # now that we have the polices for each site lets process them
    for sitePolicy in policies:
        build_roster(pathToRosterFolder, sitePolicy['name'], shiftBoardRoster, shiftBoardDate, sitePolicy, rosterType='txt') 
        

        
    write_to_log("*** Auto generator completed ***")

    # add the console log to rosters folder
    with open(pathToHome + "Desktop/Rosters/roster-log.txt", 'w') as f:
        f.write("Console Log\n")
        for row in messageLog:
            f.write(row + "\n")
if __name__ == "__main__":
  main()
