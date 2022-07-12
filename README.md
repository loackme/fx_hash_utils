# fx_hash_utils

Some Python scripts that [fx(hash)](https://fxhash.xyz/) users might find useful.

## dependencies

Install the python dependencies.

```
python3 -m pip install -r requirements.txt
```

## get_images

This script downloads all the static images of the tokens generated from a generative token into a local folder.

Usage:
```
python3 get_images.py --id <GT_id> --folder <folder>
```

## pin_tokens

This script allows you to pin all tokens generated from a given generative token to Pinata.
See https://nftbiker.xyz/pin for instructions on how to generate an api key.

Usage:
```
python3 pin_tokens.py --id <GT_id> --api_key <api_key> --api_secret <api_secret>
```

## pin_tokens_infura

This script allows you to pin all tokens generated from a given generative token on Infura. Once you have created an account on https://infura.io/, create a new IPFS project. In the project settings, look for 'PROJECT ID' and 'PROJECT SECRET'. That's what you need to use the API.

Usage:
```
python3 pin_tokens_infura.py --id <GT_id> --api_id <PROJECT_ID> --api_secret <PROJECT_SECRET>
```

## pin_collection

This script allows you to pin all the tokens in your fx(hash) collection to Pinata.
See https://nftbiker.xyz/pin for instructions on how to generate an api key.

Usage:
```
python3 pin_collection.py --wallet <wallet> --api_key <api_key> --api_secret <api_secret>
```

## pin_creations

This script allows you to pin all the tokens you have created as an artist on fx(hash) to Pinata.
See https://nftbiker.xyz/pin for instructions on how to generate an api key.

Usage:
```
python3 pin_creations.py --wallet <wallet> --api_key <api_key> --api_secret <api_secret>
```

# Pinning to your local IPFS node

You can also use these scripts to pin to your own locally-running IPFS node with the `ipfs` command line.

Use any of the script commands above, but add ` --service_type ipfs` to the end of the command.

Note that pinning the generator (last step) can take a very long time, depending on your node and the size of the artwork.