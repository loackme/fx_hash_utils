# fx_hash_utils

Some Python scripts that [fx(hash)](https://fxhash.xyz/) users might find useful.

## dependencies

Install the python dependencies.

```
python3 -m pip install -r requirements.txt
```

## Download all the images of a generative token

This script downloads all the static images of the tokens generated from a generative token into a local folder.

Usage:
```
python3 get_images.py --id <GT_id> --folder <folder>
```

## Pinning tokens

These scripts allow you to pin tokens using different services.

- Pinata ('pinata'): see https://nftbiker.xyz/pin for instructions on how to generate an api key.
- Infura ('infura'): once you have created an account on https://infura.io/, create a new IPFS project. In the project settings, look for 'PROJECT ID' and 'PROJECT SECRET'. That's what you need to use as 'api_key' and 'api_secret' respectively.
- Local Node ('ipfs'): You can also use these scripts to pin to your own locally-running IPFS node. Note that pinning the generator (last step) can take a very long time, depending on your node and the size of the artwork.

### pin_tokens

This script allows you to pin all tokens generated from a given generative token.

Usage:
```
python3 pin_tokens.py --id <GT_id> --api_key <api_key> --api_secret <api_secret> --service_type [pinata|infura|ipfs]
```

### pin_collection

This script allows you to pin all the tokens in your fx(hash) collection.

Usage:
```
python3 pin_collection.py --wallet <wallet> --api_key <api_key> --api_secret <api_secret> --service_type [pinata|infura|ipfs]
```

### pin_creations

This script allows you to pin all the tokens you have created as an artist on fx(hash).

Usage:
```
python3 pin_creations.py --wallet <wallet> --api_key <api_key> --api_secret <api_secret> --service_type [pinata|infura|ipfs]
```
