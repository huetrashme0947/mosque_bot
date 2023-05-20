# Mosque Bot for TeamSpeak 3

TeamSpeak 3 bot written in Python for moving users to a specific channel at prayer times


## Features

- Automatic retrieval of prayer times via Aladhan Prayer Times API ([https://aladhan.com/prayer-times-api](https://aladhan.com/prayer-times-api))
	- Customizable location for retrieving prayer times
- Different channels for each prayer time
- Poking or messaging clients when being moved
	- Customizable messages for each prayer time
- Customizable display name of bot user
- Excluding clients...
	- in specific server groups
	- with specific unique identifiers
	- being in specific channels
	- with away/AFK status
	- being in temporary channels


## Requirements

The bot uses and needs access to the ServerQuery raw (not SSH) interface to communicate with the TeamSpeak server. The bot needs a Query account with the  ```b_serverinstance_textmessage_send``` permission set if the bot should message clients when moving them or the ```i_client_poke_power``` permission set high enough to poke clients if the bot should poke clients (75 should do the trick for most server configurations). Also the ```i_client_move_power``` needs to be high enough to move clients (75 should also work here in most cases).


## Installation

Clone the repository and install the dependencies:

	git clone https://github.com/huetrashme0947/mosque_bot
	cd mosque_bot
	pip install -r requirements.txt


## Configuration

The bot supports a range of customization options which can be configured in the ```mosque_bot.ini``` file. The file includes comments explaining every option, so please refer to those when configuring the bot.

## Starting the Bot

The bot can be started directly in a shell by simply executing the ```mosque_bot.py``` script:

	python3 mosque_bot.py
