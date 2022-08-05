#roles
merlin = 'Merlin'
assassin = 'Assassin'
morgana = 'Morgan'
percival = 'Percival 西瓜人'
mordred = 'Mordred 佛地魔'
goodguy1 = 'Chris Wong Useless'
goodguy2 = 'Son of Hugo Useless'
oberon = 'Oberon Parco'
goodguy3 = 'Leo the Moral'
goodguy4 = 'J-420'
badguy1 = 'Evil Oscar'

#desc
roledesc = {mordred: "\U0001F47D You are a bad guy who Merlin\U0001F9D9 does not see",
            assassin: "\U0001F52A You are a bad guy who decides who to kill should the good guys succeed in passing 3 quests",
            morgana: "\U0001F52E You are a bad guy that appears as Merlin to Percival\U0001F349",
             oberon: "\U0001F921 You are a bad guy that other bad guys do not know about",
            badguy1: "\U0001F47B You are a standard bad guy. Sad. Hope you have stando power.",
             merlin: "\U0001F9D9 You can see bad guys. If the Assassin\U0001F52A guesses who you are at the end of the game, good guys lose.",
           percival: "\U0001F349 You know who Merlin is (Morgana\U0001F52E also appears as Merlin\U0001F9D9)",
           goodguy1: "\U0001FAB4 You are a good guy, but useless. Sad.",
           goodguy2: "\U0001FAB4 You are a good guy, but useless. Why u no smarter?",
           goodguy3: "\U0001FAB4 You are a good guy. R U moral?",
           goodguy4: "\U0001FAB4 You are a good guy. Weed is gd."}

#lists
coolguys = [merlin, percival, goodguy1, goodguy2, goodguy3, goodguy4]
badguys = [assassin, morgana, mordred, oberon, badguy1]

#rules
genrules = """Game Rules:

0. DO NOT FORWARD PRIVATE BOT MESSAGES DURING A GAME
1. There are 2 parties: \U0001F9E0 Good guys & \U0001F9DF Old ghosts
2. All players will go through 5 Missions \U00002694 
3. Good guys win IF 3 Missions are SUCCESS \U00002714\U00002714\U00002714 and Merlin is not killed \U0001F9D9
4. Old ghosts win IF 3 Missions are FAILURE \U0000274C\U0000274C\U0000274C OR if the Assassin correctly guesses who is Merlin in the end \U0001F52A\U0001F9D9
5. Each turn, a leader \U0001F9D4 will pick members to go on a Mission \U00002694
6. All players vote \U0001F5F3 if they allow this team (Accepted only if Yes \U00002705 votes are MORE than half)
7. Team members secretly vote if the Mission is SUCCESS \U00002714 or FAILURE \U0000274C
8. In most Missions, 1 FAILURE vote \U0000274C will result in FAILURE \U0000274C, except for Round 4 in a 7-or-more-player game (needs 2 FAILURE votes)"""

rolerules = """Roles:
\U0001F9E0 Good guys - \U0001F9D9 Merlin: You can see all bad guys EXCEPT Mordred. If you are picked by the Assassin, your team will lose.
\U0001F9E0 Good guys - \U0001F349 Percival: You can see Merlin and Morgana, but you do not know which is which.
\U0001F9E0 Good guys - \U0001FAB4 Others: No special powers. Try to mislead bad guys by pretending to be Merlin.
\U0001F9DF Bad guys - \U0001F52E Morgana: You look like Merlin to Percival.
\U0001F9DF Bad guys - \U0001F52A Assassin: You can choose 1 good guy to kill in the end. If it is Merlin, you win.
\U0001F9DF Bad guys - \U0001F47D Mordred: Merlin cannot see you.
\U0001F9DF Bad guys - \U0001F921 Oberon: Your fellow bad guys cannot see you.
\U0001F9DF Bad guys - \U0001F47B Others: No special powers. Try to mislead and help your team get FAILURE votes."""

rolecons = """Role constituion:
5-Player games - 3 vs 2 \U0001F9E0\U0001F9E0\U0001F9E0 \U0001F9DF\U0001F9DF
Basic: Merlin, Percival, Good Guy1, Morgana, Assassin

6-Player games - 4 vs 2 \U0001F9E0\U0001F9E0\U0001F9E0\U0001F9E0 \U0001F9DF\U0001F9DF
Basic + Good Guy 2

7-Player games - 4 vs 3 \U0001F9E0\U0001F9E0\U0001F9E0\U0001F9E0 \U0001F9DF\U0001F9DF\U0001F9DF
Basic + Mordred + Good Guy2

8-Player games - 5 vs 3 \U0001F9E0\U0001F9E0\U0001F9E0\U0001F9E0\U0001F9E0 \U0001F9DF\U0001F9DF\U0001F9DF
Basic + Mordred + Good Guy2 + Good Guy3

9-Player games - 6 vs 3 or 5 vs 4
\U0001F9E0\U0001F9E0\U0001F9E0\U0001F9E0\U0001F9E0 ←(\U00002754)→ \U0001F9DF\U0001F9DF\U0001F9DF
Basic + Mordred + Good Guy2 + Good Guy3 + (25% chance) Good Guy4 OR (75% chance) Oberon

10-Player games - 6 vs 4 \U0001F9E0\U0001F9E0\U0001F9E0\U0001F9E0\U0001F9E0\U0001F9E0 \U0001F9DF\U0001F9DF\U0001F9DF\U0001F9DF
Basic + Modred + Good Guy2, 3, 4 + Oberon
"""
