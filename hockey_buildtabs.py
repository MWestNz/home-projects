import Tkinter
import ttk
import mysql.connector
import re
from AutoCompleteEntry import AutoCompleteEntry, AutoCompleteCombobox
import copy
import numpy as np

def build_tab(parent, index):
	parent.db.commit()
	parent.refresh()
	if parent.tab_up == index:
		return
	else:
		if parent.tab_up != None:
			parent.main_frame[parent.tab_up].destroy()
		parent.tab_up = index
		if index == 0:
			parent.main_frame[index] = TabOne(parent)
		elif index == 1:
			parent.main_frame[index] = TabTwo(parent)
		elif index == 2:
			parent.main_frame[index] = TabThree(parent)
		elif index == 3:
			parent.main_frame[index] = TabFour(parent)

class TabOne(Tkinter.Frame):

	def __init__(self,parent):
		Tkinter.Frame.__init__(self,parent)
		self.buildgrid_one(parent)
		self.grid(column=0,row=1)
		self.isgridded=True
		self.parent = parent

	def buildgrid_one(self, parent):

		self.build_main_game_result(parent)

		self.errLabel = Tkinter.StringVar()
		self.error_label = Tkinter.Label(self,textvariable=self.errLabel, anchor="w",fg="white",bg="black")
		self.error_label.grid(column=0,row=15,columnspan=7,sticky='EW')

		self.botLabel = Tkinter.StringVar()
		self.bottom_label = Tkinter.Label(self,textvariable=self.botLabel, anchor="w",fg="white",bg="black")
		self.bottom_label.grid(column=0,row=16,columnspan=7,sticky='EW')

		team_button = Tkinter.Button(self,text=u"Enter!",
		command=lambda:self.OnButtonClick(parent))
		team_button.grid(column=7,row=16,columnspan=1)

	def opposition_control(self, parent):
		
		self.player_section(parent)

		self.squad_size(parent)

		self.opp_var = Tkinter.StringVar()
		opp_club_drop_list = parent.club_list

		self.team_gen = parent.db.get_gender(team=self.team_var.get())

		self.opp_drop = Tkinter.OptionMenu(self,self.opp_var,*opp_club_drop_list,command=lambda x:self.opp_rank_control(parent))
		self.opp_drop.grid(row=11,column=4,columnspan=1)

		self.squadVar = Tkinter.StringVar()
		self.squadlabel = Tkinter.Label(self,textvariable=self.squadVar, anchor="w",fg="white",bg="blue")
		self.squadlabel.grid(column=3,row=11,columnspan=1,sticky='EW')
		self.squadVar.set("Opposition Club")

	def opp_rank_control(self,parent):
		self.opp_r_var = Tkinter.StringVar()
		opp_club_r_drop_list = parent.db.get_opp_ranks(self.opp_var.get(),self.team_gen)
		if opp_club_r_drop_list != []:
			opp_club_r_drop_list.sort()
			self.opp_r_drop = Tkinter.OptionMenu(self,self.opp_r_var,*opp_club_r_drop_list,command=lambda x:self.print_nick(parent))
			self.opp_r_drop.grid(row=11,column=6,columnspan=1)

			self.squadVar = Tkinter.StringVar()
			self.squadlabel = Tkinter.Label(self,textvariable=self.squadVar, anchor="w",fg="white",bg="blue")
			self.squadlabel.grid(column=5,row=11,columnspan=1,sticky='EW')
			self.squadVar.set("Team Rank")

			self.nickVar = Tkinter.StringVar()
			self.nicklabel = Tkinter.Label(self,textvariable=self.nickVar, anchor="w",fg="white",bg="black")
			self.nicklabel.grid(column=6,row=10,columnspan=1,sticky='EW')
		else:
			self.errLabel.set('There is no teams of this gender from this club. Please try again.')

	def print_nick(self,parent):
		self.date_controls(parent)

		var = parent.db.get_opp_nick(self.opp_var.get(),self.team_gen,self.opp_r_var.get())
		self.nickVar.set(var)

	def date_controls(self, parent):
		self.date_labels = ["Day", "Month", "Year"]
		self.dateLabel = []
		self.date_label =[]

		for a in range(len(self.date_labels)):
			self.dateLabel.append(Tkinter.StringVar())
			self.date_label.append(Tkinter.Label(self,textvariable=self.dateLabel[a], anchor="w",fg="white",bg="black"))
			self.date_label[a].grid(column=4+a,row=12,columnspan=1,sticky='EW')
			self.dateLabel[a].set(self.date_labels[a])

		self.drop_day_var = Tkinter.StringVar()
		day_list = ['1','2','3','4','5','6','7','8','9','10','11','12','13','14','15','16','17','18','19','20','21','22','23','24','25','26','27','28','29','30','31']
		self.drop_day = Tkinter.OptionMenu(self,self.drop_day_var,*day_list)
		self.drop_day.grid(row=13,column=4,columnspan=1)

		self.drop_mon_var = Tkinter.StringVar()
		self.mon_list = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']
		self.drop_mon = Tkinter.OptionMenu(self,self.drop_mon_var,*self.mon_list)
		self.drop_mon.grid(row=13,column=5,columnspan=1)

		self.drop_year_var = Tkinter.StringVar()

		parent.season_list.sort()

		self.drop_year = Tkinter.OptionMenu(self,self.drop_year_var,*parent.season_list)
		self.drop_year.grid(row=13,column=6,columnspan=1)

		self.dateVar = Tkinter.StringVar()
		self.datelabel = Tkinter.Label(self,textvariable=self.dateVar, anchor="w",fg="white",bg="blue")
		self.datelabel.grid(column=3,row=13,columnspan=1,sticky='EW')
		self.dateVar.set("Date of Game")

	def squad_size(self, parent):
		self.squad_size_var = Tkinter.StringVar()
		squad_drop_list = ['8','9','10','11','12','13','14','15','16']
		self.squad_drop = Tkinter.OptionMenu(self,self.squad_size_var,*squad_drop_list)
		self.squad_drop.grid(row=9,column=4,columnspan=1)

		self.squadVar = Tkinter.StringVar()
		self.squadlabel = Tkinter.Label(self,textvariable=self.squadVar, anchor="w",fg="white",bg="blue")
		self.squadlabel.grid(column=3,row=9,columnspan=1,sticky='EW')
		self.squadVar.set("Number of Players used")

	def player_section(self, parent):

		gend = parent.db.get_gender(team=self.team_var.get())
		self.player_list = copy.deepcopy(parent.db.get_player_list(gender=gend))

		self.title_label = []
		self.player_title = []

		self.goals_title = []
		self.goals_label = []

		self.player_title.append(Tkinter.StringVar())
		self.player_title.append(Tkinter.StringVar())
		self.title_label.append(Tkinter.Label(self,textvariable=self.player_title[0], anchor="w",fg="black"))
		self.title_label.append(Tkinter.Label(self,textvariable=self.player_title[1], anchor="w",fg="black"))

		self.player_title[0].set("Player Name")
		self.player_title[1].set("Player Name")

		self.title_label[0].grid(row=3, column=1,columnspan=1)
		self.title_label[1].grid(row=3, column=4,columnspan=1)

		self.goals_title.append(Tkinter.StringVar())
		self.goals_title.append(Tkinter.StringVar())

		self.goals_label.append(Tkinter.Label(self,textvariable=self.goals_title[0], anchor="w",fg="black"))
		self.goals_label.append(Tkinter.Label(self,textvariable=self.goals_title[1], anchor="w",fg="black"))

		self.goals_title[0].set("Goals Scored")
		self.goals_title[1].set("Goals Scored")

		self.goals_label[0].grid(row=3, column=2,columnspan=1)
		self.goals_label[1].grid(row=3, column=5,columnspan=1)

		self.player_text_fields = []
		self.player_labels = []
		self.player_label_vars = []
		self.goals_variable = []

		for a in range(11):
			self.player_label_vars.append(Tkinter.StringVar())
			self.player_labels.append(Tkinter.Label(self,textvariable=self.player_label_vars[a], anchor="w",fg="black"))
			self.player_label_vars[a].set("Player " + str(a + 1))
			self.player_labels[a].grid(row=4+a, column=0,columnspan=1)
			self.player_text_fields.append(AutoCompleteCombobox(self.player_list, self,a,postcommand=lambda:self.clean_player_list(parent)))
			self.player_text_fields[a].grid(row=4+a, column=1, columnspan=1, pady=(10,10))

			self.goals_variable.append(Tkinter.StringVar(value=0))
			self.goals_entry = Tkinter.Entry(self,textvariable=self.goals_variable[a])
			self.goals_entry.grid(row=4+a, column=2, columnspan=1, pady=(10,10), sticky='EW')
		a += 1

		for b in range(5):
			self.player_label_vars.append(Tkinter.StringVar())
			self.player_labels.append(Tkinter.Label(self,textvariable=self.player_label_vars[a+b], anchor="w",fg="black"))
			self.player_label_vars[a+b].set("Player " + str(b + 12))
			self.player_labels[a+b].grid(row=4+b, column=3,columnspan=1)
			self.player_text_fields.append(AutoCompleteCombobox(self.player_list, self,b+a,postcommand=lambda:self.clean_player_list(parent)))
			self.player_text_fields[a+b].grid(row=4+b, column=4, columnspan=1, pady=(10,10))

			self.goals_variable.append(Tkinter.StringVar(value=0))
			self.goals_entry = Tkinter.Entry(self,textvariable=self.goals_variable[a+b])
			self.goals_entry.grid(row=4+b, column=5, columnspan=1, pady=(10,10), sticky='EW')

	def clean_player_list(self,parent):
		parent.refresh()
		gend = parent.db.get_gender(team=self.team_var.get())
		self.player_list = copy.deepcopy(parent.db.get_player_list(gender=gend))

		new_list = []
		selected_list = []

		for aa in self.player_text_fields:
			if aa.get() != "":
				selected_list.append(aa.get())

		for name in self.player_list:
			if name not in selected_list:
				new_list.append(name)

		for aa in self.player_text_fields:
			if aa.get() == "":
				aa.set_main_list(new_list)

	def get_selected_list(self):
		selected_list = []

		for aa in self.player_text_fields:
			if aa.get() != "":
				selected_list.append(aa.get())

		return selected_list

	def build_main_game_result(self, parent):

		self.buildlabels(parent, ["Team Name", "Score", "Opp Score"])

		lst1 = parent.teams
		self.team_var = Tkinter.StringVar()
		self.drop = Tkinter.OptionMenu(self,self.team_var,*lst1,command=lambda x:self.opposition_control(parent))
		self.drop.grid(column=1,row=1,columnspan=1)
		
		label_array = ["Enter Team Score", "Enter Opposition Score"]
		self.buildtextfields(parent, label_array)

		self.finalLabel = Tkinter.StringVar()
		label = Tkinter.Label(self,textvariable=self.finalLabel, anchor="w",fg="white",bg="black")
		label.grid(column=0,row=2,columnspan=8,sticky='EW')

	def buildtextfields(self, parent, fieldArray):
		count = 0
		self.team_variable = []
		for aa in fieldArray:
			self.team_variable.append(Tkinter.StringVar())
			self.team_entry = Tkinter.Entry(self,textvariable=self.team_variable[count])
			self.team_entry.grid(column=2*count + 3,row=1,columnspan=1,sticky='EW')
			self.labelVariable.set(fieldArray[count])
			count += 1

	def buildlabels(self, parent, labelArray):
		count = 0
		for aa in labelArray:
			self.labelVariable = Tkinter.StringVar()
			label = Tkinter.Label(self,textvariable=self.labelVariable, anchor="w",fg="white",bg="blue")
			label.grid(column=2*count,row=1,columnspan=1,sticky='EW')
			self.labelVariable.set(labelArray[count])
			count += 1

	def OnButtonClick(self, parent):
		''' Need to make sure we check all of the entries for possible errors.
			Start with the main_game results and then move to the individual
			parts.
		'''
		self.errLabel.set("")
		score =	self.team_variable[0].get()
		opp = self.team_variable[1].get()

		team = self.team_var.get()
		if team == "":
			self.errLabel.set("Please select the team that played the game first")
			return


		num_players = self.squad_size_var.get()
		self.name_list = []
		self.goals_list = []

		if score == "" or opp == "":
			self.errLabel.set("Please enter scores for both teams correctly")
		else:
			if num_players == "":
				self.errLabel.set("Please select the correct number of players used in this game.")
			else:
				for zz in range(16):
					if zz < int(num_players):
						if (not self.player_text_fields[zz].get()):
							self.errLabel.set("Player Number " + str(zz+1) + " has not been entered.")
							return
						elif not(self.player_text_fields[zz].get() in parent.player_list):
							self.errLabel.set("Player Number " + str(zz+1) + " has not been entered correctly.")
							return
						elif (zz > 0) and (self.player_text_fields[zz].get() in self.name_list):
							self.errLabel.set("Player Number " + str(zz+1) + " is a duplicate of a previous player.")
							return
					else:
						if self.player_text_fields[zz].get() != "":
							self.errLabel.set("Player Number " + str(zz+1) + " is excess to the selected squad size, please revise selections.")
							return
					self.name_list.append(self.player_text_fields[zz].get())
					goal = self.goals_variable[zz].get()
					if goal == "":
						goal = 0
					self.goals_list.append(int(goal))
				if sum(self.goals_list) != int(score):
					self.errLabel.set("Please ensure the goal scorers and the score are recorded correctly.")
				if not self.drop_day_var.get() or not self.drop_mon_var.get() or not self.drop_year_var.get():
					self.errLabel.set("Please select the date that the game was played on from the drop down lists.")
				else:
					count = 0
					for a in self.mon_list:
						count +=1
						if a == self.drop_mon_var.get():
							self.mon_ind = count
					self.errLabel.set("")
					self.add_game_to_db(parent,score,opp)
					parent.db.commit()
					parent.refresh()
					if score > opp:
						self.botLabel.set("Nice work the " + team + " won " + score + "-" + opp + "!" )
					elif opp > score:
						self.botLabel.set("Ohh Buggar the " + team + " lost " + score + "-" + opp + "!" )
					else:
						self.botLabel.set("A  " + score + "-" + opp + " draw for the " + team + " is OK !" )
	
	def add_game_to_db(self,parent,score,opp_score):
		team = self.team_var.get()
		players = self.name_list
		goals = self.goals_list
		day = self.drop_day_var.get()
		year = self.drop_year_var.get()
		month = self.mon_ind
		opp = self.opp_var.get()
		opp_rank = self.opp_r_var.get()
		squad_size = self.squad_size_var.get()

		if int(day) < 10:
			day = "0" + str(day)
		if month < 10:
			month = "0" + str(month)

		date = str(self.drop_year_var.get()) + "-" + month + "-" + day

		arg_tup =(team,players,goals,date,opp,opp_rank,self.team_gen,int(squad_size))

		err = parent.db.add_game_main(arg_tup,score,opp_score)

		if err != None:
			self.botLabel.set(err)
			print err

