import json, requests, sys, getopt, time

def do_fxhash_request(id, take, skip):
    url = "https://api.fxhash.xyz/graphql/"
    query = f"""{{
        generativeToken(id: {id}){{
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
    api_id = ''
    api_secret = ''

    try:
        opts, args = getopt.getopt(argv, "i:k:s:",["id=","api_id=","api_secret="])

    except:
        print("Error in arguments: pin_tokens.py --id <GT_token> --api_id <api_id> --api_secret <api_secret>")

    for opt, arg in opts:
        if opt in ['-i', '--id']:
            GT_id = arg
        elif opt in ['-k', '--api_id']:
            api_id = arg
        elif opt in ['-s', '--api_secret']:
            api_secret = arg

    def add_pin_infura(params):
        params = tuple(params)
        return requests.post('https://ipfs.infura.io:5001/api/v0/pin/add', params=params, auth=(api_id, api_secret))

    def addTokenHashes(objkt,params,forcedMain=False):
        name = objkt['name']
        #Metadata
        ipfs_hash = objkt['metadataUri'][7:]
        params.append(('arg', ipfs_hash))

        # Display
        ipfs_hash = objkt['metadata']['displayUri'][7:]
        params.append(('arg', ipfs_hash))

        # Thumbnail
        ipfs_hash = objkt['metadata']['thumbnailUri'][7:]
        params.append(('arg', ipfs_hash))

        # Main
        ipfs_hash = objkt['metadata']['artifactUri'][7:]
        if not("?" in ipfs_hash) or forcedMain:
            params.append(('arg', ipfs_hash.split('?')[0]))


    valid_request = True
    token_count = 0
    take_count = 20

    while valid_request:
        # Do multiple requests to get all tokens, like a pagination.
        r = do_fxhash_request(GT_id, take_count, token_count)

        if r.status_code == 200:
            binary = r.content
            output = json.loads(binary)
            output = output['data']['generativeToken']
            params = []

            # Pinning the objkts generated from the generative token
            if len(output["objkts"]) > 0:
                print(f'Pinning {output["name"]} {token_count+1}-{token_count+len(output["objkts"])}...')
                for objkt in output['objkts']:
                    addTokenHashes(objkt,params)

            if len(output['objkts']) < take_count:
                # Pinning the generative token metadata & example
                addTokenHashes(output,params,True)
                print('and GT')
                valid_request = False

            maxRetry = 3
            retry = 0
            while retry < maxRetry :
                response = add_pin_infura(params)
                if response.status_code == 200:
                    pins = response.json()['Pins']
                    if len(pins) != len(params):
                        print(f'Missed {len(params) - len(pins)} hashe(s)')
                        for arg in params:
                            if not(arg[1] in pins):
                                print(arg[1])
                    else:
                        print('Done')
                    break
                else:
                    print(f'Error {str(response.status_code)}')
                    retry += 1
                    if retry == maxRetry:
                        print('Trying hashes individually (takes a bit longer)...')
                        nb_success = 0
                        for arg in params:
                            response = add_pin_infura([arg])
                            time.sleep(0.11)
                            if response.status_code == 200:
                                nb_success += 1
                            else:
                                print(f'Hash not pinned: {arg[1]}')
                        print(f'Pinned {nb_success}/{len(params)}')
                    else:
                        print('Retrying this batch...')

        else:
            print(f'Error {str(r.status_code)}')
            valid_request = False

        token_count += take_count

main(sys.argv[1:])
