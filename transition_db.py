from hockey_gui import Database

if __name__ == "__main__":
	db = Database()
	ply = db.db_command("Select * from playersused")
	goals = db.db_command("Select * from playersgoals")
	in_v2 = db.db_command('Select games_id from game_detail')
	index = 0
	for game in ply:
		gg = goals[index]
		count = 0
		for a in game:
			if count == 0:
				game_id = a
			else:
				if a != None and (game_id,) not in in_v2:
					# print str(game_id)+ ": " + str(a) + ": " + str(gg[count])
					cmd = "INSERT into game_detail (games_id,player_id,playersgoals) values (" + str(game_id) + "," + str(a) + "," + str(gg[count]) + ");"
					# print cmd
					db.db_command(cmd,False)
			count += 1
		index += 1
