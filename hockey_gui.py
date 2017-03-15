import Tkinter
import ttk
import mysql.connector
import numpy as np
import re
import hockey_buildtabs as buildtabs
from AutoCompleteEntry import AutoCompleteEntry

class SimpleAppTk(Tkinter.Tk):
	''' This Tkinter Instance controls the actual GUI and deals with all of the
		GUI interactions, it leaves all of the database management to the 
		Database class.
	'''

	def __init__(self,parent):
		''' This initialises the TK Instance, it also creates the applications
			database instance. Calls the initialize method which begins
			building the GUI.
		'''

		Tkinter.Tk.__init__(self,parent)
		self.parent = parent
		self.db = Database()
		self.refresh()
		
		self.tab_up = None
		
		self.initialize()

	def initialize(self):
		''' Creates the grid and the two frames within the main GUI, the tab
			switching buttons and the main_frame which holds the individual
			tabs one at a time.
		'''
		self.grid()

		self.top_frame = Tkinter.Frame(self)
		self.top_frame.grid(column=0,row=0)
		self.top_frame.isgridded=True

		self.tab_buttons(self.top_frame)

		self.main_frame = [buildtabs.TabOne(self), None, None, None]
		self.tab_up = 0

	def refresh(self):
		''' Refreshes the Applications holding values from the database to
			account for any updates to the database that may have happened
			since the last refreshing call.
		'''
		self.teams = self.db.get_team_list()
		self.player_list = self.db.get_player_list()
		self.club_list = self.db.get_opp_list()
		self.season_list = self.db.get_seasons()

	def tab_buttons(self,framing):
		''' Builds the tab switching buttons, which change the currently active
			operation tab by calling the build tab utility in the tab file.
		'''
		tab1_button = Tkinter.Button(framing,text=u"Go to Game Addition Tab",
			command=lambda:buildtabs.build_tab(self, 0))
		tab1_button.grid(column=0,row=0,columnspan=2)
		tab2_button = Tkinter.Button(framing,text=u"Go to Management Tab",
			command=lambda:buildtabs.build_tab(self, 1))
		tab2_button.grid(column=2,row=0,columnspan=2)
		tab3_button = Tkinter.Button(framing,text=u"Go to Statistics Tab",
			command=lambda:buildtabs.build_tab(self, 2))
		tab3_button.grid(column=4,row=0,columnspan=2)
		tab4_button = Tkinter.Button(framing,text=u"Go to Game View Tab",
			command=lambda:buildtabs.build_tab(self, 3))
		tab4_button.grid(column=6,row=0,columnspan=2)

	def main_err_bar(self,err_string):
		''' Builds the main error bar with the text string showing the value
			of the err_string parameter.
		'''
		self.errlabelVar = Tkinter.StringVar()
		errlabel = Tkinter.Label(self,textvariable=self.errlabelVar,
			anchor="w",fg="white",bg="black")
		errlabel.grid(column=0,row=2,columnspan=6,sticky='EW')
		self.errlabelVar.set(err_string)

