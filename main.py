import sys
from PySide6.QtWidgets import (
    QApplication,
    QMainWindow,
    QWidget,
    QHBoxLayout,
    QStackedWidget,
)
from PySide6.QtGui import QIcon

from core.config import load_config, build_stylesheet, ICON_PATH
from core.database import load_questions
from ui.widgets import Sidebar
from ui.pages import DashboardPage, SimuladoPage, SimuladoIAPage, ConfigPage

# ──────────────────────── MAIN WINDOW ─────────────────────────


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("CNH Simulated - Preparatório")
        self.resize(1000, 650)

        if ICON_PATH.exists():
            self.setWindowIcon(QIcon(str(ICON_PATH)))

        self.questions = load_questions()

        self.central = QWidget()
        self.setCentralWidget(self.central)
        self.main_lay = QHBoxLayout(self.central)
        self.main_lay.setContentsMargins(0, 0, 0, 0)
        self.main_lay.setSpacing(0)

        self.sidebar = Sidebar()
        self.main_lay.addWidget(self.sidebar)

        self.stack = QStackedWidget()
        self.main_lay.addWidget(self.stack, 1)

        self._build_pages()
        self.sidebar.page_changed.connect(self.switch_page)

    def switch_page(self, key):
        idx_map = {"dashboard": 0, "simulado": 1, "simulado_ia": 2, "config": 3}
        idx = idx_map.get(key, 0)
        self.stack.setCurrentIndex(idx)
        page = self.stack.widget(idx)
        if hasattr(page, "slide_in"):
            page.slide_in(direction_up=True)

    def _on_q_saved(self, new_q_list):
        self.questions = new_q_list
        self.page_sim.refresh_questions(self.questions)
        self.page_ia.refresh_questions(self.questions)

    def _on_settings_changed(self):
        QApplication.instance().setStyleSheet(build_stylesheet())
        self.sidebar.rebuild()
        self._build_pages()
        self.sidebar._click("config")

    def _build_pages(self):
        # Limpa as páginas antigas da memória
        while self.stack.count() > 0:
            w = self.stack.widget(0)
            self.stack.removeWidget(w)
            w.deleteLater()

        # Recria as páginas com as novas cores globais
        self.page_dash = DashboardPage(self.questions)
        self.page_sim = SimuladoPage(self.questions)
        self.page_ia = SimuladoIAPage(self.questions)
        self.page_cfg = ConfigPage()
        self.stack.addWidget(self.page_dash)
        self.stack.addWidget(self.page_sim)
        self.stack.addWidget(self.page_ia)
        self.stack.addWidget(self.page_cfg)

        # Reconecta os sinais
        self.page_dash.go.connect(self.sidebar._click)
        self.page_ia.work_started.connect(self.sidebar.show_ai_running)
        self.page_ia.work_finished.connect(self.sidebar.hide_ai_running)
        self.page_ia.questions_saved.connect(self._on_q_saved)
        self.page_cfg.settings_changed.connect(self._on_settings_changed)


if __name__ == "__main__":
    load_config()
    app = QApplication(sys.argv)
    app.setStyleSheet(build_stylesheet())
    win = MainWindow()
    win.show()
    sys.exit(app.exec())
