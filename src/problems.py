class ProblemeEchecs:
    def __init__(self):
        self.problemes = [
            {
        'nom': 'Mat avec la dame en un coup',
        'fen': '6kp/6p1/6K1/8/8/8/8/5Q2 w - - 0 1',
        'solution': ['f1f7']  
    },
    {
        'nom': 'Mat du berger',
        'fen': 'r1bqkb1r/pppp1ppp/2n2n2/4p2Q/2B1P3/8/PPPP1PPP/RNB1K1NR w KQkq - 0 1',
        'solution': ['h5f7']  
    },
    {
        'nom': 'Mat tour',
        'fen': '6k1/5pp1/7p/8/PP6/q1P5/2B2PPP/4RK2 w - - 0 1',
        'solution': ['e1e8']  
    },
    {
        'nom': 'Mat avec fou',
        'fen': 'r3q1kr/ppNnb1pp/5n2/8/8/8/PPP2PPP/R1BQKB1R w - - 0 1',
        'solution': ['f1c4']  
    },
            
        ]
        self.probleme_actuel = 0
        self.coups_joues = []

    def obtenir_probleme_actuel(self):
        return self.problemes[self.probleme_actuel]

    def verifier_coup(self, coup):
        if len(self.coups_joues) < len(self.obtenir_probleme_actuel()['solution']):
            coup_attendu = self.obtenir_probleme_actuel()['solution'][len(self.coups_joues)]
            if coup == coup_attendu:
                self.coups_joues.append(coup)
                return True
        return False

    def est_resolu(self):
        return len(self.coups_joues) == len(self.obtenir_probleme_actuel()['solution'])

    def probleme_suivant(self):
        self.probleme_actuel = (self.probleme_actuel + 1) % len(self.problemes)
        self.coups_joues = []