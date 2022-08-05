#game texts
newgamebutton = " Start a Kingdom"
newgamecaption = "Avalon PythonTelegramBot by DJPeace@CityBitcoinChannel\n(Beta Ver. 5.01 - 05 Aug 2022)"
joingamebutton = "Join the Kingdom"
resetbutton = 'RESET'
donebutton = 'DONE'
clicktojoin = 'Click to JOIN at group: '
plsstartgrp = "Please start a game in group with /newgame first."
joinbelow = "There is currently a game in play. Click the button below to join."
cantjoin = "It is not the time to join."
nogame = "There is no game in queue. Use /newgame instead."
started = "The game has started."
need5 = "There is not enough player. (Need 5)"
test2 = "Starting game in 2 people test mode. (Not recommended for play)"
full10 = "10 Players are in game. You may not join."
enoughplayers = "Enough players. You can wait for more or use /startgame to start."
assigning = "Assigning roles..."
oberonchance = 'In a game of 9 players, there is a chance for Oberon. (See /rolecons .)'
playersare = "Players:"
mervision = 'You see the bad guys \U0001F9DF: \n'
badfdvision = 'You see your friends \U0001F9DF: \n'
psychicvision = 'You see two psychics \U0001F52A\U0001F52E: \n'
wellreceived = 'All players have received their roles.'
ordermsg = 'Your turn order is: '
ordersare = "Order:"
cantbattle = "It is not the time to start round."
vote5 = "This is the last chance to pick. You are NOT allowed to vote NO."
picknow = 'Choose members for journey'
selected = " has been selected."
choicereset = "Choice reset."
chosen = "Members for journey have been chosen."
voteyes = "Vote YES"
voteno = "Vote NO"
confirmselect = "Do you agree the following to start the journey?"
selectionis = " You have voted on this journey party - "
successelect = "Motion carried. Journey will begin."
failselect = "Motion rejected."
tobattle = "Discuss among yourselves, then use /battle to start next turn when you are ready."
battlewin = "Journey is a success."
battlelost = "Journey has failed."
battlechoice = 'Do you want the journey to succeed?'
battlecannotno = 'You are not allowed to vote NO.'
confirmyes = 'I confirm to vote YES.'
changetono = 'Wait. Change to NO.'
confirmno = 'I confirm to vote NO.'
changetoyes = 'Wait. Change to YES.'
selectedby = "You have decided on the success of this journey: "
journeywin = 'Success'
journeylost = 'Failure'
journeyname = 'Journey'
gamewinend = 'After a long battle, you and your party have completed the journey.\nThe bad guys send their last attempt to assassinate your Merlin.\nWill they discover who Merlin is?'
gamelostend = """As dawn breaks, the crowd turns to see the kingdom in ruins. \n
The last hope of the kingdom lies motionless on the floor.\n
You were confused to the very last moment of the kingdom, not knowing who were the spies among you."""
winners = 'Winner(s): \U0001F9DF Bad guys'
losers = 'Loser(s): \U0001F9E0 Good guys'
assassincaption = """The bad guys slowly reveals themselves.\n
They gather for a final discussion on who is the Merlin behind the kingdom.
Bad guys: """

kill = "Assassinate "
assguymsg = 'LAST CHANCE TO DEFEAT GOOD GUYS'
killsuccess = "Assassination COMPLETED"
killfail = "Assassination FAILED"
gameover = 'Game over. Use /endgame to clear the board.'

def alreadinqueue(username, user):
    return "@"+username+ " (ID: " + user + ") is already in queue."
    
def joinedqueue(username, user):
    return "@"+username + " (ID: " + user + ") has joined the queue."

def assignmsg(value, role):
    return 'Your role is: ' + value + '\n\n' + role

def firstleader(user):
    return "First leader is: " + user + ". Please type /battle to start round."
    
def selectmsg(leader, roundNo, pickNo):
    return "@"+leader+ " \U0001F9D4 is selecting party for Round " + roundNo + "\n\n" + "You need to select: " + pickNo + " players."

def leaderselected(leader):
    return "\U0001F9D4 @"+leader+" selected:"

def assasinatemsg(assguy):
    return 'Assassin @' + assguy + ' will now administer the final blow.' + '\n'

def finalkillwin(gametime, killchoice, assassin, badguys, coolguys):
    caption = (gametime + ' \n\nAs dawn breaks, the crowd turns to see the kingdom in ruins. \n@' +
              killchoice + ' lies motionless on the floor.' + '\n' +
              '@' + assassin + ' has made the right choice.' + '\n' +
              'Once again, the party failed to protect the kingdom, and the bad guys have triumphed.' + '\n\n' +
              'Winner(s): \U0001F9DF Bad guys'+'\nWon - @'+ badguys +'\n\n'+
              'Loser(s): \U0001F9E0 Good guys'+'\nLost - @'+ coolguys)
    return caption

def finalkilllost(gametime,merlin,target,assassin,coolguys,badguys):
    caption = (gametime + ' \n\nAs dawn breaks, the party notices the villagers gathering at the town hall. \n@' +
              merlin + ' smiles quietly behind @' + target + ' , who has silently protected them.\n' +
              'Assassin @' + assassin + ' falls to the ground, as their last attempt of assassination has been thwarted.\n\n' +
              'Winner(s): \U0001F9E0 Good guys'+'\nWon - @'+ coolguys +'\n\n'+
              'Loser(s): \U0001F9DF Bad guys'+'\nLost - @'+ badguys)
    return caption