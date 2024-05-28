This is an instant runoff vote counter designed to work with a string of values including an --END BALLOT-- marker and a ";" to seperate names of people.

This is Ideal for dealing with the outputs of a microsoft form outputted to excel spreadsheet.

Coded by Tom for the TTG AGM elections on 28th may 2024

## User Manual:

### Match Names()

This is a function for matching names via IDs and requires 2 files
"voters.txt" and "membership.txt".

It simply takes the ID from the voters file and tries to find it in voters, if it finds it displays them both next to each other and asks the user for <y> or <n>. If any other character(s) are entered it just skips the line and moves on.
After completing all comparisons it outputs the lines of each problematic entry for review

Voters.txt should be in format "John Smith 	2000001", with an entry on each line.
The format is that of ctrl+c ctrl+v of 2 adjacent columns in Excel online.

The style is where "John smith" is the name of the voter, and "200001" is the Student ID of the voter.
The code splits the data via finding the 2 at the beginning of the student ID, therefore will not work with differently formatted IDs.

"membership.txt" should be in format "John, Smith	2000001". It also splits via the 2 in the number.
The code will then display line by line "John Smith = John, Smith"? and ask for "y" or "n".

After completion all lines where user inputted "n" or lines without match in "membership.txt" are listed.

If a vote is invalid, delete their line from the "votes.txt" file, or the orignal spreadsheet. "run_vote()" skips over empty lines, so they are not a problem.

### run_vote()

This requires 1 file, "votes.txt".
The format of each row is as follows:

"Candidate 1;--END BALLOT--;RON : Re Open Nominations;Candidate 2;"

Where each item is encapsulated by a right side ";", and the items are in any order with one item being "--END BALLOT--"

All rows are in this format, or blank (no characters at all).
This is the format of a whole column from Excel being copied into a txt file, this means each vote run (as in for each candidate), must be separately copied in one at a time and run.

The ballot is chopped off at "--END BALLOT--", and as such it and all following items are removed from the ballot before tallying begins.

The Code will run the whole vote and print out each step and calculation as it passes, unless a tie in which case the user must decide which candidate to keep.