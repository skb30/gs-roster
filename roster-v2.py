from random import randrange, shuffle
import csv

# Generate the shift roasters by placing the staff randomly in positions.
# This will eliminate any bias as to where the staff is posted.
# skb

# dgs - Consider moving this out of global
# if its a varaible that is used in main, then move the placement to main
# placement of this variable looks out of plac here.
must_fill = []


# dgs I realize this is just test, but you should consider moving
# this into a data.json file. and just read the file with the python program
roster_policy = [
    {
        "shift": [{
            "name": "5:00AM - 2:00PM",
            "groups":  [{
                "name": "Gates",
                "mustFillPosts": ["Charlie 1", "Charlie 2", "Charlie 3"],
                "overflowPosts": []
            }, {
                "name": "Booths",
                "mustFillPosts": ["Wofle 1", "Wofle 2", "Tantau 1"],
                "overflowPosts": []
            }, {
                "name": "Mobiles",
                "mustFillPosts": ["Paul 1", "Paul 2"],
                "overflowPosts": ["Paul 3", "Paul 4", "Paul 5"]
            }, {
                "name": "Edwards",
                "mustFillPosts": [],
                "overflowPosts": ["Edward 1", "Edward 2", "Edward 3", "Edward 4", "Edward 5"]
            }]
        },
            {
            "name":  "7:00AM - 4:00PM",
            "groups":  [{
                "name": "Georges",
                "mustFillPosts": ["George 2", "George 3", "George 6", "George 7", "George 8"],
                "overflowPosts": ["George 1", "George 4", "George 5", "George 9"]
            }, {
                "name": "Roberts",
                "mustFillPosts": ["Robert 1", "Robert 2"],
                "overflowPosts": ["Tantau 2"]
            }, {
                "name": "Mobiles",
                "mustFillPosts": [],
                "overflowPosts": ["Paul 3", "Paul 4", "Paul 5"]
            }, {
                "name": "Edwards",
                "mustFillPosts": ["Edward 1"],
                "overflowPosts": ["Edward 2", "Edward 3", "Edward 4", "Edward 5", "Edward 6"]
            }]
        },
            {
            "name":  "1:00PM - 10:00PM",
            "groups": [{
                "name": "Gates",
                "mustFillPosts": ["Charlie 1", "Charlie 2", "Charlie 3"],
                "overflowPosts": []
            }, {
                "name": "Booths",
                "mustFillPosts": ["Wofle 1", "Wofle 2", "Tantau 1"],
                "overflowPosts": []
            }, {
                "name": "Mobiles",
                "mustFillPosts": ["Paul 1", "Paul 2"],
                "overflowPosts": ["Paul 3", "Paul 4"]
            }, {
                "name": "Edwards",
                "mustFillPosts": [],
                "overflowPosts": ["Edward 1", "Edward 2", "Edward 3", "Edward 4", "Edward 5"]
            }]
        },
            {
            "name":  "9:00PM - 6:00AM",
            "groups":  [{
                "name": "Georges",
                "mustFillPosts": ["George 1", "George 2", "George 3", "George 4", "George 5", "George 6", "George 7"],
                "overflowPosts": []
            }, {
                "name": "Roberts",
                "mustFillPosts": ["Robert 1", "Robert 2"],
                "overflowPosts": ["Tantau 2"]
            }, {
                "name": "Mobiles",
                "mustFillPosts": ["Paul 1", "Paul 2"],
                "overflowPosts": ["Paul 3", "Paul 4", "Paul 5"]
            }, {
                "name": "Edwards",
                "mustFillPosts": ["Edward 1"],
                "overflowPosts": ["Edward 2", "Edward 3", "Edward 4", "Edward 5", "Edward 6"]
            }]
        }]
    }
]

# -------------------------
# buildRoster()
#  Inputs: shift (object) - This is the policy of how the roster should be built
#          staff (array) - This is raw input array as read from a CSV
#          site (string) - This is just a string with the site name we are processing
#  Outputs:


