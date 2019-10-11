from random import randrange, shuffle
# from csv import writer
import csv



# create the types hat

# create the staff hat

# create the must-fill hat

# process the must-fill hat. If there's anything left over then
# create the what's left hat and process it 


rosters = {
    "day_priority_roster" : {
        "Gates" : {
            "Charlie 1" : "Vacant",
            "Charlie 2" : "Vacant",
            "Charlie 3" : "Vacant"
        },
        "Booths": {
            "Wofle 1" : "Vacant",
            "Wofle 2" : "Vacant",
            "Tantau 1" : "Vacant"
        },
        "Mobiles" : {
            "Paul 1" : "Vacant"
        }
    },
    "day_roster" : {
        "Booths": {
            "Wofle 3" : "Vacant",
            "Tantau 2" : "Vacant"
        },
        "Mobiles" : {
            "Paul 2" : "Vacant",
            "Paul 3" : "Vacant",
            "Paul 4" : "Vacant"
        },
        "Edwards" : {
            "Edward 1" : "Vacant",
            "Edward 2" : "Vacant",
            "Edward 3" : "Vacant",
            "Edward 4" : "Vacant",
            "Edward 5" : "Vacant"
        }
    }
} 
 
def merge(d1, d2):
    d2.update(d1) 
    for r in rosters["day_roster"]:
        for p in rosters["day_roster"][r]:
            print("{} - {} - {}".format(rosters["day_roster"],r,p))
                

def create_rosters(staff, roster):
    shuffle(staff)
    
    # fill the rosters
    shift_roster = rosters[roster]
    for position_type in shift_roster:
        for position in shift_roster[position_type]:
            if len(staff) != 0:
                shift_roster[position_type][position] = staff.pop()
            else:
                print("No more staff")
                return
    return 

def create_list(filename):
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
    staff = create_list("large-input.csv")
    # build the post list

    create_rosters(staff,"day_priority_roster")
    if len(staff) > 0:
        create_rosters(staff,"day_roster")

    # merge rosters

    merge(rosters["day_priority_roster"],rosters["day_roster"])
    # shift_rosters = list(rosters.keys()) 


    
    # write_roster("day-p1-roster.csv", rosters["day_priority_roster"])
    # write_roster("day-p2-roster.csv", rosters["day_roster"])
    
    print("done")

if __name__ == "__main__":
  main()