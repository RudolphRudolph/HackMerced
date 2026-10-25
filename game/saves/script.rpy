'''
# --------------------------------------------------
# CHARACTER DEFINITIONS
# --------------------------------------------------

define maomao = Character("Maomao", color="#c8ffc8")
define sakuya = Character("Sakuya", color="#c8d8ff")
define chichi = Character("Chichi", color="#ffc8dc")
define mon = Character("Mon", color="#ffc8dc")
define ani = Character("Ani", color="#ffc8dc")
define trevor = Character("Trevor", color="#ffc8dc")


# --------------------------------------------------
# PERSISTENT PROGRESS
# --------------------------------------------------

# Starting balance for a player without existing progress.
default persistent.summon_tickets = 5

# Characters the player has unlocked.
default persistent.owned_girls = []

# Optional flags for first-time story rewards.
default persistent.maomao_reward_claimed = False
default persistent.sakuya_reward_claimed = False
default persistent.chichi_reward_claimed = False
default persistent.mon_reward_claimed = False
default persistent.ani_reward_claimed = False
default persistent.trevor_reward_claimed = False

# --------------------------------------------------
# SUMMON SETTINGS
# --------------------------------------------------

define summon_pool = ("Maomao", "Sakuya", "Chichi", "Mon", "Ani", "Trevor")

default summon_message = "Spend a token to summon a character!"
default summoned_girl = None


# --------------------------------------------------
# SUMMON AND COLLECTION SCREEN
# --------------------------------------------------

screen summon_screen():

    modal True

    add Solid("#151522")

    frame:
        xalign 0.5
        yalign 0.5
        xsize 900
        padding (40, 35)

        vbox:
            spacing 20

            text "Character Summon":
                xalign 0.5
                size 44

            text "Tokens: [persistent.summon_tickets]":
                xalign 0.5
                size 28

            text "Equal odds: each girl has a 1-in-3 chance.":
                xalign 0.5
                size 22

            textbutton "Summon — 1 Token":
                xalign 0.5
                sensitive persistent.summon_tickets > 0
                action Return("summon")

            if persistent.summon_tickets <= 0:
                text "You have no tokens left.":
                    xalign 0.5
                    color "#ffaaaa"

            text summon_message:
                xalign 0.5
                text_align 0.5
                size 25

            null height 15

            text "Your Collection":
                xalign 0.5
                size 32

            for girl in summon_pool:

                if girl in persistent.owned_girls:

                    textbutton ("Play " + girl + "'s story"):
                        xalign 0.5
                        action Return(girl)

                else:

                    text (girl + " — Locked"):
                        xalign 0.5
                        color "#888888"

            null height 15

            textbutton "Finish":
                xalign 0.5
                action Return("finish")


# --------------------------------------------------
# GAME START
# --------------------------------------------------

label start:

    jump summon_hub


# --------------------------------------------------
# SUMMON HUB
# --------------------------------------------------

label summon_hub:

    scene bg room
    window hide

    call screen summon_screen

    # Spend a token and summon a random character.
    if _return == "summon":

        if persistent.summon_tickets > 0:

            $ persistent.summon_tickets -= 1
            $ summoned_girl = renpy.random.choice(summon_pool)

            if summoned_girl not in persistent.owned_girls:

                $ persistent.owned_girls.append(summoned_girl)

                $ summon_message = "New character! You summoned " + summoned_girl + "!"

            else:

                # Refund duplicates.
                $ persistent.summon_tickets += 1

                $ summon_message = "You summoned " + summoned_girl + " again. Token refunded!"

            # Save the updated token balance and collection.
            $ renpy.save_persistent()

        jump summon_hub

    # Play an unlocked character's independent story.
    elif _return == "Maomao":

        window auto
        call maomao_route
        jump summon_hub

    elif _return == "Sakuya":

        window auto
        call sakuya_route
        jump summon_hub

    elif _return == "Chichi":

        window auto
        call chichi_route
        jump summon_hub


    elif _return == "Mon":

        window auto
        call mon_route
        jump summon_hub

    elif _return == "Ani":
        window auto
        call ani_route
        jump summon_hub

    elif _return == "Trevor":
        window auto
        call trevor_route
        jump summon_hub        

    # End the current game session.
    elif _return == "finish":

        return




# --------------------------------------------------
# MAOMAO'S ROUTE
# --------------------------------------------------

label maomao_route:

    scene bg room

    # Uncomment after adding your character image.
    # show maomao happy

    "The room smells faintly of dried herbs."

    "At a crowded worktable, Maomao studies a small ceramic cup."

    maomao "You're early."

    maomao "Good. That means you can help me solve something."

    "She gestures toward two jars sitting beside the cup."

    maomao "Someone mixed up the labels."

    maomao "One contains tea. The other contains something considerably less pleasant."

    menu:
        "How do you respond?"

        "Ask how to tell them apart.":
            maomao "By observing carefully. Not by tasting everything you find."

            "She opens one jar and holds it beneath the light."

            maomao "Look at the shape of the leaves."

            "You lean closer while she explains the differences."

            maomao "You're a better assistant when you ask questions."

        "Offer to organize the worktable.":
            maomao "You want to organize this?"

            "She looks over the piles of notes and scattered containers."

            maomao "Fine. But don't move anything without asking."

            "You spend the afternoon sorting jars while she checks their contents."

            maomao "I suppose having you around isn't entirely inconvenient."

    "By sunset, every jar has its proper label."

    "Maomao places a fresh cup of tea in front of you."

    maomao "This one is definitely tea."

    "After a moment, she sits beside you with a cup of her own."

    maomao "You can come back tomorrow."

    "End of Maomao's route."

    return


# --------------------------------------------------
# SAKUYA'S ROUTE
# --------------------------------------------------

label sakuya_route:

    scene bg room

    # Uncomment after adding your character image.
    # show sakuya happy

    "A clock ticks steadily in the quiet room."

    "Sakuya stands beside a table set for two."

    sakuya "Right on time."

    sakuya "I have a rare afternoon without any obligations."

    "She straightens an already perfectly aligned teacup."

    sakuya "Although I'm not entirely sure what to do with it."

    menu:
        "What do you suggest?"

        "Have tea together.":
            sakuya "Tea without discussing work?"

            "She considers the idea, then takes the seat opposite yours."

            sakuya "That would be a change."

            "At first, she keeps glancing at the clock."

            "Eventually, your conversation draws her attention away from it."

            sakuya "I hadn't realized how much time had passed."

        "Try a card game.":
            sakuya "A game?"

            "She retrieves a deck from a nearby drawer."

            sakuya "Very well. But I won't let you win out of politeness."

            "Several close rounds later, she begins smiling at your increasingly ambitious strategies."

            sakuya "That was almost a good plan."

            sakuya "Shall we try another round?"

    "The afternoon light softens as your time together draws to a close."

    sakuya "Usually, I measure a successful day by how much I finish."

    "She leaves the empty cups on the table for a moment longer."

    sakuya "Perhaps today can be an exception."

    "End of Sakuya's route."

    return


# --------------------------------------------------
# CHICHI'S ROUTE
# --------------------------------------------------

label chichi_route:

    scene bg room

    # Uncomment after adding your character image.
    # show chichi happy

    "You arrive to find Chichi studying a handwritten list."

    chichi "There you are!"

    chichi "I was going to make dinner, but there's still a lot to do."

    "She hands you an apron before you can answer."

    chichi "If you're staying to eat, you're helping."

    menu:
        "Which job do you take?"

        "Help prepare the ingredients.":
            chichi "Good. Start with these vegetables."

            "She demonstrates what she wants, then makes room beside her."

            "Your first few attempts are uneven, but you gradually find a rhythm."

            chichi "There. That's much better."

            "Working together, you finish sooner than either of you expected."

        "Set the table and clean up.":
            chichi "Now that's an offer I won't turn down."

            "You clear the table, arrange the dishes, and wash the utensils as she finishes using them."

            "When she turns around, the kitchen is already tidy."

            chichi "You actually cleaned as we went?"

            chichi "You can help with dinner more often."

    "Finally, you both sit down to eat."

    "For the first time all evening, Chichi stops checking what still needs doing."

    chichi "It's nice not having to handle everything myself."

    "She places another helping on your plate."

    chichi "Eat before it gets cold."

    "End of Chichi's route."

    return

label ani_route:

    scene bg room
    image ani kirk = "AniKirk.jpg"

    play music "audio/anitheme.wav"
    
    #ani
    show ani kirk
    "balls"

    return

label mon_route:

    scene bg room

    play music "audio/montheme.wav"

    return
'''

