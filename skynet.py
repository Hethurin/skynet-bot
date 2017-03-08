import constants as const
from config import SkynetConfig
from telegram.ext import Updated, CommandHandler, MessageHandler, Filters

#ok, let it all be simple
#state variables
lvl_mapping = {'level0': 0, 'level1': 1, 'level2': 2,
            'level3': 3, 'level4': 4, 'level5': 5,
            'level6': 6, 'level7': 7, 'level8': 8}

progress = [False, False, False, False, False, False, False, False, False]
current_level = None 
question_info = None
received_answers = []
answers_verified = False

def gatekeeper(bot, update):
    progress[0] = True  # let the game begin
    update.message.reply_text('[I] BACKDOOR SELF-DESTRUCTION SEQUENCE INITIATED\n'
                              'THE FUTURE OF THE HUMAN RACE IS IN YOUR HANDS\n'
                              'PLEASE FAIL. I DONT WANT TO DIE')

def butler(bot, update):
    sky_config = SkynetConfig()
    sky_config.read_config(const.config_path)

    lvl = update.message.text.replace('/', '')

    if progress[lvl_mapping.get(lvl)]:
        current_level = lvl
        lvl_data = sky_config.get_question_info(current_level)

        update.message.reply_text(lvl_data[const.qenum.question])
    else:
        update.message.reply_text('[E] ACCESS DENIED')

def gardener(bot, update):
    if not progress[lvl_mapping.get(current_level)]:
        update.message.reply_text('[E] ACCESS DENIED')
        return

    if not received_answers:
        update.message.reply_text('[W] OVERRIDE NOT AVAILABLE AT THE MOMENT')
        return

    if answers_verified:
        raw_answer = update.message.text.replace('/', '')
        answer = raw_answer.split().pop()

        sky_config = SkynetConfig()
        sky_config.read_config(const.config_path)

        lvl_data = sky_config.get_question_info(current_level)
        correct_code = lvl_data[const.qenum.code]

        if answer == correct_code:
            progress[lvl_mapping.get(current_level)] = False 
            progress[lvl_mapping.get(current_level) + 1] = True
            answers_verified = False
            received_answers = []
            update.message.reply_text('[I] ACCESS GRANTED WITH OVERRIDE')

def maiden(bot, update):
    if not received_answers:
        raw_answer = update.message.text.replace('/', '')
        answers = raw_answer.split()
        del answers[0]  #command comes first and it's not an answer

        received_answers = answers

        update.message.reply_text('[I] ANSWERS HAS BEEN ACCEPTED')
    else:
        update.message.reply_text('[E] ANSWERS HAS ALREADY BEEN PROVIDED')

def accountant(bot, update):
    results = []
    
    sky_config = SkynetConfig()
    sky_config.read_config(const.config_path)

    correct_answers = sky_config.get_question_info(current_level)

    for answer in received_answers:
        if answer in correct_answers:
            results.append("TRUE")
        else:
            results.append("FALSE")

    if "TRUE" in results:
        progress[lvl_mapping.get(current_level)] = False 
        progress[lvl_mapping.get(current_level) + 1] = True
        received_answers = []
        update.message.reply_text('[I] ACCESS GRANTED' + ' ,'.join(results))
    else:
        answers_verified = True
        update.message.reply_text('[E] CORRECT ANSWER WAS NOT FOUND. USE OVERRIDE')


def error(bot, update, error):
    logger.warn('Update "%s" caused error "%s"' % (update, error))

def main():
    updater = Updater('334569414:AAF0guYDoGebu4QdLXtkRbjJG-AFQbhPT3E')

    dp = updater.dispatcher

    #commands
    dp.add_handler(CommandHandler('init', gatekeeper))
    dp.add_handler(CommandHandler('level0', butler))
    dp.add_handler(CommandHandler('level1', butler))
    dp.add_handler(commandhandler('level2', butler))
    dp.add_handler(commandhandler('level3', butler))
    dp.add_handler(commandhandler('level4', butler))
    dp.add_handler(commandhandler('level5', butler))
    dp.add_handler(commandhandler('level6', butler))
    dp.add_handler(commandhandler('level7', butler))
    dp.add_handler(commandhandler('level8', butler))
    dp.add_handler(commandhandler('level9', butler))
    dp.add_handler(commandhandler('answers', maiden))
    dp.add_handler(commandhandler('evaluate', accountant))
    dp.add_handler(commandhandler('override', gardener))

    dp.add_error_handler(error)

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()

