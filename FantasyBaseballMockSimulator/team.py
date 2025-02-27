#Represents a team in fantasy baseball

class Team():

    def  __init__(self, team_name):
        '''Represents a team in fantasy baseball. Each team is composed of a team name, and a dictionary
        representing each position on the team and the corresponding players'''
        self.teamName = team_name
        self.roster = {
            "C":[],
            "1B": [],
            "2B": [],
            "3B": [],
            "SS": [],
            "IF": [],
            "OF": [],
            "U" : [],   #U stands for utility, or any player eligible for offense i.e. any IF, OF, or DH
            "SP": [],
            "RP": [],
            "Bench": []
        }

    def draft_player(self, player_name, player_position):
        '''Handles drafting a player to a team'''
        positions = []
        if '/' in player_position or player_position == 'DH':
            positions = player_position.split('/')
            if 'DH' in positions:
                new_position = 'U'
                positions = [new_position if pos == 'DH' else pos for pos in positions]  #Ohtani case
            return self.assign_roster_spot(player_name, positions)
        else:
            positions.append(player_position)
            return self.assign_roster_spot(player_name, positions)

    def print_team_roster(self):
        '''Prints team roster to the console'''
        print(f"{self.teamName}:")
        for position in self.roster:
            print(f"{position}: {self.roster[position]}")
        print("\n")

    def build_roster_string(self):
        '''Builds a list of strings used to represent each roster after the draft. Used for
        writing the final rosters out to a text file'''
        roster_text = []
        roster_text.append(f"{self.teamName} \n")
        for position in self.roster:
            roster_text.append(f"{position}: {self.roster[position]} \n")
        roster_text.append("\n")
        return roster_text

    def assign_roster_spot(self, player_name, positions):
        ''' Assigns player to a team's roster based on player's position'''
        for position in positions:
            match position:
                case 'C':
                    if len(self.roster[position]) == 1:
                        if not self.utility_spots_filled():
                            self.roster["U"].append(player_name)
                            return True
                        else:
                            return False
                    else:
                        self.roster[position].append(player_name)
                        return True
                case '1B' | '2B' | '3B' | 'SS':
                    if len(self.roster[position]) == 1:
                        if len(self.roster["IF"]) == 1:
                            if not self.utility_spots_filled():
                                self.roster["U"].append(player_name)
                                return True
                            else:
                                return False
                        else:
                            self.roster["IF"].append(player_name)
                            return True
                    self.roster[position].append(player_name)
                    return True
                case 'OF':
                    if len(self.roster[position]) == 4:
                        if not self.utility_spots_filled():
                            self.roster["U"].append(player_name)
                            return True
                        else:
                            return False
                    else:
                        self.roster[position].append(player_name)
                        return True
                case 'U' | 'DH':
                    if not self.utility_spots_filled():
                        self.roster["U"].append(player_name)
                        return True
                    else:
                        return False
                case 'SP':
                    if len(self.roster[position]) == 7:
                        return False
                    self.roster[position].append(player_name)
                    return True
                case 'RP':
                    if len(self.roster[position]) == 5:
                        return False
                    self.roster[position].append(player_name)
                    return True
                case 'Bench':
                    self.roster["Bench"].append(player_name)
                    return True

    def utility_spots_filled(self):
        '''Determines if a roster's utility spaces have been filled. Each team's limit is two.'''
        if len(self.roster["U"]) == 2:
            return True
        else:
            return False

    def add_player_to_bench(self, player_name):
        '''Adds a player to a team's bench. Each team has four bench spots'''
        self.roster["Bench"].append(player_name)