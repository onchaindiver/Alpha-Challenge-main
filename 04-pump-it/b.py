from requests import Session
from concurrent.futures import ThreadPoolExecutor
import os
import json, orjson


RPC_URL: str = os.getenv('RPC')
session = Session()
session.headers.update({ 'Accept': 'application/json', 'Content-Type': 'application/json' })


HOW_MANY_K_OF_TXS: int = 15
MIGRATION_ACCOUNT: str = '39azUYFWPz3VHgKCf3VChUwbpURdCHRxjWVowf5jUJjg'
MINT_AUTH_ACCOUNT: str = 'TSLvdd1pWpHVjahSpsvCXUbgwsL3JAcvokwaKt1eokM'


signatures = []
def get_signatures(account_pubkey, before=None):
    payload = {'jsonrpc': '2.0', 'id': 1, 'method': 'getSignaturesForAddress', 'params': [
        account_pubkey, {'limit': 1000, 'before': before}]}
    resp = session.post(url=RPC_URL, data=orjson.dumps(payload))
    js = orjson.loads(resp.text)
    if len(js['result']) < 100: return
    for s in js['result']:
        sig = s['signature']
        if s['err'] is not None: continue
        signatures.append(sig)
    
    return sig
    

migrations = {}
def parse_migration(sig):
    global fee_from_migration
    payload = {'jsonrpc': '2.0', 'id': 1, 'method': 'getTransaction', 'params': [
        sig, {'maxSupportedTransactionVersion': 0, 'encoding': 'json'}]}
    resp = session.post(url=RPC_URL, data=orjson.dumps(payload))
    tx = orjson.loads(resp.text)['result']
    mint = None
    for b in tx['meta']['postTokenBalances']:
        if b['owner'] == MIGRATION_ACCOUNT:
            mint = b['mint']
    if mint is None: return
    slot = tx['slot']
    migrations[mint] = slot
    

creates = {}
def parse_mint_auth(sig):
    global fee_from_migration
    payload = {'jsonrpc': '2.0', 'id': 1, 'method': 'getTransaction', 'params': [
        sig, {'maxSupportedTransactionVersion': 0, 'encoding': 'json'}]}
    resp = session.post(url=RPC_URL, data=orjson.dumps(payload))
    tx = orjson.loads(resp.text)['result']
    if len(tx['meta']['postTokenBalances']) != 2: return
    mints = set([b['mint'] for b in tx['meta']['postTokenBalances']])
    if len(mints) != 1: return
    mint = list(mints)[0]
    slot = tx['slot']
    creates[mint] = slot
    

# parse_migration('VS6t5aagngNFqK8YzfN2zvQmmv8dHpSTtf87Va6Yd432RN8iFjsSXiEdQU8Xfo5HsdGwAVbq4JCsqtywC5LUmrW')
# parse_mint_auth('53tqBkcWCZxXJiZUd1iicKwgft1NnEenierUREitrGceBpWkmv1jWUgrCgwisFf4nnKy2aKiHp2T8m4DHtyrmxov')

pool = ThreadPoolExecutor(max_workers=300)

sig = None
for i in range(HOW_MANY_K_OF_TXS):
    sig = get_signatures(MIGRATION_ACCOUNT, sig)
    if sig is None: break
for _ in pool.map(parse_migration, signatures): pass

signatures = []
sig = None
for i in range(HOW_MANY_K_OF_TXS):
    sig = get_signatures(MINT_AUTH_ACCOUNT, sig)
    if sig is None: break
for _ in pool.map(parse_mint_auth, signatures): pass

migrated_mints = {}
for m in migrations:
    if m in creates:
        migrated_mints[m] = migrations[m] - creates[m]
        
migrated_sorted = sorted(list(migrated_mints), key=lambda x: migrated_mints[x], reverse=True)
m = migrated_sorted[0]
l = migrated_sorted[-1]
print('total migrations %d' % len(migrated_sorted))
print('most', m, 'slots to migrate %d start %d finish %d' % (migrated_mints[m], creates[m], migrations[m]))
print('least', l, 'slots to migrate %d start %d finish %d' % (migrated_mints[l], creates[l], migrations[l]))
