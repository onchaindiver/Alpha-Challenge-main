from requests import Session
from concurrent.futures import ThreadPoolExecutor
import os
import json, orjson


RPC_URL: str = os.getenv('RPC')
session = Session()
session.headers.update({ 'Accept': 'application/json', 'Content-Type': 'application/json' })


HOW_MANY_K_OF_TXS: int = 5
FEE_ACCOUNT: str = 'CebN5WGQ4jvEPvsVU4EoHEpgzq1VV7AbicfhtW4xC9iM'
MIGRATION_ACCOUNT: str = '39azUYFWPz3VHgKCf3VChUwbpURdCHRxjWVowf5jUJjg'
fee_from_txs = 0
fee_from_migration = 0


signatures = []
def get_signatures(account_pubkey, before=None):
    payload = {'jsonrpc': '2.0', 'id': 1, 'method': 'getSignaturesForAddress', 'params': [
        account_pubkey, {'limit': 1000, 'before': before}]}
    resp = session.post(url=RPC_URL, data=orjson.dumps(payload))
    js = orjson.loads(resp.text)
    # print(js)
    if len(js['result']) < 100: return
    for s in js['result']:
        if s['err'] is not None: continue
        sig = s['signature']
        signatures.append(sig)
    
    return sig


def parse_fee(sig):
    global fee_from_txs
    payload = {'jsonrpc': '2.0', 'id': 1, 'method': 'getTransaction', 'params': [
        sig, {'maxSupportedTransactionVersion': 0, 'encoding': 'json'}]}
    resp = session.post(url=RPC_URL, data=orjson.dumps(payload))
    tx = orjson.loads(resp.text)['result']
    try:
        fee_acc_index = tx['transaction']['message']['accountKeys'].index(FEE_ACCOUNT)
    except ValueError: return
    fee_sum = tx['meta']['postBalances'][fee_acc_index] - tx['meta']['preBalances'][fee_acc_index]
    fee_from_txs += fee_sum
    

def parse_migration(sig):
    global fee_from_migration
    payload = {'jsonrpc': '2.0', 'id': 1, 'method': 'getTransaction', 'params': [
        sig, {'maxSupportedTransactionVersion': 0, 'encoding': 'json'}]}
    resp = session.post(url=RPC_URL, data=orjson.dumps(payload))
    tx = orjson.loads(resp.text)['result']
    try:
        fee_acc_index = tx['transaction']['message']['accountKeys'].index(MIGRATION_ACCOUNT)
    except ValueError: return
    fee_sum = tx['meta']['postBalances'][fee_acc_index] - tx['meta']['preBalances'][fee_acc_index]
    fee_from_migration += fee_sum


pool = ThreadPoolExecutor(max_workers=600)

sig = None
for i in range(HOW_MANY_K_OF_TXS):
    sig = get_signatures(FEE_ACCOUNT, sig)
    if sig is None: break

for _ in pool.map(parse_fee, signatures): pass

signatures = []
sig = None
for i in range(HOW_MANY_K_OF_TXS):
    sig = get_signatures(MIGRATION_ACCOUNT, sig)
    if sig is None: break
for _ in pool.map(parse_migration, signatures): pass


print('%dk of last txs by sig | tx fee %d SOL | migration fee %d SOL' % (HOW_MANY_K_OF_TXS, fee_from_txs/10**9, fee_from_migration/10**9))