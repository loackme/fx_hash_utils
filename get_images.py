import json, requests, shutil, os

GT_id = "13"                   #   id of the generative token
folder = "sticky_circles"      #   folder to save files in

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
    print("Error " + r.status_code)
