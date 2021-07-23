import os, sys
currentdir = os.path.dirname(os.path.realpath(__file__))
parentdir = os.path.dirname(currentdir)
sys.path.append(parentdir)

from Resources.dungeon import Room, Boss, Dungeon, Treasure, Interactable

def hardMode(user):
    if user.Mainhand == "F-F-F-F-F-F" and user.Offhand == "F-F-F-F-F-F":
        return True
    return False

def checkKey(user):
    curLockout = ""
    lister = user.Lockouts.split(",")
    for i in lister:
        if "DMVC" in i:
            curLockout = i
    if curLockout[17] == "I" or curLockout[17] == "B":
        return True
    return False

def cannonReq(user):
    curLockout = ""
    lister = user.Lockouts.split(",")
    for i in lister:
        if "DMVC" in i:
            curLockout = i
    if curLockout[18] == "I":
        return True
    return False

def VCCheck(user):
    curLockout = ""
    lister = user.Lockouts.split(",")
    for i in lister:
        if "DMVC" in i:
            curLockout = i
    if curLockout[9] == "H" and curLockout[10] == "H" and (curLockout[11] == "H" or curLockout[11] == "S") and curLockout[13] == "H" and curLockout[14] == "H":
        return hardMode(user)
    return False

def noHM(user):
    return False

def noCReqs(user):
    return True

