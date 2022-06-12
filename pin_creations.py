import json, requests, sys, getopt

def do_fxhash_request(wallet, take, skip):
    url = "https://api.fxhash.xyz/graphql/"
    query = f'{{user(id: "{wallet}") {{generativeTokens(take: {take}, skip: {skip}) {{name metadataUri metadata}}}}}}'
    return requests.post(url, json={'query': query})

def main(argv):
    wallet = ''
    api_key = ''
    api_secret = ''

    try:
        opts, args = getopt.getopt(argv, "w:k:s:",["wallet=","api_key=","api_secret="])

    except:
        print("Error in arguments: pin_creations.py --wallet <wallet> --api_key <api_key> --api_secret <api_secret>")

    for opt, arg in opts:
        if opt in ['-w', '--wallet']:
            wallet = arg
        elif opt in ['-k', '--api_key']:
            api_key = arg
        elif opt in ['-s', '--api_secret']:
            api_secret = arg

    def pinataRequest(ipfs_hash,name,type_data):
        url_pin = "https://api.pinata.cloud/pinning/pinByHash"
        headers = {
            'content-type': 'application/json',
            'pinata_api_key': api_key,
            'pinata_secret_api_key': api_secret
        }
        body = {
            'pinataMetadata' : {
                'name' : f'{name} {type_data}',
            },
            'hashToPin' : ipfs_hash
        }
        r = requests.post(url_pin, data=json.dumps(body), headers=headers)
        if r.status_code == 200:
            print(f'{type_data} pinned')

    def pinToken(objkt):
        name = objkt['name']
        print(f'Pinning {name}...')

        #Metadata
        ipfs_hash = objkt['metadataUri'][7:]
        pinataRequest(ipfs_hash,name,"Metadata")

        # Main
        ipfs_hash = objkt['metadata']['artifactUri'][7:]
        pinataRequest(ipfs_hash,name,"Artifact")

        # Display
        ipfs_hash = objkt['metadata']['displayUri'][7:]
        pinataRequest(ipfs_hash,name,"Display")

        # Thumbnail
        ipfs_hash = objkt['metadata']['thumbnailUri'][7:]
        pinataRequest(ipfs_hash,name,"Thumbnail")

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
                pinToken(objkt)
                print("\n")

            if len(output) < take_count:
                break

        else:
            print(f'Error {str(r.status_code)}')
            valid_request = False

main(sys.argv[1:])
