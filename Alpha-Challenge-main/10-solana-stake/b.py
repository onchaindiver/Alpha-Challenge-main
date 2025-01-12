from concurrent.futures import ThreadPoolExecutor
import requests
import time
import orjson, json


sfdp_list_api_url = 'https://api.solana.org/api/validators/list?offset={}&limit={}&order_by=name&order=asc'
sfdp_validator_api_url = 'https://api.solana.org/api/validators/{}'

rejected_validators = {}


def parse_page(offset=0, limit=100) -> bool:
    r = requests.get(sfdp_list_api_url.format(offset, limit))
    if r.status_code == 429:
        time.sleep(5)
        return parse_page(offset, limit)
    if r.status_code != 200:
        print('req err', r)
        return
    js = orjson.loads(r.text)
    for i in js['data']:
        validator_pubkey: str = i['mainnetBetaPubkey']
        state: str = i['state']
        if state == 'Rejected':
            # print(validator_pubkey, state)
            rejected_validators[validator_pubkey] = 0
    
    # print(len(js['data']))
    if len(js['data']) < 10: return False
    return True


def parse_validator(pubkey: str):
    r = requests.get(sfdp_validator_api_url.format(pubkey))
    if r.status_code == 429:
        time.sleep(5)
        return parse_validator(pubkey)
    if r.status_code != 200:
        print('req err', r)
        return
    js = orjson.loads(r.text)
    try:
        rejected_in: int = int(list(js['mnStats']['epochs'])[-1])
    except: return
    rejected_validators[pubkey] = rejected_in


limit = 100
page_num = 0
while 1:
    if not parse_page(page_num*limit, limit): break
    page_num += 1

with ThreadPoolExecutor(max_workers=2) as pool:
    for _ in pool.map(parse_validator, rejected_validators): pass

print('INDETITY\t WHEN REJECTED')
for v in sorted(list(rejected_validators), key=lambda x: rejected_validators[x], reverse=True):
    print(v, rejected_validators[v])
