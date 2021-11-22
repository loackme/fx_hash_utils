import json, requests, sys, getopt

def main(argv):
    GT_id = ''
    api_key = ''
    api_secret = ''

    try:
        opts, args = getopt.getopt(argv, "i:k:s:",["id=","api_key=","api_secret="])

    except:
        print("Error in arguments: pin_tokens.py --id <GT_token> --api_key <api_key> --api_secret <api_secret>")

    for opt, arg in opts:
        if opt in ['-i', '--id']:
            GT_id = arg
        elif opt in ['-a', '--api_key']:
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

    query = """{
        generativeTokensByIds(ids: """ + GT_id + """){
        name
        metadataUri
        objkts {
              metadataUri
              metadata
              }
        }
    }"""

    r = requests.post(url, json={'query': query})

    if r.status_code == 200:
        print("Request succesful")
        binary = r.content
        output = json.loads(binary)
        output = output['data']['generativeTokensByIds'][0]

        # Generative Token Metadata
        GT_name = output['name']
        print("Pinning generative token " + GT_name + "...")
        ipfs_hash = output['metadataUri'][7:]
        body = {
            'pinataMetadata' : {
                'name' : GT_name + " Metadata",
            },
            'hashToPin' : ipfs_hash
        }
        r = requests.post(url_pin, data=json.dumps(body), headers=headers)
        if r.status_code == 200:
            print("Generative token metadata pinned")

        # Objkts
        output = output['objkts']

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

    else:
        print("Error " + str(r.status_code))

main(sys.argv[1:])
