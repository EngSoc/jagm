import csv

# Was made for JAGM 2021, never got used outside of test data
# That's what happens when you have exactly enough nominees
HAS_SET_GLOBAL_VARIABLES = False

FIRST_BALLOT_INDEX = 1 # A = 0, B = 1, C = 2, ...
NUMBER_OF_NOMINEES = 4 # number of questions = number of nominees
NUMBER_OF_SLOTS = 2 # should be 4
NO_CANDIDATE_NAME = "No Candidate" # exact case required
CSV_FILE_NAME = "boardofdirectorsvoting_test.csv"

# read all ballots from spreadsheet
def read_ballots_and_nominees():
    ballots = []
    nominees = []
    with open(CSV_FILE_NAME) as csvfile:
        reader = csv.reader(csvfile)
        headers = next(reader, None)
        if FIRST_BALLOT_INDEX + NUMBER_OF_NOMINEES > len(headers):
            print("ERROR: INVALID NUMBER OF QUESTIONS. PLEASE FIX.")
        for row in reader:
            new_ballot = []
            for i in range(FIRST_BALLOT_INDEX, \
                FIRST_BALLOT_INDEX + NUMBER_OF_NOMINEES):
                # accounting for valid but incorrectly filled ballots
                if row[i] == "" or row[i] in new_ballot:
                    continue
                if row[i] == NO_CANDIDATE_NAME:
                    break
                if not row[i] in nominees:
                    nominees.append(row[i])
                new_ballot.append(row[i])
            if len(new_ballot) == 0 or new_ballot[-1] != NO_CANDIDATE_NAME:
                new_ballot.append(NO_CANDIDATE_NAME)
            ballots.append(new_ballot)
    # just in case; shouldn't happen
    if NO_CANDIDATE_NAME in nominees:
        nominees.remove(NO_CANDIDATE_NAME)
    if NUMBER_OF_NOMINEES != len(nominees):
        print("ERROR: INVALID NUMBER OF NOMINEES")
    nominees = sorted(nominees)
    return ballots, nominees

def get_nominees_inverted_index(nominees):
    nominees_inverted_index = {}
    for i in range(len(nominees)):
        nominees_inverted_index[nominees[i]] = i
    return nominees_inverted_index

# get the number of each type of vote
def get_nominees_complete_voting(ballots, nominees, nominees_inverted_index):
    nominees_complete_voting = []
    for i in range(len(nominees)):
        nominees_complete_voting.append([0 for i in nominees])
    for ballot in ballots:
        for i in range(len(ballot) - 1): # don't record no candidate
            nominees_complete_voting[nominees_inverted_index[\
                ballot[i]]][i] += 1
    return nominees_complete_voting

# tiebreaker process
def tiebreaker_process(nominees_to_tiebreak, nominees_complete_voting, \
    nominees_inverted_index):
    print("WARNING: EXACT TIE IN VOTES. TIEBREAKING VIA ORDERED VOTES.")
    for i in range(NUMBER_OF_NOMINEES):
        print("VOTE %d TIEBREAKING" % (i+1))
        least_votes_count = nominees_complete_voting[ \
            nominees_inverted_index[nominees_to_tiebreak[0]]][i]
        least_votes_names = [nominees_to_tiebreak[0]]
        for j in range(1, len(nominees_to_tiebreak)):
            name = nominees_to_tiebreak[j]
            votes_for_nominee = nominees_complete_voting[ \
                nominees_inverted_index[name]][i]
            if votes_for_nominee < least_votes_count:
                least_votes_count = votes_for_nominee
                least_votes_names = [name]
            elif votes_for_nominee == least_votes_count:
                least_votes_names.append(name)
        nominees_to_tiebreak = least_votes_names
        if len(nominees_to_tiebreak) == 1:
            return nominees_to_tiebreak[0]
    print("WARNING: STILL A TIE! PICKING ARBITRARILY")
    return nominees_to_tiebreak[0]

