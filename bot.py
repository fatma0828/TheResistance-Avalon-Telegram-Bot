# -*- coding: utf-8 -*-
"""
Created on Sun Oct 10 22:59:01 2021

@author: DJPeace @CantonesePeaceChannel
"""

from myconfig import TOKEN, WEBHOOKURL, BOTURL
import gameroles as gr
import gamemsg as msg
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler
from datetime import datetime
import pytz
import os
import random
import time

PORT = int(os.environ.get('PORT', 5000))

CurrentGames = {}
    
class GameID:
    
    def __init__(self, name):
        self.name = name
        self.grpname = None
        self.Players = {}
        self.Roles = {}
        self.order = {}
        self.leader = None
        self.selection = {}
        self.vote = {}
        self.journey = {}
        self.roundRes = {}
        self.roundmsgid = []
        self.votemsgid = []
        self.votemsgtext = None
        self.numVote = 1
        self.turn = 1
        self.round = 1
        self.status = 0
        self.votetimer = None
        self.journeytimer = None
        self.checks = 0
    def addPlayer(self, userid, username):
        self.Players[userid] = username
    def addRole(self, userid, role):
        self.Roles[userid] = role
    def nextstage(self):
        self.status += 1
    def setorder(self):
        randlist = list(self.Players)
        random.shuffle(randlist)
        order = 1
        for x in range(len(randlist)):
            self.order[order] = randlist[x]
            order += 1
    def setLeader(self):
        nowturn = self.turn
        while nowturn > len(self.Players):
            nowturn -= len(self.Players)
        leaderID = self.order[nowturn]
        self.leader = self.Players[leaderID]
    def nextturn(self):
        self.turn += 1
    def nextround(self):
        self.round += 1
        self.selection = {}
        self.vote = {}
        self.journey = {}
    def pick(self, userid):
        if userid == "Reset":
            self.selection = {}
            return
        self.selection[userid] = self.Players[userid]
    def needpick(self):
        req = {5:[2,3,2,3,3],
               6:[2,3,4,3,4],
               7:[2,3,3,4,4],
               8:[3,4,4,5,5],
               9:[3,4,4,5,5],
               10:[3,4,4,5,5],
               2:[2,2,2,2,2]}
        thisreq = req[len(self.Players)]
        roundreq = thisreq[self.round-1]
        return roundreq
    def voting(self, userid, choice):
        voter = self.Players[userid]
        self.vote[voter] = choice
    def nextvote(self):
        self.numVote += 1
    def gojourney(self, userid, choice):
        voter = self.Players[userid]
        self.journey[voter] = choice
    def recround(self, result):
        self.roundRes['Round '+str(self.round)] = result
            

