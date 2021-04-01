import csv

# Was made for JAGM 2021, went through a few bug fix iterations
# Throws out excess data, feel free to comment print functions
HAS_SET_GLOBAL_VARIABLES = False

NAME_COLUMN_INDEX = 1
QUEST_ID_COLUMN_INDEX = 2
EMAIL_COLUMN_INDEX = 3
YEAR_COLUMN_INDEX = 4
CLASS_COLUMN_INDEX = 5
SOCIETY_COLUMN_INDEX = 6
A_SOCIETY_STRING = "A-Society [You are currently on a Co-op Term]"
B_SOCIETY_STRING = "B-Society [You are currently on an Academic Term]"
ATTENDANCE_COLUMN_INDEX = 7
ATTEND_WITH_PROXIES_STRING = "Attend JAGM 2021 and accept up to 2 proxies"
ATTEND_NO_PROXIES_STRING = "Attend JAGM 2021 but not accept proxies"
JUST_PROXY_STRING = "Proxy my vote At JAGM 2021"
PROXY_QUEST_ID_COLUMN_INDEX = 9
PROXY_ALLOW_ASSIGNIGN_COLUMN_INDEX = 10
PROXY_VOTE_PERMISSION_COLUMN_INDEX = 11
FULL_VOTE_PERMISSION_STRING = "Yes, they can use my vote how they would like"
NO_VOTE_PERMISSION_STRING = "No, follow the comments below"
NO_VOTE_AND_NOTED_PERMISSION_STRING = ("No, follow the comments below "
    "and have my vote noted in the minutes on each motion if applicable")
PROXY_COMMENTS_COLUMN_INDEX = 12

MEETING_YEAR = "2021"
MEETING_WEEKDAY = "Sunday at 9:30am EDT at https://zoom.us/j/94743110038 "
MEGA_DRIVE_LINK = "https://bit.ly/JAGM2021 "
SIGNATURE = ("\n---\nThomas Dedinsky\nJAGM Chair, Engineering Society\n"
    "He/Him/Il\nUniversity of Waterloo\njagm@engsoc.uwaterloo.ca")
CSV_FILE_NAME = "registrations.csv"

# read all ballots from spreadsheet
def read_participants_and_proxies():
    participants = {}
    proxies = []
    with open(CSV_FILE_NAME) as csvfile:
        reader = csv.reader(csvfile)
        headers = next(reader, None)
        for row in reader:
            if row[ATTENDANCE_COLUMN_INDEX] == JUST_PROXY_STRING:
                proxies.append({
                    "name": row[NAME_COLUMN_INDEX],
                    "quest_id": row[QUEST_ID_COLUMN_INDEX],
                    "email": row[EMAIL_COLUMN_INDEX],
                    "year": row[YEAR_COLUMN_INDEX],
                    "class": row[CLASS_COLUMN_INDEX],
                    "is_asoc": row[SOCIETY_COLUMN_INDEX] == A_SOCIETY_STRING,
                    "proxy_quest_id": row[PROXY_QUEST_ID_COLUMN_INDEX],
                    "allow_assigning": row[PROXY_ALLOW_ASSIGNIGN_COLUMN_INDEX] \
                        == "Yes",
                    "vote_on_behalf": row[PROXY_VOTE_PERMISSION_COLUMN_INDEX] \
                        == FULL_VOTE_PERMISSION_STRING,
                    "noted": row[PROXY_VOTE_PERMISSION_COLUMN_INDEX] == \
                        NO_VOTE_AND_NOTED_PERMISSION_STRING,
                    "comments": row[PROXY_COMMENTS_COLUMN_INDEX]
                })
            else:
                participants[row[QUEST_ID_COLUMN_INDEX]] = {
                    "name": row[NAME_COLUMN_INDEX],
                    "quest_id": row[QUEST_ID_COLUMN_INDEX],
                    "email": row[EMAIL_COLUMN_INDEX],
                    "year": row[YEAR_COLUMN_INDEX],
                    "class": row[CLASS_COLUMN_INDEX],
                    "is_asoc": row[SOCIETY_COLUMN_INDEX] == A_SOCIETY_STRING,
                    "accepting_proxies": row[ATTENDANCE_COLUMN_INDEX] \
                        == ATTEND_WITH_PROXIES_STRING,
                    "proxies": []
                }
    return participants, proxies

