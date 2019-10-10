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
    #
    #



def init_posts(shift):

    days = {
    "Gates" : {
        "Charlie 1": "Vacant",
        "Charlie 2": "Vacant",
        "Charlie 3": "Vacant",
        "fill" : "3"

    },
    "Booths": {
        "Wofle 1": "Vacant",
        "Wofle 2": "Vacant",
        "Tantau 1": "Vacant",
        "fill" : "3"
    },
    "Mobiles" : {
        "Paul 1" : "Vacant",
        "Paul 2" : "Vacant",
        "Paul 3" : "Vacant",
        "Paul 4" : "Vacant",
        "fill" : "2"
    },
    "Edwards": {
        "Edward 1": "Vacant",
        "Edward 2": "Vacant",
        "Edward 3": "Vacant",
        "Edward 4": "Vacant",
        "Edward 5": "Vacant",
        "fill" : "0"
    }

}
    swing = {
    "Mobiles" : {
        "Paul 1" : "Vacant",
        "Paul 2" : "Vacant",
        "Paul 3" : "Vacant",
        "1" : "ID"
    },
    "Gates" : {
        "Charlie 1": "Vacant",
        "Charlie 2": "Vacant",
        "Charlie 3": "Vacant",
        "5D": "Vacant",
        "1C": "Vacant",
        "7D": "Vacant",
        "2": "ID"
    },
    "Booths": {
        "Wofle 1": "Vacant",
        "Wofle 2": "Vacant",
        "Wofle 3": "Vacant",
        "Tantau 1": "Vacant",
        "Tantau 2": "Vacant",
        "3": "ID"
    },
    "Breakers": {
        "Edward 1": "Vacant",
        "Edward 2": "Vacant",
        "Edward 3": "Vacant",
        "Edward 4": "Vacant",
        "Edward 5": "Vacant",
        "Edward 6": "Vacant",
        "Edward 7": "Vacant",
        "Edward 8": "Vacant",
        "4": "ID"
    }
}   
    return days
def create_roster(staff, posts):

    shuffle(staff)
    must_fill = {}
    
    # get the group of positions 
    position_types = list(posts.keys()) # convert to list for shuffle

    # shuffle(position_types)
    
    i = 0
    # create the must_fill hat
    for position_type in position_types:
        must_fill[position_type] = posts[position_type]["fill"]

    # process the "must-fill" hat
     
    for position_type, numberToFill in must_fill.items():

        # get the positions for this type
        positions = list(posts[position_type])
        j = 0
        if i < len(staff):
            while j < int(numberToFill):
                posts[position_type][positions[j]] = staff.pop()
                # staff.remove(staff[i])
                i += 1
                j += 1
        else:
            print("No more staff.")
        # print(x, y)

    return posts

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
    dayShift = init_posts("Day")
    staff = create_list("small-input.csv")
    # build the post list
    roster = create_roster(staff, dayShift)

    write_roster("roster-day.csv", roster)
    
    print("done")

if __name__ == "__main__":
  main()