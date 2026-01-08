import random
import time
import psutil
import os

rooms = [
    {
        # 0; Beginning room, ACT 1: SCENE 1
        "description": "“You are, and forever will be, unfinished…”\n\n"
        "You wake up from a nightmare, sitting straight up in your bed. Your skin is slicked with sweat, and your heart pounds in your chest.\n\n"
        "You can't recall the specific details of the nightmare.\n\n"
        "\tYOU: It was just a nightmare...\n\n"
        "The bed is pushed to the center of the back wall. There's a window to your right covered by curtains, and the door remains closed to your far left."
        " Just beside the door are the closet doors that also remain shut. There's nothing else in the room for you to note.",
        "actions": ["Look out the window", "Look in the closet", "Head out the room"],
    },
    {
        # 1; Look out the window
        "description": "You slowly stride towards the window. You reach forward and push aside the curtains,"
        " squinting against the harsh light of the sun. It sits above the horizon, ready to encase the suburban neighborhood in darkness."
        " Many replicas of your house adorn the streets, but there's nothing important to note.",
        "actions": ["Look in the closet", "Head out the room"],
    },
    {
        # 2; Look in the closet
        "description": "You move to the closet, opening the doors. It's bare of any clothes; the bottom of the closet is empty,"
        " but there remains only one jacket in a hanger.",
        "actions": ["Take the jacket", "Look out the window", "Head out the room"],
    },
    {
        # 3; Take the jacket
        "description": "You pick up the jacket and discard the hanger, pulling it over your arms and shrugging it over your shoulders."
        " The jacket is worn but comfortable, calming you down from the lingering anxiety of my nightmare.",
        "actions": ["Search the jacket", "Look out the window", "Head out the room"],
    },
    {
        # 4; Search the jacket
        "description": "In the jacket pockets, you find a pack of untouched cigarettes.",
        "actions": ["Look out the window", "Head out the room"],
    },
    {
        # 5; Head out the room
        "description": "You move to the door with dragging feet, opening the door and revealing the hallway.\n\n"
        "Your bedroom is the last door at the end of this hallway, revealing two more doors, one on the right and one on the left, before the hall reveals"
        " the living room. The wallpaper is yellowed and peeling, bare of any decorations. Stains of unknown origin are all that greets you, colored in a washed,"
        " deep red and what looks like soot.",
        "actions": [
            "Open the door on the right",
            "Open the door on the left",
            "Enter the living room",
            "Go back to the room",
        ],
    },
    {
        # 6; Door on the right
        "description": "You walk to the door on the right, and upon opening the door, you reveal a small bathroom with a single sink, toilet, and a bathtub and shower"
        " combination. Stepping into the bathroom, you look in the mirror.\n\nYou look tired with dark bruises underneath your eyes. Turning the faucet on, the"
        " water pressure is minimal yet still clean-looking, and you pool water in your cupped hands, splashing it against your face.",
        "actions": ["Search the bathroom", "Go back to the hallway"],
    },
    {
        # 7; Search the bathroom
        "description": "The only thing you can find are ashes littered amongst the countertop of the sink and the small, lone window just above the toilet."
        " There is nothing else left to note.",
        "actions": ["Go back to the hallway"],
    },
    {
        # 8; Door on the left
        "description": "You move to the door on the left, revealing a small office. There's one window with the burned remains of a curtain barely hanging to the mantle."
        " It only blocks the top of the window with scraps creating a silhouette in the barren office. A desk made of what once was wood is simply charcoal, standing"
        " on a husk of itself. The stench of the office is enough to make your eyes water and your nose burn.",
        "actions": ["Search the office", "Go back to the hallway"],
    },
    {
        # 9; Search the office, take the piece of burned picture?
        "description": "You take a few steps towards the desks and notice a few picture frames. Its contents are burned just like its living area, but you notice"
        " that there's only one frame that holds a piece of a picture that's burned at the edges.\n\n"
        "Do you take the piece of burned picture?",
        "actions": ["Yes", "No"],
    },
    {
        # 10; Yes, take the piece of burned picture?
        "description": "You carefully peel away the edges of the picture frame and manage to pick up the remaining burned piece of the picture. It"
        " seems to have split into one corner of the rectangular picture. The picture is of the bottom left part of the frame, showing the legs of two children and two"
        " adults.",
        "actions": ["Go back to the hallway"],
    },
    {
        # 11; No, take the piece of burned picture?
        "description": "You leave the burned picture alone, deciding it isn't worth your curiosity.",
        "actions": ["Go back to the hallway"],
    },
    {
        # 12; Enter the living room
        "description": "You travel down the hall into the living room, surveying how you left the state of the place. There isn't anything you remember leaving behind.\n\n"
        "\tYOU: Damn, guess I forgot to clean up. It's messy around here.\n\n"
        "The couch is covered in soot, and the windows are all bare of their curtains. The walls are blackened with a substance.\n\n"
        "\tYOU: I could never get those stains to come out... Dunno what it is.\n\n"
        "Adorning the walls are burned picture frames whose contents are blurred or burned or smudged away.\n\n"
        "\tYOU: Could never remember what they were.\n\n"
        "Beside the couch is the door that leads to the backyard with a glass sliding door, revealing a treeline that seemingly features an endless sea of trees."
        " There is another archway that leads into the kitchen.",
        "actions": [
            "Go to the kitchen",
            "Go to the backyard",
            "Go back to the hallway",
        ],
    },
    {
        # 13; Go to the kitchen
        "description": "The kitchen is bare like the rest of the house with only an empty sink, an empty fridge, and empty walls to greet you. Connected to the"
        " kitchen is the front door.",
        "actions": [
            "Search the kitchen",
            "Head outside and into town",
            "Go back to the living room",
        ],
    },
    {
        # 14; Search the kitchen
        "description": "The kitchen has bags full of trash littering the floor and mounds of ash cover the window sills and sink. It strangely doesn't smell"
        " like anything.\n\n"
        "\tYOU: Wonder if my sense of smell finally got snuffed out.\n\n"
        "The dining table is directly connected to the kitchen. You notice that it has a broken piece of glass where a picture frame sits.",
        "actions": ["Head outside and into town", "Go back to the living room"],
    },
    {
        # 15; Go to the backyard
        "description": "You decide to head outside, cringing a bit at the whining noise of the sliding back door. You step into your shoes and walk towards the"
        " treeline where there seems to be dense woods bordering the edge of the backyard. It's full and darkens a few mere feet into the treeline. You feel uneasy"
        " staring into the woods and don't wish to step any further.\n\n"
        "You turn around to head back into the house, but you stop to view it. For a moment, you smell smoke burning your nostrils, making you sneeze. When you look"
        " up again, the house seems to be in okay condition. It feels like nothing is out of sorts.\n\n"
        "\tYOU: I wonder what that was...",
        "actions": ["Go back to the living room"],
    },
    {
        # 16; Head outside and into town
        "description": "You head to the front door, grab your keys hanging on the key holder beside it, and go outside. You survey the small"
        " suburban neighborhood where replicas of your own house are repeated throughout the whole street.\n\n"
        "\tYOU: Weird. There's usually kids screaming outside at this hour.\n\n"
        "The whole neighborhood is quiet, and it makes you feel on edge, like something is wrong, yet you can't put your finger on it. You shake the feeling off"
        " as best as you can and head to your SUV, deciding to drive downtown.\n\n"
        "You head downtown, either for the drive itself or if you're looking for anything in particular to catch your eye. The downtown area is rather small"
        " and only holds a few local shopping places, restaurants, and a library. There's also a church where most of the town gathers on Wednesdays or Sundays,"
        " not that you personally attend.",
        "actions": ["Explore the town", "Go to the church"],
    },
    {
        # 17; Explore the town
        "description": "You park your car and look through the windows of the shops, noticing how none of them are open or accessible. Eventually, you find an"
        " old newspaper clipping on a nearby table. The newspaper article talks about one of the houses in your neighborhood burning down.\n\n"
        "Pick up the newspaper article?",
        "actions": ["Yes", "No"],
    },
    {
        # 18; Yes, pick up the newspaper article?
        "description": "You decide to take the newspaper clipping, stuffing it in your pocket. It resonates with you deeply somehow, and you wonder if the residents"
        " of the house are okay.",
        "actions": ["Go back to the town square"],
    },
    {
        # 19; No, pick up the newspaper article?
        "description": "You don't give the newspaper clipping another thought, turning away.",
        "actions": ["Go back to the town square"],
    },
    {
        # 20; Go to the church
        "description": "You then come upon the church with its lights on, and on the porch, you spot a woman in a wedding dress whose face is obscured by Her veil."
        " She seems to have pale skin underneath Her white dress, and no matter what angle you perceive Her in, you cannot see Her face.\n\n"
        "\tYOU: Hey there, miss... Are they... holding a wedding today?\n\n"
        "\tHER: Hello...\n\n"
        "She says your name, much to your surprise.\n\n"
        "\tYOU: How do you know my name?\n\n"
        "You don't recognize Her.\n\n"
        "\tHER: You simply seem like one...\n\n"
        "\tHER: No, there's no wedding today.\n\n"
        "\tYOU: What's with the dress then? If you don't mind me asking.\n\n"
        "She softly chuckles.\n\n"
        "\tHER: It's simply a fashion choice. How have you been lately?\n\n"
        "You don't notice the subject change.\n\n"
        "\tYOU: I... Well, to be honest, I've been pretty tired lately. I don't know why though.\n\n"
        "\tHER: Is it something personal? Or more of a workplace thing?\n\n"
        "You feel like this woman is familiar, someone to be trusted. Her voice is soft and soothing, and you find conversing with Her easy.\n\n"
        "\tYOU: I think it might be more of a personal thing.\n\n"
        "\tHER: I see… Have you thought about finding solace in your community?\n\n"
        "You look at the church with a skeptical expression. You purse your lips and try to remain as cordial as possible.\n\n"
        "\tYOU: If you mean religion, I'm afraid I'm not very religious. I don't… I don't really believe in God, ma'am.\n\n"
        "She laughs, though it doesn't seem like She moves much at all.\n\n"
        "\tHER: That's fine...\n\n"
        "She says your name again, and you feel more comfortable around Her.\n\n"
        "\tHER: Humor me a little... Join me in the church?",
        "actions": ["Yes", "No"],
    },
    {
        # 21; Yes, go to the church
        "description": "You decide to humor Her and help Her up from Her seat, guiding them into the church. The interior of the church is simple and homely,"
        " a sight that you haven't seen much of at all. It's built of wood and beams with benches laying before the altar where you suppose a priest or"
        " father would be holding a sermon.\n\n"
        "You sit with the woman on one of the benches in the middle of the floor.\n\n"
        "\tHER: What about your personal life has you so weighed down?\n\n"
        "You take a moment to think about your answer."
        # No actions needed, IF HAVE ITEMS or IF NOT HAVE ITEMS
    },
    {
        # 22; No, don't go to the church
        "description": "Even if you feel safe and comfortable around Her, you decide against it. You don't like it when people push you to do things you don't want"
        " to do.\n\n"
        "\tYOU: On second thought... I'm sorry, ma'am, but I'm not very comfortable with that.\n\n"
        "For a moment, you see something underneath the veil that makes the air tense and uncomfortable. Flashes of something horrible come to mind, and your"
        " stomach sinks; a feeling of dread washes over you, and you take numerous steps back from Her. Belatedly, you realize, it's because of Her.\n\n"
        "\tHER: Well then... That's a decision I didn't think you'd take.\n\n"
        "Her voice is dangerously low, and you feel the need to scream.\n\n"
        "You don't get the chance to.\n\n"
        "Everything goes black."
        # No actions needed, END OF GAME
    },
    {
        # 23; THE RED CHAPEL, ACT 2: SCENE 1
        "description": "You venture into the woods, following the trail She mentioned. You bring a flashlight with you because of how dark the dense forest clouds"
        " out the moonlight as the sun sat well below the horizon when you made it back to your home. The temperature in the woods is cold, making you shiver as you"
        " clutch the flashlight in your hand even tighter.\n\n"
        "The trees in the woods are oak, that much you know, but oak trees should have a brown color. The trees you see are completely black, devoid of color, and"
        " you don't remember how long you've been walking on the trail at this point.",
        "actions": ["Take a break"],
    },
    {
        # 24; Success chance
        "description": "Feeling tired, you take a moment to stop and stretch your limbs above your head, yawning wide, causing you to close your eyes. For a second,"
        " adrenaline courses through your veins as your eyes are taken off of the trail, and you try your best to keep calm.\n\n"
        "\tYOU: *There's no way I could possibly wander off the trail when I know it continues straight, right?*\n\n"
        "You open your eyes again and stop in your tracks, holding your breath, pressing the butt of your flashlight against your chest.\n\n"
        "\tYOU: *Did I wander off the trail?*\n\n"
        "In front of you is a small building, and you look up to see the steeple, noticing the cross planted on top of it.\n\n"
        "\tYOU: *Even I know that God would question the looks of this place. I don't know what I was expecting, but it wasn't this.*\n\n"
        "The chapel is red as She has described, but you can't tell if it's really red or if it's because of the light hanging on the front of the building illuminating"
        " the area. The color is so vibrant and saturated that it swallows any chance for another color to break through. Around where the chapel is placed, the light at"
        " the front illuminates the clearing with its red color, but the ground doesn't reflect the light. All you see is a void.\n\n"
        "You remind yourself that there is ground beneath you and take a few steps forward. You raise your flashlight, noticing how its yellow color gets consumed"
        " by the red light. With no point in keeping it on, you turn it off and tuck it away. In a few more strides, you're under the lights of the chapel, just in"
        " front of the door.\n\n"
        "Before you can reach for it, it slowly opens by itself.",
        "actions": ["Enter the church", "Wait for an invitation", "Turn away"],
    },
    {
        # 25; Fail chance
        "description": "Feeling tired, you take a moment to stop and stretch your limbs above your head, yawning wide, causing you to close your eyes. For a second,"
        " adrenaline courses through your veins as your eyes are taken off of the trail, and you try your best to keep calm.\n\n"
        ". . .\n\n"
        ". . .\n\n"
        "You can't see anything.\n\n"
        "All that's in front of you is void. Not even the light from your flashlight can penetrate the veil of darkness that has consumed you.\n\n"
        "Faintly, you hear a low growl right next to your ear. Your heart races, and your brain is stuck between wanting to scream and run.\n\n"
        ". . .\n\n"
        "The choice is made for you..."
        # No actions needed, END OF GAME
    },
    {
        # 26; Enter the church
        "description": "\tHER: You made it. Come on in.\n\n"
        "You enter the chapel a little wearily, quickly surveying your surroundings. There's a light inside, but you aren't expecting it to be a white"
        " light in contrast to the red light outside the door.\n\n"
        "\tHER: I wasn't expecting you to come so soon. Got some things to get off your chest?\n\n"
        "You give a mixture of a sigh and a laugh.\n\n"
        "\tYOU: I... don't know. You said something about redemption, and even though I never mentioned it...\n\n"
        "You trail off, unsure of where you meant to go with your words.\n\n"
        "\tYOU: But I'm here anyway, seeking redemption, as you put.\n\n"
        "You look up at Her where She stands atop the elevated stage at the front of the chapel. Her back is turned to you.\n\n"
        "At first, She says nothing in response. A noise erupts from Her figure, similar to a quaint giggling.\n\n"
        "\tHER: Let's talk.\n\n"
        "You don't mind going back to talking with the woman.\n\n"
        "\tHER: Tell me about yourself.\n\n"
        "You don't know why you give in. It's not like you're hiding something; it's not like you have anything to hide... Right?\n\n"
        "As you prepare yourself, you take a deep breath to begin explaining but promptly close it upon one simple thing: you... can't quite remember."
        # No actions needed, IF HAVE ITEMS or IF NOT HAVE ITEMS
    },
    {
        # 27; Wait for an invitation
        "description": "Despite the door opening by itself, you wait outside the chapel a little wearily. Since you've never really been into religion,"
        " especially any that fall under Christianity, you feel like you may be offending God or otherwise by intruding. It's not that you even mean to"
        " intrude. As always, religion tends to make you so flighty in response. You're not sure how to move on.\n\n"
        "Just then, you hear a soothing voice say your name. Confused, you lift your head towards the still open door, and you hear your name being"
        " repeated once more. You then recognize that it's Her calling out to you. Her mere voice makes you feel calm at once.\n\n"
        "\tHER: There's no need to wait. Come on in...\n\n"
        "You enter the chapel a little more confidently now that you have explicit permission, and you quickly survey your surroundings. There's a light"
        " inside, but you aren't expecting it to be a white light in contrast to the red light outside the door.\n\n"
        "\tHER: I wasn't expecting you to come so soon. How are you faring?\n\n"
        "You let out an exhausted sigh.\n\n"
        "\tYOU: I... I'm not entirely sure, to be honest. I just feel really tired, and...\n\n"
        "You pause, frowning slightly. Your heart feels heavy again, and you raise your hand to rub at the space just above your heart. You then remember what"
        " She said earlier in the day.\n\n"
        "\tYOU: Redemption.\n\n"
        "After saying that out loud, your heart feels a little lighter. That makes the most sense. She tends to always make sense, somehow.\n\n"
        "You become silent and lift your head to look up at Her where She stands atop the elevated stage at the front of the chapel. She is facing you,"
        " and you get the vague impression that she's smiling lightly.\n\n"
        "\tHER: You've come a long way. Why don't you tell me about yourself?\n\n"
        "You don't mind talking with the woman. You don't know why you give in either. It's not like you're hiding something; it's not like you have something"
        " to hide... Right?\n\n"
        "As you prepare yourself, you take a deep breath to begin explaining but promptly close it upon one simple thing: you... can't quite remember."
        # No actions needed, IF HAVE ITEMS or IF NOT HAVE ITEMS
    },
    {
        # 28; Turn away
        "description": "Suddenly, you don't feel good about this. Despite the door being open, you shake your head and turn around, taking a step forward."
        " You expect your feet to touch the ground, void of anything at all, like before, but you're taken by surprise when nothing meets your feet. You fall"
        " forward with a yelp, throwing your hands out in an attempt to catch your fall, but nothing stops you.\n\n"
        ". . .\n\n"
        "You don't know how long you've been falling for.\n\n"
        "You don't know if you're still falling.\n\n"
        "You just want it all to end...\n\n"
        "And it does."
        # No actions needed, END OF GAME
    },
    {
        # 29; Step out of the RED CHAPEL, ENTER ACT 2: SCENE 2
        "description": "You raise your hands to shield your eyes from the sudden shift in the colors, brightness, and temperature. You hear the door close behind you,"
        " making you jump and turn around, only to find that the RED CHAPEL is gone. You are standing at the edge of the beginning of the trail, and a shiver runs down"
        " your spine as you look at the border of the woods.",
        "actions": ["Walk forward", "Turn back around"],
    },
    {
        # 30; Walk forward
        "description": "Sighing, you survey your surroundings and take in all that you can. You had to have been in the woods for the full night considering the time you"
        " first left. Your journey isn't long; exiting the Red Chapel immediately brings you upon the red hills.\n\n"
        "You climb the hill and see the WHITE CHAPEL in the distance, crowded by a sea of red flowers that are stringy and look like spiders. To your surprise, there's"
        " another trail for you to take, and it guides you to the White Chapel nested in the red hill.\n\n"
        "You frown as the cobblestone trail blends with the ground, looking up at the tall building as you come closer to it. There's a cross in the front of the White"
        " Chapel rather than at the back like the Red Chapel.",
        "actions": ["Enter the church", "Wait for an invitation", "Turn away"],
    },
    {
        # 31; Turn back around
        "description": "You think back on Her words, and you wrench your lips into a frown. You don't want to do this. You don't want to keep doing this.\n\n"
        "For a moment, you fear that you don't have the strength to continue.\n\n"
        "You feel weak as you turn around; your stomach grumbles as you begin to feel queasy.\n\n"
        "For some reason, you feel lightheaded as you begin trekking back into the dark forest in hopes of... something. You're not sure what.\n\n"
        "You barely make it past the treeline before you pass out.\n\n"
        ". . .\n\n"
        "Why don't you try again? Surely, you'll be strong enough the next time 'round."
        # No actions needed, END OF GAME
    },
    {
        # 32; Enter the church
        "description": "You walk up to the doors, expecting it to open on its own like last time, but it doesn't. You kick the door open,"
        " shoving your shoulder into the door to open it wider as you stumble through the interior.\n\n"
        "You don't see Her here, but the layout of the interior of this chapel is the same as the RED CHAPEL. You hurry over to take a seat at one of the benches,"
        " spreading your legs wide and stretching them far to give them time to rest. You let out a grunt of relief, digging through your pocket for the pack of"
        " cigarettes you're suddenly craving for."
        # No needed actions, IF HAVE ITEMS or IF NOT HAVE ITEMS
    },
    {
        # 33; Wait for an invitation
        "description": "You walk up to the doors, half expecting it to open on its own like last time, but when it doesn't, you feel a little silly. You duck your head"
        " and push open the door with the needed force, cautiously stepping inside.\n\n"
        "You take a look at the interior, noticing how similar it is compared to the Red Chapel. You don't see Her here, so you slowly walk over to one of the benches"
        " in the middle of the floor, gently sitting down."
        # No needed actions, IF HAVE ITEMS or IF NOT HAVE ITEMS
    },
    {
        # 34; Turn away
        "description": "No.\n\n"
        "N O.\n\n"
        "You can't do this.\n\n"
        "This isn't you.\n\n"
        "\tYOU: Fuck this!\n\n"
        "Panicked, you run away from the White Chapel, but you trip on the bed of flowers in the field.\n\n"
        "It feels like spiders are crawling all over you, and you yell out in panic, scrambling your limbs around to get whatever it is off.\n\n"
        ". . .\n\n"
        "It is a fruitless endeavor.\n\n"
        ". . .\n\n"
        "The spider lillies have reclaimed another lost soul."
        # No needed actions, END OF GAME
    },
    {
        # 35; Deny your fate
        "description": "\tYOU: No, no, no...\n\n"
        "You plead under your breath.\n\n"
        "You don't want this.\n\n"
        "You never wanted this.\n\n"
        "\tYOU: Please, stop, stop...\n\n"
        "Something looms above you, causing you to involuntarily hold your breath.\n\n"
        "\tHER: What... a... SHAME.\n\n"
        "You feel the bones in your neck cracking from some pressure. It is quick.\n\n"
        "But not painless."
        # No needed actions, END OF GAME
    },
    {
        # 36; Step out of the WHITE CHAPEL, BLACK CHAPEL ACT 2: SCENE 3
        "description": "Your lungs breathe in and out to take in the fresh air..."
        # No needed actions, IF HAVE ITEMS or IF NOT HAVE ITEMS
    },
    {
        # 37; ACT 3
        "description": "You wake up from a nightmare, sitting straight up in your bed. Your skin is slicked with sweat, and your heart pounds in your chest.\n\n"
        "You can't recall the specific details of the nightmare.\n\n"
        "“You are, and forever will be, unfinished…”"
        # No needed actions, END OF GAME
    },
    {
        # 38; White Chapel have items actions
        "actions": ["Accept your fate", "Deny your fate"]
    },
]

