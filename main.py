from fastapi import FastAPI
from basketchamp import NBA
import json
import time

app = FastAPI()

@app.get("/load_links")
def home():
    nba = NBA()
    player_links_dict = {
            "links":[]
        }
    for letter in "abcdefghijklmnopqrstuvwy": # xz
        player_links_dict["links"]  = player_links_dict["links"] + nba.get_all_player_links(letter)["links"]
    
    with open("player_links.json","w") as file:
        player_links_json = json.dumps(player_links_dict, indent=4)
        file.write(player_links_json)
        
    return {"message":nba.get_player_info("https://www.basketball-reference.com/players/b/baumjo01.html")}

@app.get("/load_players")
def update_player():
    nba = NBA()
    with open("nbaplayer.json", "w") as f_nbaplayer, open("player_links.json", "r") as f_player_links:
        player_links = json.load(f_player_links)["links"]
        nba_player = {
            "players":[
            ]
        } 
        for cont, link in enumerate(player_links):
            nba_player["players"].append(nba.get_player_info(link["link"], link["name"]))
            time.sleep(5)
            if cont == 3:
                break
        f_nbaplayer.write(json.dumps(nba_player, indent=4))

    return {"message":"success"}
    
        
            

