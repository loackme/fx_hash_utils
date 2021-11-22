import json, requests, sys, getopt

def main(argv):
    wallet = ''
    api_key = ''
    api_secret = ''

    try:
        opts, args = getopt.getopt(argv, "w:k:s:",["wallet=","api_key=","api_secret="])

    except:
        print("Error in arguments: pin_collection.py --wallet <wallet> --api_key <api_key> --api_secret <api_secret>")

    for opt, arg in opts:
        if opt in ['-w', '--wallet']:
            wallet = arg
        elif opt in ['-k', '--api_key']:
            api_key = arg
        elif opt in ['-s', '--api_secret']:
            api_secret = arg

    url = "https://api.fxhash.xyz/graphql/"
    url_pin = "https://api.pinata.cloud/pinning/pinByHash"

    headers = {
        'content-type': 'application/json',
        'pinata_api_key': api_key,
        'pinata_secret_api_key': api_secret
    }

    query = '{user(id: "' + wallet + '") {objkts {name metadataUri metadata}}}'

    r = requests.post(url, json={'query': query})

    if r.status_code == 200:
        print("Request succesful")
        binary = r.content
        output = json.loads(binary)
        output = output['data']['user']['objkts']

        print("\n")
        print(str(len(output)) + " tokens to pin")
        print("\n")

        for objkt in output:

            token_name = objkt['metadata']['name']
            print('Pinning ' + token_name + "...")

            # Metadata
            ipfs_hash = objkt['metadataUri'][7:]
            body = {
                'pinataMetadata' : {
                    'name' : token_name + " Metadata",
                },
                'hashToPin' : ipfs_hash
            }
            r = requests.post(url_pin, data=json.dumps(body), headers=headers)
            if r.status_code == 200:
                print("Metadata pinned")


            # Main
            ipfs_hash = objkt['metadata']['artifactUri'][7:]
            body = {
                'pinataMetadata' : {
                    'name' : token_name + " Artifact",
                },
                'hashToPin' : ipfs_hash
            }
            r = requests.post(url_pin, data=json.dumps(body), headers=headers)
            if r.status_code == 200:
                print("Artifact pinned")

            # Display
            ipfs_hash = objkt['metadata']['displayUri'][7:]
            body = {
                'pinataMetadata' : {
                    'name' : token_name + " Display",
                },
                'hashToPin' : ipfs_hash
            }
            r = requests.post(url_pin, data=json.dumps(body), headers=headers)
            if r.status_code == 200:
                print("Display pinned")

            # Thumbnail
            ipfs_hash = objkt['metadata']['thumbnailUri'][7:]
            body = {
                'pinataMetadata' : {
                    'name' : token_name + " Thumbnail",
                },
                'hashToPin' : ipfs_hash
            }
            r = requests.post(url_pin, data=json.dumps(body), headers=headers)
            if r.status_code == 200:
                print("Thumbnail pinned")

            print("\n")

    else:
        print("Error " + str(r.status_code))

main(sys.argv[1:])