church_have_items = {
    "have": "\tYOU: I… I feel like I'm missing something. It hurts here.\n\n"
    "You pat your chest right above where your heart lays. It makes you sad and uncomfortable that you don't know the reason why you feel so tired.\n\n"
    "You then look up at Her and have a vague feeling She's giving you a knowing look despite being unable to see Her face.\n\n"
    "\tHER: Perhaps you are here for something a bit deeper.\n\n"
    "You give Her a confused look.\n\n"
    "\tYOU: What do you mean?\n\n"
    "\tHER: Perhaps you are looking for redemption.\n\n"
    "You go silent again as you contemplate what She means. As you speak, you sound a bit hesitant, a bit scared.\n\n"
    "\tYOU: Why… Why would I be looking for redemption?\n\n"
    "\tHER: Perhaps this church cannot offer what you currently seek.\n\n"
    "It makes sense to you that you are searching for something, yet you do not know what.\n\n"
    "\tHER: Visit the red chapel in the black woods. Perhaps you can seek redemption there. Be wary. Don't wander away from the trail; you will get lost."
    " There are things in those woods that you don't want to see. Be careful.\n\n"
    "She says this in a soft tone that it was almost mesmerizing for you to hear.\n\n"
    "\tYOU: Will I see you at this red chapel?\n\n"
    "\tHER: Perhaps...\n\n"
    "\tYOU: I'll get to it then.",
    "have not": "\tYOU: I… I don't know. I can't say, it's… it's not coming to me.\n\n"
    "You frown and lean back into the bench a little, searching desperately in your head for a possible reason. You then look back at the woman and have"
    " the vague feeling that She's frowning at you despite being unable to see Her face.\n\n"
    "\tHER: Perhaps… you are here for something deeper.\n\n"
    "Her voice is a little darker, surprising you.\n\n"
    "\tYOU: What do you mean?\n\n"
    "\tHER, RESOLUTELY: Perhaps you are looking for redemption.\n\n"
    "This doesn't make sense to you.\n\n"
    "\tHER: Visit the red chapel in the black woods. Perhaps you can seek redemption there. Don't wander away from the trail; you will get lost. There are"
    " things in those woods that you don't want to see.\n\n"
    "Despite Her earlier tone, it is now soft and mesmerizing for you to hear.\n\n"
    "\tYOU: Will I see you at this red chapel?\n\n"
    "\tHER: Perhaps...\n\n"
    "\tYOU: I'll get to it then.",
}
redchapel_have_items = {
    "have": "\tYOU: I... I have a family.\n\n"
    "You don't quite remember them, but you dig in the pockets of your jacket, finding the NEWSPAPER CLIPPING and 1/3 OF BURNED PHOTO. They help ground you.\n\n"
    "\tYOU: I worked pretty late a lot of times, so I think... I think I didn't get to be in my children's life as much as I wanted to be.\n\n"
    "You frown at what you say, upset with yourself. You think that's a shame on your part.\n\n"
    "\tHER: My partner... I think... I think my partner was upset with me. I tried my best, I believe.\n\n"
    "There's a lot you think, but none of them seem very concrete. Nevertheless, you are earnest in what you say, only hesitant on what others may have thought with"
    " you rather than you yourself. You know what you think about yourself.\n\n"
    "\tYOU: I don't think I tried hard enough...\n\n"
    "Her back is still turned to you, but you get the vague feeling that She's satisfied with your answer.\n\n"
    "\tHER: Thank you for telling me.\n\n"
    "She sounds sincere.\n\n"
    "\tHER: There isn't much more I can do for you here. Your visit, however, proved to be insightful, and your coming path has become more open.\n\n"
    "\tYOU: What are you talking about?\n\n"
    "\tHER: Fret not.\n\n"
    "She finally turns around and raises her gloved, pale hand, showing a burned piece of something.\n\n"
    "\tHER: Take this.\n\n"
    "She gently flicks it from her hand, and as if by magic, the burned piece of paper floats to your hands. It's another part of the first piece of burned photo you"
    " picked up from your house.\n\n"
    ">>> 2/3 OF BURNED PHOTO has been added to your inventory.\n\n"
    "It completes the other part you have of the bottom half of the photograph. You can't yet see the faces of the two children and adults in the picture, but you can"
    " tell that this is obviously posed as a family photograph. Still, you cannot recognize anyone in the photo.\n\n"
    "\tHER: Seek the white chapel over the red hills. Perhaps you can seek your desires there. Don't get lost in the red hills; you will not be able to find your way"
    " back if you do. I believe you can make it today.\n\n"
    "\tYOU: Will I see you there?\n\n"
    "You look at Her with hope.\n\n"
    "\tHER: Follow your footsteps back out.\n\n"
    "You dip your head farewell and linger a bit before doing as She says. You don't think you seek desires, but maybe there's something more to it.\n\n"
    "You step out of the door of the Red Chapel, expecting to be swallowed by the unnatural red light on the porch, but you are greeted by the sun instead.",
    "have not": "You are apprehensive and actively dodge the question.\n\n"
    "\tYOU: Is it okay for me to be here?\n\n"
    "\tHER: We welcome anyone who is in need of help.\n\n"
    "\tYOU: I need help?\n\n"
    "You ask this more towards yourself.\n\n"
    "\tYOU: Maybe you're mistaken, Miss...\n\n"
    "You then recall that you have no idea what this miss' name is. What have you been calling Her this whole time?\n\n"
    "\tHER: We know when people are in need of help — of guidance. Don't try to fool us.\n\n"
    "Her voice is stern, and you're taken aback a bit. This is the first time you've heard Her voice be anything but soft.\n\n"
    "You're not trying to “fool” anybody. You frown and focus on the floor of the chapel, actively avoiding Her gaze.\n\n"
    "\tYOU: I'm not trying to fool you or… or anyone. I don't think I am at least...\n\n"
    "She doesn't immediately respond, and you're only met with silence. You can't bring yourself to look back up at her.\n\n"
    "\tHER: Then tell me… do you smoke?\n\n"
    "You stop fidgeting in your stance.",
    "have jacket": "You bring out the pack of cigarettes you found in your jacket, still unopened, and look it over. You almost say that you don't smoke but suddenly"
    " feel as if you could go for one right now.\n\n"
    "\tYOU: Maybe...\n\n"
    "You clear your throat, putting it back in your pocket.\n\n"
    "\tYOU: I don't know. I don't even have a lighter for it, so maybe I don't.\n\n"
    "\tHER: Seek the white chapel over the red hills. Perhaps you can seek your desires there. Don't get lost in the red hills; you will not be able to find your way"
    " back if you do. I believe you can make it today.\n\n"
    "\tYOU: Will I see you there?\n\n"
    "You look at Her with hope.\n\n"
    "\tHER: Follow your footsteps back out.\n\n"
    "You dip your head farewell and linger a bit before doing as She says. You don't think you seek desires, but maybe there's something more to it.\n\n"
    "You step out of the door of the Red Chapel, expecting to be swallowed by the unnatural red light on the porch, but you are greeted by the sun instead.",
    "have not jacket": "\tYOU: Maybe… I-I don't know.\n\n"
    "She grows silent again, and you narrow your eyes at her figure. For a moment, you think you see beneath the veil, but She moves again and the veil blurs. You smile"
    " a bit at what you saw.\n\n"
    "\tHER: I see. Maybe we cannot guide you here.\n\n"
    "You twist your face in confusion for a moment, wondering who “we” is, but Her voice is back to being soft, swaying you a bit.\n\n"
    "\tHER: Seek the white chapel over the red hills. Perhaps you can seek your desires there. Don't get lost in the red hills; you will not be able to find your way"
    " back if you do. I believe you can make it today.\n\n"
    "\tYOU: Will I see you there?\n\n"
    "You look at Her with hope.\n\n"
    "\tHER: Follow your footsteps back out.\n\n"
    "You dip your head farewell and linger a bit before doing as She says. You don't think you seek desires, but maybe there's something more to it.\n\n"
    "You step out of the door of the Red Chapel, expecting to be swallowed by the unnatural red light on the porch, but you are greeted by the sun instead.",
}
whitechapel_have_items = {
    "have": "You reach your hands in your pockets, remembering the fresh pack of cigarettes. You pull it out and look at it with a frown, fingering the cellophane around"
    " it.\n\n"
    ". . .\n\n"
    "You find that you don't like it.\n\n"
    "\tHER: Does it upset you?\n\n"
    "You snap your head up and look at the raised platform where She is, Her back still turned to you.\n\n"
    "\tHER: The pack. Does it upset you?\n\n"
    "You blink at her back before looking down at the pack of cigarettes again, finding a swell of emotions bubbling inside your chest. You don't know where it's"
    " coming from or why Her question invoked such feelings, but it makes you crumple the pack of cigarettes.\n\n"
    "Unable to use your words, you nod your head, keeping your sobs in.\n\n"
    "She calls out your name again, and you slowly look up at Her with blurred vision. She's closer now, sitting right next to you, and She hands you a tissue to"
    " wipe your tears with.\n\n"
    "You wipe your tears.\n\n"
    "\tYOU: I don't — I'm sorry, I don't know where this is coming from…\n\n"
    "\tHER: There is no need to be sorry…\n\n"
    "The both of you sit in silence before She lets out a soft sigh.\n\n"
    "\tHER: Perhaps this will help you.\n\n"
    "She hands you one last piece of the burned photo, and you frown as you bring out the others to piece it together. You flimsily put it together in your hands,"
    " taking in the photo, and you *remember*.\n\n"
    ">>> 3/3 OF BURNED PHOTO has been added to your inventory.\n\n"
    "The photo reveals a small family of four: a mother, a father, and their two children. The oldest doesn't look older than four, while the youngest doesn't look"
    " older than three. One of the parent's faces you recognize as yours.\n\n"
    "This family is yours. Your partner is next to you with a bright smile, and you remember the day you took that photo together.\n\n"
    "You choke on a wet laugh at the memories as tears blur  your vision once more, yet you don't hold them back.\n\n"
    "Your two children were fidgety after you and your partner promised to reward them with ice cream afterwards, so their faces are adorned with huge smiles. The"
    " oldest one, you remember, has your eyes and smile, but the youngest one has your partner's smile.\n\n"
    "You remember them giggling and laughing away during the photoshoot.\n\n"
    "You were happy then.\n\n"
    "Yet you were the cause of their demise.\n\n"
    "She comforts you with soft pats on your back, and you don't realize that She is leading you out of the White Chapel.\n\n"
    "\tHER: The black chapel on the white snow is your F A T E.",
    "have jacket": "You take out the pack of cigarettes and remember that you don't have a lighter on you. Despite knowing this,"
    " you still attempt to search through your pockets for one.",
    "have not jacket": "You find a stray cigarette, searching for a lighter. You click your tongue in disappointment, slouching against the back of the bench. You"
    " then notice the lit up candle at the altar and nearly grimace.",
    "have not": "\tYOU: That'd be kind of rude, wouldn't it? Using the flame of the candle on the altar to light up my cigarette for a moment of relaxation.\n\n"
    "You take a moment to contemplate.\n\n"
    "\tYOU: Fuck it, I'll do it anyway.\n\n"
    "You don't know where this bravery is coming from, but you find your feet dragging themselves to the altar and bending over with the cigarette hanging in your"
    " mouth, waiting for the end to catch light.\n\n"
    "The first breath is of relief, and you stagger back to a nearby bench, propping your feet upon the small elevated stage and using the back of the bench as an"
    " armrest.\n\n"
    "The second breath brings a bit of scratchiness in your throat, and you sigh.\n\n"
    "The third breath makes your throat burn, and you clear it to mediate the burning.\n\n"
    "The fourth breath makes you realize the stench in the air. It isn't the cigarette smoke you can make a face at and wave away; it was rotten and burnt, seeping"
    " into your clothes and skin.\n\n"
    "You quickly flick the cigarette away and stomp on it to kill the embers, but as you breathe in, you choke on the lingering stench. You grasp at your throat while"
    " coughing as you trip while trying to get up, grimacing through the pain surging through your legs and falling on your back. The bench moves over from your weight,"
    " screeching against the floor. The combined heat from outside seeping into the chapel, the stench, the pain, and the sound of the bench scraping against the floor,"
    " it was all too much for you for one moment.\n\n"
    "You struggle to get up and use your legs from overworking them, and your lungs are equally struggling to deal with the contaminated air. Your only option is to"
    " crawl towards the exit. You're on all fours as you shuffle into the aisle and towards the doors, but as you glance up to put your target in sight, you notice the"
    " writing painted in red.\n\n\n\n"
    "THIS PLACE IS NOT FOR YOU. THE BLACK CHAPEL ON THE WHITE SNOW IS YOUR F A T E.\n\n\n\n"
    "You can only put your remaining hope to this last place. You don't know what redemption you were seeking at the Red Chapel, but these desires that come forth in"
    " the White Chapel are killing you. You don't have a choice. This was better than nothing.\n\n"
    "Your feet skitter against the flooring, and you throw your whole body against the doors. This time you are prepared, and you breathe in the sharp cold air that was"
    " outside the White Chapel.\n\n"
    ". . .\n\n"
    "No, you're not at the White Chapel anymore. You don't see those red spider flowers in your peripheral view; you only see white now.",
}
blackchapel_have_items = {
    "have": "It's colder now. You shiver and lean more into Her comfort, and you know She knows.\n\n"
    "It was an accident.\n\n"
    "You tell yourself that to make yourself feel better. You needed your nicotine fix, but you weren't allowed to smoke."
    " You promised yourself you'd stop smoking. It was too dangerous to light one up, yet you did anyway.\n\n"
    "Important papers, family pictures, sentimental and valuable items all burned down that day. All because you didn't realize the heat from the cigarette"
    " wasn't fully out. You stomped on it and everything. That usually does the trick.\n\n"
    "Usually.\n\n"
    "You thought it was safe to discard it in the trashcan and hide it there rather than outside in the grass.\n\n"
    "But there were added screams and the stench of melting flesh. Screams for help, for either parent, for anything. There were kids — your kids — still in"
    " that house. Your significant other was still in there.\n\n"
    "The roof was the first to cave in. One of the shelves tipped over and collapsed on your partner, pinning them down to the ground with the flames on the"
    " shelf ripping their flesh.\n\n"
    "You remember how their flesh boiled and charred from the heat, sticking and melding with the carpet.\n\n"
    "You remember the sound they made as they tried to reach out for the kids, and their desperate attempts and gurgles they made to reach for their children.\n\n"
    "You couldn't make out the words they were saying as the pain from the flames made them cry out in between whatever noises they attempted to coherently say.\n\n"
    "You sob as you remember everything, pressing your palms against your eyelids. You miss them so much; you regret everything you did, wishing that you could take"
    " it all back and give your family the life they deserved.\n\n"
    "You tried to help.\n\n"
    "You had already burned your hand on one of the doorknobs to the kids' room. You went to find something to safely open the door, but by the time you came back,"
    " the whole door was on fire. There wasn't any way you could break the door down without hurting your kids on the other side or yourself, so you just stood there"
    " while choking on the ash.\n\n"
    "You could hear the kids cry on the other side.\n\n"
    "You didn't even say anything to them.\n\n"
    "Maybe you were a coward for not trying. You were still with them, but you said nothing.\n\n"
    "You couldn't say anything.\n\n"
    "There was nowhere for you to go, so you just sat on your knees on the other side of the door, cradling your head in your hands as you bore with the searing heat"
    " from the flames.\n\n"
    "You remember crying with them as you continued to hear their raw screams, pleading for you to help them. They probably weren't even coughing from the smoke of"
    " the flames.\n\n"
    "As the flames burned hotter and hotter, they continued to cry out for someone to help them. One of them threw up from crying and yelling so much.\n\n"
    "You wanted to tell them to stop talking, to stop pleading and save their breath for when someone could actually help them.\n\n"
    "But you knew there was no one to help them. If you couldn't, who else could?\n\n"
    "The crying stopped when the floor lost its structural weight, bringing you down to the bottom floor.\n\n"
    "That's all you remembered feeling at that final moment.\n\n"
    "The last thing you heard was screaming.\n\n"
    "Someone cradles your head and brings it onto something soft; you don't realize that you have knelt down into the snow. They brush your hair aside, gently"
    " comforting you.\n\n"
    "\tYOUR PARTNER: I know, my love. I know.\n\n"
    "You sob harder, unable to choke out all the words you want to say.\n\n"
    "\tYOUR PARTNER: Your time has come, my love. It's time to go.\n\n"
    "You're too scared to open your eyes. You're still grieving the loss of your family, the loss you directly caused.\n\n"
    "\tYOUR PARTNER: That's fine… She's forgiving like that.\n\n"
    "\tYOUR PARTNER: It'll be okay…\n\n"
    "What sounds like your partner reaches for the finished photo in your lap, taking it away from you.\n\n"
    "\tYOUR PARTNER: We'll always be waiting for you…",
    "have not": "It doesn't stop once you feel like it's been long enough. You're hyperventilating as your body responds to the sudden change in atmosphere, but"
    " you can't look up.\n\n"
    "There's something horrifying to look at if you look up, and you can't look. You try to bury your face in the snow, but it doesn't help to ease the feeling.\n\n"
    "There's an overwhelming presence in front of you, and your stomach is dropping at the feeling. It has such an aura that is overbearing, and your heart sinks and"
    " you feel like crying.\n\n"
    "It feels like it's telling you something.\n\n"
    "I T  K N O W S.\n\n"
    "I T  K N O W S.\n\n"
    "I T  K N O W S.\n\n"
    "The cold is stinging your face. Your mouth is open in a silent cry, your hands are full of soft snow, and tears stick the snow to your face.\n\n"
    "The Black Chapel knows why you are here.\n\n"
    "It knows what you have done.\n\n"
    "You remember what you have done.\n\n"
    "It was an accident.\n\n"
    "You tell yourself that to make yourself feel better. You needed your nicotine fix, but you weren't allowed to smoke. You promised yourself you'd stop"
    " smoking. It was too dangerous to light one up, yet you did anyway.\n\n"
    "Important papers, family pictures, sentimental and valuable items all burned down that day. All because you didn't realize the heat from the cigarette"
    " wasn't fully out. You stomped on it and everything. That usually does the trick.\n\n"
    "Usually.\n\n"
    "You thought it was safe to discard it in the trashcan and hide it there rather than outside in the grass.\n\n"
    "But there were added screams and the stench of melting flesh. Screams for help, for either parent, for anything. There were kids — your kids — still in"
    " that house. Your significant other was still in there.\n\n"
    "The roof was the first to cave in. One of the shelves tipped over and collapsed on your partner, pinning them down to the ground with the flames on the"
    " shelf ripping their flesh.\n\n"
    "You remember how their flesh boiled and charred from the heat, sticking and melding with the carpet.\n\n"
    "You remember the sound they made as they tried to reach out for the kids, and their desperate attempts and gurgles they made to reach for their children.\n\n"
    "You couldn't make out the words they were saying as the pain from the flames made them cry out in between whatever noises they attempted to coherently say.\n\n"
    "You tried to help.\n\n"
    "You had already burned your hand on one of the doorknobs to the kids' room. You went to find something to safely open the door, but by the time you came back,"
    " the whole door was on fire. There wasn't any way you could break the door down without hurting your kids on the other side or yourself, so you just stood there"
    " while choking on the ash.\n\n"
    "You could hear the kids cry on the other side.\n\n"
    "You didn't even say anything to them.\n\n"
    "Maybe you were a coward for not trying. You were still with them, but you said nothing.\n\n"
    "You couldn't say anything.\n\n"
    "There was nowhere for you to go, so you just sat on your knees on the other side of the door, cradling your head in your hands as you bore with the searing heat"
    " from the flames.\n\n"
    "You remember crying with them as you continued to hear their raw screams, pleading for you to help them. They probably weren't even coughing from the smoke of the"
    " flames.\n\n"
    "As the flames burned hotter and hotter, they continued to cry out for someone to help them. One of them threw up from crying and yelling so much.\n\n"
    "You wanted to tell them to stop talking, to stop pleading and save their breath for when someone could actually help them.\n\n"
    "But you knew there was no one to help them. If you couldn't, who else could?\n\n"
    "The crying stopped when the floor lost its structural weight, bringing you down to the bottom floor.\n\n"
    "That's all you remembered feeling at that final moment.\n\n"
    "The last thing you heard was screaming.\n\n"
    "Someone cradles your head and brings it onto something soft.\n\n"
    "You can't open your eyes as they are frozen shut by your tears and the snow. Soft touches brush the remaining debris off your face, and you want to open your"
    " eyes, but you can't.\n\n"
    "You can't look.\n\n"
    "\tHER: Have you sought your guidance?\n\n"
    "You want to move and cling to Her for comfort, but you can't tell if any of your body parts are moving.\n\n"
    "The cold has made your body so numb.\n\n"
    "\tYOU: Yes.\n\n"
    "You croak your response, your voice barely a whisper above the icy wind.\n\n"
    "You press your lips together, feeling the warmth emanate slowly. Your eyes feel warm from the overflow of tears. There's probably snot running down your nose"
    " and coating your lips.\n\n"
    "You don't know why you hesitate to say something more, but you revel in the grace She has given you.\n\n"
    "Now you understand why people devote their lives to a single person. You don't mind devoting your life to Her, but now remembering that you already have lived,"
    " you almost sob at the thought of being unable to properly pray to Her.\n\n"
    "What would you even pray for?\n\n"
    "\tYOU: Thank you…\n\n"
    "That's all you can manage to say.\n\n"
    "She doesn't say anything. You feel like She's looking down at you with pity, and you simply cling onto Her for all you can.\n\n"
    "\tHER: Your time has come. Perhaps you can see your family another day.\n\n"
    "You think back to the Red Chapel and almost laugh.\n\n"
    "You won't be seeing your family again at all.\n\n"
    "Not after what you've done.\n\n"
    "You won't be able to reach their level.",
}

