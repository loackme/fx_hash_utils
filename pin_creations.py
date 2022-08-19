import json, requests, sys, getopt
from ipfs_utils import IPFSPinner

def do_fxhash_request(wallet, take, skip):
    url = "https://api.fxhash.xyz/graphql/"
    query = f'{{user(id: "{wallet}") {{generativeTokens(take: {take}, skip: {skip}) {{name metadataUri metadata}}}}}}'
    return requests.post(url, json={'query': query})

def main(argv):
    wallet = ''
    api_key = ''
    api_secret = ''
    service_type = 'pinata'

    try:
        opts, args = getopt.getopt(argv, "w:k:s:t:",["wallet=","api_key=","api_secret=","service_type="])

    except:
        print("Error in arguments: pin_creations.py --wallet <wallet> --api_key <api_key> --api_secret <api_secret> --service_type [pinata|ipfs|infura]")

    for opt, arg in opts:
        if opt in ['-w', '--wallet']:
            wallet = arg
        elif opt in ['-k', '--api_key']:
            api_key = arg
        elif opt in ['-s', '--api_secret']:
            api_secret = arg
        elif opt in ['-t', '--service_type']:
            service_type = arg

    pinner = IPFSPinner(service_type, api_key, api_secret)

    valid_request = True
    token_count = 0
    take_count = 20

    while valid_request:
        # Do multiple requests to get all tokens, like a pagination.
        r = do_fxhash_request(wallet, take_count, token_count)
        token_count += take_count

        if r.status_code == 200:
            binary = r.content
            output = json.loads(binary)
            output = output['data']['user']['generativeTokens']

            for objkt in output:
                pinner.pinToken(objkt)
                print("\n")

            if len(output) < take_count:
                break

        else:
            print(f'Error {str(r.status_code)}')
            valid_request = False

main(sys.argv[1:])