class TabTwo(Tkinter.Frame):

	def __init__(self,parent):
		Tkinter.Frame.__init__(self,parent)
		self.buildgrid_two(parent)
		self.grid(column=0,row=1)
		self.isgridded=True

	def clean_player_list(self,parent):
		parent.refresh()
		gend = parent.db.get_gender(team=self.team_var.get())
		self.player_list = copy.deepcopy(parent.db.get_player_list(gender=gend))

		new_list = []
		selected_list = []

		for aa in self.player_text_fields:
			if aa.get() != "":
				selected_list.append(aa.get())

		for name in self.player_list:
			if name not in selected_list:
				new_list.append(name)

		for aa in self.player_text_fields:
			if aa.get() == "":
				aa.set_main_list(new_list)


	def buildgrid_two(self, parent):
		self.buildlabels = ["Add New Player", "Edit Player Name", "Edited Player Name", 'Select New Player Gender','Add New Club','Club for New Team','Add New Team','Merge Players Into','Merge and Delete']
		self.drop_list = ['M', 'F']
		
		self.build_add_player(parent)		
		self.build_edit_player(parent)
		self.build_merge_players(parent)
		self.build_add_new_team(parent)
		self.season_management(parent)
		
	def build_edit_player(self,parent):
		self.current_player_label_var = Tkinter.StringVar()
		self.current_player_label = Tkinter.Label(self,textvariable=self.current_player_label_var, anchor="w",fg="black")
		self.current_player_label.grid(column=1,row=3,columnspan=1,sticky='EW',pady=(10,0))
		self.current_player_label_var.set(self.buildlabels[1])
		self.current_players = AutoCompleteCombobox(parent.player_list, self,0)
		self.current_players.grid(column=2,row=3,columnspan=1,pady=(10,0))

		self.edit_player_label_var = Tkinter.StringVar()
		self.edit_player_label = Tkinter.Label(self,textvariable=self.edit_player_label_var, anchor="w",fg="black")
		self.edit_player_label.grid(column=3,row=3,columnspan=1,sticky='EW',pady=(10,0))
		self.edit_player_variable = Tkinter.StringVar()
		self.edit_player_entry = Tkinter.Entry(self,textvariable=self.edit_player_variable)
		self.edit_player_entry.grid(column=4,row=3,columnspan=1,sticky='EW',pady=(10,0))
		self.edit_player_label_var.set(self.buildlabels[2])

		edit_button = Tkinter.Button(self,text=u"Enter!", command=lambda:self.OnButtonClick(parent,1))
		edit_button.grid(column=6,row=3,columnspan=1,pady=(10,0))
		self.edit_label_var = Tkinter.StringVar()
		self.edit_label = Tkinter.Label(self,textvariable=self.edit_label_var, anchor="w",fg="white",bg="blue")
		self.edit_label.grid(column=1,row=4,columnspan=6,sticky='EW',pady=(10,0))

	def build_merge_players(self,parent):
		self.m_player_label_var = Tkinter.StringVar()
		self.m_player_label = Tkinter.Label(self,textvariable=self.m_player_label_var, anchor="w",fg="black")
		self.m_player_label.grid(column=1,row=5,columnspan=1,sticky='EW',pady=(10,0))
		self.m_player_label_var.set(self.buildlabels[7])
		self.m_players = AutoCompleteCombobox(parent.player_list, self,0)
		self.m_players.grid(column=2,row=5,columnspan=1,pady=(10,0))

		self.medit_player_label_var = Tkinter.StringVar()
		self.medit_player_label = Tkinter.Label(self,textvariable=self.medit_player_label_var, anchor="w",fg="black")
		self.medit_player_label.grid(column=3,row=5,columnspan=1,sticky='EW',pady=(10,0))
		self.medit_player_variable = Tkinter.StringVar()
		self.medit_player_entry = AutoCompleteCombobox(parent.player_list, self,0)
		self.medit_player_entry.grid(column=4,row=5,columnspan=1,sticky='EW',pady=(10,0))
		self.medit_player_label_var.set(self.buildlabels[8])

		medit_button = Tkinter.Button(self,text=u"Merge!", command=lambda:self.OnButtonClick(parent,5))
		medit_button.grid(column=6,row=5,columnspan=1,pady=(10,0))
		self.medit_label_var = Tkinter.StringVar()
		self.medit_label = Tkinter.Label(self,textvariable=self.medit_label_var, anchor="w",fg="white",bg="blue")
		self.medit_label.grid(column=1,row=6,columnspan=6,sticky='EW',pady=(10,0))

	def build_add_player(self,parent):
		
		self.new_player_label_var = Tkinter.StringVar()
		self.new_player_label = Tkinter.Label(self,textvariable=self.new_player_label_var, anchor="w",fg="black")
		self.new_player_label.grid(column=1,row=1,columnspan=1,sticky='EW')
		self.new_player_variable = Tkinter.StringVar()
		self.new_player_entry = Tkinter.Entry(self,textvariable=self.new_player_variable)
		self.new_player_entry.grid(column=2,row=1,columnspan=1,sticky='EW')
		self.new_player_label_var.set(self.buildlabels[0])

		self.new_player_gender_var = Tkinter.StringVar()
		self.new_player_gen_label = Tkinter.Label(self,textvariable=self.new_player_gender_var, anchor="w",fg="black")
		self.new_player_gen_label.grid(column=3,row=1,columnspan=1,sticky='EW')
		self.new_player_gender_var.set(self.buildlabels[3])

		self.gender_drop_var = Tkinter.StringVar()
		self.gender_drop = Tkinter.OptionMenu(self,self.gender_drop_var,*self.drop_list)
		self.gender_drop.grid(row=1,column=4,columnspan=1)

		add_button = Tkinter.Button(self,text=u"Enter!", command=lambda:self.OnButtonClick(parent,0))
		add_button.grid(column=6,row=1,columnspan=1)
		self.add_label_var = Tkinter.StringVar()
		self.add_label = Tkinter.Label(self,textvariable=self.add_label_var, anchor="w",fg="white",bg="blue")
		self.add_label.grid(column=1,row=2,columnspan=6,sticky='EW')

	def build_add_new_team(self,parent):
		self.new_club_label_var = Tkinter.StringVar()
		self.new_club_label = Tkinter.Label(self,textvariable=self.new_club_label_var, anchor="w",fg="black")
		self.new_club_label.grid(column=1,row=7,columnspan=1,sticky='EW',pady=(10,0))
		self.new_club_label_var.set(self.buildlabels[4])

		self.new_club_variable = Tkinter.StringVar()
		self.new_club_entry = Tkinter.Entry(self,textvariable=self.new_club_variable)
		self.new_club_entry.grid(column=2,row=7,columnspan=1,sticky='EW')

		club_button = Tkinter.Button(self,text=u"Enter!", command=lambda:self.OnButtonClick(parent,2))
		club_button.grid(column=6,row=7,columnspan=1)

		self.old_club_label_var = Tkinter.StringVar()
		self.old_club_label = Tkinter.Label(self,textvariable=self.old_club_label_var, anchor="w",fg="white",bg="blue")
		self.old_club_label.grid(column=3,row=7,columnspan=1,sticky='EW')
		self.old_club_label_var.set("Existing Clubs: ")

		cl_list = parent.db.get_opp_list()

		self.cl_list_var = Tkinter.StringVar()
		self.cl_ld = Tkinter.OptionMenu(self,self.cl_list_var,*cl_list)
		self.cl_ld.grid(column=4,row=7,columnspan=1,sticky='EW')

		self.club_label_var = Tkinter.StringVar()
		self.club_label = Tkinter.Label(self,textvariable=self.club_label_var, anchor="w",fg="white",bg="blue")
		self.club_label.grid(column=1,row=8,columnspan=6,sticky='EW',pady=(10,0))

		newteamlines = ["Club for New Team","Gender of New Team","Rank of New Team","Nickname of New Team"]
		self.club_labels = []
		self.new_team_labels_var = [Tkinter.StringVar(), Tkinter.StringVar(), Tkinter.StringVar(), Tkinter.StringVar()]
		for a in range(len(self.new_team_labels_var)):
			self.club_labels.append(Tkinter.Label(self,textvariable=self.new_team_labels_var[a], anchor="w",fg="white",bg="black"))
			self.club_labels[a].grid(column=2+a,row=9,columnspan=6,sticky='EW',pady=(10,0))
			self.new_team_labels_var[a].set(newteamlines[a])

		self.new_team_label_var = Tkinter.StringVar()
		self.new_team_label = Tkinter.Label(self,textvariable=self.new_team_label_var, anchor="w",fg="black")
		self.new_team_label.grid(column=1,row=10,columnspan=1,sticky='EW',pady=(10,0))
		self.new_team_label_var.set(self.buildlabels[5])

		self.team_club_var = Tkinter.StringVar()
		self.team_drop = Tkinter.OptionMenu(self,self.team_club_var,*parent.db.get_opp_list(),command=lambda x:self.show_these_teams(parent))
		self.team_drop.grid(column=2,row=10,columnspan=1,pady=(10,0))

		self.team_gender_drop_var = Tkinter.StringVar()
		self.team_gender_drop = Tkinter.OptionMenu(self,self.team_gender_drop_var,*self.drop_list,command=lambda x:self.show_these_teams(parent))
		self.team_gender_drop.grid(row=10,column=3,columnspan=1,pady=(10,0))

		self.new_team_rank_var = Tkinter.StringVar()
		self.new_team_rank = Tkinter.Entry(self,textvariable=self.new_team_rank_var)
		self.new_team_rank.grid(column=4,row=10,columnspan=1,sticky='EW',pady=(10,0))

		self.new_team_nick_var = Tkinter.StringVar()
		self.new_team_nick = Tkinter.Entry(self,textvariable=self.new_team_nick_var)
		self.new_team_nick.grid(column=5,row=10,columnspan=1,sticky='EW',pady=(10,0))

		add_button = Tkinter.Button(self,text=u"Enter!", command=lambda:self.OnButtonClick(parent,3))
		add_button.grid(column=6,row=10,columnspan=1)

		self.team_label_var = Tkinter.StringVar()
		self.team_label = Tkinter.Label(self,textvariable=self.team_label_var, anchor="w",fg="white",bg="blue")
		self.team_label.grid(column=1,row=11,columnspan=6,sticky='EW')

	def process_new_team(self,parent,new_club,gen,rank,nickname):
		if self.check_for_nick(parent,new_club,gen,rank,nickname):
			self.team_label_var.set("Team added to the system.")

	def show_these_teams(self,parent):

		if self.team_club_var.get() != "" and self.team_gender_drop_var.get() != "":
			self.t_label_var = Tkinter.StringVar()
			self.t_label = Tkinter.Label(self,textvariable=self.t_label_var, anchor="w",fg="white",bg="black")
			self.t_label.grid(column=4,row=11,columnspan=2,sticky='EW')

			team_list = parent.db.get_opp_ranks(self.team_club_var.get(),self.team_gender_drop_var.get())
			string = ""
			for a in team_list:
				string += a + " "
			self.t_label_var.set(string)

	def check_for_nick(self,parent,club,gen,rank,nickname):
		if nickname == "":
			check = None
		else:
			check = nickname
		if len(parent.db.get_opp_nick(club,gen,rank,check)) != 0:
			self.team_label_var.set("This team nickname already exists you need to review your entries.")
			return False
		else:
			parent.db.add_team(club,gen,rank,nickname)
			return True

	def season_management(self,parent):
		self.season_label_var = Tkinter.StringVar()
		self.season_label = Tkinter.Label(self,textvariable=self.season_label_var, anchor="w",fg="black")
		self.season_label.grid(column=1,row=12,columnspan=1,sticky='EW',pady=(10,0))
		self.season_label_var.set("Add New Season")

		self.new_s_variable = Tkinter.StringVar()
		self.new_s_entry = Tkinter.Entry(self,textvariable=self.new_s_variable)
		self.new_s_entry.grid(column=2,row=12,columnspan=1,sticky='EW')

		self.season_label_var2 = Tkinter.StringVar()
		self.season_label2 = Tkinter.Label(self,textvariable=self.season_label_var2, anchor="w",fg="black")
		self.season_label2.grid(column=3,row=12,columnspan=1,sticky='EW',pady=(10,0))
		self.season_label_var2.set("Current Seasons")

		self.query_s = Tkinter.StringVar()
		self.query_s_drop = Tkinter.OptionMenu(self,self.query_s,*parent.season_list)
		self.query_s_drop.grid(column=4,row=12,columnspan=1,pady=(10,0))

		edit_button = Tkinter.Button(self,text=u"Enter!", command=lambda:self.OnButtonClick(parent,4))
		edit_button.grid(column=6,row=12,columnspan=1,pady=(10,0))

	def OnButtonClick(self, parent, button):
		if button == 0:
			name = self.new_player_entry.get()
			gender = self.gender_drop_var.get()
			if name != "" and self.gender_drop_var.get() !="":
				if (name in parent.player_list):
					self.add_label_var.set("Player " + name + " already in the System.") 
				else:
					parent.db.add_player(name,gender)
					self.add_label_var.set("New Player " + name + " added to the System.") 
			else:
				self.add_label_var.set("Please enter the name of the new player and gender before pressing the button.") 
		elif button == 1:
			if self.edit_player_entry.get() != ""  and self.current_players.get() != "":
				if (self.current_players.get() in parent.player_list):
					self.edit_label_var.set("Player: " + self.current_players.get() + " renamed as " + self.edit_player_entry.get() + " in the System.")
					parent.db.rename_player(self.current_players.get(),self.edit_player_entry.get())
				else:
					self.edit_label_var.set("Existing Player Record does not exist.")
			else:
				self.edit_label_var.set("Please enter the name of current player entry and the new name for player before pressing the button.") 
		elif button == 2:
			new_club = self.new_club_variable.get()
			if new_club != "":
				if (new_club in parent.club_list):
					self.club_label_var.set("This club is already on the list. No need to add this club.")
				else:
					parent.db.add_club(new_club)
					self.club_label_var.set("Club " + new_club + " has been added to the System.")
		elif button == 3:
			new_club = self.team_club_var.get()
			gen = self.team_gender_drop_var.get()
			rank = self.new_team_rank_var.get()
			nickname = self.new_team_nick_var.get()
			if (new_club in parent.club_list):
				if parent.db.get_opp_ranks(new_club,gen) != None:
					if (rank in parent.db.get_opp_ranks(new_club,gen)):
						self.team_label_var.set("This team is already on the list. No need to add this team.")
					else:
						self.process_new_team(parent,new_club,gen,rank,nickname)
				else:
					self.process_new_team(parent,new_club,gen,rank,nickname)
			else:
				self.team_label_var.set("This club is not on the list, you need to add the club first.")
		elif button == 4:
			new_season = self.new_s_variable.get()
			parent.db.add_season(new_season)

		elif button == 5:
			to_keep = self.m_players.get()
			to_delete = self.medit_player_entry.get()
			keep_id = parent.db.get_player_id(to_keep)
			delete_id = parent.db.get_player_id(to_delete)
			if keep_id == delete_id:
				self.medit_label_var.set('Players are the same ID, please review.')
			else:
				parent.db.merge_players(keep_id,delete_id)
				self.medit_label_var.set('Player ' + to_delete + ' now merged into Player ' + to_keep + '.')

		parent.db.commit()
		parent.refresh()

