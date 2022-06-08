# NFT-parser
## It's python class of parse NFT from OpenSea.
## Quick start
```
from NFTParser import OpenSeaParser
if __name__ == '__main__':
    parser = OpenSeaParser(log=True)
    parser.downloadPhotos(10) # download 10 photos from OpenSea
    parser.getInstagram(10)  # get 10 instagramms href from OpenSea
    parser.getTwitters(10) # get 10 twitter href from OpenSea
```
## Download packages
```
- pip install selenium
- pip install requests
- pip install bs4
- download [chromedriver](https://chromedriver.chromium.org/downloads)
```
## Methods
### downloadPhotos(x) - download x NFT picture from OpenSea
### getInstagram(x) - get x href instagramm from OpenSea
### getTwitters(x) - get x href twitters from OpenSea
## All methotds download [there](https://opensea.io/activity?search[eventTypes][0]=AUCTION_SUCCESSFUL)
## For communication write me [@DenchicEz](https://t.me/DenchicEz)
