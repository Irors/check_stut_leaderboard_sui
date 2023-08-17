import requests
import openpyxl

headers = {
    'authority': 'quests.mystenlabs.com',
    'content-type': 'application/json',
    'referer': 'https://quests.mystenlabs.com/'
}


with open("wallet_addres.txt") as file:
    wallets = [i.strip() for i in file]

cou = 2
workbook = openpyxl.Workbook()
sheet = workbook.active
print(f"Загружено {len(wallets)} кошельков")

for wallet in wallets:
    print(f"Записываю {wallet[:10]}...{wallet[-10:]}")
    params = {
        'batch': '1',
        'input': '{"0":{'
                 f'"address":"{wallet}",'
                    '"questId":2}}'
    }

    response = requests.get('https://quests.mystenlabs.com/api/trpc/user', params=params, headers=headers)
    address = response.json()[0]['result']['data']['address']
    bot = response.json()[0]['result']['data']['bot']
    score = response.json()[0]['result']['data']['score']
    rank = response.json()[0]['result']['data']['rank']
    protocol = response.json()[0]['result']['data']['metadata']['appsUsed']


    ''''Работа с excel'''

    sheet['A1'] = 'address'
    sheet['B1'] = 'bot'
    sheet['C1'] = 'score'
    sheet['D1'] = 'rank'
    sheet['E1'] = 'protocol'

    sheet[f'A{cou}'] = address
    sheet[f'B{cou}'] = bot
    sheet[f'C{cou}'] = score
    sheet[f'D{cou}'] = rank
    sheet[f'E{cou}'] = len(protocol)
    cou += 1

    workbook.save('Leaderboard_stat.xlsx')