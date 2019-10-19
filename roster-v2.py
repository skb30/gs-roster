from random import randrange, shuffle
# from csv import writer
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
            "name" :  "day",
            "groups" :  [ {
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
        } , 
        {
            "name" :  "swing",
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
            "name" :  "graveyard",
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
        } ]
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


def get_staff(filename):
    filelist = []

    with open(filename, newline='') as csvfile:
        shiftsRoaster = csv.reader(csvfile, delimiter=',', quotechar='|')
        for name in shiftsRoaster:
            filelist.append(name[0])

    return filelist
def write_roster(roster_file, roster):
    with open(roster_file, 'w') as f:


        f.write("%s,%s\n" % ("POST","NAME"))
        for position in roster:
            f.write("%s,%s\n" % (position[0],position[1]))


def main():
    print("*** Start ***")

    # staff = get_staff("really-small-input.csv")
    # staff = get_staff("small-input.csv")
    staff = get_staff("large-input.csv")
    shuffle(staff)
    mustFillRoster = get_blank_rosters("day", roster_policy, 1)
    overFlowRoster = get_blank_rosters("day", roster_policy, 2)
    
    row            = 0
    fullRoster     = []
    # sizeOfStaff    = len(staff)
    sizeOfMustFill = len(mustFillRoster)
    sizeOfOverFlow = len(overFlowRoster)
    combined       = sizeOfMustFill + sizeOfOverFlow

    if len(staff) <= len(mustFillRoster): # More positions to fill than staff so we'll fill the must-fill
        shuffle(mustFillRoster)

        while len(staff) > 0:
            mustFillRoster[row][1] = staff.pop()
            row += 1
        mustFillRoster.sort()
        fullRoster = mustFillRoster + overFlowRoster

    elif len(staff) <= combined: 
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
        # We have more staff than positions
        fullRoster = mustFillRoster + overFlowRoster 
        shuffle(fullRoster)
        sizeOfFullRoster = len(fullRoster)
        while sizeOfFullRoster > 0:
            fullRoster[row][1] = staff.pop()
            row += 1
            sizeOfFullRoster -= 1
        fullRoster.sort()    

    write_roster("new-roster.csv", fullRoster) 
    for p in fullRoster:
        print("{},{}".format(p[0], p[1]))    
    print("*** End ***")

if __name__ == "__main__":
  main()