#Boss definition:
rhakazor = Boss({
    "ID": "1",
    "name":"Rhak'azor",
    "level":"19",
    "type":"boss",
    "health":"450",
    "damage":"50-70",
    "loot":{
        "mage":{83:40},
        "rogue":{91:40},
        "warrior":{74:40}
    },
    "lootamount":1,
    "hardmodecheck":hardMode,
    "killquote":"%BOSS Rhahk\'Zor ) strikes you down with his hammer, cackling as he scoffs, \"Is this best heroes can do? Hah!\" \n \nWith that, your run ends. Rest up before trying again!",
    "diequote":"After an intense fight, %BOSS Rhahk'zor ) goes down! He mutters, \"VanCleef not gonna be happy when he find out!\" with his dying breath."
})
johnson = Boss({
    "ID": "2",
    "name":"Miner Johnson",
    "level":"21",
    "type":"rare",
    "chance":"50",
    "suprise":" \n \nSuddenly, a hole opens up in front of you! A rugged, tall miner climbs from the hole and turns to you. \n \nYou now face Miner Johnson. Will you engage him? Or flee and live another day?",
    "health":"550",
    "damage":"52-71",
    "loot":{
        "mage":{1000:100},
        "rogue":{95:40},
        "warrior":{78:40}
    },
    "lootamount":1,
    "hardmodecheck":noHM,
    "killquote":"%BOSS Rhahk\'Zor ) strikes you down with his hammer, cackling as he scoffs, \"Is this best heroes can do? Hah!\" \n \nWith that, your run ends. Rest up before trying again!",
    "diequote":"After an intense fight, %BOSS Rhahk'zor ) goes down! He mutters, \"VanCleef not gonna be happy when he find out!\" with his dying breath."
})
sneed = Boss({
    "ID": "3",
    "name":"Sneed",
    "level":"20",
    "type":"boss",
    "health":"470",
    "damage":"52-70",
    "loot":{
        "mage":{82:40},
        "rogue":{90:40},
        "warrior":{73:40}
    },
    "lootamount":1,
    "hardmodecheck":hardMode,
    "killquote":"As %BOSS Sneed ) cuts you down, you hear him guffaw, \"Who said you couldn't mix business with pleasure? Now get out of my sight, you buffooning oaf!\" \n \nWith that, your run ends. Rest up before trying again!",
    "diequote":"With all the might you can muster, you rip the Shredder to shreds. Sneed squirms as he says, \"VanCleef can't replace me! I'm Sneed! The... \" and with those words, he breathes his last."
})
gilnid = Boss({
    "ID": "4",
    "name":"Gilnid",
    "level":"20",
    "type":"boss",
    "health":"500",
    "damage":"53-71",
    "loot":{
        "mage":{85:40},
        "rogue":{93:40},
        "warrior":{76:40}
    },
    "lootamount":1,
    "cmloot":{
        "mage":{85:70},
        "rogue":{93:70},
        "warrior":{76:70}
    },
    "cmlootamount":1,
    "killquote":"Overwhelmed by harvest golems, you\'re shot down by %BOSS Gilnid ) as he sneers, \"You're no threat to the Brotherhood! Now leave before you're our next weapon rack!\" \n \nWith that, your run ends. Rest up before trying again!",

    "diequote":"Putting up the best fight he can, %BOSS Gilnid ) finally falls as he squawks, \"You\'ll never get to VanCleef! Never! Hahaha...\" and dies..",

    #Hardmode
    
    "hardmodecheck":hardMode,

    "cmodecheck":noCReqs,

    "cmode":"🔴",

    "cmkill":"You fiend! You've got no right pushing the self-destruct button!\" an irate voice howls in the distance. \n \nAs the ceiling begins to crumble around you, the air is getting heavier and heavier. \n \n%BOSS Gilnid ) , furious, gouges you until you can no longer stand. \n \n\"YOU\'VE. GOT. NO. RIGHT. PUSHING. THAT... BUTTON! NEVER COME BACK!\" \n \nWith that, your run ends. Rest up before trying again!",

    "cmdie":"You fiend! You've got no right pushing the self-destruct button!\" an irate voice howls in the distance. \n \nAs the ceiling begins to crumble around you, Gilnid begins to cough as he falls to the ground, unable to breathe. \n \n\"You've... destroyed this place... ruined us all! You\'ll... you'll pay for this! The brotherhood, will... prevail\" he yells before he collapses, lifeless and cold."
})
smite = Boss({
    "ID": "5",
    "name":"Mr. Smite",
    "level":"21",
    "type":"boss",
    "health":"520",
    "damage":"54-71",
    "loot":{
        "mage":{86:40},
        "rogue":{94:40},
        "warrior":{77:40}
    },
    "lootamount":1,
    "hardmodecheck":hardMode,
    "killquote":"After beating you with his incredible arsenal, %BOSS Smite ) simply looks back and spits on you as he walks back on board. \n \nWith that, your run ends. Rest up before trying again!",
    "diequote":"As %BOSS Mr.Smite ) duels you to his final breath, he mutters, \"You landlubbers are tougher than I thought. I should have improvised.\" \n \nHe collapses to the floor, and the way to the dock is cleared."
})
cookie = Boss({
    "ID": "6",
    "name":"Cookie",
    "level":"21",
    "type":"optional",
    "health":"500",
    "damage":"53-71",
    "loot":{
        "mage":{84:40},
        "rogue":{92:40},
        "warrior":{75:40}
    },
    "lootamount":1,
    "hardmodecheck":noHM,
    "killquote":"As %BOSS Cookie ) finishes beating you with his rolling pin, he leaves as a gang of bandits come and finish you off. \n \n\"We\'ll use you as an example to the others.\" one says, as he stabs your throat. \n \nWith that, your run ends. Rest up before trying again!",
    "diequote":"As you quickly defeat %BOSS Cookie ) , you see a band of thugs run towards you. You hide and avoid them, waiting for the area to clear up."
})
vancleef = Boss({
    "ID": "7",
    "name":"Edwin Vancleef",
    "level":"22",
    "type":"boss",
    "health":"600",
    "damage":"58-80",
    "loot":{
        "mage":{79:40},
        "rogue":{87:40},
        "warrior":{70:40}
    },
    "lootamount":1,
    "cmloot":{
        
        "mage":{10000:100,
        81:40},
        "rogue":{10000:100,
        89:40},
        "warrior":{10000:100,
        72:40}
    },
    "cmlootamount":2,
    "killquote":"%BOSS VanCleef ) mercilessly cuts you down with his sabers. \n \nHe turns around and smirks as he says, \"You're the guy that slaughtered my crew? I expected so much more.\" \n \nWith that, your run ends. How pathetic. Rest up before trying again!",
    "diequote":"You strike %BOSS VanCleef ) down with all your might. The head of %BOSS Edwin VanCleef ) rolls around on the floor and off the boat. \n \nThe leader of the Brotherhood is no more.",

    "hardmodecheck":hardMode,

    "cmodecheck":VCCheck,

    "cmode":"👊",

    "cmkill":"%BOSS VanCleef ) mercilessly cuts you down with his sabers. \n \nHe turns around and smirks as he says, \"You're the guy that slaughtered my crew? I expected so much more.\" \n \nWith that, your run ends. How pathetic. Rest up before trying again!",

    "cmdie":"%BOSS Edwin VanCleef ) lay on the floor bloodied, bruised and cold. Amidst the fight, purple shards dropped from his jacket. The Leader of the Brotherhood is no more. The Deadmines have been rid of all evil, Hero, thanks to your stoic bravery."
})
greenskin = Boss({
    "ID": "8",
    "name":"Captain Greenskin",
    "level":"21",
    "type":"boss",
    "health":"550",
    "damage":"54-72",
    "loot":{
        "mage":{80:40},
        "rogue":{88:40},
        "warrior":{71:40}
    },
    "lootamount":1,
    "hardmodecheck":hardMode,
    "killquote":"%BOSS Greenskin ) skewers you with his spear, snickering to himself. \n \n\"What did ye hope to accomplish against the cap'n? Win? Pathetic! To Davy Jones's locker with you, imbecile!\" \n \nWith that, your run ends. Rest up before trying again!",
    "diequote":"As you strike down %BOSS Captain Greenskin ) , he yells \"VanCleef! They, they have... arrived. The cap'n... didn't make it!\""
})