def newgame(update, context):
    chatid = str(update.message.chat.id)
    grpname = update.message.chat.title
    link = BOTURL + '?start=' + chatid
    
    if update.message.chat.type == 'private':
        update.message.reply_text(msg.plsstartgrp)
        return
    
    if chatid in CurrentGames:
        update.message.reply_text(msg.joinbelow)
        thisGame = CurrentGames[chatid]       
    else:
        thisGame = GameID(chatid)
        thisGame.nextstage()
        CurrentGames[chatid] = thisGame
        thisGame.grpname = grpname
        
    keyboard = [[InlineKeyboardButton(grpname + msg.newgamebutton, url=link)]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_animation(animation=open('img/start.gif', 'rb'), caption=msg.newgamecaption,
                                   reply_markup=reply_markup, quote=False)

        
def startgame(update, context):
    chatid = str(update.message.chat.id)
    if chatid not in CurrentGames:
        update.message.reply_text(msg.nogame)
        return
    if CurrentGames[chatid].status != 1:
        update.message.reply_text(msg.started)
        return
    if len(CurrentGames[chatid].Players) in [0, 1, 3, 4]:
        update.message.reply_text(msg.need5)
        return
    if len(CurrentGames[chatid].Players) == 2:
        update.message.reply_text(msg.test2)
    
    update.message.reply_text(msg.assigning)
    time.sleep(5)
    assign(chatid, context)
    CurrentGames[chatid].nextstage()


def genrules(update, context):
    update.message.reply_text(gr.genrules)
def rolerules(update, context):
    update.message.reply_text(gr.rolerules)
def rolecons(update, context):
    update.message.reply_text(gr.rolecons)


def start(update, context):
    try: context.args[0]
    except IndexError:
        update.message.reply_text(msg.plsstartgrp)
        return

    payload = str(context.args[0])
    keyboard = [[InlineKeyboardButton(msg.joingamebutton, callback_data=
                {"groupid":payload})]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text(
        msg.clicktojoin + CurrentGames[payload].grpname,
        reply_markup=reply_markup)


def joingame(update, context):
    cbq = update.callback_query
    cbq.answer()
    chatid = str(cbq.data.get('groupid'))
    user = str(cbq.from_user.id)
    username = str(cbq.from_user.username)
    
    if len(CurrentGames[chatid].Players) >= 10:
        cbq.bot.send_message(chatid, msg.full10)
        return
    
    if CurrentGames[chatid].status != 1:
        cbq.bot.send_message(user, msg.cantjoin)
        return
    
    # Check if player on list
    if user in CurrentGames[chatid].Players:
        cbq.bot.send_message(user, msg.alreadyinqueue(username, user))
    else:
        # Record player
        CurrentGames[chatid].addPlayer(user, username)
        cbq.bot.send_message(chatid, msg.joinedqueue(username, user))
        cbq.edit_message_text(text="JOINED")
        
        if len(CurrentGames[chatid].Players) >= 5:
            cbq.bot.send_message(chatid, msg.enoughplayers)


def playerlist(update, context):
    chatid = str(update.message.chat.id)
    if chatid in CurrentGames:
        update.message.reply_text(msg.playersare+'\n'+
                                  '\n'.join(f'{value}' for key, value in CurrentGames[chatid].Players.items()))
    else:
        update.message.reply_text(msg.nogame)


def forcefinal(update, context):
    chatid = str(update.message.chat.id)
    assassinate(chatid, context)
    
    
def assign(ID, context):
    roles = [gr.merlin,gr.assassin,gr.morgana,gr.percival,gr.goodguy1]
    
    if len(CurrentGames[ID].Players) in [6, 7, 8]:
        roles.append(gr.goodguy2)
        if len(CurrentGames[ID].Players) > 6:
            roles.append(gr.mordred)
            if len(CurrentGames[ID].Players) > 7:
                roles.append(gr.goodguy3)
    
    if len(CurrentGames[ID].Players) == 9:
        randlist = [gr.goodguy2,gr.goodguy3,gr.goodguy4,gr.oberon]
        random.shuffle(randlist)
        context.bot.send_message(ID, msg.oberonchance)
        for x in range(3):
            roles.append(randlist[x])
        roles.append(gr.mordred)
        
        if len(CurrentGames[ID].Players) == 10:
            addlist = [gr.goodguy2,gr.goodguy3,gr.goodguy4,gr.oberon,gr.mordred]
            roles.extend(addlist)
        
    randlist = list(CurrentGames[ID].Players)
    random.shuffle(randlist)
    for x in range(len(CurrentGames[ID].Players)):
        CurrentGames[ID].addRole(randlist[x],roles[x])
    CurrentGames[ID].setorder()
    notifyrole(ID, context)
    

def notifyrole(ID, context):
    rolelist = CurrentGames[ID].Roles.items()
    for key, value in rolelist:
        context.bot.send_message(key, msg.assignmsg(value, gr.roledesc[value]))
    badguys = [CurrentGames[ID].Players[key] for key, value in rolelist if value in [gr.assassin, gr.morgana, gr.oberon]]
    badfriends = [CurrentGames[ID].Players[key] for key, value in rolelist if value in [gr.assassin, gr.morgana, gr.mordred]]
    psychics = [CurrentGames[ID].Players[key] for key, value in rolelist if value in [gr.merlin, gr.morgana]]

    for key, value in rolelist:
        if value in gr.merlin:
            context.bot.send_message(key, msg.mervision + '\n'.join(badguys))
        if value in [gr.assassin, gr.morgana, gr.mordred]:
            context.bot.send_message(key, msg.badfdvision + '\n'.join(badfriends))
        if value in gr.percival:
            context.bot.send_message(key, msg.psychicvision + '\n'.join(psychics))
    context.bot.send_message(ID, msg.wellreceived)
    orderlist = CurrentGames[ID].order.items()
    orderlist2 = {}
    for key, value in orderlist:
        context.bot.send_message(value, msg.ordermsg + str(key))
        orderlist2[CurrentGames[ID].Players[value]] = str(key)
    context.bot.send_message(ID, msg.ordersare+'\n'+'\n'.join(f'{key}: {value}' for key, value in orderlist2.items()))
    del orderlist2
    CurrentGames[ID].setLeader()
    context.bot.send_message(ID, msg.firstleader(CurrentGames[ID].leader))


def setround(update, context):
    chatid = str(update.message.chat.id)
    if chatid not in CurrentGames:
        update.message.reply_text(msg.nogame)
    thisGame = CurrentGames[chatid]
    if thisGame.status != 2:
       context.bot.send_message(chatid, msg.cantbattle)
       return
    thisGame.setLeader()
    roundmsg = context.bot.send_message(chatid, msg.selectmsg(thisGame.leader,str(thisGame.round),str(thisGame.needpick())))
    thisGame.roundmsgid.append(roundmsg.message_id)
    if thisGame.numVote >= 5:
        update.message.reply_text(msg.vote5)
    
    keyboard = []
    for x in range(len(thisGame.Players)):
        name = thisGame.Players[thisGame.order[x+1]]
        keyboard.append([InlineKeyboardButton(text="@"+name, callback_data="Select: " + str(thisGame.order[x+1]))])

    keyboard.append([InlineKeyboardButton(text=msg.resetbutton, callback_data="Select: Reset")])
    keyboard.append([InlineKeyboardButton(text=msg.donebutton, callback_data="Select: Done")])
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    context.bot.send_message(chatid, msg.picknow, reply_markup=reply_markup)


def playerselection(update, context):
    cbq = update.callback_query
    cbq.answer()
    chatid = str(cbq.message.chat.id)
    thisGame = CurrentGames[chatid]
    choice = cbq.data.split(": ")[-1]
    user = str(cbq.from_user.id)
    if thisGame.Players[user] != thisGame.leader:
        return
    if choice in thisGame.selection:
        return
    if choice.isnumeric():
        thisGame.pick(choice)
        roundmsg = cbq.bot.send_message(chatid, thisGame.Players[choice] + msg.selected)
        thisGame.roundmsgid.append(roundmsg.message_id)
    if choice == "Reset":
        thisGame.pick("Reset")
        cbq.bot.send_message(chatid, msg.choicereset)
    if choice == "Done":
        if len(thisGame.selection) == thisGame.needpick():
            thisGame.votemsgtext = (msg.leaderselected(thisGame.leader) +
                                    '\n\n@'+'\n@'.join(f'{x}' for x in thisGame.selection.values()))
            votemsg = cbq.bot.send_message(chatid, thisGame.votemsgtext)
            thisGame.votemsgid = votemsg.message_id
            cbq.edit_message_text(text=msg.chosen)
            for x in thisGame.roundmsgid:
                context.bot.delete_message(chatid, x)
            thisGame.roundmsgid = []
            votetime(chatid, context)
            thisGame.votetimer = int(time.time())
        else:
            cbq.bot.send_message(chatid, "You need to select: " + str(thisGame.needpick()) + " players."+'\n'+
                                         "You now have " + str(len(thisGame.selection)) + " players selected.")


def votetime(ID, context):
    thisGame = CurrentGames[ID]
    selection = '\n@'+'\n@'.join(f'{x}' for x in thisGame.selection.values())
    keyboard = [[InlineKeyboardButton(msg.voteyes, callback_data="Vote: Yes: " + str(ID)),
                 InlineKeyboardButton(msg.voteno, callback_data="Vote: No: " + str(ID))]]
    if thisGame.numVote >= 5:
        keyboard = [[InlineKeyboardButton(msg.voteyes, callback_data="Vote: Yes: " + str(ID))]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    for x in thisGame.Players.keys():
        context.bot.send_message(x, msg.confirmselect + selection,
                                 reply_markup=reply_markup)


def voteselection(update, context):
    cbq = update.callback_query
    cbq.answer()
    chatid = cbq.data.split(": ")[-1]
    thisGame = CurrentGames[chatid]
    choice = cbq.data.split(": ")[-2]
    user = str(cbq.from_user.id)
    if user in thisGame.vote:
        context.bot.send_message(user, 'You have already voted.')
        return
    thisGame.voting(user, choice)
    cbq.edit_message_text(text="(Round: "+str(thisGame.round)+")"+msg.selectionis + choice)
    if len(thisGame.vote) == len(thisGame.Players):
        thisGame.votetimer = None
        thisGame.checks = 0
        
        time.sleep(5)
        numYes = list(thisGame.vote.values()).count('Yes')
        numNo = list(thisGame.vote.values()).count('No')
        voteRes = numYes > numNo
        thisGame.votemsgtext = thisGame.votemsgtext + '\n\n' + "Votes casted:" +'\n@'+'\n@'.join(f'{key}: {value}' for key, value in thisGame.vote.items())
        
        context.bot.delete_message(chatid, thisGame.votemsgid)
        votemsg = context.bot.send_message(chatid, thisGame.votemsgtext)
        thisGame.votemsgid = votemsg.message_id
        
        if voteRes:
            thisGame.journeytimer = int(time.time())
            thisGame.votemsgtext = thisGame.votemsgtext + '\n\n' + msg.successelect
            context.bot.edit_message_text(thisGame.votemsgtext, chat_id = chatid, message_id = thisGame.votemsgid)
            thisGame.votemsgtext = None
            thisGame.numVote = 1
            journey(chatid, context)
        else:
            context.bot.send_message(chatid, msg.failselect)
            thisGame.nextvote()
            context.bot.send_message(chatid, "Vote attempts: " + str(thisGame.numVote) + "/5\n" + msg.tobattle)
        thisGame.vote = {}
        thisGame.nextturn()
        

def journey(ID, context):
    thisGame = CurrentGames[ID]
    keyboard = [[InlineKeyboardButton(msg.battlewin, callback_data="Journey1: Yes: " + str(ID)),
                 InlineKeyboardButton(msg.battlelost, callback_data="Journey1: No: " + str(ID))]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    for x in thisGame.selection.keys():
        context.bot.send_message(x, msg.battlechoice,
                                 reply_markup=reply_markup)


def journeying(update, context):
    cbq = update.callback_query
    cbq.answer()
    chatid = cbq.data.split(": ")[-1]
    thisGame = CurrentGames[chatid]
    choice = cbq.data.split(": ")[-2]
    user = str(cbq.from_user.id)
    if thisGame.Roles[user] not in gr.badguys:
        if choice == 'No':
            context.bot.send_message(user, msg.battlecannotno)
            return
    if user not in thisGame.selection:
        context.bot.send_message(user, 'You are not allowed to vote.')
        return
    if choice == 'Yes':
        keyboard = [[InlineKeyboardButton(msg.confirmyes, callback_data="Journey2: Yes: " + chatid)],
                    [InlineKeyboardButton(msg.changetono, callback_data="Journey1: No: " + chatid)]]
    if choice == 'No':
        keyboard = [[InlineKeyboardButton(msg.confirmno, callback_data="Journey2: No: " + chatid)],
                    [InlineKeyboardButton(msg.changetoyes, callback_data="Journey1: Yes: " + chatid)]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    cbq.delete_message()
    cbq.bot.send_message(user, "Confirm to vote: " + choice, reply_markup=reply_markup)


def journeyresult(update, context):
    cbq = update.callback_query
    cbq.answer()
    chatid = cbq.data.split(": ")[-1]
    thisGame = CurrentGames[chatid]
    choice = cbq.data.split(": ")[-2]
    user = str(cbq.from_user.id)
    thisGame.gojourney(user, choice)
    cbq.bot.send_message(chatid, thisGame.Players[user]+" has voted.")
    cbq.edit_message_text(text="(Round: "+str(thisGame.round)+") " + msg.selectedby + choice)
    
    if len(thisGame.journey) == thisGame.needpick():
        thisGame.journeytimer = None
        thisGame.checks = 0
        
        time.sleep(5)
        numYes = list(thisGame.journey.values()).count('Yes')
        numNo = list(thisGame.journey.values()).count('No')
        jourRes = numNo == 0
        if len(thisGame.Players) >= 7:
            if thisGame.round == 4:
                jourRes = numNo < 2
        Resgif = ['img/roundlost.gif', 'img/roundwin.gif'][jourRes]
        
        cbq.bot.send_animation(chatid, open(Resgif, 'rb'), 
                               caption = "Round "+str(thisGame.round)+" Result:" + '\n' +
                                       msg.journeywin+': ' + str(numYes) + '\n' +
                                       msg.journeylost+': ' + str(numNo) + '\n\n' +
                                       msg.journeyname + [msg.journeylost,msg.journeywin][jourRes])
        thisGame.recround(['Lost','Win'][jourRes])
        
        gameRes = list(thisGame.roundRes.values())
        
        if gameRes.count('Win') >= 3:
            time.sleep(5)
            context.bot.send_animation(chatid, open('img/gamewin.gif', 'rb'), 
                                       caption = msg.gamewinend)
            time.sleep(5)
            assassinate(chatid, context)
            return

        if gameRes.count('Lost') >= 3:
            gametime = datetime.now(pytz.timezone("Asia/Hong_Kong")).strftime("%Y-%m-%d %H:%M:%S")
            rolelist = thisGame.Roles.items()
            badguys = [thisGame.Players[key]+" ("+thisGame.Roles[key]+")" for key, value in rolelist if value in gr.badguys]
            coolguys = [thisGame.Players[key]+" ("+thisGame.Roles[key]+")" for key, value in rolelist if value in gr.coolguys]
            context.bot.send_animation(chatid, open('img/gamelost.gif', 'rb'), 
                                   caption = gametime + msg.gamelostend +
                                 msg.winners+'\nWon - @'+ '\nWon - @'.join(badguys) +'\n\n'+
                                 msg.losers+'\nLost - @'+ '\nLost - @'.join(coolguys))
            context.bot.send_message(chatid, msg.gameover)
            thisGame.nextstage()
            return
        
        thisGame.selection = {}
        thisGame.vote = {}
        thisGame.journey = {}
        thisGame.nextround()
        context.bot.send_message(chatid, "Results:"+'\n'+'\n'.join(f'{key}: {value}' for key, value in thisGame.roundRes.items())+'\n'+msg.tobattle)

def assassinate(ID, context):
    thisGame = CurrentGames[ID]
    rolelist = thisGame.Roles.items()
    badguys = [thisGame.Players[key] for key, value in rolelist if value in gr.badguys]
    context.bot.send_animation(ID, open('img/reveal.gif', 'rb'), 
                               caption = msg.assassincaption + '\n@'+ '\n@'.join(badguys))
    assguyID = [key for key, value in rolelist if value == gr.assassin][0]
    context.bot.send_animation(ID, open('img/assready.gif', 'rb'), 
                               caption = msg.assasinatemsg(thisGame.Players[assguyID]))
    
    targets = [key for key, value in rolelist if value not in gr.badguys]
    keyboard = []
    for x in range(len(targets)):
        targetID = targets[x]
        name = thisGame.Players[targetID]
        keyboard.append([InlineKeyboardButton(text=msg.kill+name, callback_data="Kill: " +
                                                                              str(ID) + ": " +
                                                                              str(targetID))])
        
    reply_markup = InlineKeyboardMarkup(keyboard)
    context.bot.send_message(assguyID, msg.assguymsg,
                             reply_markup=reply_markup)
    
def finalkill(update, context):
    cbq = update.callback_query
    cbq.answer()
    chatid = cbq.data.split(": ")[-2]
    thisGame = CurrentGames[chatid]
    choice = cbq.data.split(": ")[-1]
    rolelist = thisGame.Roles.items()
    assassin = [thisGame.Players[key] for key, value in rolelist if value in [gr.assassin]][0]
    merlin = [thisGame.Players[key] for key, value in rolelist if value in [gr.merlin]][0]
    badguys = [thisGame.Players[key]+" ("+thisGame.Roles[key]+")" for key, value in rolelist if value in gr.badguys]
    coolguys = [thisGame.Players[key]+" ("+thisGame.Roles[key]+")" for key, value in rolelist if value in gr.coolguys]
    gametime = datetime.now(pytz.timezone("Asia/Hong_Kong")).strftime("%Y-%m-%d %H:%M:%S")
    
    if thisGame.Roles[choice] == gr.merlin:
        context.bot.send_animation(chatid, open('img/asswin.gif', 'rb'), 
                                   caption = msg.finalkillwin(gametime,thisGame.Players[choice],assassin,'\nWon - @'.join(badguys),'\nLost - @'.join(coolguys)))
        cbq.edit_message_text(text=msg.killsuccess)
        thisGame.nextstage()
    else:
        context.bot.send_animation(chatid, open('img/assfail.gif', 'rb'), 
                                   caption = msg.finalkilllost(gametime,merlin,thisGame.Players[choice],assassin,'\nWon - @'.join(coolguys),'\nLost - @'.join(badguys)))
        cbq.edit_message_text(text=msg.killfail)
        thisGame.nextstage()

    context.bot.send_message(chatid, msg.gameover)


def checkvote(update, context):
    chatid = str(update.message.chat.id)
    user = str(update.message.from_user.id)
    
    if chatid not in CurrentGames:
        update.message.reply_text(msg.nogame)
        return
    
    thisGame = CurrentGames[chatid]
    if user in thisGame.Players:        
        if bool(thisGame.votetimer):
            waittimev = int(time.time()) - thisGame.votetimer
            if waittimev < 120:
                update.message.reply_text('Please wait 2 minutes before using this function.')
                return
            voters = [key for key, value in thisGame.vote.items()]
            update.message.reply_text('These players have voted:\n'+ '\n'.join(voters)+'\n\n'+'Waiting for: '+str(waittimev)+ ' seconds.\n\n(Check is only available twice per round to avoid flood.)')
            thisGame.checks += 1
            if thisGame.checks >= 2:
                thisGame.votetimer = None
            return

        if bool(thisGame.journeytimer):
            waittimej = int(time.time()) - thisGame.journeytimer
            if waittimej < 120:
                update.message.reply_text('Please wait 2 minutes before using this function.')
                return
            voters = [key for key, value in thisGame.journey.items()]
            update.message.reply_text('These players have voted:\n'+ '\n'.join(voters)+'\n\n'+'Waiting for: '+str(waittimej)+ ' seconds.\n\n(Check is only available twice per round to avoid flood.)')
            thisGame.checks += 1
            if thisGame.checks >= 2:
                thisGame.journeytimer = None
            return
        
        if thisGame.checks in [0,2]:
            update.message.reply_text('Please wait until next selection vote OR mission vote.')


def endgame(update, context):
    chatid = str(update.message.chat.id)
    user = str(update.message.from_user.id)
    if chatid not in CurrentGames:
        update.message.reply_text(msg.nogame)
        return
    if user in CurrentGames[chatid].Players:
        keyboard = [[InlineKeyboardButton(text="END THE GAME", callback_data="EndGame: Yes")],
                    [InlineKeyboardButton(text="NO", callback_data="EndGame: No")]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        if CurrentGames[chatid].status != 3:
            context.bot.send_message(chatid, 'The game has not ended yet. Are you sure?', reply_markup=reply_markup)
        else:
            context.bot.send_message(chatid, 'Thank you for playing. Please support the developer by visiting:\n\n https://www.buymeacoffee.com/fatma0828')
            context.bot.send_message(chatid, 'Thank you for helping with debugging:\n\nOscarIcarus, LongB, PParco, Icy, TobyXpress, TerryBa, Harry420, Soloman', reply_markup=reply_markup)
    else:
        update.message.reply_text("Non-playes cannot end game.")


def clearboard(update, context):
    cbq = update.callback_query
    cbq.answer()
    chatid = str(cbq.message.chat.id)
    choice = cbq.data.split(": ")[-1]
    if choice == "Yes":
        cbq.message.reply_text("Game ending...")
        CurrentGames.pop(chatid)
        cbq.delete_message()
    else:
        cbq.delete_message()
        return
    
    
def rolelist(update, context):
    chatid = str(update.message.chat.id)
    username = str(update.message.from_user.username)
    if username != 'insertadminnamehere':
        update.message.reply_text("This command is for testing only.")
        return
        
    if chatid in CurrentGames:
        if len(CurrentGames[chatid].Roles) < 1:
            update.message.reply_text("No roles assigned yet.")
        else:
            update.message.reply_text("Roles:"+'\n'+'\n'.join(f'{key} {value}' for key, value in CurrentGames[chatid].Roles.items()))
    else:
        update.message.reply_text("There is currently no game in play.")


def main():
    updater = Updater(TOKEN, use_context=True, arbitrary_callback_data=True)
    dp = updater.dispatcher

    dp.add_handler(CallbackQueryHandler(joingame, pattern=dict))
    dp.add_handler(CallbackQueryHandler(playerselection, pattern='Select: '))
    dp.add_handler(CallbackQueryHandler(voteselection, pattern='Vote: '))
    dp.add_handler(CallbackQueryHandler(journeying, pattern='Journey1: '))
    dp.add_handler(CallbackQueryHandler(journeyresult, pattern='Journey2: '))
    dp.add_handler(CallbackQueryHandler(finalkill, pattern='Kill: '))
    dp.add_handler(CallbackQueryHandler(clearboard, pattern='EndGame: '))

    dp.add_handler(CommandHandler("newgame", newgame))
    dp.add_handler(CommandHandler("startgame", startgame))
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("playerlist", playerlist))
    dp.add_handler(CommandHandler("battle", setround))
    dp.add_handler(CommandHandler("endgame", endgame))
    dp.add_handler(CommandHandler("genrules", genrules))
    dp.add_handler(CommandHandler("rolerules", rolerules))
    dp.add_handler(CommandHandler("rolecons", rolecons))
    dp.add_handler(CommandHandler("checkvote", checkvote))
    

    updater.start_webhook(listen="0.0.0.0",
                          port=int(PORT),
                          url_path=TOKEN,
                          webhook_url=WEBHOOKURL + TOKEN,
                          drop_pending_updates=True)
    print("================================")
    print("========= Bot Running ==========")
    print("================================")

    updater.idle()

if __name__ == "__main__":
    main()
