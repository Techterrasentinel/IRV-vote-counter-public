import re


# Tom's vote counter

class Voter:  # The class for each instance of a voter
    def __init__(self, input_line: str):
        self.ballot: list[str] = []
        self.ballot = input_line.split(";")  # values from Excel are separated by ";", split them into list
        self.ballot = self.ballot[:(self.ballot.index("--END BALLOT--"))]  # removes all candidates beyond then end

    def remove_candidate(self, candidate) -> int:
        """Remove the stated candidate from the voters ballot, if they exist."""
        if candidate in self.ballot:  # only remove candidate if they exist
            self.ballot.remove(candidate)
            return 1
        else:
            return 0

    def return_ballot(self) -> list[str]:
        """Return the whole ballot, this is a debug function."""
        return self.ballot

    def return_first(self) -> str | None:
        """Return the current first choice of the voter."""
        if len(self.ballot) > 0:
            return self.ballot[0]
        else:
            return None


class Election:
    def __init__(self, input_line: str, _voters: list[Voter]):
        self.candidates: list[str] = input_line.split(";")  # split down to get candidates
        self.candidates.pop(len(self.candidates)-1)  # remove double quote at the end, that weirdly appears
        self.candidates.remove("--END BALLOT--")  # makes the list proper
        self.round = 0  # counts the rounds of voting
        self.active_candidates: dict[str, int] = {}
        self.voters: list[Voter] = _voters

        for entry in self.candidates:  # Create the instant of the candidates and their vote counts
            self.active_candidates[entry] = 0

    def tally_votes(self) -> str:
        """Tally up the votes for all candidates, print the outputs and remove the lowest candidate."""
        for candidate in self.active_candidates:  # clear all vote tallies
            self.active_candidates[candidate] = 0

        lost_votes: int = 0
        self.round += 1
        for current_voter in self.voters:
            entry = current_voter.return_first()
            if entry is None or not self.active_candidates.__contains__(entry):
                lost_votes += 1
            else:
                self.active_candidates[entry] += 1

        print("\n")
        print(f"During round {self.round} of voting the tallies are {self.active_candidates}.")
        print(f"Currently {lost_votes} votes have been lost.")

        lowest_candidate = ""
        lowest_votes: int = 1000  # set arbitrarily large value so it will be replaced
        for candidate in self.active_candidates:
            count = self.active_candidates[candidate]
            if count < lowest_votes:
                lowest_votes = count
                lowest_candidate = candidate
            elif count == lowest_votes:
                print("WARNING TIED VOTE, recommendation run vote twice and see if it changes result")
                response = input(
                    f"enter <c> to keep current candidate{lowest_candidate}"
                    f" or anything else to change to new candidate {candidate} :"
                )
                if response == "c":
                    print("keeping current")
                else:
                    print("changing")
                    lowest_votes = count
                    lowest_candidate = candidate

        self.active_candidates.pop(lowest_candidate)
        for voter in self.voters:
            voter.remove_candidate(lowest_candidate)

        print(f"Lowest candidate {lowest_candidate} with {lowest_votes} has been removed.")

        if len(self.active_candidates) == 1:
            print(f"{self.active_candidates} is the winner!")
            return "Finish"
        else:
            print("Proceeding to next round of voting.")
            return "Continue"


def match_names():
    """A function to compare membership.txt entries with voters.txt"""
    member_reader = open("membership.txt", "r")
    members: list[str] = []
    for read_line in member_reader:
        members.append(read_line.rstrip("\n"))
    member_reader.close()  # get all the members

    formatted_members: dict[str, str] = {}
    for member in members:
        if member.find("2") != -1:
            index = member.find("2")
            name = member[:index]
            id_number = member[index:]
            formatted_members[id_number] = name  # format all members to ID: NAME in a dictionary

    voters_reader = open("voters.txt", "r")
    all_input: list[str] = []
    for read_line in voters_reader:
        all_input.append(read_line.rstrip("\n"))
    voters_reader.close()  # get all voters

    externals = 0  # no real case handling for externals as none voted and it adds complexity

    formatted_voters: dict[str, str] = {}
    for voter in all_input:
        if voter.find("2") != -1:
            index = voter.find("2")
            name = voter[:index]
            id_number = voter[index:]
            formatted_voters[id_number] = name  # format all voters to ID: NAME in a dictionary
        else:
            externals += 1
            formatted_voters[f"external {externals}"] = voter  # make an entry for externals (no ID)

    counter = 0
    invalids: list[int] = []
    for entry in formatted_voters:
        if formatted_members.__contains__(entry):  # if the student id from voters matches an entry in members
            print(f"voter on line {counter} is correct! ")
            print(f"{formatted_voters[entry]} = {formatted_members[entry]}?")  # display both names
            validate = input()
            if validate == "y":  # ask user if names match, if yes fine, if no list them
                pass
            elif validate == "n":
                invalids.append(counter)
        else:
            print(f"could not find {entry} in dict")
            invalids.append(counter)
        counter += 1

    print(f"invalid lines are {invalids}")

# Main code Stuff


def run_vote():
    """A function to run the whole vote from the data in the vote file"""
    file = open("votes.txt", "r")  # open the file storing the list of votes

    all_candidates = file.readline().rstrip("\n")  # get all possible candidates as each voter has entered them all
    file.seek(0)  # reset index of pointer in file

    all_voters: list[Voter] = []
    for line in file:  # instantiate all voters
        if line != "\n":
            all_voters.append(Voter(line.rstrip("\n")))
        else:
            print("blank line here")

    file.close()  # close file as good practice

    this_election = Election(all_candidates, all_voters)  # create the whole election

    flag_over = True
    while flag_over:
        if this_election.tally_votes() != "Continue":
            flag_over = False

# lets a go, write which function you want to run!


run_vote()
