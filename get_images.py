import json, requests, shutil, os, sys, getopt

def do_request(id, take, skip):
    url = "https://api.fxhash.xyz/graphql/"
    query = f"""{{
        generativeTokensByIds(ids: {id}){{
        objkts(take: {take}, skip: {skip}) {{
              metadata
              }}
        }}
    }}"""

    return requests.post(url, json={'query': query})
    

def main(argv):
    GT_id = ''
    folder = ''

    try:
        opts, args = getopt.getopt(argv, "i:f:",["id=","folder="])

    except:
        print("Error in arguments: get_images.py --id <GT_id> --folder <folder>")

    for opt, arg in opts:
        if opt in ['-i', '--id']:
            GT_id = arg
        elif opt in ['-f', '--folder']:
            folder = arg

    if not os.path.exists(folder):
        os.mkdir(folder)

    valid_request = True
    token_count = 0

    while (valid_request):
        # Do multiple requests to get all tokens, like a pagination.
        r = do_request(GT_id, 20, token_count)
        token_count += 20

        if r.status_code == 200:
            binary = r.content
            output = json.loads(binary)

            output = output['data']['generativeTokensByIds'][0]['objkts']

            for objkt in output:
                objkt_name = objkt['metadata']['name']
                image_url = f"https://gateway.fxhash.xyz/ipfs/{objkt['metadata']['displayUri'][7:]}"
                filename = f'{folder}/{objkt_name}.png'

                r_img = requests.get(image_url, stream = True)
                if r_img.status_code == 200:
                    r_img.raw.decode_content = True

                    with open(filename,'wb') as f:
                        shutil.copyfileobj(r_img.raw, f)

                    print(f'{objkt_name} downloaded')

                else:
                    print(f'Error downloading {objkt_name}')
                    valid_request = False

        else:
            print(f'Error {str(r.status_code)}')
            valid_request = False

main(sys.argv[1:])
