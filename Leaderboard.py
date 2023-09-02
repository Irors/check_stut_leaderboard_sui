import requests
import openpyxl

headers = {
    'authority': 'quests.mystenlabs.com',
    'accept': '*/*',
    'accept-language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
    'content-type': 'application/json',
    'referer': 'https://quests.mystenlabs.com/',
    'sec-ch-ua': '"Chromium";v="116", "Not)A;Brand";v="24", "Google Chrome";v="116"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36',
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
    try:
        bot = response.json()[0]['result']['data']['bot']
        score = response.json()[0]['result']['data']['score']
        rank = response.json()[0]['result']['data']['rank']
        protocol = response.json()[0]['result']['data']['metadata']['appsUsed']
        SUI_TVL = response.json()[0]['result']['data']['metadata']['SUI_TVL']
        reward = response.json()[0]['result']['data']['reward']


        ''''Работа с excel'''

        sheet['A1'] = 'address'
        sheet['B1'] = 'bot'
        sheet['C1'] = 'score'
        sheet['D1'] = 'rank'
        sheet['E1'] = 'protocol'
        sheet['F1'] = 'SUI_TVL'
        sheet['G1'] = 'reward'


        sheet[f'A{cou}'] = wallet
        sheet[f'B{cou}'] = bot
        sheet[f'C{cou}'] = score
        sheet[f'D{cou}'] = rank
        sheet[f'E{cou}'] = len(protocol)
        sheet[f'F{cou}'] = SUI_TVL
        sheet[f'G{cou}'] = reward
        cou += 1

        workbook.save('Leaderboard_stat.xlsx')
    except:
        pass