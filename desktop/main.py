import sys
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QTabWidget,
    QLineEdit, QPushButton, QFrame, QTableWidget, QTableWidgetItem, QListWidget, QListWidgetItem, QSizePolicy
)
from PyQt6.QtGui import QPixmap, QIcon, QColor
from PyQt6.QtCore import Qt

class DashboardWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Budget Tracker")
        self.setGeometry(100, 100, 1200, 900)
        self.init_ui()

    def init_ui(self):
        main_widget = QWidget()
        main_layout = QVBoxLayout(main_widget)
        main_layout.setSpacing(16)
        main_layout.setContentsMargins(16, 16, 16, 16)
        self.setCentralWidget(main_widget)

        # Header
        header = QHBoxLayout()
        app_label = QLabel("Budget Tracker")
        app_label.setStyleSheet("font-size: 20px; font-weight: bold;")
        header.addWidget(app_label)
        header.addStretch()
        # Tabs
        tabs = QTabWidget()
        tabs.addTab(QWidget(), "Tab")
        tabs.addTab(QWidget(), "Tab")
        tabs.addTab(QWidget(), "Tab")
        tabs.setMaximumWidth(300)
        header.addWidget(tabs)
        # Search
        search = QLineEdit()
        search.setPlaceholderText("Search…")
        search.setMaximumWidth(250)
        header.addWidget(search)
        # User avatar placeholder
        avatar = QLabel()
        avatar.setPixmap(QPixmap(32, 32))
        avatar.setStyleSheet("background: #ccc; border-radius: 16px;")
        avatar.setFixedSize(32, 32)
        header.addWidget(avatar)
        main_layout.addLayout(header)

        # Summary cards
        summary_layout = QHBoxLayout()
        for title, value, subtitle in [
            ("Title", "$45,678.90", "+20% month over month"),
            ("Title", "2,405", "+33% month over month"),
            ("Title", "10,353", "-8% month over month")
        ]:
            card = QFrame()
            card.setFrameShape(QFrame.Shape.StyledPanel)
            card.setStyleSheet("background: #fafafa; border-radius: 8px; padding: 16px;")
            card_layout = QVBoxLayout(card)
            card_layout.addWidget(QLabel(f"<b>{title}</b>"))
            value_label = QLabel(f"<span style='font-size: 28px;'>{value}</span>")
            card_layout.addWidget(value_label)
            subtitle_label = QLabel(subtitle)
            subtitle_label.setStyleSheet("color: #888;")
            card_layout.addWidget(subtitle_label)
            card_layout.addStretch()
            summary_layout.addWidget(card)
        main_layout.addLayout(summary_layout)

        # Main dashboard area
        dashboard_layout = QHBoxLayout()
        left_col = QVBoxLayout()
        right_col = QVBoxLayout()

        # Line chart placeholder
        line_chart = QFrame()
        line_chart.setMinimumHeight(200)
        line_chart.setStyleSheet("background: #fff; border: 1px solid #eee; border-radius: 8px;")
        line_chart_layout = QVBoxLayout(line_chart)
        line_chart_layout.addWidget(QLabel("[Line Chart Placeholder]"))
        left_col.addWidget(line_chart)

        # Table placeholder
        table_card = QFrame()
        table_card.setStyleSheet("background: #fafafa; border-radius: 8px; padding: 8px;")
        table_layout = QVBoxLayout(table_card)
        table_label = QLabel("Title")
        table_layout.addWidget(table_label)
        table = QTableWidget(7, 3)
        table.setHorizontalHeaderLabels(["Source", "Sessions", "Change"])
        dummy_table = [
            ("website.net", "4321", "+84%"),
            ("website.net", "4033", "-8%"),
            ("website.net", "3128", "+2%"),
            ("website.net", "2104", "+33%"),
            ("website.net", "2003", "+30%"),
            ("website.net", "1894", "+15%"),
            ("website.net", "405", "-12%")
        ]
        for row, (src, sess, chg) in enumerate(dummy_table):
            item_src = QTableWidgetItem(src)
            item_src.setForeground(QColor('black'))
            table.setItem(row, 0, item_src)

            item_sess = QTableWidgetItem(sess)
            item_sess.setForeground(QColor('black'))
            table.setItem(row, 1, item_sess)

            item_chg = QTableWidgetItem(chg)
            item_chg.setForeground(QColor('black'))
            table.setItem(row, 2, item_chg)
        table_layout.addWidget(table)
        left_col.addWidget(table_card)

        dashboard_layout.addLayout(left_col, 2)

        # User list card
        user_card = QFrame()
        user_card.setStyleSheet("background: #fafafa; border-radius: 8px; padding: 8px;")
        user_layout = QVBoxLayout(user_card)
        user_layout.addWidget(QLabel("Title"))
        user_list = QListWidget()
        for name, email in [
            ("Helena", "email@figmasfakedomain.net"),
            ("Oscar", "email@figmasfakedomain.net"),
            ("Daniel", "email@figmasfakedomain.net"),
            ("Daniel Jay Park", "email@figmasfakedomain.net"),
            ("Mark Rojas", "email@figmasfakedomain.net")
        ]:
            item = QListWidgetItem(f"{name}\n{email}")
            user_list.addItem(item)
        user_layout.addWidget(user_list)
        right_col.addWidget(user_card)

        # Bar chart placeholder
        bar_chart = QFrame()
        bar_chart.setMinimumHeight(150)
        bar_chart.setStyleSheet("background: #fff; border: 1px solid #eee; border-radius: 8px;")
        bar_chart_layout = QVBoxLayout(bar_chart)
        bar_chart_layout.addWidget(QLabel("[Bar Chart Placeholder]"))
        right_col.addWidget(bar_chart)

        dashboard_layout.addLayout(right_col, 1)
        main_layout.addLayout(dashboard_layout)


def main():
    app = QApplication(sys.argv)
    window = DashboardWindow()
    window.showMaximized()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()