class Database():
	''' This is the actual database, this class needs to handle all of the
		loading, changing and adding to the MYSQL database while the App
		class deals with the GUI.
	'''

	def __init__(self):
		''' Initialises the database, this should take parameters from outside
			for the username, password and database host/name. At this stage
			just uses the database.
		'''
		self.cnx = mysql.connector.connect(user='matt', password='Olivia0815', 
		host='localhost', database='taierihockey')
		self.cursor = self.cnx.cursor()

	#These methods are non specific database management methods
	def db_command(self,cmd_string,result=True):
		''' Sends the database an MYSQL command with the command from 
			cmd_string.
		'''
		# print cmd_string
		self.cursor.execute(cmd_string)
		if result==True:
			response = self.cursor.fetchall()
			return (response)
		else:
			self.commit()

	def __truncate_table(self,table):
		''' Truncates a table, this method should not be called unless
			absolutely neccessary.
			Is not currently being used anywhere.
		'''
		if self.test_for_table(table):
			self.cursor.execute("truncate table " + table)

	def test_for_table(self,table):
		if len(self.db_command("SHOW TABLES LIKE '" + table + "';")) > 0:
			return True
		else: return False

	def select_from_table(self,table,selection,where_type=None,where_info=None):
		# print table
		if self.test_for_table(table):
			if not where_type:
				return self.db_command("select " + selection + " from " + table + ";")
			elif not where_info:
				return
			elif len(where_type) == len(where_info):
				if len(where_info) == 1:
					string_out = "select " + selection + " from " + table + " where " + where_type[0] + " = '" + where_info[0]
				else:
					string_out = "select " + selection + " from " + table + " where " + where_type[0] + " = '" + where_info[0]
					for a in range(len(where_type)):
						if a != 0:
							string_out += "' and " + where_type[a] + " = '" + where_info[a]
				return self.db_command(string_out + "';")
			else:
				return

	def select_whole_table(self,table):
		if self.test_for_table(table):
			return self.db_command("select * from " + table + ";")

	def close(self):
		self.cnx.commit()
		self.cnx.close()

	def commit(self):
		''' Commits any changes to the database, this does not need to be called
				for Queries.
		'''
		self.cnx.commit()

	def tuple_to_list(self,tup):
		list_out = []
		if tup != None:
			for a in tup:
				list_out.append(str(a[0]))
			return list_out
		return None

	#These methods are more specific to the actual hockey gui.
	def add_player(self,player_name,gender):
		''' This method simply adds a new player into the system, this method
			does not have any safety checks, these need to be done by the
			calling method.
		'''
		if "'" in player_name:
				player_name = player_name.replace("'","''")
		self.db_command("INSERT into players (name,gender) values ('" + player_name + "','" + gender + "');",result=False)

	def get_player_list(self,gender=False):
		if gender == False:
			players = self.select_from_table('players','name')
			return self.tuple_to_list(players)
		else:
			players = self.select_from_table('players','name',['gender'],[gender])
			return self.tuple_to_list(players)

	def rename_player(self,old,new):
		p_id = self.get_player_id(player_name=old)

		self.db_command("UPDATE players SET name='" + new + "' WHERE id='" + str(p_id) + "';",result=False)

	def get_team_list(self,teamID=None):
		if teamID == None:
			teams = self.select_from_table('teams','name')
			return self.tuple_to_list(teams)
		else:
			team = self.select_from_table('teams','name',['id'],[str(teamID)])
			return self.strip_single_info(team)

	def get_team_id(self,name=None,gender=None):
		if gender == None:
			teamid = self.select_from_table('teams','id',['name'],[name])
			return self.strip_single_info(teamid)
		else:
			teamid = self.select_from_table('teams','id',['gender'],[gender])
			return self.tuple_to_list(teamid)

	def strip_single_info(self,item):
		''' Takes the standard format of a single piece of information returned
				from the database and returns just the information without the tuple.
		'''
		if item == []:
			return item
		else:
			return item[0][0]

	def get_gender(self,team=None,teamID=None):
		if team !=None:
			gen = self.select_from_table('teams','gender',['name'],[team])
		elif teamID !=None:
			gen = self.select_from_table('teams','gender',['id'],[str(teamID)])
		return self.strip_single_info(gen)

	def get_opp_list(self,clubID=None):
		if clubID == None:
			opp = self.select_from_table('opposition','clubname')
			return self.tuple_to_list(opp)
		else:
			opp = self.select_from_table('opposition','clubname',['id'],[str(clubID)])
			return self.strip_single_info(opp)

	def get_opp_ranks(self,club,gen,teamID=None):
		if " " in club:
			club = club.replace(" ","_")
		if club == "Taieri":
			if teamID == None:
				ranks = self.select_from_table('teams','rank',where_type=['gender'],where_info=[gen])
				return self.tuple_to_list(ranks)
			else:
				ranks = self.select_from_table('teams','rank',where_type=['gender','id'],where_info=[gen,str(teamID)])
				return self.strip_single_info(ranks)
		else:
			if teamID == None:
				ranks = self.select_from_table(club,'rank',where_type=['gender'],where_info=[gen])
				return self.tuple_to_list(ranks)
			else:
				ranks = self.select_from_table(club,'rank',where_type=['gender','teamID'],where_info=[gen,str(teamID)])
				return self.strip_single_info(ranks)

	def get_opp_nick(self,club,gen,rank,nickname=None):
		if " " in club:
				club = club.replace(" ","_")
		if nickname == None:
			w_t = ['gender','rank']
			w_i = [gen,rank]
			if club == 'Taieri':
				nick = self.select_from_table('teams','name',where_type=w_t,where_info=w_i)
			else:
				nick = self.select_from_table(club,'nickname',where_type=w_t,where_info=w_i)
		else:
			if club == 'Taieri':
				nick = self.select_from_table('teams','id',where_type=['name'],where_info=[nickname])
			else:
				nick = self.select_from_table(club,'teamID',where_type=['nickname'],where_info=[nickname])
			
		return self.strip_single_info(nick)

	def add_club(self,club):
		cmd_string = "INSERT into opposition (clubname) values ('" + club + "');"
		self.db_command(cmd_string,result=False)
		if not self.test_for_table(club):
			if " " in club:
				club = club.replace(" ","_")
			self.db_command("CREATE table " + club + " ( teamID int(11) NOT NULL auto_increment, nickname varchar(255), gender enum('M','F'), rank varchar(1), primary key (teamID));",result=False)

	def get_seasons(self):
		seasons = self.select_from_table('seasons','year')
		seasons = self.tuple_to_list(seasons)
		return seasons

	def add_season(self,new_season):
		cmd_string = "INSERT into seasons (year) values ('" + new_season + "');"
		self.db_command(cmd_string,result=False)

	def add_team(self,club,gen,rank,nickname):
		if " " in club:
			club = club.replace(" ","_")
				
		''' Adds a new team to the Database, given the club to add to and the
				gender rank and nickname of the team to add.
		'''
		self.db_command("INSERT into " + club + " (nickname,gender,rank) values ('" + nickname + "','" + gen + "','" + rank + "');", result=False)

	def get_game_id(self,date,teamID):
		id_inf = self.select_from_table('games','id',['teams_id','datevar'],[str(teamID),date])
		if id_inf == []:
			return None, False
		else:
			return self.strip_single_info(id_inf), True

	def get_player_id(self,player_name=None):
		if player_name == None:
			ids = self.select_from_table('players','id')
			return self.tuple_to_list(ids)
		else:
			if "'" in player_name:
				player_name = player_name.replace("'","''")
			id_inf = self.select_from_table('players','id',['name'],[player_name])
			return self.strip_single_info(id_inf)

	def get_player_name(self,player_id):
		if player_id != None:
			pl_inf = self.select_from_table('players','name',['id'],[str(player_id)])
			return self.strip_single_info(pl_inf)
		else:
		 return None

	def add_game_main(self,tup,score,opp_score):
		team = tup[0]
		players = tup[1]
		goals = tup[2]
		date = tup[3]
		opp = tup[4] 
		opp_rank = tup[5]
		gen = tup[6]
		squad_size = tup[7]

		teamID = self.strip_single_info(self.select_from_table('teams','id',['name'],[team]))
		oppID = self.strip_single_info(self.select_from_table('opposition','id',['clubname'],[opp]))
		if " " in opp:
			opp = opp.replace(" ","_")
		if opp == 'Taieri':
			rankID = self.strip_single_info(self.select_from_table('teams','id',['rank','gender'],[opp_rank,gen]))
		else:
			rankID = self.strip_single_info(self.select_from_table(opp,'teamID',['rank','gender'],[opp_rank,gen]))

		game_id, state = self.get_game_id(date,teamID)

		if state == False:
			game_string = "INSERT into games (teams_id, opposition_id, opp_rank_id, datevar, score, opp_score) values ('" + \
			 str(teamID) + "','" + str(oppID) + "','" + str(rankID) + "','" + date + "','" + score + "','" + opp_score + "');"
			self.db_command(game_string,result=False)
			game_id, state = self.get_game_id(date,teamID)
			self.add_game_players(game_id,players,squad_size)
			self.add_game_goals(game_id,goals,squad_size)
			return None
		else:
			return "This team already played on this day in the Database"

	def add_game_players(self,game_id,players,squad_size):
		columns = ['playerOne', 'playerTwo', 'playerThree', 'playerFour', 'playerFive', 'playerSix', 'playerSeven', 'playerEight','playerNine','playerTen','playerEleven','playerTwelve','playerThirteen','playerFourteen','playerFifteen','playerSixteen']
		command_str = "INSERT into playersused (games_id,"

		for a in range(squad_size):
			command_str += columns[a] + ","

		command_str = command_str[:-1] + ") values (" + str(game_id) + ",'"

		for a in range(squad_size):
			person = self.get_player_id(players[a])
			command_str += str(person) + "','"

		command_str = command_str[:-2] + ")"

		self.db_command(command_str,result=False)

	def add_game_goals(self,game_id,goals,squad_size):
		columns = ['playerOne', 'playerTwo', 'playerThree', 'playerFour', 'playerFive', 'playerSix', 'playerSeven', 'playerEight','playerNine','playerTen','playerEleven','playerTwelve','playerThirteen','playerFourteen','playerFifteen','playerSixteen']
		command_str = "INSERT into playersgoals (games_id,"

		for a in range(int(squad_size)):
			command_str += columns[a] + ","

		command_str = command_str[:-1] + ") values (" + str(game_id) + ",'"

		for a in range(int(squad_size)):
			
			command_str += str(goals[a]) + "','"

		command_str = command_str[:-2] + ")"

		# print command_str

		self.db_command(command_str,result=False)

	def get_game_list(self,season,team):
		if team == 'All Teams':
			teamID = None
		elif team == 'Mens Teams':
			teamID = self.get_team_id(gender='M')
		elif team == 'Womens Teams':
			teamID = self.get_team_id(gender='F')
		else:
			teamID = [self.get_team_id(name=team)]
		 
		if season == 'All Seasons':
			if teamID == None:
				gameslist = self.select_from_table('games','id')
			else:
				gameslist = []
				for tee in teamID:
					var = self.select_from_table('games','id',['teams_id'],[str(tee)])
					if var != []:
						for a in var:
							gameslist.append(a)
		else:
			if teamID == None:
				gameslist = self.select_from_table('games','id',['YEAR(datevar)'],[str(season)])
			else:
				gameslist = []
				for tee in teamID:
					var = self.select_from_table('games','id',['teams_id','YEAR(datevar)'],[str(tee),str(season)])
					if var != []:
						for a in var:
							gameslist.append(a)

		return_list = []
		for a in gameslist:
			return_list.append(a[0])
		return return_list

	def get_game_info(self,gameslist):
		inf = []
		for game in gameslist:
			inf.append(self.db_command("SELECT * FROM games JOIN playersused ON games.id = playersused.games_id JOIN playersgoals  ON games.id = playersgoals.games_id WHERE games.id = '" + str(game) + "';")[0])
		return inf

	def get_players_played_games(self,player_id):
		pl_num = ['playerOne', 'playerTwo', 'playerThree', 'playerFour', 'playerFive', 'playerSix', 'playerSeven', 'playerEight','playerNine','playerTen','playerEleven','playerTwelve','playerThirteen','playerFourteen','playerFifteen','playerSixteen']
		array = []
		for a in pl_num:
			newlist = (self.tuple_to_list(self.select_from_table('playersUsed','games_id',where_type=[a],where_info=[str(player_id)])))
			for b in newlist:
				array.append(b)

			array.append(0)
		return array

	def merge_players(self,keep_id,delete_id):
		pl_num = ['playerOne', 'playerTwo', 'playerThree', 'playerFour', 'playerFive', 'playerSix', 'playerSeven', 'playerEight','playerNine','playerTen','playerEleven','playerTwelve','playerThirteen','playerFourteen','playerFifteen','playerSixteen']
		to_change = self.get_players_played_games(delete_id)
		
		count = 0
		for bb in to_change:
			if bb == 0:
				count += 1
			else:
				self.db_command("UPDATE playersUsed SET " + pl_num[count] + "='" + str(keep_id) + "' WHERE games_id='" + bb + "';",result=False) 
		self.db_command("DELETE from players WHERE id='" + str(delete_id) + "';",result=False)


if __name__ == "__main__":

	app = SimpleAppTk(None)
	app.title('Hockey GUI')
	app.mainloop()
	app.db.close()

	# db = Database()
	# db.get_players_played_games(318)
	# db.merge_players(1,346)
	# db.commit()

	# db.close()
