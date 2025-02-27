from team import Team
import pandas

DRAFT_ORDER = ["The Crushers", "The Bowie Blinkin Bobs", "Scottish Brutes", "Cruentus Corsairs", "Team Casey Jones",
               "El Dandies", "Epic Fail", "The Edge", "Scarlet Moon Stars", "Charm City Convoluters",
               "Team Moon", "Seishun Gakuen"]

KEEPERS = {
    "The Crushers": ["Aaron Judge", "Spencer Strider", "Jackson Holliday"],
    "Scottish Brutes": ["Anthony Santander", "Shohei Ohtani", "Gunnar Henderson"],
    "Team Casey Jones": ["Elly De La Cruz", "Paul Skenes", "Mookie Betts"]
}
DRAFT_ROUNDS = 25

class Drafter:
    '''Handles running the fantasy draft. Imports the player list from a csv file containing the top 300 players as ranked
    by EPSN. Replace the csv file if ranking change. Only drafts for the top 300 ranked players.'''
    def  __init__(self):
        self.teams = [Team(team) for team in DRAFT_ORDER]
        self.currentRound = 1
        self.overallSelectionNumber = 1
        self.results_text = []
        self.final_rosters = []
        self.top_300 = pandas.read_csv("Top300.csv")
        self.player_pool = {row.Player_Name:row.Player_Position for(index, row) in self.top_300.iterrows()}
        self.keeper_pool = self.create_keeper_player_pool()

    def run_mock_draft(self):
        '''Handles running each draft round'''
        for draft_round in range(DRAFT_ROUNDS):
            self.log_round_change()
            if draft_round != 0:
                self.teams.reverse()
            if draft_round <= 2:
                self.draft_keeper_rounds(draft_round)
                self.currentRound += 1
            else:
                self.draft_current_round()
                self.currentRound += 1
        self.show_final_result()
        self.write_output_files()

    def draft_keeper_rounds(self, draft_round):
        '''Handles drafting the keepers for the first three rounds of the draft'''
        for team in self.teams:
            if team.teamName in KEEPERS:
                team.draft_player(
                    [KEEPERS[team.teamName][draft_round]],
                    self.keeper_pool[KEEPERS[team.teamName][draft_round]]
                )
                self.overallSelectionNumber += 1
                print(f"With the {self.overallSelectionNumber} overall pick"
                      f" {team.teamName} has picked {KEEPERS[team.teamName][draft_round]}")
                self.log_draft_round_result(team.teamName, KEEPERS[team.teamName][draft_round])
            else:
                team.draft_player(
                    next(iter(self.player_pool)),
                    self.player_pool[next(iter(self.player_pool))]
                )
                self.overallSelectionNumber += 1
                print(f"With the {self.overallSelectionNumber} overall pick"
                      f" {team.teamName} has picked {next(iter(self.player_pool))}")
                self.log_draft_round_result(team.teamName, next(iter(self.player_pool)))
                del self.player_pool[next(iter(self.player_pool))]

    def draft_current_round(self):
        '''Drafts players to a team for the current round. Loops through each team in the league.'''
        for team in self.teams:
            pick_successful = False
            keys = iter(self.player_pool)
            current_key = next(keys)
            while not pick_successful:
                pick_successful = team.draft_player(
                    current_key,
                    self.player_pool[current_key]
                )
                if not pick_successful:
                    try:
                        current_key = next(keys)
                    except StopIteration:
                        #If we get here it means we ran out of players so just get the highest player
                        #and put them on the team's bench
                        current_key = next(iter(self.player_pool))
                        team.draft_player(
                            next(iter(self.player_pool)),
                            "Bench"
                        )
                        pick_successful = True
            # need to delete the right player
            self.overallSelectionNumber += 1
            print(f"With the {self.overallSelectionNumber} overall pick"
                  f" {team.teamName} has picked {current_key}")
            self.log_draft_round_result(team.teamName, current_key)
            del self.player_pool[current_key]

    def create_keeper_player_pool(self):
        '''Creates a new dictionary containing all players who have been specified as Keepers.
        This also removes the keepers from the draftable player pool'''
        keeper_pool = (
            {player:self.player_pool[player] for player in self.player_pool
             if any(player in name for name in KEEPERS.values())}
        )
        for player in keeper_pool:
            del self.player_pool[player]
        return keeper_pool

    def show_final_result(self):
        '''Prints to the console the final rosters of each team'''
        for team in self.teams:
            team.print_team_roster()

    def log_round_change(self):
        """handles appending the draft round change text"""
        self.results_text.append("\n")
        text = f"************ Round:{self.currentRound} ************** \n"
        self.results_text.append(text)

    def log_draft_round_result(self, teamName, player_selection):
        '''Handles logging the draft result for a team during any given round'''
        text = f"{teamName} - {self.overallSelectionNumber}: {player_selection} \n"
        #stripped_text = text.replace("{", "}", "'", "")
        self.results_text.append(text)

    def write_output_files(self):
        '''Creates output files displaying the results of the draft'''
        try:
            with open("draft_results.txt", 'a') as results_file:
                for line in self.results_text:
                    results_file.write(line)
        except Exception as error:
            print(f"Error writing to file: {error}")

        try:
            final_rosters_list = []
            with open("final_rosters.txt", 'a') as final_rosters:
                for team in self.teams:
                    final_rosters_list.append(team.build_roster_string())
                for roster in final_rosters_list:
                    for line in roster:
                        final_rosters.write(line)
        except Exception as error:
            print(f"Error writing to file: {error}")