class TabThree(Tkinter.Frame):

	def __init__(self,parent):
		Tkinter.Frame.__init__(self,parent)
		self.buildgrid_three(parent)
		self.grid(column=0,row=1)
		self.isgridded=True		

	def buildgrid_three(self, parent):
		self.build_selection_function(parent)
		self.errLabel = Tkinter.StringVar()
		self.error_label = Tkinter.Label(self,textvariable=self.errLabel, anchor="w",fg="white",bg="black")

	def build_selection_function(self,parent):
		self.q_label_var = Tkinter.StringVar()
		self.q_label = Tkinter.Label(self,textvariable=self.q_label_var, anchor="w",fg="white",bg="blue")
		self.q_label.grid(column=0,row=0,columnspan=1,sticky='EW',pady=(0,10))
		self.q_label_var.set("Choose Options for Query")

		team_list = parent.db.get_team_list()
		self.q_list = ['All Teams', 'Mens Teams', 'Womens Teams'] + team_list
		self.query_team = Tkinter.StringVar()
		self.query_team_drop = Tkinter.OptionMenu(self,self.query_team,*self.q_list)
		self.query_team_drop.grid(column=1,row=0,columnspan=1,pady=(0,10))

		self.s_label_var = Tkinter.StringVar()
		self.s_label = Tkinter.Label(self,textvariable=self.s_label_var, anchor="w",fg="white",bg="blue")
		self.s_label.grid(column=2,row=0,columnspan=1,sticky='EW',pady=(0,10))
		self.s_label_var.set("Seasons")

		season_list = parent.db.get_seasons()
		self.s_list = ['All Seasons'] + season_list
		self.s_team = Tkinter.StringVar()
		self.s_team_drop = Tkinter.OptionMenu(self,self.s_team,*self.s_list)
		self.s_team_drop.grid(column=3,row=0,columnspan=1,pady=(0,10))

		q_button = Tkinter.Button(self,text=u"Send Query",
			command=lambda:self.retreive_stats(parent))
		q_button.grid(column=4,row=0,columnspan=1,pady=(0,10))

		self.base_frame = Tkinter.Frame(master=self,relief=Tkinter.GROOVE)
		self.base_frame.grid(column=0,row=3,columnspan=10)

	def retreive_stats(self,parent):
		if 'next_frame' in dir(self):
			self.next_frame.destroy()

		self.next_frame = Tkinter.Frame(master=self.base_frame)
		self.next_frame.grid(column=0,row=2,columnspan=10)

		self.build_sorts(parent)

		self.fetch_info(parent)
		return

	def fetch_info(self,parent):
		team = self.query_team.get()
		season = self.s_team.get()

		if team == "" or season == "":

			self.error_label.grid(column=0,row=1,columnspan=7,sticky='EW')
			self.errLabel.set("You must select an option for all menus to query the system.")
		else:
			games_list = parent.db.get_game_list(season,team)
			self.error_label.grid_forget()
			if games_list != []:
				self.prepare_result(games_list,parent)
		return 

	def prepare_result(self,games_list,parent):
		self.info = parent.db.get_game_info(games_list)
		self.player_list = parent.db.get_player_list()
		self.id_list = parent.db.get_player_id()
		self.p_index_a = np.zeros(int(self.id_list[len(self.id_list)-1]))
		self.g_index_a = np.zeros(int(self.id_list[len(self.id_list)-1]))
		self.w_index_a = np.zeros(int(self.id_list[len(self.id_list)-1]))
		self.d_index_a = np.zeros(int(self.id_list[len(self.id_list)-1]))
		self.l_index_a = np.zeros(int(self.id_list[len(self.id_list)-1]))

		for a in self.info:
			for b in range(16):
				player_id = a[b+8]
				if player_id != None:
					self.p_index_a[player_id-1] += 1
					self.g_index_a[player_id-1] += a[b+25]
					if a[5] > a[6]:
						self.w_index_a[player_id-1] += 1
					elif a[5] == a[6]:
						self.d_index_a[player_id-1] += 1
					else:
						self.l_index_a[player_id-1] += 1

		self.p_index = []
		self.g_index = []
		self.w_index = []
		self.d_index = []
		self.l_index = []
		self.name_index = []

		for a in range(len(self.p_index_a)):
			if self.p_index_a[a] != 0:
				self.p_index.append(self.p_index_a[a])
				self.g_index.append(self.g_index_a[a])
				self.w_index.append(self.w_index_a[a])
				self.d_index.append(self.d_index_a[a])
				self.l_index.append(self.l_index_a[a])
				self.name_index.append(parent.db.get_player_name(a+1))

		self.print_array = []
		self.string_array = []
		self.print_array2 = []
		self.string_array2 = []
		self.print_array3 = []
		self.string_array3 = []
		self.print_array4 = []
		self.string_array4 = []

		
		self.canvas=Tkinter.Canvas(master=self.next_frame)
		self.frame=Tkinter.Frame(master=self.canvas)
		self.myscrollbar=Tkinter.Scrollbar(self.next_frame,orient="vertical",command=self.canvas.yview)
		self.canvas.configure(yscrollcommand=self.myscrollbar.set)

		self.myscrollbar.pack(side="right",fill="y")
		self.canvas.pack(side="left")
		self.canvas.create_window((0,0),window=self.frame,anchor='nw')
		self.frame.bind("<Configure>",lambda event: self.frame_function(self.canvas))

		self.sort_by(1,parent)

	def frame_function(event,canvas):
		canvas.configure(scrollregion=canvas.bbox("all"),width='10c',height='10c')
		return

	def build_sorts(self,parent):

		tab1_button = Tkinter.Button(self.base_frame,text=u"Player",padx=20,
			command=lambda:self.sort_by(0,parent))
		tab1_button.grid(column=0,row=0,columnspan=2)
		tab2_button = Tkinter.Button(self.base_frame,text=u"Matches Played",
			command=lambda:self.sort_by(1,parent))
		tab2_button.grid(column=2,row=0,columnspan=2)
		tab3_button = Tkinter.Button(self.base_frame,text=u"Goals Scored",
			command=lambda:self.sort_by(2,parent))
		tab3_button.grid(column=4,row=0,columnspan=2)
		tab4_button = Tkinter.Button(self.base_frame,text=u"Maybe sort by wins/losses etc",
			command=lambda:self.sort_by(3,parent))
		tab4_button.grid(column=6,row=0,columnspan=2)

	def sort_by(self,button,parent):

		if button == 0:
			ziplist = zip(self.name_index, self.p_index, self.g_index, self.w_index, self.l_index, self.d_index)
			ziplist.sort()
			self.name_index, self.p_index, self.g_index, self.w_index, self.l_index, self.d_index = zip(*ziplist)
		elif button == 1:
			ziplist = zip(self.p_index, self.name_index, self.g_index, self.w_index, self.l_index, self.d_index)
			ziplist.sort(reverse=True)
			self.p_index, self.name_index, self.g_index, self.w_index, self.l_index, self.d_index = zip(*ziplist)
		elif button == 2:
			ziplist = zip(self.g_index, self.p_index, self.name_index, self.w_index, self.l_index, self.d_index)
			ziplist.sort(reverse=True)
			self.g_index, self.p_index, self.name_index, self.w_index, self.l_index, self.d_index = zip(*ziplist)
		elif button == 3:
			ratio_list = [a/b for a,b in zip(2*self.w_index+self.d_index,self.l_index)]
			ziplist = zip(ratio_list, self.g_index, self.p_index, self.name_index, self.w_index, self.l_index, self.d_index)
			ziplist.sort(reverse=True)
			ratio_list, self.g_index, self.p_index, self.name_index, self.w_index, self.l_index, self.d_index = zip(*ziplist)


		for a in range(len(self.p_index)):
			self.string_array.append(Tkinter.StringVar())
			self.print_array.append(Tkinter.Label(self.frame,textvariable=self.string_array[a], anchor="w",fg="black"))
			self.print_array[a].grid(column=0,row=0+a,ipadx=5,columnspan=2,sticky='EW',pady=(0,0))
			self.string_array[a].set(self.name_index[a])

			self.string_array2.append(Tkinter.StringVar())
			self.print_array2.append(Tkinter.Label(self.frame,textvariable=self.string_array2[a], anchor="w",fg="black"))
			self.print_array2[a].grid(column=2,row=0+a,ipadx=20,columnspan=2,sticky='EW',pady=(0,0))
			self.string_array2[a].set(int(self.p_index[a]))

			self.string_array3.append(Tkinter.StringVar())
			self.print_array3.append(Tkinter.Label(self.frame,textvariable=self.string_array3[a], anchor="w",fg="black"))
			self.print_array3[a].grid(column=4,row=0+a,ipadx=20,columnspan=2,sticky='EW',pady=(0,0))
			self.string_array3[a].set(int(self.g_index[a]))

			self.string_array4.append(Tkinter.StringVar())
			self.print_array4.append(Tkinter.Label(self.frame,textvariable=self.string_array4[a], anchor="w",fg="black"))
			self.print_array4[a].grid(column=6,row=0+a,columnspan=2,sticky='EW',pady=(0,0))
			self.string_array4[a].set(str(int(self.w_index[a])) + "-" + str(int(self.d_index[a])) + "-" + str(int(self.l_index[a])))

