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

## pin_collection

This script allows you to pin all the tokens in your fx(hash) collection to Pinata.
See https://nftbiker.xyz/pin for instructions on how to generate an api key.

Usage:
```
python3 pin_collection.py --wallet <wallet> --api_key <api_key> --api_secret <api_secret>
```