#Treasure definition
treasure1 = Treasure({
    "ID":"1",
    "loot":{
        "mage":{1000:100},
        "rogue":{1000:100},
        "warrior":{1000:100}
        
    },
    "lootamount":1,
    "req": checkKey,
    "success":"Clink! With the key in place, the chest opens wide.",
    "failure":"No matter how much you try to budge it, the chest wont open. It requires a key... maybe there's one somewhere nearby."
})

#Interactable definition
interactable1 = Interactable({
    "ID":"1",
    "name":"Glistening Key",
    "req": noCReqs,
    "success":"In your peripheral vision, you notice a small, glistening key buried in the dirt. You reach for the key and polish it off. \n \nYou picked up the key."
})

interactable2 = Interactable({
    "ID":"2",
    "name":"Defias Cannon",
    "restriction":["forward"],
    "req":cannonReq,
    "success":"3... 2... 1... \n \nKABOOM! The cannon goes off with a roar and the cave quivers.\n \nYou use the gunpowder to blow a hole in the door, opening the way forward.",
    "failure":"You do not have anything to put in the cannon to make it work. Maybe there's something around..."
})

interactable3 = Interactable({
    "ID":"3",
    "name":"Defias Gunpowder Keg",
    "req":noCReqs,
    "success":"You open one of the crates and notice it's filled to the brim with gunpowder. It's heavy, but you can move it if you're careful about it. \n \nYou picked up the Defias Gunpowder Keg"
})

