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

    query = """{
        generativeTokensByIds(ids: """ + GT_id + """){
        name
        metadataUri
        metadata
        objkts {
              name
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

        def pinToken(objkt):
            name = objkt['name']
            print("Pinning " + name + "...")

            #Metadata
            ipfs_hash = objkt['metadataUri'][7:]
            body = {
                'pinataMetadata' : {
                    'name' : name + " Metadata",
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
                    'name' : name + " Artifact",
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
                    'name' : name + " Display",
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
                    'name' : name + " Thumbnail",
                },
                'hashToPin' : ipfs_hash
            }
            r = requests.post(url_pin, data=json.dumps(body), headers=headers)
            if r.status_code == 200:
                print("Thumbnail pinned")

        # Pinning the generative token metadata & example
        pinToken(output)

        # Pinning the objkts generated from the generative token
        output = output['objkts']
        for objkt in output:
            pinToken(objkt)

    else:
        print("Error " + str(r.status_code))

main(sys.argv[1:])
