from random import randrange, shuffle
# from csv import writer
import csv
import operator

def init_posts(shift):

    days = {
    "Gates" : {
        "Charlie 1": "Vacant",
        "Charlie 2": "Vacant",
        "Charlie 3": "Vacant",
        "3" : "Fill",
        "1" : "Priority"
    },
    "Booths": {
        "Wofle 1": "Vacant",
        "Wofle 2": "Vacant",
        "Tantau 1": "Vacant",
        "3": "Fill",
        "1" : "Priority"
    },
    "Mobiles" : {
        "Paul 1" : "Vacant",
        "Paul 2" : "Vacant",
        "Paul 3" : "Vacant",
        "Paul 4" : "Vacant",
        "2" : "Fill",
        "2" : "Priority"
    },
    "Edwards": {
        "Edward 1": "Vacant",
        "Edward 2": "Vacant",
        "Edward 3": "Vacant",
        "Edward 4": "Vacant",
        "Edward 5": "Vacant",
        "1" : "Fill",
        "2" : "Priority"
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

    # get the group of positions 
    position_types = list(posts.keys()) # convert to list for shuffle
    shuffle(position_types)
    
    i = 0
    # collect position types and get their priortiy and fill numbers

    # sort by priority
    sorted_x = sorted(posts.items(), key=operator.itemgetter("Priority"))


    for position_type in position_types:

        # get the positions for this type
        positions = list(posts[position_type])
        shuffle(positions)
        # if position_type != "Edwards":
        #     shuffle(positions)
        # assign staff to the position
        for position in positions:
            if i < len(staff):
                if posts[position_type][position] == 'Fill' or posts[position_type][position] == 'Priority':
                    print("Fill = {}".format(posts[position_type][position]))
                    break
                posts[position_type][position] = staff[i]
                i += 1

    # for position in posts.keys():
    #     for unit in posts[position]:
    
    #         if posts[position][unit] != 'ID':
    #             posts[position][unit] = staff[i]
    #             i += 1
                # staff.remove(staff[i])

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