class TabFour(Tkinter.Frame):

	def __init__(self,parent):
		Tkinter.Frame.__init__(self,parent)
		self.buildgrid_four(parent)
		self.grid(column=0,row=1)
		self.isgridded=True
		self.errLabel = Tkinter.StringVar()
		self.error_label = Tkinter.Label(self,textvariable=self.errLabel, anchor="w",fg="white",bg="black")

	def buildgrid_four(self, parent):

		self.q_label_var = Tkinter.StringVar()
		self.q_label = Tkinter.Label(self,textvariable=self.q_label_var, anchor="w",fg="white",bg="blue")
		self.q_label.grid(column=0,row=0,columnspan=1,sticky='EW',pady=(0,10))
		self.q_label_var.set("Choose Teams for Query")

		team_list = parent.db.get_team_list()
		self.q_list = ['All Teams', 'Mens Teams', 'Womens Teams'] + team_list
		self.query_team = Tkinter.StringVar()
		self.query_team_drop = Tkinter.OptionMenu(self,self.query_team,*self.q_list)
		self.query_team_drop.grid(column=1,row=0,columnspan=1,pady=(0,10))

		self.s_label_var = Tkinter.StringVar()
		self.s_label = Tkinter.Label(self,textvariable=self.s_label_var, anchor="w",fg="white",bg="blue")
		self.s_label.grid(column=2,row=0,columnspan=1,sticky='EW',pady=(0,10))
		self.s_label_var.set("Seasons")

		season_list = parent.db.get_seasons()
		self.s_list = ['All Seasons'] + season_list
		self.s_team = Tkinter.StringVar()
		self.s_team_drop = Tkinter.OptionMenu(self,self.s_team,*self.s_list)
		self.s_team_drop.grid(column=3,row=0,columnspan=1,pady=(0,10))

		q_button = Tkinter.Button(self,text=u"Send Query",
			command=lambda:self.retreive_games(parent))
		q_button.grid(column=4,row=0,columnspan=1,pady=(0,10))
		
	def retreive_games(self,parent):
		if 'game_frame' in dir(self):
			self.game_frame.destroy()
		if 'view_frame' in dir(self):
			self.view_frame.destroy()

		self.game_frame = Tkinter.Frame(master=self)
		self.game_frame.grid(column=0,row=3,columnspan=20,sticky='EW')

		self.canvas=Tkinter.Canvas(master=self.game_frame)
		self.frame=Tkinter.Frame(master=self.canvas)
		self.myscrollbar=Tkinter.Scrollbar(self.game_frame,orient="vertical",command=self.canvas.yview)
		self.canvas.configure(yscrollcommand=self.myscrollbar.set)

		self.myscrollbar.pack(side="right",fill="y")
		self.canvas.pack(side="left")
		self.canvas.create_window((0,0),window=self.frame,anchor='nw')
		self.frame.bind("<Configure>",lambda event: self.frame_function(self.canvas))

		team = self.query_team.get()
		season = self.s_team.get()

		if team == "" or season == "":

			self.error_label.grid(column=0,row=2,columnspan=7,sticky='EW')
			self.errLabel.set("You must select an option for all menus to query the system.")
		else:
			games_list = parent.db.get_game_list(season,team)
			if games_list == []:
				self.error_label = Tkinter.Label(self,textvariable=self.errLabel, anchor="w",fg="white",bg="black")
				self.error_label.grid(column=0,row=2,columnspan=7,sticky='EW')
				self.errLabel.set("There are no games for this Query.")
			else:
				info = parent.db.get_game_info(games_list)
				self.error_label.destroy()
				self.error_label = Tkinter.Label(self,textvariable=self.errLabel, anchor="w",fg="white",bg="black")
				self.display_games(parent,info,self.frame)

	def display_games(self,parent,info,frame):
		self.game_labels = ['Date', 'Gender', 'Team', 'Opposition', 'Team', 'Result', 'Score','View Game']
		self.game_label = []
		self.g_lab = []
		for a in range(len(self.game_labels)):
			self.g_lab.append(Tkinter.StringVar())
			self.game_label.append(Tkinter.Label(frame,textvariable=self.g_lab[a], anchor="w",fg="white",bg="blue"))
			self.game_label[a].grid(column=2*a,row=0,columnspan=2,sticky='EW')
			self.g_lab[a].set(self.game_labels[a])
		
		date_l = ([],[])
		gend_l = ([],[])
		team_l = ([],[])
		opp = ([],[])
		rank = ([],[])
		res = ([],[])
		scored = ([],[])
		view_game_button = []

		count = 0
		for a in info:
			team = a[1]
			opp_c = a[2]
			date = a[3]
			opp_r = a[4]
			score = a[5]
			opp_score = a[6]
			gend = parent.db.get_gender(teamID=team)
			if gend == "M":
				gender = "Mens"
			else:
				gender = "Womens"

			date_l[0].append(Tkinter.StringVar())
			date_l[1].append(Tkinter.Label(frame,textvariable=date_l[0][count], anchor="w",fg="black",bg="white"))
			date_l[0][count].set(a[3])
			date_l[1][count].grid(column=0,row=count+1,columnspan=2,sticky='EW')

			gend_l[0].append(Tkinter.StringVar())
			gend_l[1].append(Tkinter.Label(frame,textvariable=gend_l[0][count], anchor="w",fg="black",bg="white"))
			gend_l[0][count].set(gender)
			gend_l[1][count].grid(column=2,row=count+1,columnspan=2,sticky='EW')

			team_l[0].append(Tkinter.StringVar())
			team_l[1].append(Tkinter.Label(frame,textvariable=team_l[0][count], anchor="w",fg="black",bg="white"))
			team_l[0][count].set(parent.db.get_team_list(team))
			team_l[1][count].grid(column=4,row=count+1,columnspan=2,sticky='EW')

			clubname = parent.db.get_opp_list(opp_c)

			opp[0].append(Tkinter.StringVar())
			opp[1].append(Tkinter.Label(frame,textvariable=opp[0][count], anchor="w",fg="black",bg="white"))
			opp[0][count].set(clubname)
			opp[1][count].grid(column=6,row=count+1,columnspan=2,sticky='EW')

			t_r = parent.db.get_opp_ranks(clubname,gend,opp_r)

			rank[0].append(Tkinter.StringVar())
			rank[1].append(Tkinter.Label(frame,textvariable=rank[0][count], anchor="w",fg="black",bg="white"))
			rank[0][count].set(t_r + " " + parent.db.get_opp_nick(clubname,gend,str(t_r)))
			rank[1][count].grid(column=8,row=count+1,columnspan=2,sticky='EW')

			if score > opp_score:
				res_str = 'Won'
			elif score < opp_score:
				res_str = 'Lost'
			else:
				res_str = 'Draw'

			res[0].append(Tkinter.StringVar())
			res[1].append(Tkinter.Label(frame,textvariable=res[0][count], anchor="w",fg="black",bg="white"))
			res[0][count].set(res_str)
			res[1][count].grid(column=10,row=count+1,columnspan=2,sticky='EW')

			scored[0].append(Tkinter.StringVar())
			scored[1].append(Tkinter.Label(frame,textvariable=scored[0][count], anchor="w",fg="black",bg="white"))
			scored[0][count].set(str(score) + "-" + str(opp_score))
			scored[1][count].grid(column=12,row=count+1,columnspan=2,sticky='EW')

			view_game_button.append(Tkinter.Button(frame,text=u"Go",command=lambda row=count: self.view_game(parent,info[row])))
			view_game_button[count].grid(column=14,row=count+1,columnspan=2)

			count += 1

	def frame_function(event,canvas):
		canvas.configure(scrollregion=canvas.bbox("all"),width='14c',height='12c')
		return

	def view_game(self,parent,gameinf):
		if 'view_frame' in dir(self):
			self.view_frame.destroy()

		self.view_frame = Tkinter.Frame(master=self)
		self.view_frame.grid(column=0,row=2,columnspan=10)

		team = parent.db.get_team_list(gameinf[1])
		clubname = parent.db.get_opp_list(gameinf[2])

		date = gameinf[3]

		gend = parent.db.get_gender(team=team)
		t_r = parent.db.get_opp_ranks(clubname,gend, gameinf[4])
		opp_r = parent.db.get_opp_nick(clubname,gend,str(t_r))

		score = gameinf[5]
		opp_score = gameinf[6]

		if score > opp_score:
			res_str = 'Won'
		elif score < opp_score:
			res_str = 'Lost'
		else:
			res_str = 'Draw'

		#Up to here is good, the rest needs work.

		team_var = Tkinter.StringVar()
		team_lab = (Tkinter.Label(self.view_frame,textvariable=team_var, anchor="w",fg="white",bg="black"))
		team_var.set(team + ' VS ' +  clubname + " " + t_r + " " + opp_r + " on " + str(date) + ".")
		team_lab.grid(column=1,row=0,columnspan=5,sticky='EW')

		scorel_var = Tkinter.StringVar()
		scorel_lab = (Tkinter.Label(self.view_frame,textvariable=scorel_var, anchor="w",fg="white",bg="blue"))
		scorel_var.set("Match Result")
		scorel_lab.grid(column=0,row=1,columnspan=2,sticky='EW')

		score_var = Tkinter.StringVar()
		score_lab = (Tkinter.Label(self.view_frame,textvariable=score_var, anchor="w",fg="white",bg="blue"))
		score_var.set(res_str + " " + str(score) + "-" + str(opp_score))
		score_lab.grid(column=2,row=1,columnspan=1,sticky='EW')

		header = []
		header_var = []
		headers = ["Player","Goals","Player","Goals"]
		for a in range(len(headers)):
			header_var.append(Tkinter.StringVar())
			header.append(Tkinter.Label(self.view_frame,textvariable=header_var[a], anchor="w",fg="black",bg="white"))
			header_var[a].set(headers[a])
			header[a].grid(column=0+a,row=2,columnspan=1,sticky='EW')

		player_id = []
		goals = []
		player_name = []

		p_grid = []
		p_grid_var = []
		g_grid = []
		g_grid_var = []
		
		for a in range(16):
			player_id.append(gameinf[a+8])
			goals.append(gameinf[a+25])
			player_name.append(parent.db.get_player_name(player_id[a]))

		for a in range(8):		
			p_grid_var.append(Tkinter.StringVar())
			p_grid.append(Tkinter.Label(self.view_frame,textvariable=p_grid_var[a], anchor="w",fg="black",bg="white"))
			
			g_grid_var.append(Tkinter.StringVar())
			g_grid.append(Tkinter.Label(self.view_frame,textvariable=g_grid_var[a], anchor="w",fg="black",bg="white"))
			if player_name[a] != None:
				p_grid_var[a].set(player_name[a])
				p_grid[a].grid(column=0,row=3+a,columnspan=1,sticky='EW')

				g_grid_var[a].set(goals[a])
				g_grid[a].grid(column=1,row=3+a,columnspan=1,sticky='EW')

		for b in range(8):
			c = a+b+1
			p_grid_var.append(Tkinter.StringVar())
			p_grid.append(Tkinter.Label(self.view_frame,textvariable=p_grid_var[c], anchor="w",fg="black",bg="white"))
			
			g_grid_var.append(Tkinter.StringVar())
			g_grid.append(Tkinter.Label(self.view_frame,textvariable=g_grid_var[c], anchor="w",fg="black",bg="white"))
			if player_name[c] != None:
				p_grid_var[c].set(player_name[c])
				p_grid[c].grid(column=2,row=3+b,columnspan=1,sticky='EW')

				g_grid_var[c].set(goals[c])
				g_grid[c].grid(column=3,row=3+b,columnspan=1,sticky='EW')