def print_complete_voting_results(nominees, nominees_complete_voting, \
    nominees_inverted_index, num_ballots):
    print("")
    max_name_length = 0
    for name in nominees:
        max_name_length = max(len(name), max_name_length)
    max_name_length += 1
    header_string_list = ["".rjust(max_name_length)]
    for i in range(NUMBER_OF_NOMINEES):
        header_string_list.append("\tVOTE %d" % ((i+1)))
    print(''.join(header_string_list))
    for name in nominees:
        nominee_string_list = [name.rjust(max_name_length)]
        for i in range(NUMBER_OF_NOMINEES):
            nominee_string_list.append("\t%d" % (\
                nominees_complete_voting[nominees_inverted_index[name]][i]))
        print(''.join(nominee_string_list))
    print("\nTOTAL VOTES: %d\n---\n" % (num_ballots))
    return

def print_round_results(nominees, nominees_inverted_index, nominees_votes, \
    round_num, eliminated_nominee):
    print("\nROUND %d RESULTS:\n" % (round_num+1))
    for name in nominees:
        votes_for_nominee = nominees_votes[nominees_inverted_index[name]]
        if votes_for_nominee > 0:
            if name == eliminated_nominee:
                print("%d\t- %s (ELIMINATED)" % (votes_for_nominee, name))
            else:
                print("%d\t- %s" % (votes_for_nominee, name))
    print("\nELIMINATED NOMINEE: %s\n---\n" %(eliminated_nominee))
    return

# actual vote process
def determination_of_results(ballots, nominees, nominees_complete_voting, \
    nominees_inverted_index):
    eliminated_nominees = []
    while len(eliminated_nominees) < NUMBER_OF_NOMINEES - NUMBER_OF_SLOTS:
        nominees_votes = [0 for i in nominees]
        no_candidate_votes = 0
        for ballot in ballots:
            for name in ballot:
                if name == NO_CANDIDATE_NAME:
                    no_candidate_votes += 1
                    break
                elif name not in eliminated_nominees:
                    nominees_votes[nominees_inverted_index[name]] += 1
                    break
        least_votes_count = -1
        least_votes_names = []
        for name in nominees:
            if name not in eliminated_nominees:
                votes_for_nominee = nominees_votes[\
                    nominees_inverted_index[name]]
                if least_votes_count == -1 or \
                    votes_for_nominee < least_votes_count:
                    least_votes_count = votes_for_nominee
                    least_votes_names = [name]
                elif votes_for_nominee == least_votes_count:
                    least_votes_names.append(name)
        least_vote_name = least_votes_names[0]
        if len(least_votes_names) > 1:
            # tiebreaking
            least_vote_name = tiebreaker_process(least_votes_names, \
                nominees_complete_voting, nominees_inverted_index)
        print_round_results(nominees, nominees_inverted_index, \
            nominees_votes, len(eliminated_nominees), least_vote_name)
        eliminated_nominees.append(least_vote_name)
    chosen_nominees = []
    for name in nominees:
        if name not in eliminated_nominees:
            chosen_nominees.append(name)
    return chosen_nominees

def main():
    if not HAS_SET_GLOBAL_VARIABLES:
        print("PLEASE SET GLOBAL VARIABLES BEFORE RUNNING")
        return
    result = read_ballots_and_nominees()
    ballots = result[0]
    nominees = result[1]
    nominees_inverted_index = get_nominees_inverted_index(nominees)
    nominees_complete_voting = get_nominees_complete_voting(ballots, \
        nominees, nominees_inverted_index)
    print_complete_voting_results(nominees, nominees_complete_voting, \
        nominees_inverted_index, len(ballots))
    chosen_nominees = determination_of_results(ballots, nominees, \
        nominees_complete_voting, nominees_inverted_index)
    print("\nBOARD MEMBERS HAVE BEEN CHOSEN:")
    for name in chosen_nominees:
        print("* %s" % (name))
    print("\nEND OF CODE\n")
    return

if __name__ == "__main__":
    main()