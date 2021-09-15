from pathlib import Path
import json


SOURCE_FILE = Path(__file__).resolve()
SOURCE_DIR = SOURCE_FILE.parent
DATA_DIR = SOURCE_DIR / "DATA"
DATA_FILE = DATA_DIR / "staff.json"


def load_data():
    DATA_DIR.mkdir(exist_ok=True, parents=True)
    if DATA_FILE.exists():
        with open(DATA_FILE, "r") as f:
            return json.load(f)


class Staff:
    def __init__(self, matricule, nom="", prenom="", service="", fonction="",
                 salaire="", sexe="", adresse="", situation=""):
        self.matricule = matricule
        self.nom = nom
        self.prenom = prenom
        self.service = service
        self.fonction = fonction
        self.salaire = salaire
        self.sexe = sexe
        self.adresse = adresse
        self.situation = situation
        self.data = load_data()
        self.return_entry()

    def return_entry(self):
        return [self.nom, self.prenom, self.service, self.fonction, self.salaire,
                self.sexe, self.adresse, self.situation]

    def add_employe_to_data(self):
        self.data[self.matricule] = self.return_entry()
        self._write_in_json()
        return True

    def remove_by_id(self, matricule):
        if self.data.get(matricule):
            self.data.pop(matricule)
            self._write_in_json()

    def _write_in_json(self):
        with open(DATA_FILE, "w") as f:
            json.dump(self.data, f, indent=4)