shortest_knowing = [
    "Head out the room",
    "Enter the living room",
    "Go to the kitchen",
    "Head outside and into town",
    "Go to the church",
    "Yes",
    "Take a break",
    "Enter the church",  # For consistency, choosing "Enter the church"
    "Walk forward",
    "Enter the church",  # Again, choosing "Enter the church"
]

technical_shortest = [
    "Head out the room",
    "Enter the living room",
    "Go to the kitchen",
    "Head outside and into town",
    "Go to the church",
    "No",
]

longest_knowing = [
    "Look out the window",
    "Look in the closet",
    "Take the jacket",
    "Search the jacket",
    "Head out the room",
    "Open the door on the right",
    "Search the bathroom",
    "Go back to the hallway",
    "Open the door on the left",
    "Search the office",
    "Yes",
    "Enter the living room",
    "Go to the backyard",
    "Go back to the living room",
    "Go to the kitchen",
    "Search the kitchen",
    "Head outside and into town",
    "Explore the town",
    "Yes",
    "Go back to the town square",
    "Go to the church",
    "Yes",
    "Take a break",
    "Enter the church",
    "Walk forward",
    "Enter the church",
    "Accept your fate",
]


def get_next_action(sequence):
    if sequence:
        return sequence.pop(0)
    else:
        return "quit"


