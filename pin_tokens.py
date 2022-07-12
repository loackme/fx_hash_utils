import json, requests, sys, getopt
from ipfs_utils import IPFSPinner

def do_fxhash_request(id, take, skip):
    url = "https://api.fxhash.xyz/graphql/"
    query = f"""{{
        generativeTokensByIds(ids: {id}){{
        name
        metadataUri
        metadata
        objkts(take: {take}, skip: {skip}) {{
              name
              metadataUri
              metadata
              }}
        }}
    }}"""

    return requests.post(url, json={'query': query})

def main(argv):
    GT_id = ''
    api_key = ''
    api_secret = ''
    service_type = 'pinata'

    try:
        opts, args = getopt.getopt(argv, "i:k:s:t:",["id=","api_key=","api_secret=","service_type"])

    except:
        print("Error in arguments: pin_tokens.py --id <GT_token> --api_key <api_key> --api_secret <api_secret> --service_type [pinata|ipfs|infura]")

    for opt, arg in opts:
        if opt in ['-i', '--id']:
            GT_id = arg
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
        r = do_fxhash_request(GT_id, take_count, token_count)
        token_count += take_count

        if r.status_code == 200:
            binary = r.content
            output = json.loads(binary)
            output = output['data']['generativeTokensByIds'][0]

            # Pinning the objkts generated from the generative token
            for objkt in output['objkts']:
                pinner.pinToken(objkt)
                print("\n")

            if len(output['objkts']) < take_count:
                # Pinning the generative token metadata & example
                pinner.pinToken(output)
                print("\n")
                break

        else:
            print(f'Error {str(r.status_code)}')
            valid_request = False

main(sys.argv[1:])
