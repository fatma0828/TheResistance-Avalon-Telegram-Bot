# TheResistance-Avalon-Telegram-Bot
Telegram bot for hosting The Resistance: Avalon games made with the python-telegram-bot.

# Installation Guide
0. Download this repo.
1. Register at BotFather for a token and bot URL.
2. Prepare a host server with webhook compatibility. (e.g Heroku)
3. Input (1) Bot token, (2) bot URL, and (3) Webhook URL to myconfig.py
4. Deploy on server.

(Optional) Edit gamemsg.py to change the game text.

(Optional) Change the images in the /img folder to change game images.

# Game rules
Use the /genrules command to invoke game rules message.
Or, visit https://www.ultraboardgames.com/avalon/game-rules.php

# Commands
/newgame - Start a new game in the current group

/startgame - Begin the game when there are enough players

/endgame - End the game when it is stuck or when it is over

/genrules - Show the rules of the game

/rolerules - Show the functions of all roles

/rolecons - Show the distribution of roles for different number of players

/checkvote - Show the current voting status of the current round, to check who has not voted yet (once per round)


# Disclaimer
This bot was built for educational purposes. The right to all characters and gameplay mechanisms belong to the original owner of the game. Also, this bot has only been tested on Heroku; connection methods may differ for other service hosts.

# Screenshots

/rolerules

![image](https://user-images.githubusercontent.com/70230072/183017521-c4706fc3-e566-440e-bdc5-1cb542e57e0e.png)

/newgame

![image](https://user-images.githubusercontent.com/70230072/183018102-ffe38199-9479-4565-a2bf-f07afebbabf6.png)

Entering /startgame invokes the role assignment function, which then notifies players of their roles in private message.

![image](https://user-images.githubusercontent.com/70230072/183018343-2fb848b6-5daf-4963-a034-366d574491fb.png)

Messages in main chat will show instructions to proceed.

![image](https://user-images.githubusercontent.com/70230072/183018713-c20dd707-2add-482e-be0b-c02e2ee1a04e.png)

Selecting players for a Round - journey

![image](https://user-images.githubusercontent.com/70230072/183018925-aa739a0b-b64a-48b9-9777-a64d81b142a7.png)

Voting for the success of a journey

![image](https://user-images.githubusercontent.com/70230072/183019324-5691bbd3-1498-4179-9601-ab4a4c2009fb.png)