# Define character objects matching backend IDs
define player = Character("You", color="#c8c8c8")
define mon = Character("Mon", color="#5865F2")
define trev = Character("Trev", color="#E91E63")
define ani = Character("Ani", color="#FF5722")
define narrator = Character(None, color="#ffffff")

label start:
    scene bg office
    
    "You boot up the dating sim, ready to find out which developer fate has chosen for your date."
    "Connecting to the FastAPI backend..."

    menu:
        "Pick a strapping young man"

        "Trevor":

            jump route_trev
        "Mon":

            jump route_mon
        "Ani":

            jump route_ani  


# ==========================================
# ROUTE: MON
# ==========================================
label route_mon:
    image mon = "monneutral.png"
    image mon happy = "monhappy.png"
    image mon sad = "monsad.png"    
    image mon mad = "monmad.png"
    image mon neutral = "monneutral.png"
    image mon flirty = "monflirty.png"
    image mon disappointed = "mondisappointed.png"
    image mon content = "moncontent.png"
    image mon error = "monerror.png"
    image tenniscourt = "TennisCourt.jpg" 


    scene bg tenniscourt
    play music "audio/montheme.wav"
    show mon
    mon "Oh, you pulled me? Let's eat some meat or play some tennis!"
    
    label chat_mon_loop:
        python:
            import urllib.request
            import json

            chat_url = "http://10.0.0.164:8001/chat" 
            player_input = renpy.input("What do you want to say? (Type 'exit' to end date)")
            player_input = player_input.strip()

        if player_input.lower() == "exit":
            jump end_date

        python:
            payload = {
                "character_id": "mon",
                "player_message": player_input
            }
            try:
                data = json.dumps(payload).encode('utf-8')
                req = urllib.request.Request(
                    chat_url, 
                    data=data, 
                    headers={'Content-Type': 'application/json'}, 
                    method='POST'
                )
                with urllib.request.urlopen(req) as response:
                    res_json = json.loads(response.read().decode('utf-8'))
                    ai_reply = res_json.get("reply", "My terminal froze.")
                    emotion = res_json.get("emotion", "N")
            except Exception as e:
                ai_reply = "(Error: Could not reach Mon's server.)"
                emotion = "E"

        # Update Mon's sprite based on the emotion returned by backend
        if emotion == "H":
            show mon happy
        elif emotion == "F":
            show mon flirty
        elif emotion == "M":
            show mon mad
        elif emotion == "D":
            show mon disappointed
        elif emotion == "S":
            show mon sad
        elif emotion == "C":
            show mon content
        elif emotion == "E":
            show mon error
        else:
            show mon neutral

        mon "[ai_reply]"
        jump chat_mon_loop

