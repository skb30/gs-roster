from random import randrange, shuffle
# from csv import writer
import csv



# create the types hat

# create the staff hat

# create the must-fill hat

# process the must-fill hat. If there's anything left over then
# create the what's left hat and process it 
new_roster = {}
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
def create_rosters(staff, roster):
    shuffle(staff)
    for shift in roster[0]["shift"]:
        # for group in shift["groups"]
        print(shift["name"])
        for groups in shift["groups"]:
            print(groups["name"])
            for mustFillPosts in groups["mustFillPosts"]:
                print("shift: {} postion: {} unit: {}".format(shift["name"],groups["name"],mustFillPosts))
            # process day shift

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

    create_rosters(staff, roster_policy)

    # print(roster_policy[0]["shift"][0]["groups"][0]["mustFillPosts"][1])
    
    print("*** done ***")

if __name__ == "__main__":
  main()