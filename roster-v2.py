from random import randrange, shuffle
# from csv import writer
import csv



# create the types hat

# create the staff hat

# create the must-fill hat

# process the must-fill hat. If there's anything left over then
# create the what's left hat and process it 


# logic
    # 1) create the must-fill hat from the types hat
    #   add the type and the position
    #
    #
    #
    #
    # "Paul 3", "Paul 4"
    #["Edward 1","Edward 2","Edward 3","Edward 3","Edward 5"],

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
                return roster
    return roster

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
                if roster[position][unit] != 'Fill':
                    f.write("%s,%s\n" % (unit, roster[position][unit]))

def main():
    # constructor 
    # dayShiftPriority = init_posts("Day")
    staff = create_list("small-input.csv")
    # build the post list
    day_priority_roster = create_rosters(staff,"day_priority_roster")
    if len(staff) > 0:
        day_roster = create_rosters(staff,"day_roster")

    write_roster("day-p1-roster.csv", day_priority_roster)
    write_roster("day-p2-roster.csv", day_roster)
    
    print("done")

if __name__ == "__main__":
  main()