current_room = 0
inventory = []


def create_save():
    save_file_name = input("What is the name of your saved file? ")
    save_file = open(save_file_name + ".txt", "w")
    save_file.write(str(current_room) + "\n")
    for i in range(len(inventory)):
        save_file.write(inventory[i] + "\n")
    print("Save file: '", save_file_name, "' successfully created.")
    save_file.close()


def load_game():
    validation = True
    while validation:
        load_file_name = input("What is the name of your saved file? ")
        path = "./" + load_file_name + ".txt"
        if os.path.isfile(path):
            load_file = open(load_file_name + ".txt", "r")
            global current_room
            current_room = int(load_file.readline())
            global inventory
            inventory = load_file.read().splitlines()
            print("Save file: '", load_file_name, "' successfully loaded.\n\n")
            load_file.close()
            validation = False
        else:
            print(
                "That file doesn't exist or cannot be found. Do you wish to try again? Y/N\n\n"
            )
            while True:
                again = input("> ")
                if again.lower() == "n":
                    validation = False
                    False
                elif again.lower() == "y":
                    validation = True
                    False
                else:
                    print("Unknown command. Try again.\n\n")


def getDesc(room):
    return room[current_room]["description"]


def getActions(room):
    for x in range(len(room[current_room]["actions"])):
        print("- ", room[current_room]["actions"][x])