def build_roster(shift, staff, site):
    # dgs consider moving this function to main()
    #    it reads hard when you call a function, then immediatly
    #    call another function. Its hard to follow.
    staff, callOffList = get_staff(staff, shift, site)

    # create staff list by shift
    # dgs - refactor this. Dont like seeing hard coded values.
    mustFillRoster = get_blank_rosters(shift, roster_policy, 1)
    shuffle(mustFillRoster)
    overFlowRoster = get_blank_rosters(shift, roster_policy, 2)
    shuffle(overFlowRoster)

    row = 0
    fullRoster = []
    sizeOfMustFill = len(mustFillRoster)
    sizeOfOverFlow = len(overFlowRoster)
    combined = sizeOfMustFill + sizeOfOverFlow

    # More positions to fill than staff so we'll fill the must-fill first
    if len(staff) <= len(mustFillRoster):

        while len(staff) > 0:
            mustFillRoster[row][1] = staff.pop()
            row += 1
        fullRoster = mustFillRoster + overFlowRoster

    elif len(staff) <= combined:  # leftover staff so let's fill overflow
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


# -------------------------
# getBlankRoster()
#  1 liner that explains what this funciton does
# -------------------------
def get_blank_rosters(shift_roster, roster, priority):
    # dgs - refactor this. Dont like seeing hard coded values.
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
                    blank_roster.append([])  # create a roster row
                    size -= 1

                for unit in mustFillPosts:
                    blank_roster[i].append(unit)  # add unit column to the row
                    # add name column to the row
                    blank_roster[i].append("Vacant")
                    i += 1
                    if size != 0:
                        blank_roster.append([])
                        size -= 1
    return blank_roster


# -------------------------
# getBlankRoster()
#  1 liner that explains what this funciton does
# -------------------------
def get_staff(filename, shift, site):
    staffList = []
    callOffList = []
    callOff = "CALL OFF"
    with open(filename, newline='') as csvfile:
        shiftsRoaster = csv.reader(csvfile, delimiter=',', quotechar='|')
        for name in shiftsRoaster:

            # strip out the quotes

            roleFromFile = name[4].strip('\"')
            shiftFromFile = name[5].strip('\"')
            firstNameFromFile = name[7].strip('\"')
            lastNameFromFile = name[8].strip('\"')
            subjectFromFile = name[9].strip('\"')

            if roleFromFile == site and len(firstNameFromFile) > 0:
                # print("4-{} 5-{} 7-{} 8-{} 9-{}".format(name[4],name[5],name[7],name[8],name[9]))
                fullName = firstNameFromFile + " " + lastNameFromFile
                if shiftFromFile == shift and subjectFromFile != callOff:
                    staffList.append(fullName)
                elif shiftFromFile == shift and subjectFromFile == callOff:
                    callOffList.append(fullName)

        shuffle(staffList)
    return staffList, callOffList


# -------------------------
# writeRoster()
#  1 liner that explains what this funciton does
# -------------------------
def write_roster(roster_file, roster, callOffList):
    shiftName = roster_file
    roster_file = "./output-files/" + roster_file + ".txt"
    with open(roster_file, 'w') as f:
        f.write("%s\n" % ("Shift: " + shiftName))
        f.write("%s\t%s\n" % ("POST", "NAME"))
        for position in roster:
            f.write("%s\t%s\n" % (position[0], position[1]))
        f.write("%s\n" % ("Call Off List"))
        for name in callOffList:
            f.write("%s\t%s\n" % (" ", name))
            # print("call name {}".format(name))


def main():
    print("*** Start ***")
    leftoverStaff = []
    # staff = "really-small-input.csv"
    # staff = "small-input.csv"
    # staff = "./input-files/ShiftboardShifts-5.csv"
    staff = "./input-files/ShiftboardShifts-6.csv"
    # staff = "./input-files/today1.csv"
    site = "Apple Park"

    # shift = "shift5"

    shifts = ['5:00AM - 2:00PM', '7:00AM - 4:00PM',
              '1:00PM - 10:00PM', '9:00PM - 6:00AM']
    for shift in shifts:
        (roster, leftoverStaff, callOffList) = build_roster(shift, staff, site)
        write_roster(shift, roster, callOffList)
        # for p in roster:
        # print("{},{}".format(p[0], p[1]))

        # Check to see if there's any leftover staff
        if len(leftoverStaff) > 0:
            print("Over Staff")
            for name in leftoverStaff:
                print("  {} ".format(name))
    print("*** End ***")


if __name__ == "__main__":
    main()
