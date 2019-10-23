from random import randrange, shuffle
import csv

must_fill = []

# create the types hat

# create the staff hat

# create the must-fill hat

# process the must-fill hat. If there's anything left over then
# create the what's left hat and process it 

roster_policy  = [  
    {
        "shift" : [ { 
            "name" :  "5:00AM - 2:00PM",
            "groups" :  [ {
                "name" : "Gates", 
                "mustFillPosts" : ["Charlie 1","Charlie 2"],
                "overflowPosts" : ["Charlie 3"]
            } , {
                "name" : "Booths", 
                "mustFillPosts" : ["Wofle 1","Wofle 2","Tantau 1"],
                "overflowPosts" : []
            } , { 
                "name" : "Mobiles" , 
                "mustFillPosts" : ["Paul 1", "Paul 2"],
                "overflowPosts" : ["Paul 3", "Paul 4"]
            } , {
                "name" : "Edwards", 
                "mustFillPosts" : [],
                "overflowPosts" : ["Edward 1","Edward 2","Edward 3","Edward 4","Edward 5"]
            } ] 
        } , 
        {
            "name" :  "7:00AM - 4:00PM",
            "groups" :  [ {
                "name" : "Georges", 
                "mustFillPosts" : ["George 1","George 2","George 3","George 4","George 5","George 6","George 7"],
                "overflowPosts" : []
            } , {
                "name" : "Roberts", 
                "mustFillPosts" : ["Robert 1","Robert 2"],
                "overflowPosts" : ["Tantau 2"]
            } , { 
                "name" : "Mobiles" , 
                "mustFillPosts" : ["Paul 1", "Paul 2"],
                "overflowPosts" : ["Paul 3", "Paul 4","Paul 5"]
            } , {
                "name" : "Edwards", 
                "mustFillPosts" : ["Edward 1"],
                "overflowPosts" : ["Edward 2","Edward 3","Edward 4","Edward 5","Edward 6"]
            } ]
        } , 
        {
            "name" :  "1:00PM - 10:00PM",
            "groups" : [ {
                "name" : "Gates", 
                "mustFillPosts" : ["Charlie 1","Charlie 2","Charlie 3"],
                "overflowPosts" : []
            } , {
                "name" : "Booths", 
                "mustFillPosts" : ["Wofle 1","Wofle 2","Tantau 1"],
                "overflowPosts" : []
            } , { 
                "name" : "Mobiles" , 
                "mustFillPosts" : ["Paul 1", "Paul 2"],
                "overflowPosts" : ["Paul 3", "Paul 4"]
            } , {
                "name" : "Edwards", 
                "mustFillPosts" : [],
                "overflowPosts" : ["Edward 1","Edward 2","Edward 3","Edward 4","Edward 5"]
                } ]
        }, 
        {
            "name" :  "9:00PM - 6:00AM",
            "groups" :  [ {
                "name" : "Georges", 
                "mustFillPosts" : ["George 1","George 2","George 3","George 4","George 5","George 6","George 7"],
                "overflowPosts" : []
            } , {
                "name" : "Roberts", 
                "mustFillPosts" : ["Robert 1","Robert 2"],
                "overflowPosts" : ["Tantau 2"]
            } , { 
                "name" : "Mobiles" , 
                "mustFillPosts" : ["Paul 1", "Paul 2"],
                "overflowPosts" : ["Paul 3", "Paul 4","Paul 5"]
            } , {
                "name" : "Edwards", 
                "mustFillPosts" : ["Edward 1"],
                "overflowPosts" : ["Edward 2","Edward 3","Edward 4","Edward 5","Edward 6"]
            } ]
        }]        
    }
]
def get_blank_rosters(shift_roster, roster, priority):
    if priority == 1:
        fill = "mustFillPosts"
    else:
        fill = "overflowPosts"
    blank_roster = []

    for shift in roster[0]["shift"]:
        i = 0
        if shift["name"] == shift_roster:
            posts = shift["groups"]
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

def get_staff(filename, shift):
    staffList = []
    callOffList = []
    with open(filename, newline='') as csvfile:
        shiftsRoaster = csv.reader(csvfile, delimiter=',', quotechar='|')
        for name in shiftsRoaster:
            # print("0-{} 1-{} 2-{} 3-{} 4-{} 5-{} 6-{} 9-{}".format(name[0],name[1],name[2],name[3],name[4],name[5],name[6],name[9]))
            if name[5] == shift and name[9] != 'CALL OFF':
                staffList.append(name[6])
            elif name[5] == shift and name[9] == 'CALL OFF':
                # callOffList.append("Call Off")
                callOffList.append(name[6])
    return staffList, callOffList

def write_roster(roster_file, roster, callOffList):
    roster_file = "./output-files/" + roster_file + ".csv"
    with open(roster_file, 'w') as f:
        f.write("%s,%s\n" % ("POST","NAME"))
        for position in roster:
            f.write("%s,%s\n" % (position[0],position[1]))
        f.write("%s\n" % ("Call Off List"))
        for name in callOffList:
            f.write("%s,%s\n" % (" ",name))


def build_roster(shift, staff):
    staff, callOffList = get_staff(staff, shift)

    # create staff list by shift
    
    mustFillRoster = get_blank_rosters(shift, roster_policy, 1)
    shuffle(mustFillRoster)
    overFlowRoster = get_blank_rosters(shift, roster_policy, 2)
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


def main():
    print("*** Start ***")
    leftoverStaff = []
    # staff = "really-small-input.csv"
    # staff = "small-input.csv"
    staff = "./input-files/today1.csv"

    # shift = "shift5"

    shifts = ['5:00AM - 2:00PM','7:00AM - 4:00PM','1:00PM - 10:00PM','9:00PM - 6:00AM']
    for shift in shifts:
        (roster, leftoverStaff, callOffList) = build_roster(shift, staff) 
        write_roster(shift, roster, callOffList)
        # for p in roster:
            # print("{},{}".format(p[0], p[1]))    


        # Check to see if there's any leftover staff
        if len(leftoverStaff) > 0:
            print("Unassigned")
            for name in leftoverStaff:
                print("  {} ".format(name))     
    print("*** End ***")

if __name__ == "__main__":
  main()