def assign_quest_id_proxies(participants, proxies):
    remaining_proxies = []
    unfulfilled_proxies = []
    for proxy in proxies:
        proxy_quest_id = proxy["proxy_quest_id"]
        if proxy_quest_id in participants and \
            participants[proxy_quest_id]["accepting_proxies"] and \
            len(participants[proxy_quest_id]["proxies"]) < 2:
            participants[proxy_quest_id]["proxies"].append(proxy)
        elif proxy["allow_assigning"]:
            remaining_proxies.append(proxy)
        else:
            unfulfilled_proxies.append(proxy)
    return remaining_proxies, unfulfilled_proxies

def assign_remaining_proxies_class_year_society(participants, proxies):
    remaining_proxies = []
    for proxy in proxies:
        found_proxy = False
        for participant in participants:
            if participant["class"] == proxy["class"] and \
                participant["year"] == proxy["year"] and \
                participant["is_asoc"] == proxy["is_asoc"] and \
                participant["accepting_proxies"] and \
                len(participant["proxies"]) < 2:
                    participant["proxies"].append(proxy)
                    found_proxy = True
                    break
        if not found_proxy:
            remaining_proxies.append(proxy)
    return remaining_proxies

def assign_remaining_proxies_class_year(participants, proxies):
    remaining_proxies = []
    for proxy in proxies:
        found_proxy = False
        for participant in participants:
            if participant["class"] == proxy["class"] and \
                participant["year"] == proxy["year"] and \
                participant["accepting_proxies"] and \
                len(participant["proxies"]) < 2:
                    participant["proxies"].append(proxy)
                    found_proxy = True
                    break
        if not found_proxy:
            remaining_proxies.append(proxy)
    return remaining_proxies

def assign_remaining_proxies_class_society(participants, proxies):
    remaining_proxies = []
    for proxy in proxies:
        found_proxy = False
        for participant in participants:
            if participant["class"] == proxy["class"] and \
                participant["is_asoc"] == proxy["is_asoc"] and \
                participant["accepting_proxies"] and \
                len(participant["proxies"]) < 2:
                    participant["proxies"].append(proxy)
                    found_proxy = True
                    break
        if not found_proxy:
            remaining_proxies.append(proxy)
    return remaining_proxies

def assign_remaining_proxies_year_society(participants, proxies):
    remaining_proxies = []
    for proxy in proxies:
        found_proxy = False
        for participant in participants:
            if participant["year"] == proxy["year"] and \
                participant["is_asoc"] == proxy["is_asoc"] and \
                participant["accepting_proxies"] and \
                len(participant["proxies"]) < 2:
                    participant["proxies"].append(proxy)
                    found_proxy = True
                    break
        if not found_proxy:
            remaining_proxies.append(proxy)
    return remaining_proxies

def assign_remaining_proxies_society(participants, proxies):
    remaining_proxies = []
    for proxy in proxies:
        found_proxy = False
        for participant in participants:
            if participant["is_asoc"] == proxy["is_asoc"] and \
                participant["accepting_proxies"] and \
                len(participant["proxies"]) < 2:
                    participant["proxies"].append(proxy)
                    found_proxy = True
                    break
        if not found_proxy:
            remaining_proxies.append(proxy)
    return remaining_proxies

def assign_remaining_proxies_any(participants, proxies):
    remaining_proxies = []
    for proxy in proxies:
        found_proxy = False
        for participant in participants:
            if participant["accepting_proxies"] and \
                len(participant["proxies"]) < 2:
                    participant["proxies"].append(proxy)
                    found_proxy = True
                    break
        if not found_proxy:
            remaining_proxies.append(proxy)
    return remaining_proxies

def print_email(email_to, email_cc, email_bcc, subject, body):
    print("\n---")
    print("\nFrom:\njagm@engsoc.uwaterloo.ca")
    print("\nTo:")
    print(email_to)
    if len(email_cc) > 0:
        print("\nCC:")
        print(", ".join(email_cc))
    if len(email_bcc) > 0:
        print("\nBCC:")
        print(", ".join(email_bcc))
    print("\nSubject:")
    print(subject)
    print("\nBody:")
    print(body)
    print(SIGNATURE)
    return

