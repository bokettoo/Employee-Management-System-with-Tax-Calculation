from abc import ABC, abstractmethod
from datetime import datetime

class IR:
    tranches = [30000, 50000, 60000, 80000, 180000]
    tauxIR = [0, 10, 20, 30, 34, 38]

    @staticmethod
    def getIR(salaire):
        for i in range(len(IR.tranches)):
            if salaire <= IR.tranches[i]:
                return IR.tauxIR[i]
        return IR.tauxIR[-1]

class IEmploye(ABC):
    @abstractmethod
    def age(self):
        pass

    @abstractmethod
    def anciennete(self):
        pass

    @abstractmethod
    def dateRetraite(self, ageRetraite):
        pass

class Employe(IEmploye):
    matricule_count = 0  # Class variable to keep track of matricule

    def __init__(self, nom, dateNaissance, dateEmbauche, salaireBase):
        Employe.matricule_count += 1
        self.matricule = Employe.matricule_count
        self.nom = nom
        self.dateNaissance = datetime.strptime(dateNaissance, "%Y-%m-%d").date()
        self.dateEmbauche = datetime.strptime(dateEmbauche, "%Y-%m-%d").date()
        self.salaireBase = salaireBase

        # Vérifier que l'âge de l'employé à la date d'embauche n'est pas inférieur à 20 ans
        age_embauche = self.age()
        if age_embauche < 20:
            raise ValueError("L'âge de l'employé à la date d'embauche ne peut pas être inférieur à 20 ans.")

    @abstractmethod
    def age(self):
        today = datetime.now().date()
        return today.year - self.dateNaissance.year - ((today.month, today.day) < (self.dateNaissance.month, self.dateNaissance.day))

    @abstractmethod
    def anciennete(self):
        today = datetime.now().date()
        return today.year - self.dateEmbauche.year - ((today.month, today.day) < (self.dateEmbauche.month, self.dateEmbauche.day))

    @abstractmethod
    def dateRetraite(self, ageRetraite):
        return self.dateNaissance.year + ageRetraite

    @abstractmethod
    def salaireAPayer(self):
        pass

    def __str__(self):
        return f"{self.matricule}-{self.nom}-{self.dateNaissance}-{self.dateEmbauche}-{self.salaireBase}"

    def __eq__(self, other):
        return self.matricule == other.matricule

class Formateur(Employe):
    def __init__(self, nom, dateNaissance, dateEmbauche, salaireBase, heureSup, tarifHSup=70.00):
        super().__init__(nom, dateNaissance, dateEmbauche, salaireBase)
        self.heureSup = heureSup
        self.tarifHSup = tarifHSup

    def salaireAPayer(self):
        tauxIR = IR.getIR(self.salaireBase)
        salaire_net = (self.salaireBase + self.heureSup * self.tarifHSup) * (1 - tauxIR / 100)
        return salaire_net

    def __str__(self):
        return f"{super().__str__()}-{self.heureSup}-{self.tarifHSup}"

class Agent(Employe):
    def __init__(self, nom, dateNaissance, dateEmbauche, salaireBase, primeResponsabilite):
        super().__init__(nom, dateNaissance, dateEmbauche, salaireBase)
        self.primeResponsabilite = primeResponsabilite

    def salaireAPayer(self):
        tauxIR = IR.getIR(self.salaireBase)
        salaire_net = (self.salaireBase + self.primeResponsabilite) * (1 - tauxIR / 100)
        return salaire_net