def print_split_text():
    desc = getDesc(rooms)
    split_text = desc.split("\n\n")
    for x in range(len(split_text)):
        print(split_text[x])
        input()


def print_list(list):
    for x in range(len(list)):
        print(list[x])
        input()


# Instructions
print(
    "INSTRUCTIONS:\n"
    "\t* To get the next line of description or dialogue, please simply press ENTER.\n"
    "\t* All player commands must be written exactly, although it isn't case sensitive. If you misspell a word,\n\tit will not recognize the command.\n\n"
    '\t* TO LOAD A GAME: simply type in "LOAD" to access your saved file.\n'
    '\t* TO SAVE YOUR GAME: simply type in "SAVE" when prompted to put in an input.\n'
    '\t* TO QUIT YOUR GAME: simply type in "QUIT" when prompted to put in an input.\n\t***NOTE: If you quit your game without saving, you will lose your progress.\n'
    "Press ENTER to start a new game or LOAD to load a saved game.\n\n\n"
)
game_state = input("> ")

# Start CPU monitoring
initial_cpu = psutil.cpu_times()
# Gets the CPU times specifically for the current process
initial_process_cpu = psutil.Process().cpu_times()
# records the time when the game starts
start_time = time.time()

if game_state.lower() == "load":
    load_game()
    print_split_text()
    getActions(rooms)
