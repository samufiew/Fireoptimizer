import sys
from PyQt6 import QtCore, QtGui, QtWidgets
from modules import system_tools, network_tools, cleanup_tools, utils

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Fireoptimizer — Premium")
        self.resize(980, 640)
        self.central = QtWidgets.QWidget()
        self.setCentralWidget(self.central)
        self.layout = QtWidgets.QHBoxLayout(self.central)

        # Sidebar
        self.sidebar = QtWidgets.QFrame()
        self.sidebar.setFixedWidth(220)
        self.sidebar.setStyleSheet("background:#121212; color:#FFFFFF;")
        self.sb_layout = QtWidgets.QVBoxLayout(self.sidebar)
        self.app_label = QtWidgets.QLabel("Fireoptimizer")
        self.app_label.setStyleSheet("font-size:18px; font-weight:600; color:#ffffff; padding:12px;")
        self.sb_layout.addWidget(self.app_label)
        self.sb_layout.addSpacing(6)

        # buttons
        self.btn_home = QtWidgets.QPushButton("Dashboard")
        self.btn_perf = QtWidgets.QPushButton("Performance")
        self.btn_net = QtWidgets.QPushButton("Network")
        self.btn_clean = QtWidgets.QPushButton("Cleaning")
        self.btn_tools = QtWidgets.QPushButton("Tools")

        for b in (self.btn_home, self.btn_perf, self.btn_net, self.btn_clean, self.btn_tools):
            b.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
            b.setStyleSheet("background:transparent; color:#ddd; text-align:left; padding:10px; border:none;")
            self.sb_layout.addWidget(b)

        self.sb_layout.addStretch()
        self.layout.addWidget(self.sidebar)

        # Main content
        self.content = QtWidgets.QFrame()
        self.content_layout = QtWidgets.QVBoxLayout(self.content)
        self.header = QtWidgets.QLabel("Dashboard")
        self.header.setStyleSheet("font-size:20px; color:#eee;")
        self.content_layout.addWidget(self.header)

        # cards row
        self.cards = QtWidgets.QHBoxLayout()
        card_style = "background:#ffffff; border-radius:10px; padding:12px;"
        self.card1 = QtWidgets.QFrame()
        self.card1.setStyleSheet(card_style)
        self.card1.setFixedHeight(100)
        self.card1_layout = QtWidgets.QVBoxLayout(self.card1)
        self.card1_layout.addWidget(QtWidgets.QLabel("RAM Libera"))
        self.card1_layout.addWidget(QtWidgets.QLabel("..."))
        self.cards.addWidget(self.card1)

        self.card2 = QtWidgets.QFrame()
        self.card2.setStyleSheet(card_style)
        self.card2.setFixedHeight(100)
        self.card2_layout = QtWidgets.QVBoxLayout(self.card2)
        self.card2_layout.addWidget(QtWidgets.QLabel("CPU Load"))
        self.card2_layout.addWidget(QtWidgets.QLabel("..."))
        self.cards.addWidget(self.card2)

        self.content_layout.addLayout(self.cards)

        # action buttons
        self.hbox_actions = QtWidgets.QHBoxLayout()
        self.full_opt_btn = QtWidgets.QPushButton("Full Optimize (Safe Advanced)")
        self.full_opt_btn.setStyleSheet("background:#0078d7; color:white; padding:10px; border-radius:6px;")
        self.hbox_actions.addWidget(self.full_opt_btn)
        self.content_layout.addLayout(self.hbox_actions)

        # log/status
        self.log = QtWidgets.QTextEdit()
        self.log.setReadOnly(True)
        self.log.setFixedHeight(180)
        self.content_layout.addWidget(self.log)

        self.layout.addWidget(self.content, 1)

        # events
        self.btn_home.clicked.connect(self.show_dashboard)
        self.btn_perf.clicked.connect(self.show_performance)
        self.btn_net.clicked.connect(self.show_network)
        self.btn_clean.clicked.connect(self.show_cleaning)
        self.btn_tools.clicked.connect(self.show_tools)
        self.full_opt_btn.clicked.connect(self.full_optimize)

        # initial UI populate
        self.show_dashboard()

    def log_msg(self, txt):
        self.log.append(txt)

    def show_dashboard(self):
        self.header.setText("Dashboard")
        self.log_msg("Opened Dashboard")

    def show_performance(self):
        self.header.setText("Performance")
        self.log_msg("Opened Performance")

    def show_network(self):
        self.header.setText("Network")
        self.log_msg("Opened Network")

    def show_cleaning(self):
        self.header.setText("Cleaning")
        self.log_msg("Opened Cleaning")

    def show_tools(self):
        self.header.setText("Tools")
        self.log_msg("Opened Tools")

    def full_optimize(self):
        # confirm elevated actions
        if not utils.is_admin():
            QtWidgets.QMessageBox.warning(self, "Permessi", "Esegui l'app come amministratore per applicare tutte le ottimizzazioni.")
            return
        res = QtWidgets.QMessageBox.question(self, "Conferma",
                                             "Applichiamo tutte le ottimizzazioni conservative e avanzate (richiede tempo). Procedere?",
                                             QtWidgets.QMessageBox.StandardButton.Yes | QtWidgets.QMessageBox.StandardButton.No)
        if res != QtWidgets.QMessageBox.StandardButton.Yes:
            return

        # Sequence: performance -> network reset -> clean -> trim -> disable services (confirm)
        self.log_msg("Applying High Performance plan...")
        rc, out, err = system_tools.enable_high_performance()
        self.log_msg(f"powercfg rc={rc}")

        self.log_msg("Flushing DNS...")
        rc, out, err = network_tools.flush_dns()
        self.log_msg(out or err)

        self.log_msg("Resetting Winsock...")
        rc, out, err = network_tools.reset_winsock()
        self.log_msg(out or err)

        self.log_msg("Cleaning temp...")
        ok, msg = cleanup_tools.clear_temp_user()
        self.log_msg(msg)

        self.log_msg("Trimming memory (soft)...")
        ok, msg = cleanup_tools.trim_memory_soft()
        self.log_msg(msg)

        # show & ask about disabling services
        services = system_tools.list_safe_services_to_disable()
        if QtWidgets.QMessageBox.question(self, "Services",
            "Vuoi disabilitare alcuni servizi non critici per migliorare stabilità (consigliato)?",
            QtWidgets.QMessageBox.StandardButton.Yes | QtWidgets.QMessageBox.StandardButton.No) == QtWidgets.QMessageBox.StandardButton.Yes:
            ok, res = system_tools.safe_disable_services(services)
            self.log_msg(f"Disabled services: {res}")

        QtWidgets.QMessageBox.information(self, "Completato", "Full Optimize completato (conservative).")

def main():
    app = QtWidgets.QApplication(sys.argv)
    # set global style: antracite background
    app.setStyleSheet("""
        QMainWindow { background: #2b2b2b; }
        QTextEdit { background: #1f1f1f; color:#ddd; border-radius:8px; padding:8px; }
        QLabel { color:#eee; }
    """)
    win = MainWindow()
    win.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
