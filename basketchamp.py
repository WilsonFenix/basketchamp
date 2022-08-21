from ast import Return, Try
from selenium import webdriver
from bs4 import BeautifulSoup      
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_prefs = {}
chrome_options.experimental_options["prefs"] = chrome_prefs
chrome_prefs["profile.default_content_settings"] = {"images": 2}

class NBA:
    def __init__(self):
        self.driver = webdriver.Chrome(options=chrome_options)
        self.baseURL = "https://www.basketball-reference.com"
        pass
    
    def start(self) -> bool:
        self.driver.get(self.baseURL + "/players/a/")
        return True
    
    def get_all_player_links(self, initial_letter="a"):
        player_links_dict = {
            "links":[]
        }
        self.driver.get(self.baseURL + "/players/" + initial_letter + "/")
        content = self.driver.page_source
        bs_nba = BeautifulSoup(content, 'html.parser')
        list_player = bs_nba.find_all("th", attrs={"data-stat":"player", "class":"left"})
        for player in list_player:
            player_link = player.find("a")["href"]
            player_name = player.get_text()

            player_links_dict["links"].append({"name":player_name, "link":self.baseURL + player_link})

        return player_links_dict

    def get_player_info(self, link, name):
        self.driver.get(link)
        
        try:
            player = {
            "name": name,
            "games":self.driver.find_element(By.XPATH, '//*[@id="info"]/div[4]/div[2]/div[1]/p[2]').text.strip(),
            "points":self.driver.find_element(By.XPATH, '//*[@id="info"]/div[4]/div[2]/div[2]/p[2]').text.strip(),
            "total_rebounds":self.driver.find_element(By.XPATH, '//*[@id="info"]/div[4]/div[2]/div[3]/p[2]').text.strip(),
            "assists":self.driver.find_element(By.XPATH, '//*[@id="info"]/div[4]/div[2]/div[4]/p[2]').text.strip(),
            "field_goal_percentage":self.driver.find_element(By.XPATH, '//*[@id="info"]/div[4]/div[3]/div[1]/p[2]').text.strip(),
            "three_point_field_goal_percentage":self.driver.find_element(By.XPATH, '//*[@id="info"]/div[4]/div[3]/div[2]/p[2]').text.strip(),
            "free_hrow_percentage":self.driver.find_element(By.XPATH, '//*[@id="info"]/div[4]/div[3]/div[3]/p[2]').text.strip(),
            "effective_field_goal_percentage":self.driver.find_element(By.XPATH, '//*[@id="info"]/div[4]/div[3]/div[4]/p[2]').text.strip()
        }
        except:
            return {}
        

        return player
    def end(self):
        self.driver.quit()