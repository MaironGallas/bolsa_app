from qt_core import *

# IMPORT CUSTOM WIDGETS
from gui.widgets.py_push_button import PyPushButton
# IMPORT PAGES
from gui.windows.pages.ui_pages import Ui_application_pages


class UiMainWindow():
    def setup_ui(self, parent):
        if not parent.objectName():
            parent.setObjectName("MainWindow")

        # SET INITIAL PARAMETERS
        parent.resize(1200, 720)
        parent.setMinimumSize(960, 540)

        # CREATE CENTRAL WIDGET
        self.central_frame = QFrame()
        self.central_frame.setStyleSheet("background-color: #282a36")

        # CREATE MAIN LAYOUT
        self.main_layout =QHBoxLayout(self.central_frame)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(0)

        # LEFT MENU
        self.left_menu = QFrame()
        self.left_menu.setStyleSheet("background-color: #44475a")
        self.left_menu.setMaximumWidth(50)
        self.left_menu.setMinimumWidth(50)

        # LEFT MENU LAYOUT
        self.left_menu_layout = QVBoxLayout(self.left_menu)
        self.left_menu_layout.setContentsMargins(0,0,0,0)
        self.left_menu_layout.setSpacing(0)

        # TOP FRAME MENU
        self.left_menu_top_frame = QFrame()
        self.left_menu_top_frame.setMinimumHeight(40)
        self.left_menu_top_frame.setObjectName("left_menu_top_frame")

        # TOP FRAME LAYOUT
        self.left_menu_top_layout = QVBoxLayout(self.left_menu_top_frame)
        self.left_menu_top_layout.setContentsMargins(0, 0, 0, 0)
        self.left_menu_top_layout.setSpacing(0)

        # TOP BTNS
        self.toggle_button = PyPushButton(
            text="Ocultar menu",
            icon_path="icon_menu.svg"
        )
        self.btn_1 = PyPushButton(
            text="Página inicial",
            is_active=True,
            icon_path="icon_home.svg"
        )
        self.btn_2 = PyPushButton(
            text="Página 2",
            icon_path="icon_chart.svg"
        )

        self.btn_3 = PyPushButton(
            text="Conectar",
            icon_path="icon_conectar.svg"
        )

        self.btn_4 = PyPushButton(
            text="Desconectar",
            icon_path="icon_desconectar.svg"
        )


        # ADD BTNS TO LAYOUT
        self.left_menu_top_layout.addWidget(self.toggle_button)
        self.left_menu_top_layout.addWidget(self.btn_1)
        self.left_menu_top_layout.addWidget(self.btn_2)
        self.left_menu_top_layout.addWidget(self.btn_3)
        self.left_menu_top_layout.addWidget(self.btn_4)

        # BOTTOM FRAME MENU
        self.left_menu_bottom_frame = QFrame()
        self.left_menu_bottom_frame.setMinimumHeight(40)
        self.left_menu_bottom_frame.setObjectName("left_menu_bottom_frame")

        self.left_menu_bottom_layout = QVBoxLayout(self.left_menu_bottom_frame)
        self.left_menu_bottom_layout.setContentsMargins(0, 0, 0, 0)
        self.left_menu_bottom_layout.setSpacing(0)

        # BOTTOM BTNS
        self.settings_btn = PyPushButton(
            text="Configurações",
            icon_path="icon_settings.svg"
        )

        # ADD BTNS TO LAYOUT
        self.left_menu_bottom_layout.addWidget(self.settings_btn)

        # LABEL VERSION
        self.left_menu_label_version = QLabel("v1.0.0")
        self.left_menu_label_version.setAlignment(Qt.AlignCenter)
        self.left_menu_label_version.setMinimumHeight(30)
        self.left_menu_label_version.setMaximumHeight(30)
        self.left_menu_label_version.setStyleSheet("color: #c3ccdf")

        # MENU SPACER
        self.left_menu_spacer = QSpacerItem(20, 20, QSizePolicy.Minimum, QSizePolicy.Expanding)

        # ADD TO LEFT MENU LAYOUT
        self.left_menu_layout.addWidget(self.left_menu_top_frame)
        self.left_menu_layout.addItem(self.left_menu_spacer)
        self.left_menu_layout.addWidget(self.left_menu_bottom_frame)
        self.left_menu_layout.addWidget(self.left_menu_label_version)

        # TOP BAR
        self.top_bar = QFrame()
        self.top_bar.setMinimumHeight(30)
        self.top_bar.setMaximumHeight(30)
        self.top_bar.setStyleSheet("background-color: #21232d; color: #6272a4")
        self.top_bar_layout = QHBoxLayout(self.top_bar)
        self.top_bar_layout.setContentsMargins(10, 0, 10, 0)

        # Left label
        self.top_label_left = QLabel("Aplicativo para Análise de Dados de Mercado Financeiro Brasileiro")

        # Add to layout
        self.top_bar_layout.addWidget(self.top_label_left)

        # BOTTOM BAR
        self.bottom_bar = QFrame()
        self.bottom_bar.setMinimumHeight(30)
        self.bottom_bar.setMaximumHeight(30)
        self.bottom_bar.setStyleSheet("background-color: #21232d; color: #6272a4")

        self.bottom_bar_layout = QHBoxLayout(self.bottom_bar)
        self.bottom_bar_layout.setContentsMargins(10, 0, 10, 0)

        # Left label
        self.bottom_label_left = QLabel("Status : Desconectado")

        # Top spacer
        self.bottom_spacer = QSpacerItem(20, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        # Right label
        self.bottom_label_right = QLabel("© 2023")

        # Add to layout
        self.bottom_bar_layout.addWidget(self.bottom_label_left)
        self.bottom_bar_layout.addItem(self.bottom_spacer)
        self.bottom_bar_layout.addWidget(self.bottom_label_right)

        # CONTENT
        self.content = QFrame()
        self.content.setStyleSheet("background-color: #282a36")

        # CONTENT LAYOUT
        self.content_layout = QVBoxLayout(self.content)
        self.content_layout.setContentsMargins(0, 0, 0, 0)
        self.content_layout.setSpacing(0)

        # APPLICATION PAGES
        self.pages = QStackedWidget()
        #self.pages.setStyleSheet("font-size: 12 pt; color: #f8f8f2")
        self.ui_pages = Ui_application_pages()
        self.ui_pages.setupUi(self.pages)
        self.pages.setCurrentWidget(self.ui_pages.page_1)

        # ADD WIDGETS TO APP
        self.main_layout.addWidget(self.left_menu)
        self.main_layout.addWidget(self.content)

        #self.content_layout.addWidget(self.table)
        #self.content_layout.addWidget(self.text)
        self.content_layout.addWidget(self.top_bar)
        self.content_layout.addWidget(self.pages)
        self.content_layout.addWidget(self.bottom_bar)

        # SET CENTRAL WIDGET
        parent.setCentralWidget(self.central_frame)