#Room definition
room1 = Room({
    "ID":"1",
    "name":"Strip Miner's Room",
    "description":"The air here is musty, but you proceed into the damp, dark tunnel. \n \nYou notice a small tunnel, on the verge of collapse, on the left. Will you venture forth? Or will you flee and live another day?",

    "forward":"2",
    "left":"9"
})
room2 = Room({
    "ID":"2",
    "name":"Foreman's Office",
    "description":"The clanging of mining picks starts to get louder and louder. An ogre can be heard mercilessly beating squealing Kobolds. \n \nYou finally reach a room with a giant steel door, and the ogre thug guards it. \n \nYou\'re now face-to-face with %BOSS Rhahk\'Zor) , the mining supervisor. Will you engage him? Or will you flee and live another day?",
    "clear":"%BOSS Rhahk'Zor ) now lays dead on the floor. With a mere pull of a lever, the doors behind him creek open. Will you delve further? Or flee and live another day?",
    "boss":rhakazor,

    "forward":"3",
    "back":"1"
})
room3 = Room({
    "ID":"3",
    "name":"Mast Room",
    "description":"After dealing with a some inane lackeys, you look up to a giant mechanical shredder. \n \n\"Keep it quick, kid, I ain\'t got all day! Hey, you don\'t look familiar! Doesn\'t matter, get to chopping wood!\" \n \nYou now face %BOSS Sneed ) , the lumber supervisor. Will you engage him? Or flee and live another day?",
    'clear':"All thats left of the shredder is a corpse and a pile of scrap. A lever behind them opens a big door forward. To it's left, a very steep hole. Will you delve further? Or flee and live another day?",

    "boss":sneed,

    "forward":"4",
    "back":"2",
    "left":"10"
})
room4 = Room({
    "ID":"4",
    "name":"Goblin Foundry",
    "description":"As you exit the lumberyard, you walk into a massive room with lava pouring from the ceiling. \n \nYou can hear a goblin yelling, \"What am I paying you for! Oh, wait, I\'m not paying you. HAHAHAHA! Get back to making VanCleef\'s weapons, you halfwit, or you\'re going to regret it!\" \n \nAs you walk down the spiraling ramp, you happen upon the blacksmith supervisor, %BOSS Gilnid ) . Will you engage him? Or flee and live another day?",
    "clear":"The tinkerer lay dead before you. Behind him, a door leading into a narrow chasm. Will you delve further? Or flee to live another day?",

    "boss":gilnid,

    "forward":"5",
    "back":"3",
})
room5 = Room({
    "ID":"5",
    "name":"Ironclad Cove Enterance",
    "description":"You walk past the tinkerer into the next hallway. A large, iron door stands before you. Try as you might, there's no way to open it. You search around for a lever but there's none to be seen. There sits a cannon facing the door. \n \nMaybe if you had some way to set off the cannon...",
    "clear": "You walk into the hallway before you. Where once stood an impenetrable gate now lies a massive hole. The door's been blasted and the way through is clear.",
    "interactable":interactable2,

    "forward":"6",
    "back":"4",
    "left":"11"
})
room6 = Room({
    "ID":"6",
    "name":"Ironclad Cove",
    "description":"Exiting the forge, you walk onto a dock. In the distance, you see a ship. \n \nA deep, commanding voice roars, \"We\'re under attack! A vast, ye swabs! Repel the invaders!\" \n \nStanding at the ramp to the boat, you’re greeted by a massive Tauren. \n \nYou\'re now facing %BOSS Mr.Smite ) , VanCleef\'s deckhand. Will you engage him? Or flee and live another day?",
    "clear":"The tauren lay bruised and beaten on the floor, his arsenal spread around him. Before you lies a ramp onto the massive ship. You can keep heading forward, or take a narrow opening to the left. Will you delve further? Or flee and live another day?",

    "boss":smite,

    "forward":"7",
    "back":"5",
    "left":"12"
})
room7 = Room({
    "ID":"7",
    "name":"Juggernaut Middle",
    "description":"As you clear the path to the top of the ship, you hear a parrot squawk, \"Intruders! Intruders! RAAWK!\" \n \nA goblin mutters as he walks over to you with his crew, now at the top of the ship. \n \n\"You dare step foot on my ship? I\'ll have you skinned!\" \n \nThe goblin pulls out his spear and charges. \n \nYou now face %BOSS Greenskin ) , captain of the Deadmines. Will you engage him? Or flee and live another day?",
    "clear":"The captain lay dead, his parrot and crew nowhere to be found. A single ramp leads to the very top of the ship, and two ramps to the bottom left of the ship. Will you delve further? Or flee and live another day?",

    "boss":greenskin,

    "forward":"8",
    "back":"6",
    "left":"12"
})
room8 = Room({
    "ID":"8",
    "name":"Juggernaut Top",
    "description":"You\'re finally at the very top of the ship, you see a shadowy figure step out of the captain\'s quarters. \n \n\"None may challenge the Brotherhood, least of all you. You won\'t stop this operation or the Brotherhood. None shall defeat the Brotherhood!\" he sneers. \n \n\"You\'ve slaughtered my entire crew, it\'s time I stake you through the heart!\" \n \nYou now stand face-to-face with %BOSS Edwin VanCleef ) , leader of the Defias Brotherhood. Will you engage him? Or flee and live another day?",
    "clear":"The leader of the brotherhood lay there atop his ship. You look around, the air rings hollow. The Deadmines have been rid of all evil, Hero, thanks to your stoic bravery.",
    "boss":vancleef,

    "back":"7",
    "forward":"13"
})
room9 = Room({
    "ID":"9",
    "name":"Miner's Stash",
    "description":"Going deep into the tunnel, you see a stash of valueables at the end. Atop the throne of ore lays a solid, wooden chest. It's too heavy to lift or drag.",
    "clear":"Going deep into the tunnel, you see a stash of valueables at the end. The wooden chest above has been opened, and all it's valueables taken from it.",
    "treasure":treasure1,
    "right":"1"
})
room10 = Room({
    "ID":"10",
    "name":"Miner's Hideaway",
    "description":"You enter the extremely narrow and steep cave and fall down to the bottom of it. This seems to be an abandoned mineshaft, as there are no miners around.",

    "boss":johnson,
    "interactable":interactable1,

    "right":"3"
})
room11 = Room({
    "ID":"11",
    "name":"Gunpowder Stash",
    "description":"You turn to the left of the cannon and into a small bend in the cave system. You walk into a heavily reinforced room, surrounded by barrels and crates.",

    "interactable":interactable3,

    "right":"5"
})
room12 = Room({
    "ID":"12",
    "name":"Juggernaut Lower",
    "description":"Walking on board, you\'re quickly greeted with the sound of rushing footsteps and chaotic shouting. \n \nYou hear a murloc gurgling in the distance. Could it be? %BOSS Cookie ) and his gang have caught up to you! \n \n\"Mrglgrglglrlgl!\" he says, with a rolling pin in hand. \n \nYou now face %BOSS Cookie ) , the chef of the Brotherhood. Will you engage him? Or flee and live another day?",
    "clear": "The chef and his miscreants are nowhere to be found. The ships lower half has been evacuated. Before you stands the ramp back off the ship and a ramp to go higher.",
    "boss":cookie,

    "right":"6",
    "left":"7"
})
room13 = Room({
    "ID":"13",
    "name":"Westfall",
    "description":"You leap off the ship and crawl through a narrow cave. On the other end of it, rays of sunlight begin to fill the cave. As you step out, you are blinded by the light. You step into Westfall, the breeze hitting your face, your eyes adjusting to the light. You have rid Westfall of a great threat this day. \n \nWith that, your adventure comes to an end.",
})

#Linking rooms together
room1.forward = room2
room1.left = room9

room2.forward = room3
room2.back = room1

room3.forward = room4
room3.back = room2
room3.left = room10

room4.forward = room5
room4.back = room3

room5.forward = room6
room5.back = room4
room5.left = room11

room6.forward = room7
room6.back = room5
room6.left = room12

room7.forward = room8
room7.back = room6
room7.left = room12

room8.back = room7
room8.forward = room13

room9.right = room1

room10.right = room3
room11.right = room5
room12.right = room6
room12.left = room7