def print_unfulfilled_proxies_post_quest_id(unfulfilled_proxies, participants):
    zero_proxy_message = ("Hi %s, thanks for submitting a proxy for JAGM %s. "
        "You wanted to submit a proxy to %s, but unfortunately, they're not "
        "accepting proxies. Woops. We aren't accepting any more proxies, but "
        "you're welcome to attend the meeting on %s. Take care!")
    two_proxy_message = ("Hi %s, thanks for submitting a proxy for JAGM %s. "
        "You wanted to submit a proxy to %s, but unfortunately, they're super "
        "popular and already had 2 direct proxies. Woops. We aren't accepting "
        "any more proxies, but you're welcome to attend the meeting on %s. "
        "Take care!")
    not_found_message = ("Hi %s, thanks for submitting a proxy for JAGM "
        "%s. You wanted to submit a proxy to QUEST ID %s, but unfortunately, "
        "they're not attending JAGM. Woops. We aren't accepting any more "
        "proxies, but you're welcome to attend the meeting on %s. Take care!")
    subject = "JAGM %s Proxy Results - Unassigned" % (MEETING_YEAR)
    for proxy in unfulfilled_proxies:
        if proxy["proxy_quest_id"] in participants:
            intended_participant = participants[proxy["proxy_quest_id"]]
            if intended_participant["accepting_proxies"]:
                print_email(proxy["email"], [intended_participant["email"]], \
                    [], subject, two_proxy_message % (proxy["name"], \
                    MEETING_YEAR, intended_participant["name"], \
                    MEETING_WEEKDAY))
            else:
                print_email(proxy["email"], [intended_participant["email"]], \
                    [], subject, zero_proxy_message % (proxy["name"], \
                    MEETING_YEAR, intended_participant["name"], \
                    MEETING_WEEKDAY))
        else:
            print_email(proxy["email"], [], [], subject, not_found_message % (\
                proxy["name"], MEETING_YEAR, proxy["proxy_quest_id"], \
                MEETING_WEEKDAY))

def print_unfulfilled_proxies_post_assigning(unfulfilled_proxies):
    message = ("Hi %s, thanks for submitting a proxy for JAGM %s. We "
        "unfortunately don't have enough people attending the meeting to "
        "hold all of the proxies, either from a plethora of proxies or from "
        "a lack of consenting proxies holders. We'll try to find someone "
        "who registers at the meeting to take your proxy, but we do encourage "
        "you to attend the meeting on %s. Maybe see you then!")
    subject = "JAGM %s Proxy Results - Unassigned" % (MEETING_YEAR)
    for proxy in unfulfilled_proxies:
        print_email(proxy["email"], [], [], subject, message % (\
            proxy["name"],  MEETING_YEAR, MEETING_WEEKDAY))

def print_participants_with_proxies(participants):
    some_proxies_message = ("Hi %s, JAGM %s is only a few days away. We're "
        "excited that you're going to be able to attend. But you won't only "
        "be voting for yourself as you've been assigned proxies! Please make "
        "sure to look below for information on who you're voting for and "
        "how you're voting. Thanks again for taking on some proxies! "
        "See you at the meeting on %s.")
    proxy_addon = ("\nProxy: %s (%s)\nSociety: %s\nAre you allowed to vote on "
        "their behalf?: %s\nDo they want their votes noted?: %s\nComments: %s")
    subject = "JAGM %s Proxy Assigning" % (MEETING_YEAR)
    for participant in participants:
        if len(participant["proxies"]) == 1:
            proxy = participant["proxies"][0]
            print_email(participant["email"], [proxy["email"]], [], \
                subject, (some_proxies_message % (participant["name"], \
                MEETING_YEAR, MEETING_WEEKDAY)) + "\n" \
                + (proxy_addon % (proxy["name"], proxy["quest_id"], \
                "A-Soc" if proxy["is_asoc"] else "B-Soc", \
                "Yes" if proxy["vote_on_behalf"] else "No", \
                "Yes" if proxy["noted"] else "No", \
                proxy["comments"] if proxy["comments"] else "N/A")))
        elif len(participant["proxies"]) == 2:
            proxy_A = participant["proxies"][0]
            proxy_B = participant["proxies"][1]
            print_email(participant["email"], [proxy_A["email"], \
                proxy_B["email"]], [], subject, (some_proxies_message % (\
                participant["name"], MEETING_YEAR, MEETING_WEEKDAY)) + "\n" + \
                (proxy_addon % (proxy_A["name"], proxy_A["quest_id"], \
                "A-Soc" if proxy_A["is_asoc"] else "B-Soc", \
                "Yes" if proxy_A["vote_on_behalf"] else "No", \
                "Yes" if proxy_A["noted"] else "No", \
                proxy_A["comments"] if proxy_A["comments"] else "N/A")) + \
                "\n" + (proxy_addon % (proxy_B["name"], proxy_B["quest_id"], \
                "A-Soc" if proxy_B["is_asoc"] else "B-Soc", \
                "Yes" if proxy_B["vote_on_behalf"] else "No", \
                "Yes" if proxy_B["noted"] else "No", \
                proxy_B["comments"] if proxy_B["comments"] else "N/A")))

