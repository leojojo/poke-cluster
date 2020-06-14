import requests, re
from scipy.sparse import lil_matrix
from bs4 import BeautifulSoup as bs

BASE_URL = 'https://yakkun.com/swsh/zukan/n'
HEADERS = {'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 13_2_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.3 Mobile/15E148 Safari/604.1'}
POKEDEX_MAX = 890
MOVE_MAX = 804

def req_soup(poke_num):
    page = requests.get(BASE_URL + str(poke_num), headers=HEADERS)
    return bs(page.content, 'html.parser')

# e.g. [33, 45, 22, 74, 73, 75, 77, 79, 402, 36, 230, 235, 388, 38, 76]
# id = level_move, machine_move, record_move, egg_move
def get_moves(soup):
    moves = soup.find(id='level_move').ul.findAll('li')
    param_id = lambda x: int(re.search(r'\d+', x.a.get('href')).group())
    return list(map(param_id, moves))

def get_move_matrix():
    matrix = lil_matrix((POKEDEX_MAX, MOVE_MAX), dtype=int)
    for n in range(POKEDEX_MAX):
        soup = req_soup(n+1)
        for move in get_moves(soup):
            matrix[n, move] = 1
    return matrix

def main():
    print(get_move_matrix())

if __name__ == '__main__':
    main()
