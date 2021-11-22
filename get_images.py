import json, requests, shutil, os, sys, getopt

def main(argv):
    GT_id = ''
    folder = ''

    try:
        opts, args = getopt.getopt(argv, "i:f:",["id=",
                                    "folder="])

    except:
        print("Error in arguments: get_images.py --id <GT_id> --folder <folder>")

    for opt, arg in opts:
        if opt in ['-i', '--id']:
            GT_id = arg
        elif opt in ['-f', '--folder']:
            folder = arg

    if not os.path.exists(folder):
        os.mkdir(folder)

    url = "https://api.fxhash.xyz/graphql/"
    query = """{
        generativeTokensByIds(ids: """ + GT_id + """){
        objkts {
              metadata
              }
        }
    }"""

    r = requests.post(url, json={'query': query})

    if r.status_code == 200:
        print("Request succesful")
        binary = r.content
        output = json.loads(binary)
        output = output['data']['generativeTokensByIds'][0]['objkts']

        for objkt in output:
            objkt_name = objkt['metadata']['name']
            ipfs_url = objkt['metadata']['displayUri']
            image_url = "https://gateway.fxhash.xyz/ipfs/" + ipfs_url[7:]
            filename = folder + '/' + objkt_name + '.png'

            r_img = requests.get(image_url, stream = True)
            if r_img.status_code == 200:
                r_img.raw.decode_content = True

                with open(filename,'wb') as f:
                    shutil.copyfileobj(r_img.raw, f)

                print(objkt_name + " downloaded")

            else:
                print("Error downloading " + objkt_name )

    else:
        print("Error " + str(r.status_code))

main(sys.argv[1:])
