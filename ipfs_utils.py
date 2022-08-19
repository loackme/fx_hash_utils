import json, requests, sys, subprocess

class IPFSPinner:
    """Pins hashes to a specific service, like Infura, Pinata, or your own locally-running IPFS node."""

    def __init__(self, ipfs_service_type, api_key, api_secret):
        """Creates a new IPFSPinner for the given service type.

         Parameters
        ----------
        ipfs_service_type : str
            one of "pinata", "ipfs" (for a locally-running IPFS node), or "infura"
        api_key : str
            the API key for the service (not needed for "ipfs")
        api_secret : str
            the API secrete for the service (not needed for "ipfs")
        """
        self.api_key = api_key
        self.api_secret = api_secret
        self.ipfs_service_type = ipfs_service_type

    def pinToken(self, objkt):
        name = objkt['name']
        print(f'Pinning {name}...')
        #print(objkt)

        #Metadata
        ipfs_hash = objkt['metadataUri'][7:]
        self.pin(ipfs_hash,name,"Metadata")

        # Display
        ipfs_hash = objkt['metadata']['displayUri'][7:]
        self.pin(ipfs_hash,name,"Display")

        # Thumbnail
        ipfs_hash = objkt['metadata']['thumbnailUri'][7:]
        self.pin(ipfs_hash,name,"Thumbnail")

        # Main
        if 'generatorUri' in objkt['metadata']:
            ipfs_hash = objkt['metadata']['generatorUri'][7:]
        elif 'generativeUri' in objkt['metadata']:
            ipfs_hash = objkt['metadata']['generativeUri'][7:]
        else:
            # note: this doesn't actually work because it includes the fxhash query param.
            ipfs_hash = objkt['metadata']['artifactUri'][7:]
        self.pin(ipfs_hash,name,"Generator")


    def pin(self, ipfs_hash, name, type_data):
        if self.ipfs_service_type == 'pinata':
            self.pinataRequest(ipfs_hash, name, type_data)
        elif self.ipfs_service_type == 'ipfs':
            self.pinIpfsLocalNode(ipfs_hash, name, type_data)
        elif self.ipfs_service_type == 'infura':
            raise Exception('Infura not implemented yet.')
        else:
            raise Exception('Unknown IPFS service type')

    def pinataRequest(self, ipfs_hash,name,type_data):
        url_pin = "https://api.pinata.cloud/pinning/pinByHash"
        headers = {
            'content-type': 'application/json',
            'pinata_api_key': self.api_key,
            'pinata_secret_api_key': self.api_secret
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
        else:
            print(f'Error pinning {type_data}: {r.status_code}')

    def pinIpfsLocalNode(self, ipfs_hash, name, type_data):
        result = subprocess.call(["ipfs", "pin", "add", ipfs_hash])
        if result == 0:
            print(f'{type_data} pinned')
        else:
            print(f'Error pinning IPFS hash. Error code {result}')
