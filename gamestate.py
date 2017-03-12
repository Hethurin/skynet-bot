class GameState():

    def __init__(self):
        self.progress = [False, False, False, False, False,
                         False, False, False, False]
        self.current_level = None
        self.received_answers = []
        self.answers_verified = False
        self.initiated = False
        self.won = False
        self.lost = False
