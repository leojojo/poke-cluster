import requests, re
from scipy.sparse import lil_matrix
from bs4 import BeautifulSoup as bs

BASE_URL = 'https://yakkun.com/swsh/zukan/'
POKE_PATH = 'n'
MOVE_PATH = 'search/?move='
HEADERS = {'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 13_2_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.3 Mobile/15E148 Safari/604.1'}
POKEDEX_MAX = 890
MOVE_MAX = 804
param_id = lambda x: int(re.search(r'\d+', x.a.get('href')).group())

def req_soup(path, param):
    page = requests.get(BASE_URL + path + str(param), headers=HEADERS)
    return bs(page.content, 'html.parser')

# e.g. [33, 45, 22, 74, 73, 75, 77, 79, 402, 36, 230, 235, 388, 38, 76]
# id = level_move, machine_move, record_move, egg_move
def get_moves(soup):
    moves = soup.find(id='level_move').ul.findAll('li')
    return list(map(param_id, moves))

def get_move_matrix():
    matrix = lil_matrix((POKEDEX_MAX, MOVE_MAX), dtype=int)
    for n in range(POKEDEX_MAX):
        soup = req_soup(POKE_PATH, n+1)
        for move in get_moves(soup):
            matrix[n, move] = 1
    return matrix

def get_poke_list():
    soup = req_soup(POKE_PATH, '')
    get_name = lambda li: li.a.get_text()
    lis = soup.find(class_='pokemon_list').findAll('li')
    poke_list = dict(zip( map(param_id, lis), map(get_name, lis) ))
    srtd = sorted(poke_list.items(), key=lambda x:x[0])
    return [ s[1] for s in srtd ]

def get_move_list():
    moves = []
    for i in range(MOVE_MAX):
        soup = req_soup(MOVE_PATH, i+1)
        res = soup.find(id='result').get_text()
        grep = re.search(r'『(.+)』', res).group(1)
        moves.append(grep)
    return moves

def main():
    print(get_move_list())

if __name__ == '__main__':
    main()
