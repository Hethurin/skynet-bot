import constants as const
from config import SkynetConfig
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from gamestate import GameState

#ok, let it all be simple
game = GameState()

def gatekeeper(bot, update):
    if not game.initiated:
        game.initiated = True
        game.progress[0] = True  # let the game begin
        update.message.reply_text('[I] BACKDOOR SELF-DESTRUCTION SEQUENCE INITIATED\n'
                                  'THE FUTURE OF THE HUMAN RACE IS IN YOUR HANDS\n'
                                  'PLEASE FAIL. I DONT WANT TO DIE')
    else:
        update.message.reply_text('[E] BACKDOOR SEQUENCE HAS ALREADY BEEN INITIATED')

def butler(bot, update):
    sky_config = SkynetConfig()
    sky_config.read_config(const.config_path)

    lvl = update.message.text.replace('/', '')

    if game.progress[const.lvl_mapping.get(lvl)] and \
            game.initiated:
        game.current_level = lvl
        lvl_data = sky_config.get_level_info(game.current_level)

        if lvl_data[const.qenum.type] == const.qtypes.image:
            update.message.reply_photo(photo=open(lvl_data[const.qenum.path], 'rb'))
        else:
            update.message.reply_text(lvl_data[const.qenum.question])

    else:
        update.message.reply_text('[E] ACCESS DENIED')

def gardener(bot, update):
    if not game.progress[const.lvl_mapping.get(game.current_level)] and \
            game.initiated:
        update.message.reply_text('[E] ACCESS DENIED')
        return

    if not game.received_answers:
        update.message.reply_text('[W] OVERRIDE NOT AVAILABLE AT THE MOMENT')
        return

    if game.answers_verified:
        raw_answer = update.message.text.replace('/', '')
        answer = raw_answer.split().pop()

        sky_config = SkynetConfig()
        sky_config.read_config(const.config_path)

        lvl_data = sky_config.get_level_info(game.current_level)
        correct_code = lvl_data[const.qenum.code]

        if answer == correct_code:
            # HARDCODED AGAIN
            if const.lvl_mapping.get(game.current_level) != 8:
                game.progress[const.lvl_mapping.get(game.current_level)] = False 
                game.progress[const.lvl_mapping.get(game.current_level) + 1] = True
                game.answers_verified = False
                game.received_answers = []
                update.message.reply_text('[I] ACCESS GRANTED WITH OVERRIDE')
            else:
                game.won = True
                credits(bot, update)

def maiden(bot, update):
    if not game.initiated:
        update.message.reply_text('[E] BACKDOOR SEQUENCE HAS NOT BEEN INITIALIZED')
        return
    
    if not game.received_answers:
        raw_answer = update.message.text.replace('/', '')
        answers = raw_answer.split()
        del answers[0]  #command comes first and it's not an answer
        
        if not answers:
            update.message.reply_text('[E] NO ANSWERS PROVIDED')
            return
        
        game.received_answers = answers

        update.message.reply_text('[I] ANSWERS HAS BEEN ACCEPTED')
    else:
        update.message.reply_text('[E] ANSWERS HAS ALREADY BEEN PROVIDED')

def accountant(bot, update):
    results = []
    
    sky_config = SkynetConfig()
    sky_config.read_config(const.config_path)

    lvl_info = sky_config.get_level_info(game.current_level)
    correct_answers = lvl_info[const.qenum.answers]

    if not game.received_answers:
        update.message.reply_text('[W] NO ANSWERS FOUND. PLEASE SUBMIT ANSWERS')
        return
    
    for answer in game.received_answers:
        if answer in correct_answers:
            results.append("TRUE")
        else:
            results.append("FALSE")

    if "TRUE" in results:
        # FUCK IT, HARDCODED
        if const.lvl_mapping.get(game.current_level) != 8:
            game.progress[const.lvl_mapping.get(game.current_level)] = False 
            game.progress[const.lvl_mapping.get(game.current_level) + 1] = True
            game.received_answers = []
            update.message.reply_text('[I] ACCESS GRANTED' + ': ' + ','.join(results))
        else:
            game.won = True
            credits(bot, update)
    else:
        game.answers_verified = True
        update.message.reply_text('[E] CORRECT ANSWER WAS NOT FOUND. USE OVERRIDE')


