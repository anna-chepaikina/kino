# %%
import pandas as pd
import re
import requests
from bs4 import BeautifulSoup

# %%
cinema_des_ecoles = "https://www.allocine.fr/seance/salle_gen_csalle=C0071.html"
cinema_filmotheque = "https://www.allocine.fr/seance/salle_gen_csalle=C0020.html"
cinema_reflet_medicis = "https://www.allocine.fr/seance/salle_gen_csalle=C0074.html"
cinema_espace_jaques_tati = "https://www.allocine.fr/seance/salle_gen_csalle=C0073.html"
cinema_grand_action = "https://www.allocine.fr/seance/salle_gen_csalle=C0072.html"
cinema_christine_21 = "https://www.allocine.fr/seance/salle_gen_csalle=C0015.html"
cinema_list = [cinema_des_ecoles, cinema_filmotheque, 
               cinema_reflet_medicis, cinema_espace_jaques_tati,
               cinema_grand_action, cinema_christine_21]


json_list = []
for cinema in cinema_list:
    # load the webpage with BeautifulSoup
    page = requests.get(cinema)
    # parse the html
    soup = BeautifulSoup(page.content, 'html.parser')
    # find the div with id content-layout
    content_layout = soup.find(id="content-layout")
    lst = soup.find_all("div", class_="card entity-card entity-card-list movie-card-theater cf hred")
    for l in lst:
        #print(l)
        #print("=====================================")
        cinema = soup.find("title").text.strip()
        cinema = cinema.split("-")[0].strip()
        #print(f"Cinema : {cinema}")
        film_title = l.find("h2", class_="meta-title").text.strip()
        #print(f"Titre : {film_title}")
        try:
            film_sortie = l.find("span", class_="date").text.strip()
            #print(f"Sortie : {film_sortie}")
        except:
            film_sortie = ""
        try:            
            film_synopsis = l.find("div", class_="content-txt").text.strip()
            #print(f"Synopsis : {film_synopsis}")
        except:
            film_synopsis = ""

        try:
            film_director = l.find("div", class_="meta-body-item meta-body-direction").text.strip()
            film_director = film_director.replace("De\n", "")
            film_director = film_director.replace(",\n", ", ")
            #print(f"Director : {film_director}")
        except:
            film_director = ""

        try:
            film_actors = l.find("div", class_="meta-body-item meta-body-actor").text.strip()
            film_actors = film_actors.replace("Avec\n", "")
            film_actors = film_actors.replace(",\n", ", ")
            #print(f"Actors : {film_actors}")
        except:
            film_actors = ""
        try:
            film_date = l.find("div", class_="text").text.strip()
            #print(f"Seance : {film_date}")
        except:
            film_date = ""
        try:
            film_hour = l.find("div", class_="hours").text.strip()
            # remove multiple \n with regex
            film_hour = re.sub(r'\n+', '\n', film_hour)
            if "Réserver" in film_hour:
                film_hour = film_hour.replace("\nRéserver", "")
            film_hour = film_hour.replace("\n", ", ")
            #print(f"Hour : {film_hour}")
        except:
            film_hour = ""
        #print(f"Hour : {film_hour}")
        # save
        dico = {}
        dico["cinema"] = cinema
        dico["titre"] = film_title
        dico["director"] = film_director
        dico["actors"] = film_actors
        dico["sortie"] = film_sortie
        dico["synopsis"] = film_synopsis
        dico["jour"] = film_date
        dico["horaires"] = film_hour
        json_list.append(dico)
    

# %%
# convert json to html
df = pd.DataFrame(json_list)
df = df.sort_values(by=["horaires"])
df.to_html("horaires_pour_aujourdhui.html", encoding="utf-8", index=False)


