from requests import Session
import os
import json, orjson


RPC_URL: str = os.getenv('RPC')
s = Session()
s.headers.update({ 'Accept': 'application/json', 'Content-Type': 'application/json' })


def print_sandwich_info(txs, fr_index, br_index, mo):
    def print_victim_tx(index):
        tx = txs[index]
        tx_sig = tx['transaction']['signatures'][0]
        print(tx_sig)
    
    def print_attacker_tx(index, owner):
        tx = txs[index]
        tx_sig = tx['transaction']['signatures'][0]
        mint_and_amnt = {}
        mints_changed = {}
        
        for b in tx['meta']['preTokenBalances']: 
            mint_and_amnt[b['accountIndex']] = b['uiTokenAmount']['uiAmount']
            
        for b in tx['meta']['postTokenBalances']:
            if b['owner'] != owner: continue
            if b['accountIndex'] in mint_and_amnt:
                if mint_and_amnt[b['accountIndex']] == b['uiTokenAmount']['uiAmount']:
                    continue
            
            if b['accountIndex'] in mint_and_amnt and mint_and_amnt[b['accountIndex']] is not None: 
                pre_amnt = mint_and_amnt[b['accountIndex']]
            else: pre_amnt = 0
            post_amnt = [b['uiTokenAmount']['uiAmount'], 0][b['uiTokenAmount']['uiAmount'] is None]
            mints_changed[b['mint']] = post_amnt - pre_amnt
        
        print(tx_sig, mints_changed)
    
    mint, owner = mo.split('-')
    print('sandwich | bundle pos: %d-%d' % (fr_index, br_index))
    print_attacker_tx(fr_index, owner)
    for victim_tx_index in range(fr_index+1, br_index):
        print_victim_tx(victim_tx_index)
    print_attacker_tx(br_index, owner)
    

# 286_158_796 286_179_791 286_179_805
block_num: int = int(input('enter block: '))
payload = {
    'jsonrpc': '2.0', 'id': 1, 'method': 'getBlock',
    'params': [block_num, {
        'encoding': 'json',
        'maxSupportedTransactionVersion': 0,
        'transactionDetails': 'full',
        'rewards': True,
}]}
resp = s.post(url=RPC_URL, data=orjson.dumps(payload))
if resp.status_code != 200: print('req err', resp)
block = orjson.loads(resp.text)

validator_identity: str = block['result']['rewards'][0]['pubkey']

balance_flow = {}

print('validator identity:', validator_identity)
txs = block['result']['transactions']
for tx in txs:
    mint_and_amnt = {}
    mints_changed = {}
    tx_sig = tx['transaction']['signatures'][0]
    
    for b in tx['meta']['preTokenBalances']: 
        mint_and_amnt[b['accountIndex']] = b['uiTokenAmount']['uiAmount']
        
    for b in tx['meta']['postTokenBalances']:
        if b['accountIndex'] in mint_and_amnt:
            if mint_and_amnt[b['accountIndex']] == b['uiTokenAmount']['uiAmount']:
                continue
        
        if b['accountIndex'] in mint_and_amnt and mint_and_amnt[b['accountIndex']] is not None: 
            pre_amnt = mint_and_amnt[b['accountIndex']]
        else: pre_amnt = 0
        post_amnt = [b['uiTokenAmount']['uiAmount'], 0][b['uiTokenAmount']['uiAmount'] is None]
        s = b['mint'] + '-' + b['owner']
        mints_changed[s] = post_amnt - pre_amnt
    
    if len(mints_changed) > 0:
        for m in mints_changed:
            amnt = mints_changed[m]
            if m not in balance_flow: balance_flow[m] = {}
            if amnt not in balance_flow[m]: balance_flow[m][amnt] = []
            balance_flow[m][amnt].append(txs.index(tx))

MAX_TXS_IN_BUNDLE = 5
for mo in balance_flow:
    for a in balance_flow[mo]:
        if a > 0:
            if -a in balance_flow[mo]:
                for tx_frontrun_index in balance_flow[mo][a]:
                    for tx_backrun_index in balance_flow[mo][-a]:
                        if 2 <= (tx_backrun_index - tx_frontrun_index) <= MAX_TXS_IN_BUNDLE:
                            print_sandwich_info(txs, tx_frontrun_index, tx_backrun_index, mo)
