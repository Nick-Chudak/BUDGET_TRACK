from PyQt6.QtWidgets import QFrame, QVBoxLayout, QLabel
from PyQt6.QtGui import QFont

def create_summary_card(title, value, subtitle):
    widget = QFrame()
    widget.setFixedSize(270, 170)
    widget.setFrameShape(QFrame.Shape.StyledPanel)
    widget.setStyleSheet(
        "background: #FFFFFF; border: 1px solid #E0E0E0; border-radius: 10px;"
    )
    layout = QVBoxLayout(widget)
    layout.setContentsMargins(16, 16, 16, 16)
    layout.setSpacing(0)

    # Title
    title_label = QLabel(title)
    title_font = QFont("Arial", 16, QFont.Weight.Bold)
    title_label.setFont(title_font)
    title_label.setStyleSheet("color: #000000;")
    print(f"Title label: {title}")
    layout.addWidget(title_label)

    # Value
    value_label = QLabel(f"${value:,.2f}")
    value_font = QFont("Arial", 40, QFont.Weight.Bold)
    value_label.setFont(value_font)
    value_label.setStyleSheet("color: #000000; margin-top: 4px;")
    print(f"Value label: ${value:,.2f}")
    layout.addWidget(value_label)

    # Subtitle
    subtitle_label = QLabel(subtitle)
    subtitle_font = QFont("Arial", 16)
    subtitle_label.setFont(subtitle_font)
    subtitle_label.setStyleSheet("color: #888888; margin-top: 8px;")
    print(f"Subtitle label: {subtitle}")
    layout.addWidget(subtitle_label)

    layout.addStretch()
    return widget 