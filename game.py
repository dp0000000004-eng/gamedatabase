import random
import psycopg2

class Game:
    def __init__(self, player_uid, player_id, match_played, total_kill, total_win, total_loss, game_rank):
        if not player_uid:
            raise ValueError("Missing Uid or Invalid Uid")
        elif not player_id:
            raise ValueError("Missing Id_Name")
        self.player_uid = player_uid
        self.player_id = player_id
        self.match_played = match_played
        self.total_kill = total_kill
        self.total_win = total_win
        self.total_lose = total_loss
        self.game_rank = game_rank


    @property
    def match_played(self):
        return self._match_played
    
    @match_played.setter
    def match_played(self, match_played):
        self._match_played = match_played
    

    @property
    def total_kill(self):
        return self._total_kill
    

    @total_kill.setter
    def total_kill(self, total_kill):
        self._total_kill = total_kill

    @property
    def total_win(self):
        return self._total_win
    
    @total_win.setter
    def total_win(self, wins):
        self._total_win = wins

    
    
    @property
    def game_rank(self):
        return self._game_rank
    
    @game_rank.setter
    def game_rank(self, game_rank):
        if self._total_win > 249:
            self._game_rank = "GrandMaster"
        elif self._total_win > 200:
            self._game_rank =  "Master"
        elif self._total_win > 150:
            self._game_rank = "Heroic"
        elif self._total_win > 100:
            self._game_rank = "Diamond"
        elif self._total_win > 20:
            self._game_rank = "Silver"
        else:
            self._game_rank = "Bronze"
            

def find_player(cursor, player_uid):
    cursor.execute(
        """SELECT game.player_uid, game.player_id, 
          game.match_played, game.total_kill,
          states.total_win, states.total_loss, states.game_rank
        FROM game
        LEFT JOIN states ON game.player_uid = states.player_uid
        WHERE game.player_uid = %s""",
        (player_uid,)
    )
    return cursor.fetchone()          
        
            

def main():
    connect = psycopg2.connect(
    host="localhost",
    database="game",
    user="postgres",
    password="1234",
    port=5432
    )

    cursor = connect.cursor()
    while True:
        print("\n1. Create New Account: ")
        print("2. Find Account: ")
        print("3. Quit")
        choice = input("Chose: ")
        if choice == "1":
            player_uid = random.randint(10000000, 1000000000)
            player_id = input("Your id Name: ")
            match_played = random.randint(0, 500)
            total_kill = random.randint(10, 10000)
            total_win = random.randint(0, 600)
            total_loss = random.randint(0, 100)
            game = Game(player_uid, player_id, match_played, total_kill, total_win, total_loss, None)
            print(f"player: {game.player_id} | player_uid: {game.player_uid} | Rank: {game.game_rank}")
            cursor = connect.cursor()
            cursor.execute(
                "INSERT INTO game (player_uid, player_id, match_played, total_kill) VALUES (%s, %s, %s, %s) returning player_uid",
                (game.player_uid, game.player_id, game.match_played, game.total_kill)
            )
            
            cursor.execute(
                "INSERT INTO states (player_uid, player_id, total_win, total_loss, game_rank) VALUES (%s, %s, %s, %s, %s)",
                (game.player_uid, game.player_id, game.total_win, total_loss, game.game_rank)
            )

            connect.commit()  # ✅ Must commit to save changes
            print("Data inserted successfully!")
        elif choice == "3":
            break

            


        
        elif choice == "2":
            while True:
                try:
                    player_uid = int(input("Enter your UID : "))
                except ValueError:
                    print("Enter Valid Uid")

                player = find_player(cursor, player_uid)
                if player:
                    print(f"Player found: {player}")
                    print("\n1. Delete account")
                    print("2. Update username")
                    print("3. View stats")
                    print("4. Quit To Main Menu")
                    choice = input("Choose: ")
                    if choice == "1":
                        cursor.execute(
                            "DELETE FROM states WHERE player_uid = %s",
                            (player_uid,)
                        )

                        cursor.execute(
                            "DELETE FROM game WHERE player_uid = %s",
                            (player_uid,)
                        )
                        connect.commit()
                        print("Account deleted!")

                        break

                    elif choice == "2":

                        query = "UPDATE game SET player_id = %s WHERE player_id = %s"
                        values = (input("Enter Your New Name: "), input("Enter your past username: "))


                        cursor.execute(query, values)
                        

                        connect.commit()
                        print("Update successfully!")
                        break


                        
                
                    elif choice == "3":
                        print(f"""PLayer.Name: {player[1]} | Total.win: {player[4]} | Rank: {player[6]}""")
                        break
                
                    elif choice == "4":
                        break
                    
        elif choice == "3":
            break
        
        connect.close()
        cursor.close()
                    

if __name__ == "__main__":
    main()
