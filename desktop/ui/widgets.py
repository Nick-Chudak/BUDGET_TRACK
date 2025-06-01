from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QTableWidget, QTableWidgetItem, QGraphicsDropShadowEffect, QFrame, QTabBar, QHBoxLayout, QSizePolicy
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QColor, QFont
from desktop.services.metrics import total_earned, total_spent, savings

def create_summary_card(title, value, subtitle):
    card = QFrame()
    card.setFixedSize(220, 130)
    card.setStyleSheet("""
        QFrame {
            background: #FFFFFF;
            border: 1px solid #E0E0E0;
            border-radius: 10px;
            font-family: 'Intel', 'Segoe UI', 'Helvetica Neue', 'Arial', sans-serif;
        }
    """)
    layout = QVBoxLayout(card)
    layout.setContentsMargins(14, 14, 14, 14)
    layout.setSpacing(4)

    title_label = QLabel(title)
    title_label.setStyleSheet("font-size: 13px; font-weight: bold; color: #000000; border: none;")
    layout.addWidget(title_label)

    value_label = QLabel(f"${value:,.2f}")
    value_label.setStyleSheet("font-size: 26px; font-weight: bold; color: #000000; border: none;")
    layout.addWidget(value_label)

    subtitle_label = QLabel(subtitle)
    subtitle_label.setStyleSheet("font-size: 12px; color: #888888; border: none;")
    layout.addWidget(subtitle_label)

    layout.addStretch()
    return card


def create_summary_section(df):
    # Main widget
    summary_widget = QWidget()
    summary_layout = QVBoxLayout(summary_widget)
    summary_layout.setContentsMargins(0, 0, 0, 0)
    summary_layout.setSpacing(16)
    summary_widget.setFixedHeight(220)

    # Horizontal tab bar
    tab_bar = QTabBar()
    tab_bar.setExpanding(False)
    for name in ["Expenses", "Earnings", "Savings", "Investments"]:
        tab_bar.addTab(name)

    tab_bar.setStyleSheet("""
        QTabBar::tab {
            background: #F7F7F7;
            color: #000000;
            padding: 8px 16px;
            margin-right: 8px;
            border-radius: 8px;
            font-family: 'Intel', 'Segoe UI', 'Helvetica Neue', 'Arial', sans-serif;
        }
        QTabBar::tab:selected {
            background: #FFFFFF;
            font-weight: bold;
        }
    """)
    summary_layout.addWidget(tab_bar)

    # Summary cards row
    summary_cards_widget = QWidget()
    summary_cards_layout = QHBoxLayout(summary_cards_widget)
    summary_cards_layout.setSpacing(32)
    summary_cards_layout.setContentsMargins(8, 0, 0, 0)

    summary_cards_layout.addWidget(create_summary_card("Total Earned", total_earned(df), "+20% month over month"))
    summary_cards_layout.addWidget(create_summary_card("Total Spending", total_spent(df), "+33% month over month"))
    summary_cards_layout.addWidget(create_summary_card("Savings", savings(df), "-8% month over month"))

    summary_cards_widget.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
    summary_cards_widget.setStyleSheet("background: #FFFFFF;")
    summary_layout.addWidget(summary_cards_widget)

    return summary_widget


def create_recent_expenses_widget(df, max_rows=100):
    # Container widget
    widget = QWidget()
    layout = QVBoxLayout(widget)
    layout.setSpacing(8)
    layout.setContentsMargins(0, 0, 0, 0)

    # Apply 1px border and drop shadow to the widget
    widget.setStyleSheet("""
        QWidget {
            border: 1px solid #E0E0E0;
            border-radius: 4px;
            background: #ffffff;
            font-family: 'Intel', 'Segoe UI', 'Helvetica Neue', 'Arial', sans-serif;
        }
    """)

    shadow = QGraphicsDropShadowEffect()
    shadow.setBlurRadius(10)
    shadow.setXOffset(0)
    shadow.setYOffset(4)
    shadow.setColor(QColor(0, 0, 0, 30))
    widget.setGraphicsEffect(shadow)

    # Title (no borders)
    title = QLabel("Recent expenses")
    title.setStyleSheet("""
        QLabel {
            font-weight: bold;
            font-size: 15px;
            color: #000000;
            padding: 12px 12px 4px 12px;
            border: none;
        }
    """)
    layout.addWidget(title)

    # Table setup
    columns = ["Description", "Date", "Amount"]
    table = QTableWidget()
    table.setColumnCount(len(columns))
    table.setHorizontalHeaderLabels(columns)
    table.setRowCount(min(len(df), max_rows))

    for row_idx, (_, row) in enumerate(df.head(max_rows).iterrows()):
        table.setItem(row_idx, 0, QTableWidgetItem(str(row.get("description", ""))))
        table.setItem(row_idx, 1, QTableWidgetItem(str(row.get("amount", ""))))
        table.setItem(row_idx, 2, QTableWidgetItem(str(row.get("balance", ""))))

    # Table behavior + visuals
    table.setAlternatingRowColors(False)
    table.setShowGrid(False)
    table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
    table.setFocusPolicy(Qt.FocusPolicy.NoFocus)
    table.setSelectionMode(QTableWidget.SelectionMode.NoSelection)
    table.verticalHeader().setVisible(False)
    table.horizontalHeader().setStretchLastSection(True)
    table.horizontalHeader().setDefaultAlignment(Qt.AlignmentFlag.AlignLeft)

    # Styling for the table
    table.setStyleSheet("""
        QTableWidget {
            background: #ffffff;
            border: none;
            font-size: 13px;
            color: #000000;
            font-family: 'Intel', 'Segoe UI', 'Helvetica Neue', 'Arial', sans-serif;
        }
        QHeaderView::section {
            background-color: #ffffff;
            color: #828282;
            font-weight: 600;
            padding: 8px;
            border-top: none;
            border-bottom: 1px solid #E0E0E0;
        }
        QTableWidget::item {
            padding: 6px 12px;
            border-bottom: 1px solid #E0E0E0;
        }
        QScrollBar:vertical, QScrollBar:horizontal {
            background: transparent;
            width: 8px;
            height: 8px;
            margin: 0px;
        }
        QScrollBar::handle {
            background-color: rgba(0, 0, 0, 0.2);
            border-radius: 4px;
        }
        QScrollBar::add-line, QScrollBar::sub-line {
            width: 0px;
            height: 0px;
        }
        QScrollBar::add-page, QScrollBar::sub-page {
            background: none;
        }
    """)

    table.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
    table.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)

    layout.addWidget(table)
    return widget