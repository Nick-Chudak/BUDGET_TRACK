import os
from PyQt6.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QTabWidget, QLineEdit, QLabel, QSizePolicy, QFrame
from PyQt6.QtGui import QPixmap
from desktop.services.data_loader import load_transactions
from desktop.services.metrics import total_earned, total_spent, savings
from desktop.ui.widgets import create_summary_card
from desktop.charts.drilldown_bar import DrilldownBarChartWidget
from desktop.charts.expenses_by_month import ExpensesByMonthChart

class DashboardWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Budget Tracker")
        self.setGeometry(100, 100, 1200, 900)
        self.init_ui()

    def init_ui(self):
        try:
            main_widget = QWidget()
            main_widget.setStyleSheet("background-color: #FFFFFF;")
            main_layout = QVBoxLayout(main_widget)
            main_layout.setSpacing(16)
            main_layout.setContentsMargins(16, 16, 16, 16)
            self.setCentralWidget(main_widget)

            # Load data
            df = load_transactions(r"C:\Users\nchud\Downloads\Preferred_Package_6788_051925.xlsx")

            earned = total_earned(df)
            spent = total_spent(df)
            save = savings(df)
            earned_sub = "+20% month over month"
            spent_sub = "+33% month over month"
            save_sub = "-8% month over month"

            # 1. Slim header bar (app name + tabs)
            header_bar = QHBoxLayout()
            app_label = QLabel("Budget Tracker")
            app_label.setStyleSheet("font-size: 18px; font-weight: bold; color: #000000;")
            app_label.setFixedHeight(32)
            header_bar.addWidget(app_label)
            header_bar.addStretch()
            tabs = QTabWidget()
            tabs.setFixedHeight(32)
            tabs.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
            tabs.addTab(QWidget(), "Tab")
            tabs.addTab(QWidget(), "Tab")
            tabs.addTab(QWidget(), "Tab")
            tabs.setStyleSheet("QTabBar::tab { color: #000000; } QTabWidget { color: #000000; }")
            header_bar.addWidget(tabs)
            header_widget = QWidget()
            header_widget.setLayout(header_bar)
            header_widget.setFixedHeight(40)
            header_widget.setStyleSheet("background: transparent; border: 1px solid #E0E0E0; border-radius: 8px;")
            main_layout.addWidget(header_widget)

            # 2. Summary/search row
            summary_row = QHBoxLayout()
            # Left: summary cards (2/3)
            summary_cards_layout = QHBoxLayout()
            summary_cards_layout.setSpacing(16)
            summary_cards_layout.addWidget(create_summary_card("Total Earned", earned, earned_sub))
            summary_cards_layout.addWidget(create_summary_card("Total Spending", spent, spent_sub))
            summary_cards_layout.addWidget(create_summary_card("Savings", save, save_sub))
            summary_cards_widget = QWidget()
            summary_cards_widget.setLayout(summary_cards_layout)
            summary_cards_widget.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
            summary_cards_widget.setStyleSheet("background: transparent; border: 1px solid #E0E0E0; border-radius: 8px;")
            summary_row.addWidget(summary_cards_widget, 2)
            # Right: search + avatar (1/3)
            right_top_layout = QVBoxLayout()
            right_top_layout.setSpacing(16)
            search = QLineEdit()
            search.setPlaceholderText("Search…")
            search.setMaximumWidth(250)
            search.setStyleSheet("color: #000000; background: #FFFFFF; border: 1px solid #E0E0E0; border-radius: 4px;")
            avatar = QLabel()
            avatar.setPixmap(QPixmap(32, 32))
            avatar.setStyleSheet("background: #ccc; border-radius: 16px;")
            avatar.setFixedSize(32, 32)
            right_top_layout.addWidget(search)
            right_top_layout.addWidget(avatar)
            right_top_layout.addStretch()
            right_top_widget = QWidget()
            right_top_widget.setLayout(right_top_layout)
            right_top_widget.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
            right_top_widget.setStyleSheet("background: transparent; border: 1px solid #E0E0E0; border-radius: 8px;")
            summary_row.addWidget(right_top_widget, 1)
            summary_widget = QWidget()
            summary_widget.setLayout(summary_row)
            summary_widget.setFixedHeight(220)  # Adjust as needed for card height
            summary_widget.setStyleSheet("background: transparent;")
            main_layout.addWidget(summary_widget)

            dashboard_layout = QHBoxLayout()
            # Left: Expenses by month chart (2/3)
            if not df.empty:
                expenses_chart = ExpensesByMonthChart(df)
                dashboard_layout.addWidget(expenses_chart, 2)
            # Right: Placeholder (1/3)
            right_placeholder = QWidget()
            dashboard_layout.addWidget(right_placeholder, 1)
            dashboard_widget = QWidget()
            dashboard_widget.setLayout(dashboard_layout)
            dashboard_widget.setStyleSheet("background: transparent; border: 1px solid #E0E0E0; border-radius: 8px;")
            main_layout.addWidget(dashboard_widget)

            # Add stretch to push everything up if window is tall
            main_layout.addStretch()
        except Exception as e:
            print("Exception in init_ui:", e) 