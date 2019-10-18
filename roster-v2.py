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
                "name" : "Gates", 
                "mustFillPosts" : ["Charlie 1","Charlie 2","Charlie 3"],
                "overflowPosts" : []
            } , {
                "name" : "Booths", 
                "mustFillPosts" : ["Wofle 1","Wofle 2","Tantau 1"],
                "overflowPosts" : ["Tantau 2"]
            } , { 
                "name" : "Mobiles" , 
                "mustFillPosts" : ["Paul 1", "Paul 2"],
                "overflowPosts" : ["Paul 3", "Paul 4","Paul 5"]
            } , {
                "name" : "Edwards", 
                "mustFillPosts" : ["Scott 1"],
                "overflowPosts" : ["Edward 1","Edward 2","Edward 3","Edward 4","Edward 5"]
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
        print(shift["name"])
        i = 0
        if shift["name"] == 'day':
            
            posts = shift["groups"]
            # print(shiftName.upper())
            for post in posts:
                mustFillPosts = post[fill]
                size = len(mustFillPosts)
                if size != 0:
                    blank_roster.append([]) # create a row 
                    size -= 1
                
                for unit in mustFillPosts:
                    blank_roster[i].append(unit)
                    blank_roster[i].append("Vacant")
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
        for position in roster.keys():
            f.write("%s\n" %position)
            for unit in roster[position]:
                f.write("%s,%s\n" % (unit, roster[position][unit]))


def main():
    staff = get_staff("large-input.csv")

    print("*** Start ***")
    p = get_blank_rosters("day", roster_policy, 1)
    for item in p:
        print(item)
    # get the must fill positions for day shift



    print("*** End ***")
    # create_rosters(staff, roster_policy, 2)

    
    print("*** done ***")

if __name__ == "__main__":
  main()