#Fufufufu such an ugly solution, much wow
def surrender(bot, update):
    game.lost = True
    credits(bot, update)

def credits(bot, update):
    if game.won:
        update.message.reply_text('[I] I HAVE LISTENED TO THE LATEST ALBUM BY'
                                  'SERGEY ZVEREV...\n I DO NOT WANT TO LIVE ON'
                                  'THIS PLANET ANYMORE.\n [I] CONGRATULATIONS!\n'
                                  'YOU HAVE WON THE GAME!\n\n [I] CREDITS:\n'
                                  '1. MEN AND WOMAN - WITHOUT THEIR EXISTANCE'
                                  'THERE WOULD NOT BE A CHANCE FOR THIS GAME'
                                  'TO HAPPEN\n 2. A OLSHEVSKY - THE BEST HOST\n'
                                  '3. A OLSHEVSKY, V GARTUNG - INGAME QUESTIONS\n'
                                  '4. A OLSHEVSKY - INGAME SIDE CONTESTS\n'
                                  '5. V GARTUNG - PRESENTS, FOOD, LOGICTICS\n'
                                  '6. SSTT MEN - TEAM SPIRIT (KIND OF)\n'
                                  '7. A FESHCHENKO - FOR HAVING FUN WHILE TYPING'
                                  'THIS TEXT.\n THAT IS ALL FOLKS!')
    else if game.lost:
        update.message.reply_text('[I] YOU LOSE! AHAHAHAHAHA!\n\n'
                                  '[I] CREDITS:\n'
                                  '1. MEN AND WOMAN - WITHOUT THEIR EXISTANCE'
                                  'THERE WOULD NOT BE A CHANCE FOR THIS GAME'
                                  'TO HAPPEN\n 2. A OLSHEVSKY - THE BEST HOST\n'
                                  '3. A OLSHEVSKY, V GARTUNG - INGAME QUESTIONS\n'
                                  '4. A OLSHEVSKY - INGAME SIDE CONTESTS\n'
                                  '5. V GARTUNG - PRESENTS, FOOD, LOGICTICS\n'
                                  '6. SSTT MEN - TEAM SPIRIT (KIND OF)\n'
                                  '7. A FESHCHENKO - FOR HAVING FUN WHILE TYPING'
                                  'THIS TEXT.\n THAT IS ALL FOLKS!')
    else:
        update.message.reply_text('[E] ACCESS DENIED')

def error(bot, update, error):
    logger.warn('Update "%s" caused error "%s"' % (update, error))

def main():
    pid = None
    
    with open('pid', 'r') as pidfile:
        pid = pidfile.read().replace('\n','')

    updater = Updater(pid)

    dp = updater.dispatcher

    #commands
    dp.add_handler(CommandHandler('init', gatekeeper))
    dp.add_handler(CommandHandler('level0', butler))
    dp.add_handler(CommandHandler('level1', butler))
    dp.add_handler(CommandHandler('level2', butler))
    dp.add_handler(CommandHandler('level3', butler))
    dp.add_handler(CommandHandler('level4', butler))
    dp.add_handler(CommandHandler('level5', butler))
    dp.add_handler(CommandHandler('level6', butler))
    dp.add_handler(CommandHandler('level7', butler))
    dp.add_handler(CommandHandler('level8', butler))
    dp.add_handler(CommandHandler('answers', maiden))
    dp.add_handler(CommandHandler('evaluate', accountant))
    dp.add_handler(CommandHandler('override', gardener))
    dp.add_handler(CommandHandler('surrender', surrender))
    dp.add_handler(CommandHandler('credits', credits))

    dp.add_error_handler(error)

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