def print_all_participants(participants):
    general_message = ("Hi everyone, JAGM %s is only a few days away. We're "
        "excited that you're going to be able to attend. Please make sure "
        "to look at the mega-drive for this meeting at %s. This includes "
        "the agenda, the form for Board of Directors, and more! Please "
        "arrive promptly on %s. See you then!")
    subject = "JAGM %s Reminder Email" % (MEETING_YEAR)
    list_of_emails = []
    for participant in participants:
        list_of_emails.append(participant["email"])
    print_email("jagm@engsoc.uwaterloo.ca", ["council.a@engsoc.uwaterloo.ca", \
        "council.b@engsoc.uwaterloo.ca"], list_of_emails, subject, \
        general_message % (MEETING_YEAR, MEGA_DRIVE_LINK, MEETING_WEEKDAY))

def print_vote_csv(participants):
    vote_header = ("\nASoc Vote,ASoc Proxy 1,ASoc Proxy 2,"
        "BSoc Vote,BSoc Proxy 1,BSoc Proxy 2")
    vote_row = "%s,%s,%s,%s,%s,%s"
    print(vote_header)
    for participant in participants:
        if len(participant["proxies"]) == 0:
            print(vote_row % (participant["quest_id"] if participant["is_asoc"]
                else "", "", "", "" if participant["is_asoc"] else
                participant["quest_id"], "", ""))
        elif len(participant["proxies"]) == 1:
            proxy = participant["proxies"][0]
            print(vote_row % (participant["quest_id"] if participant["is_asoc"]
                else "", proxy["quest_id"] if proxy["is_asoc"] else "", "",
                "" if participant["is_asoc"] else participant["quest_id"],
                "" if proxy["is_asoc"] else proxy["quest_id"], ""))
        elif len(participant["proxies"]) == 2:
            proxy_A = participant["proxies"][0]
            proxy_B = participant["proxies"][1]
            print(vote_row % (participant["quest_id"] if participant["is_asoc"]
                else "", proxy_A["quest_id"] if proxy_A["is_asoc"] else (proxy_B["quest_id"] if proxy_B["is_asoc"] else ""),
                proxy_B["quest_id"] if proxy_B["is_asoc"] and proxy_A["is_asoc"] else "",
                "" if participant["is_asoc"] else participant["quest_id"],
                ("" if proxy_B["is_asoc"] else proxy_B["quest_id"]) if proxy_A["is_asoc"] else proxy_A["quest_id"],
                "" if proxy_B["is_asoc"] or proxy_A["is_asoc"] else proxy_B["quest_id"]))

def print_remaining_proxy_slots(participants):
    print("\nRemaining Proxy Slots")
    for participant in participants:
        if len(participant["proxies"]) == 0 and participant["accepting_proxies"]:
            print("%s,%s,2" % (participant["name"], participant["quest_id"]))
        elif len(participant["proxies"]) == 1 and participant["accepting_proxies"]:
            print("%s,%s,1" % (participant["name"], participant["quest_id"]))

def main():
    if not HAS_SET_GLOBAL_VARIABLES:
        print("PLEASE SET GLOBAL VARIABLES BEFORE RUNNING")
        return
    result = read_participants_and_proxies()
    participants = result[0]
    proxies = result[1]
    # assign based on quest id
    result = assign_quest_id_proxies(participants, proxies)
    proxies = result[0]
    print_unfulfilled_proxies_post_quest_id(result[1], participants)
    # assign based on a list of rules
    participants = list(participants.values())
    proxies = assign_remaining_proxies_class_year_society(participants, proxies)
    proxies = assign_remaining_proxies_class_year(participants, proxies)
    proxies = assign_remaining_proxies_class_society(participants, proxies)
    proxies = assign_remaining_proxies_year_society(participants, proxies)
    proxies = assign_remaining_proxies_society(participants, proxies)
    proxies = assign_remaining_proxies_any(participants, proxies)
    print_unfulfilled_proxies_post_assigning(proxies)
    print_participants_with_proxies(participants)
    print_all_participants(participants)
    print_remaining_proxy_slots(participants)
    print_vote_csv(participants)
    return

if __name__ == "__main__":
    main()