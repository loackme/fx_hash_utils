import json, requests, sys

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

        #Metadata
        ipfs_hash = objkt['metadataUri'][7:]
        self.pin(ipfs_hash,name,"Metadata")

        # Main
        ipfs_hash = objkt['metadata']['artifactUri'][7:]
        self.pin(ipfs_hash,name,"Artifact")

        # Display
        ipfs_hash = objkt['metadata']['displayUri'][7:]
        self.pin(ipfs_hash,name,"Display")

        # Thumbnail
        ipfs_hash = objkt['metadata']['thumbnailUri'][7:]
        self.pin(ipfs_hash,name,"Thumbnail")


    def pin(self, ipfs_hash, name, type_data):
        if self.ipfs_service_type == 'pinata':
            self.pinataRequest(ipfs_hash, name, type_data)
        elif self.ipfs_service_type == 'ipfs':
            self.pinataRequest(ipfs_hash, name, type_data)
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