else:
    # Starting room
    print_split_text()
    getActions(rooms)

# Main game loop
running = True
while running:
    player_input = input("\n> ")
    # player_input = get_next_action(shortest_knowing)

    match player_input.lower():
        case "look out the window":
            current_room = 1
            print()
            print_split_text()
            getActions(rooms)
        case "look in the closet":
            current_room = 2
            print()
            print_split_text()
            getActions(rooms)
        case "take the jacket":
            current_room = 3
            print()
            print_split_text()
            inventory.append("JACKET")
            print(">>> JACKET has been added to your inventory.\n")
            getActions(rooms)
        case "search the jacket":
            current_room = 4
            print()
            print_split_text()
            getActions(rooms)
        case "head out the room":
            current_room = 5
            state = 1
            print()
            print_split_text()
            getActions(rooms)

        # Go back to the starting room if you want
        case "go back to the room":
            current_room = 0
            print()
            getActions(rooms)
        # Go back to the hallway
        case "go back to the hallway":
            current_room = 5
            print()
            getActions(rooms)
        case "open the door on the right":
            current_room = 6
            print()
            print_split_text()
            getActions(rooms)
        case "search the bathroom":
            current_room = 7
            print()
            print_split_text()
            getActions(rooms)
        case "open the door on the left":
            current_room = 8
            print()
            print_split_text()
            getActions(rooms)
        case "search the office":
            current_room = 9
            print()
            print_split_text()
            getActions(rooms)
        case "yes":
            # Case for "Search the office, take the burned picture?"
            if current_room == 9:
                current_room = 10
                print()
                inventory.append("1/3 OF BURNED PHOTO")
                print(">>> 1/3 OF BURNED PHOTO has been added to your inventory.\n\n")
                print_split_text()
                getActions(rooms)
            # Case for "Explore downtown, take the newspaper article?"
            elif current_room == 17:
                current_room = 18
                print()
                inventory.append("NEWSPAPER ARTICLE")
                print(">>> NEWSPAPER ARTICLE has been added to your inventory.\n\n")
                print_split_text()
                getActions(rooms)
            # Case for "Go to the church, go into the church?"
            elif current_room == 20:
                current_room = 21
                print()
                print_split_text()
                if (
                    "JACKET"
                    and "1/3 OF BURNED PHOTO"
                    and "NEWSPAPER ARTICLE" in inventory
                ):
                    text = church_have_items["have"].split("\n\n")
                    print_list(text)
                else:
                    text = church_have_items["have not"].split("\n\n")
                    print_list(text)
                # Start of ACT 2, THE RED CHAPEL
                current_room = 23
                print()
                print_split_text()
                getActions(rooms)
            else:
                break
        case "no":
            # Case for "Search the office, take the burned picture?"
            if current_room == 9:
                current_room = 11
                print()
                print_split_text()
                getActions(rooms)
            # Case for "Explore downtown, take the newspaper article?"
            elif current_room == 17:
                current_room = 19
                print()
                print_split_text()
                getActions(rooms)
            # Case for "Go to the church, go into the church?" But saying no ends the game.
            elif current_room == 20:
                current_room = 22
                print()
                print_split_text()
                running = False
            else:
                break
        case "enter the living room":
            current_room = 12
            print()
            print_split_text()
            getActions(rooms)
        # Go back to the living room if you want
        case "go back to the living room":
            current_room = 12
            print()
            getActions(rooms)
        case "go to the kitchen":
            current_room = 13
            print()
            print_split_text()
            getActions(rooms)
        case "search the kitchen":
            current_room = 14
            print()
            print_split_text()
            getActions(rooms)
        case "go to the backyard":
            current_room = 15
            print()
            print_split_text()
            getActions(rooms)
        case "head outside and into town":
            current_room = 16
            print()
            print_split_text()
            getActions(rooms)

        case "explore the town":
            current_room = 17
            print()
            print_split_text()
            getActions(rooms)

        # Take the newspaper article? in previous "yes" and "no" cases.

        case "go back to the town square":
            current_room = 16
            print()
            getActions(rooms)
        case "go to the church":
            current_room = 20
            print()
            print_split_text()
            getActions(rooms)

        # START OF ACT 1, THE RED CHAPEL
        case "take a break":
            chance = random.random()
            if chance > 0.3:
                current_room = 24
                print()
                print_split_text()
                getActions(rooms)
            else:
                current_room = 25
                print()
                print_split_text()
                running = False
        case "enter the church":
            if current_room == 24:
                current_room = 26
                print()
                print_split_text()
                if (
                    "JACKET"
                    and "1/3 OF BURNED PHOTO"
                    and "NEWSPAPER ARTICLE" in inventory
                ):
                    inventory.append("2/3 OF BURNED PHOTO")
                    text = redchapel_have_items["have"].split("\n\n")
                    print_list(text)
                else:
                    text = redchapel_have_items["have not"].split("\n\n")
                    print_list(text)
                    if "JACKET" in inventory:
                        text = redchapel_have_items["have jacket"].split("\n\n")
                        print_list(text)
                    else:
                        text = redchapel_have_items["have not jacket"].split("\n\n")
                        print_list(text)
                current_room = 29
                print()
                print_split_text()
                getActions(rooms)
            elif current_room == 30:
                current_room = 32
                print()
                print_split_text()
                if (
                    "JACKET"
                    and "1/3 OF BURNED PHOTO"
                    and "NEWSPAPER ARTICLE"
                    and "2/3 OF BURNED PHOTO" in inventory
                ):
                    inventory.append("3/3 OF BURNED PHOTO")
                    text = whitechapel_have_items["have"].split("\n\n")
                    print_list(text)
                    print()
                    current_room = 38
                    getActions(rooms)
                else:
                    if "JACKET" in inventory:
                        text = whitechapel_have_items["have jacket"].split("\n\n")
                        print_list(text)
                    else:
                        text = whitechapel_have_items["have not jacket"].split("\n\n")
                        print_list(text)
                    text = whitechapel_have_items["have not"].split("\n\n")
                    print_list(text)
                    text = blackchapel_have_items["have not"].split("\n\n")
                    print_list(text)
                    current_room = 37
                    print()
                    print_split_text()
                    running = False
        case "wait for an invitation":
            if current_room == 24:
                current_room = 27
                print()
                print_split_text()
                if (
                    "JACKET"
                    and "1/3 OF BURNED PHOTO"
                    and "NEWSPAPER ARTICLE" in inventory
                ):
                    inventory.append("2/3 OF BURNED PHOTO")
                    text = redchapel_have_items["have"].split("\n\n")
                    print_list(text)
                else:
                    text = redchapel_have_items["have not"].split("\n\n")
                    print_list(text)
                    if "JACKET" in inventory:
                        text = redchapel_have_items["have jacket"].split("\n\n")
                        print_list(text)
                    else:
                        text = redchapel_have_items["have not jacket"].split("\n\n")
                        print_list(text)
                current_room = 29
                print()
                print_split_text()
                getActions(rooms)
            elif current_room == 30:
                current_room = 33
                print()
                print_split_text()
                if (
                    "JACKET"
                    and "1/3 OF BURNED PHOTO"
                    and "NEWSPAPER ARTICLE"
                    and "2/3 OF BURNED PHOTO" in inventory
                ):
                    inventory.append("3/3 OF BURNED PHOTO")
                    text = whitechapel_have_items["have"].split("\n\n")
                    print_list(text)
                    print()
                    current_room = 38
                    getActions(rooms)
                else:
                    if "JACKET" in inventory:
                        text = whitechapel_have_items["have jacket"].split("\n\n")
                        print_list(text)
                    else:
                        text = whitechapel_have_items["have not jacket"].split("\n\n")
                        print_list(text)
                    text = whitechapel_have_items["have not"].split("\n\n")
                    print_list(text)
                    text = blackchapel_have_items["have not"].split("\n\n")
                    print_list(text)
                    current_room = 37
                    print()
                    print_split_text()
                    running = False
        case "turn away":
            if current_room == 24:
                current_room = 28
                print()
                print_split_text()
                running = False
            elif current_room == 29:
                current_room = 34
                print()
                print_split_text()
                running = False

        case "walk forward":
            current_room = 30
            print()
            print_split_text()
            getActions(rooms)
        case "turn back around":
            current_room = 31
            print()
            print_split_text()
            running = False
        case "accept your fate":
            text = blackchapel_have_items["have"].split("\n\n")
            print_list(text)
            running = False
        case "deny your fate":
            current_room = 35
            print()
            print_split_text()
            running = False

        case "save":
            create_save()
            running = False

        case "quit":
            print("Exiting the game now.")
            running = False

        case _:
            print("\n\nUnknown command. Try again.\n\n")
            getActions(rooms)

# End CPU monitoring
end_time = time.time()
final_cpu = psutil.cpu_times()
final_process_cpu = psutil.Process().cpu_times()

# Calculate CPU usage
# Calculates the total CPU time available system-wide during the game's execution
total_cpu_time = sum(final_cpu) - sum(initial_cpu)
process_cpu_time = (final_process_cpu.user - initial_process_cpu.user) + (
    final_process_cpu.system - initial_process_cpu.system
)
cpu_usage_percentage = (process_cpu_time / total_cpu_time) * 100

# Print CPU usage and runtime
print("\n\nRUNTIME: %s seconds" % (end_time - start_time))
print(f"Total elapsed time: {end_time - start_time:.2f} seconds")
print(f"CPU time used by script: {process_cpu_time:.2f} seconds")
print(f"Total CPU time available: {total_cpu_time:.2f} seconds")
print(f"CPU usage percentage: {cpu_usage_percentage:.2f}%")
