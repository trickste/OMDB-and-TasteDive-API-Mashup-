import requests
import json
import requests_with_caching


def get_movies_from_tastedive(input):
    base = "https://tastedive.com/api/similar"
    par = {"q": input, "type": "movies", 'limit': 5}
    page = requests_with_caching.get(base, params=par)
    page = page.json()
    return page

def extract_movie_titles(input):
    a = input['Similar']['Results']
    b = []
    for x in a:
        b.append(x['Name'])
    return b


def get_related_titles(input):
    lst = []
    fin_lst = []
    for x in input:
        rel_movie = extract_movie_titles(x)
        if rel_movie not in lst:
            lst.append(rel_movie)
    for x in lst:
        for y in x:
            if y not in fin_lst:
                fin_lst.append(y)

    return fin_lst

def get_movie_data(input):
    base = "http://www.omdbapi.com/"
    param = {'t': input, 'r': 'json'}
    page = requests_with_caching.get(base, params=param)
    page = page.json()
    return page


def get_movie_rating(input):
 movie = get_movie_data(input)
 # print(json.dumps(movie, indent = 3))
 rat = 0
 try:
  if movie["Ratings"][1]["Source"] == "Rotten Tomatoes":
   rat = int(movie["Ratings"][1]["Value"][0:-1])
 except:
  rat = 0
 return rat


def get_sorted_recommendations(input):
 a = {}
 mov_lst = get_related_titles(input)
 for mov in mov_lst:
  a[mov] = get_movie_rating(mov)

 fun = sorted(a, key=lambda x: (a[x], x), reverse=True)
 return fun