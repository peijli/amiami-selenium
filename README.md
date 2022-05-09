# amiami-selenium

This selenium-based Python script automates the UI-interaction procedure to expedite the buying process for items on the Japanese website [Amiami](https://www.amiami.com).

It was originally designed for the highly sought-after Fumofumo plushies, inspired by characters from the video game series Touhou Project and produced by the company [Gift](https://gift-gift.jp/), but can be used for the purchase of other anime figures and merchandise on the site.

## Prerequisites

### Python Packages

Run `pip install -r requirements.txt` to install necessary packages to execute this script.

### Chrome Web Driver

This script was (initially) developed to work with the Google Chrome browser on the Microsoft Windows operating system. 
[Download the browser here](https://support.google.com/chrome/answer/95346?hl=en&co=GENIE.Platform%3DDesktop) if you have not already done so.

Open up your Chrome browser and navigate to [chrome://version/](chrome://version/). Note the version number displayed on the first line of the screen (e.g., 101.0.4951.41).

Navigate to the [online repository page for Chrome Web Driver](https://chromedriver.storage.googleapis.com/index.html), select the folder with name corresponding your Chrome's version number, and download the appropriate ZIP file for your operating system.

Unzip the downloaded file on your computer, and note the directory path to the unzipped `chromedriver.exe`. 

> The default path for the purposes of this project is  `C:/chromedriver_win32/chromedriver.exe`. It is strongly recommended that you also set up your Chrome Driver this way

### Amiami Account

Register for an account [on Amiami's website](https://secure.amiami.com/eng/registmail/1/).
Update your personal information such that you "Automtically combine" your orders by month, if you intend ordering multiple items.

![Amiami's order combination settings](combine_orders.png)

## Configuration

Make a copy of the `config.json` file named `config_private.json` on your local system (while the `.gitignore` file is set up explicitly such that you should NOT commit this file to GitHub). 
Open `config_private.json` in your text editor of choice and update the following information.

### Credentials

Enter the email and password of your Amiami account in the `credentials.email` and `credentials.password` fields of `config_private.json`. 
Be assured (or examine the source code yourself) that this information will only be directly transmitted to Amiami's servers.

The public `config.json` file in this repository has been set up with a dummy account for testing purposes. DO NOT modify them, and DO NOT make actual purchases with this account, since all the personal information associated with it are FAKE, and its email address is UNMONITORED.

### Chrome Web Driver Path

Enter the path to your Chrome driver application in the `driverPath` field.
Note that the default value is, again, set to `C:/chromedriver_win32/chromedriver.exe`.

### List of Items

The fields `testItems` and `actionItems` correspond to the ID numbers for products to be included in test runs and real, operational runs of the bot, respectively.

#### Locating product IDs

Whenever you visit a product page on Amiami, note that the URL is in the following format:  `https://www.amiami.com/eng/detail/?gcode=GOODS-00067399`.

The portion of the URL after the attribute name `gcode=`, a.k.a. `GOODS-00067399`, would be referred to as the "product ID."

Populate the `testItems` and `actionItems` attributes with lists of product IDs of your choice.

## Execution

Run the bot by issuing the following command in your terminal:

```bash
python ./main.py [argument]
```

The following arguments are available:

- `test`: (default argument) test run with dummy credentials in `config.json`, automative procedures will halt at the penultimate "Order Review" screen. 
- `action`: operational run with private user credentials in `config_private.json`, automative procedures will attempt to proceed until the final "Order Confirmation" screen.

## Known Issues

- This bot is highly dependent on reliable (and preferably wired) internet connection with bandwidths of at least 1 Gbps, otherwise...
- This bot is not very well adapted to handle error screens and 503 response codes from Amiami's servers when overall traffic to the servers are high.
- This bot cannot dynamically adjust the list of items to purchase based on whether a specific item becomes in or out of stock.
- The code base of this project needs to be refactored into that of a standardized Python package, to enable its integration of and into similar libraries.

## Contribution

We would highly appreciate your feedback on the codebase and user experience of this bot in the [Issue](https://github.com/Gensoukyou-Wolverines/amiami-selenium/issues) section of this repository.

[Fork this repository](https://github.com/Gensoukyou-Wolverines/amiami-selenium/fork) and [create pull requests](https://github.com/Gensoukyou-Wolverines/amiami-selenium/pulls) if you wish to contribute to the source code.

## Disclaimer

The usage of bots to obtain sought-after goods on online storefronts is, in the views of some, a controversial and morally ambiguous action.
It is to be made clear that we do not condone the usage of our code in the business practice of hoarding stocks of highly demanded merchandise and reselling them for exorbitant prices -- more commonly known as "scalping."

By cloning, forking, contributing to, or running code in this repository, you are to assume all responsibilities for your actions.
The authors of this repository are to claim no liability for any damage caused by malicious or inappropriate usage, in full or in part, of code in this repository.
