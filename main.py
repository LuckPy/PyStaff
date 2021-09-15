from PySide6 import QtWidgets, QtGui, QtCore
from qt_material import apply_stylesheet

from staff import *


class MainWindow(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setup_ui()
        self.setWindowTitle("pyStaff")
        apply_stylesheet(app, theme='light_blue.xml')

    def setup_ui(self):
        self.create_layouts()
        self.create_widgets()
        self.modify_widgets()
        self.add_widgets_to_layouts()
        self.setup_connections()
        self.populate_staff()

    def create_widgets(self):
        self.le_id = QtWidgets.QLineEdit()
        self.lbl_user = QtWidgets.QLabel()
        self.le_nom = QtWidgets.QLineEdit()
        self.le_prenom = QtWidgets.QLineEdit()
        self.cb_sexe = QtWidgets.QComboBox()
        self.cb_situation = QtWidgets.QComboBox()
        self.le_service = QtWidgets.QLineEdit()
        self.le_fonction = QtWidgets.QLineEdit()
        self.le_salaire = QtWidgets.QLineEdit()
        self.le_adresse = QtWidgets.QLineEdit()
        self.lw_staff = QtWidgets.QListWidget()
        self.btn_remove_user = QtWidgets.QPushButton("Retirer")
        self.btn_remove_user.setShortcut(QtGui.QKeySequence("DEL"))
        self.btn_add_user = QtWidgets.QPushButton("Ajouter/Modifier")
        self.btn_add_user.setShortcut(QtGui.QKeySequence("ENTER"))
        self.btn_clear = QtWidgets.QPushButton("Effacer")
        self.spacer_left = QtWidgets.QSpacerItem(400, 0, QtWidgets.QSizePolicy.Expanding)
        self.spacer_right = QtWidgets.QSpacerItem(400, 0, QtWidgets.QSizePolicy.Expanding)

    def modify_widgets(self):
        # COMBOBOX
        self.cb_sexe.addItems(["Homme", "Femme"])
        self.cb_situation.addItems(["Seul", "Marié", "Pacsé", "Concubinage"])

        # PICTURE
        self.lbl_user.setPixmap(QtGui.QPixmap("resources/user.png"))
        self.lbl_user.setAlignment(QtCore.Qt.AlignCenter)

        # TEXT IN LINE EDIT
        self.le_id.setPlaceholderText("ID:  ")
        self.le_nom.setPlaceholderText("Nom:  ")
        self.le_prenom.setPlaceholderText("Prénom:  ")
        self.le_service.setPlaceholderText("Service:  ")
        self.le_fonction.setPlaceholderText("Fonction:  ")
        self.le_salaire.setPlaceholderText("Salaire:  ")
        self.le_adresse.setPlaceholderText("Adresse:  ")

        # CSS
        self.lbl_user.setStyleSheet("margin: 10px;")
        self.setStyleSheet("QListWidget {color: blue; font-size: 15px;"
                           "background-color: #fffafa; margin-right: 5px;}"
                           "QListWidget::item {color: blue;}"
                           "QListWidget::item:selected {font-size: 25px; color: blue;}"
                           "QLineEdit {height: 15px;}")

    def create_layouts(self):
        # ADD WIDGETS
        self.layout = QtWidgets.QGridLayout(self)
        self.left_layout = QtWidgets.QVBoxLayout()
        self.right_layout = QtWidgets.QVBoxLayout()

        # ADD LAYOUT TO LAYOUT
        self.layout.addLayout(self.left_layout, 0, 0, 1, 1)
        self.layout.addLayout(self.right_layout, 0, 1, 1, 1)

    def add_widgets_to_layouts(self):
        self.right_layout.addWidget(self.lbl_user)
        self.right_layout.addWidget(self.le_id)
        self.right_layout.addWidget(self.le_nom)
        self.right_layout.addWidget(self.le_prenom)
        self.right_layout.addWidget(self.le_fonction)
        self.right_layout.addWidget(self.le_service)
        self.right_layout.addWidget(self.le_salaire)
        self.right_layout.addWidget(self.le_adresse)
        self.right_layout.addWidget(self.cb_sexe)
        self.right_layout.addWidget(self.cb_situation)
        self.right_layout.addWidget(self.btn_add_user)
        self.right_layout.addSpacerItem(self.spacer_right)
        self.right_layout.addWidget(self.btn_clear)
        self.left_layout.addWidget(self.lw_staff)
        self.left_layout.addSpacerItem(self.spacer_left)
        self.left_layout.addWidget(self.btn_remove_user)

    def populate_staff(self):
        self.data = load_data()
        if not self.data:
            return
        for key, value in self.data.items():
            matricule = key
            nom = self.data[key][0]
            prenom = self.data[key][1]
            service = self.data[key][2]
            fonction = self.data[key][3]
            lw_item = QtWidgets.QListWidgetItem(f"{matricule} : {nom} {prenom}\n{service}, {fonction}")
            self.lw_staff.addItem(lw_item)

    def setup_connections(self):
        self.btn_add_user.clicked.connect(self.add_user)
        self.btn_remove_user.clicked.connect(self.remove_user)
        self.lw_staff.itemClicked.connect(self.user_load)
        self.btn_clear.clicked.connect(self.clean_up_entries)

    def add_user(self):
        self.matricule = self.le_id.text()
        self.nom = self.le_nom.text().upper()
        self.prenom = self.le_prenom.text().upper()
        self.service = self.le_service.text().upper()
        self.fonction = self.le_fonction.text().upper()
        self.salaire = self.le_salaire.text()
        self.sexe = self.cb_sexe.currentText()
        self.adresse = self.le_adresse.text().capitalize()
        self.situation = self.cb_situation.currentText()

        self.user = Staff(self.matricule, self.nom, self.prenom, self.service, self.fonction, self.salaire,
                          self.sexe, self.adresse, self.situation)
        self.user.add_employe_to_data()
        self.reloading()

    def user_load(self):
        self.matricule = (self.lw_staff.currentItem().text().split(" : "))[0]
        if self.data.get(self.matricule):
            self.le_id.setText(self.matricule)
            self.le_nom.setText(self.data[self.matricule][0])
            self.le_prenom.setText(self.data[self.matricule][1])
            self.le_service.setText(self.data[self.matricule][2])
            self.le_fonction.setText(self.data[self.matricule][3])
            self.le_salaire.setText(self.data[self.matricule][4])
            self.cb_sexe.setCurrentText(self.data[self.matricule][5])
            self.le_adresse.setText(self.data[self.matricule][6])
            self.cb_situation.setCurrentText(self.data[self.matricule][7])

    def remove_user(self):
        if self.data.get(self.le_id.text()):
            self.create_objet(self.le_id.text())
            self.user.remove_by_id(self.le_id.text())
            self.data = load_data()
            self.reloading()

    def clean_up_entries(self):
        [i.setText("") for i in [self.le_id, self.le_nom, self.le_prenom, self.le_service, self.le_fonction,
                                 self.le_salaire, self.le_adresse]]
        [i.setCurrentText("") for i in [self.cb_sexe, self.cb_situation]]

    def create_objet(self, matricule):
        self.user = Staff(matricule, [self.data[matricule][i] for i in range(8)])

    def reloading(self):
        self.lw_staff.clear()
        self.populate_staff()


app = QtWidgets.QApplication()
window = MainWindow()
window.show()
app.exec_()
