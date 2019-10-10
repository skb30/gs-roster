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
        "post" : ["Charlie 1","Charlie 2","Charlie 3"],
        "fill" : "3"

    },
    "Booths": {
        "post" : ["Wofle 1","Wofle 2","Tantau 1"],
        "fill" : "3"
    },
    "Mobiles" : {
        "post" : ["Paul 1", "Paul 2", "Paul 3", "Paul 4"],
        "fill" : "2"
    },
    "Edwards": {
        "post" : ["Edward 1","Edward 2","Edward 3","Edward 3","Edward 5"],
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
    
    # print(posts["Gates"]["post"][1])

    # get the group of positions 
    position_types = list(posts.keys()) # convert to list for shuffle

    shuffle(position_types)
    
    staffCount = 0
    # create the must_fill hat
    for position_type in position_types:
        must_fill[position_type] = posts[position_type]["fill"]

    # process the "must-fill" hat
     
    for position_type, numberToFill in must_fill.items():
    #     print("position_type {} numberToFill {} ".format(position_type, numberToFill))
        # get the positions for this type
        # positions = posts[position_type]["post"]
        j = 0
        while int(numberToFill) != 0: 
            posts[position_type]["post"][j] = staff.pop()
            j += 1
            # staffCount += 1
            numberToFill -= 1
        # j = 0
        # if staffCount < len(staff):
        #     for position in positions:
        #         posts[position_type][position[j]] = staff.pop()
        #         staffCount += 1
        #         j += 1
        # else:
        #     print("No more staff.")
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