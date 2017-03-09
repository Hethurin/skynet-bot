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

    if game.progress[const.lvl_mapping.get(lvl)]:
        game.current_level = lvl
        lvl_data = sky_config.get_level_info(game.current_level)

        update.message.reply_text(lvl_data[const.qenum.question])
    else:
        update.message.reply_text('[E] ACCESS DENIED')

def gardener(bot, update):
    if not game.progress[const.lvl_mapping.get(game.current_level)]:
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
            game.progress[const.lvl_mapping.get(game.current_level)] = False 
            game.progress[const.lvl_mapping.get(game.current_level) + 1] = True
            game.answers_verified = False
            game.received_answers = []
            update.message.reply_text('[I] ACCESS GRANTED WITH OVERRIDE')

def maiden(bot, update):
    if not game.received_answers:
        raw_answer = update.message.text.replace('/', '')
        answers = raw_answer.split()
        del answers[0]  #command comes first and it's not an answer

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

    for answer in game.received_answers:
        if answer in correct_answers:
            results.append("TRUE")
        else:
            results.append("FALSE")

    if "TRUE" in results:
        game.progress[const.lvl_mapping.get(game.current_level)] = False 
        game.progress[const.lvl_mapping.get(game.current_level) + 1] = True
        game.received_answers = []
        update.message.reply_text('[I] ACCESS GRANTED' + ' ,'.join(results))
    else:
        game.answers_verified = True
        update.message.reply_text('[E] CORRECT ANSWER WAS NOT FOUND. USE OVERRIDE')


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
    dp.add_handler(CommandHandler('level9', butler))
    dp.add_handler(CommandHandler('answers', maiden))
    dp.add_handler(CommandHandler('evaluate', accountant))
    dp.add_handler(CommandHandler('override', gardener))

    dp.add_error_handler(error)

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
