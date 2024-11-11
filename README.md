# nodepay-auto-min
# Nodepay Network Bot



## Description

This script automates network or node operations for Nodepay Network.



## Features

- **Automated node interaction**

- **Mutil-account session**

- **Proxy and non-proxy support**



## Prerequisites

- [Python](https://www.python.org/) (version 3.7 or higher)



## Installation



1. Clone the repository to your local machine:

   ```bash

	git clone https://github.com/gerijr/nodepay-auto-min

   ```

2. Navigate to the project directory:

	```bash

	cd nodepay-auto-min

	```

3. Install the necessary dependencies:

	```bash

	pip install -r requirements.txt

	```



## Usage

1. Register nodepay account first, if you dont have you can register [here](https://app.nodepay.ai/register?ref=QW11yEoQCG4Hsg8), I recomended to download extension and activate your account first before running the script.

2. Set and Modify `user.txt` before running the script. Below how to setup this file, put your np_token in the text file, example below:

	```

	eyJhbGcixxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx

	eyJ23wixxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx

	```

	To get your token, follow this step:

	- Login to your grass account in https://app.nodepay.ai/dashboard, make sure you is in this link before go to next step

	- Go to inspect element, press F12 or right-click then pick inspect element in your browser

	- Go to application tab - look for Local Storage in storage list -> click `https://app.nodepay.ai` and you will see your np_token.

	- or you can go Console tab and paste this 

	```bash

	localStorage.getItem('np_token')

	```

3. If you want to use proxy, edit the `proxy.txt` with your proxy.

	```

 	ip:port

	username:password@ip:port

	http://ip:port

	http://username:password@ip:port

	socks5://ip:port

	socks5://username:password@ip:port

 	```

4. Run the script:

	```bash

	python main.py

	```

5. When running the script, select the menu if you want to use proxy or not and if you want to show the error in console or not with arrow keys, it will look like this

	```

 	? Do you want to use or run with proxy? (Use arrow keys)

	❯ Use Proxy

	  Without Proxy/Local network

 	```

	```

	? Do you want to show error in console?

	❯ Show Errors

	  Hide Errors

	```

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more details.



## Note

This script only for testing purpose, using this script might violates ToS and may get your account permanently banned.



My reff code if you want to use :) : 

https://app.nodepay.ai/register?ref=QW11yEoQCG4Hsg8