# ==========================================
# ROUTE: TREV
# ==========================================
label route_trev:
    image trev = "trevneutral.png"
    image trev happy = "trevhappy.png"
    image trev sad = "trevsad.png"    
    image trev mad = "trevmad.png"
    image trev neutral = "trevneutral.png"
    image trev flirty = "trevflirty.png"
    image trev disappointed = "trevdisappointed.png"
    image trev content = "trevcontent.png"
    image trev error = "treverror.png"
    image med = "mededbuilding.jpeg" 


    scene bg med
    play music "audio/trevtheme.wav"
    show trev
    trev "Oh, you pulled me? Can you help me with circuits?"
    
    label chat_trev_loop:
        python:
            import urllib.request
            import json

            chat_url = "http://10.0.0.164:8001/chat" 
            player_input = renpy.input("What do you want to say? (Type 'exit' to end date)")
            player_input = player_input.strip()

        if player_input.lower() == "exit":
            jump end_date

        python:
            payload = {
                "character_id": "trev",
                "player_message": player_input
            }
            try:
                data = json.dumps(payload).encode('utf-8')
                req = urllib.request.Request(
                    chat_url, 
                    data=data, 
                    headers={'Content-Type': 'application/json'}, 
                    method='POST'
                )
                with urllib.request.urlopen(req) as response:
                    res_json = json.loads(response.read().decode('utf-8'))
                    ai_reply = res_json.get("reply", "My terminal froze.")
                    emotion = res_json.get("emotion", "N")
            except Exception as e:
                ai_reply = "(Error: Could not reach Trev's server.)"
                emotion = "E"

        # Update Trev's sprite based on the emotion returned by backend
        if emotion == "H":
            show trev happy
        elif emotion == "F":
            show trev flirty
        elif emotion == "M":
            show trev   mad
        elif emotion == "D":
            show trev disappointed
        elif emotion == "S":
            show trev sad
        elif emotion == "C":
            show trev content
        elif emotion == "E":
            show trev error
        else:
            show trev neutral

        trev "[ai_reply]"
        jump chat_trev_loop

