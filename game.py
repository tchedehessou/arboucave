import random



class Personne():
    def __init__(self, nom,ev,age):
        self.nom= nom #a generer
        self.ev=ev
        self.age=age
        self.humeur = 5

class Roturier(Personne):
    def __init__(self, statut):
        super().__init__()
        self.statut=statut
        if statut=="paysan":
            self.argent=0
            self.ressources=0
            self.prod=random.randint(2,5)
        else:
            self.argent= random.randint(5,30)
            self.ressources=0
            self.prod=random.randint(5,10)

class Soldat(Personne):
    def __init__(self):
        super().__init__()


class Ecclesiastique(Personne):
    def __init__(self):
        super().__init__()
        self.don=random.choice(["prod","vie","humeur","guerre"])
