import os
from PyQt6.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QTabWidget, QLabel, QSizePolicy, QFrame, QTabBar
from PyQt6.QtGui import QPixmap, QFont
from PyQt6.QtCore import Qt
from desktop.services.data_loader import load_transactions
from desktop.services.metrics import total_earned, total_spent, savings
from desktop.ui.widgets import create_summary_card, create_recent_expenses_widget, create_summary_section
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
            df = load_transactions()
            print(df.shape)
            print(df.columns)

            header_bar = QHBoxLayout()
            header_bar.setContentsMargins(16, 0, 16, 0)  # Optional: padding left/right
            header_bar.setSpacing(0)

            # Title
            app_label = QLabel("Budget Track")
            app_label.setStyleSheet("""
                color: #000000;
                font-family: 'Intel', 'Segoe UI', 'Helvetica Neue', 'Arial', sans-serif;
                font-size: 18px;
                font-weight: bold;
                border: none;
            """)
            app_label.setAlignment(Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignLeft)
            app_label.setFixedHeight(25)

            header_bar.addWidget(app_label)
            header_bar.addStretch()

            # Container widget
            header_widget = QWidget()
            header_widget.setLayout(header_bar)
            header_widget.setFixedHeight(40)
            header_widget.setStyleSheet("""
                background: #FFFFFF;
                border: none;
                border-bottom: 1px solid #E0E0E0;
            """)

            main_layout.addWidget(header_widget)
            print("header_widget added")


            # --- Main summary section container ---
            summary_layout = QHBoxLayout()
            summary_layout.setContentsMargins(0, 0, 0, 0)
            summary_layout.setSpacing(0)

            # --- Add to main layout ---
            main_layout.addWidget(create_summary_section(df))
            print("sumary cards added")


            # 3. Dashboard area (Expenses chart 2/3, Recent transactions 1/3)
            dashboard_layout = QHBoxLayout()
            # Left: Expenses by month chart (2/3)
            if not df.empty:
                expenses_chart = ExpensesByMonthChart(df)
                dashboard_layout.addWidget(expenses_chart, 2)
            # Right: Recent transactions table (1/3)
            recent_table = create_recent_expenses_widget(df)
            dashboard_layout.addWidget(recent_table, 1)
            dashboard_widget = QWidget()
            dashboard_widget.setLayout(dashboard_layout)
            dashboard_widget.setStyleSheet("background: transparent; border: 1px solid #E0E0E0; border-radius: 8px;")
            main_layout.addWidget(dashboard_widget)
            print("dashboard_widget added")
            # Add stretch to push everything up if window is tall
            main_layout.addStretch()
        except Exception as e:
            print("Exception in init_ui:", e) 