# ==========================================
# ROUTE: ANI
# ==========================================
label route_ani:
    image ani neutral = "anineutral.png"
    image ani happy = "anihappy.png"
    image ani sad = "anisad.png"
    image ani mad = "animad.png"
    image ani flirty = "aniflirty.png"
    image ani disappointed = "anidisappointed.png"
    image ani content = "anicontent.png"
    image ani error = "anierror.png"
    
    image food = "inandout.jpg"
    scene bg food
    play music "audio/anitheme.wav"
    show ani neutral
    ani "Hmph. Out of all people, you pulled me? Don't expect me to go easy on you just because we're talking."
    
    label chat_ani_loop:
        python:
            import urllib.request
            import json

            chat_url = "http://10.0.0.164:8001/chat"
            player_input = renpy.input("What do you want to say? (Type 'exit' to end date)")
            player_input = player_input.strip()

        if player_input.lower() == "exit":
            jump end_date

        python:
            payload = {
                "character_id": "ani",
                "player_message": player_input
            }
            try:
                data = json.dumps(payload).encode('utf-8')
                req = urllib.request.Request(
                    chat_url, 
                    data=data, 
                    headers={'Content-Type': 'application/json'}, 
                    method='POST'
                )
                with urllib.request.urlopen(req) as response:
                    res_json = json.loads(response.read().decode('utf-8'))
                    ai_reply = res_json.get("reply", "My focus just crashed.")
            except Exception as e:
                ai_reply = "(Error: Could not reach the server.)"
                emotion = "E"
        
        if emotion == "H":
            show ani happy
        elif emotion == "F":
            show ani flirty
        elif emotion == "M":
            show ani mad
        elif emotion == "D":
            show ani disappointed
        elif emotion == "S":
            show ani sad
        elif emotion == "C":
            show ani content
        elif emotion == "E":
            show ani error
        else:
            show ani neutral

        ani "[ai_reply]"
        jump chat_ani_loop

# ==========================================
# ERROR & END LABELS
# ==========================================
label route_error:
    "An error occurred fetching your date. You spend the evening debugging alone."
    return

label end_date:
    scene bg office
    "The date comes to an end. You close the game, satisfied with your chaotic creation."
    return