from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from PyQt6.QtWidgets import QWidget, QVBoxLayout
import pandas as pd

class ExpensesByMonthChart(FigureCanvas):
    def __init__(self, df, parent=None):
        self.df = df
        self.fig = Figure(figsize=(6, 4), facecolor='#FFFFFF')
        super().__init__(self.fig)
        self.setParent(parent)
        self.ax = self.fig.add_subplot(111)
        self.bar_containers = None
        self.last_hovered = None
        self.plot_chart()
        self.mpl_connect('motion_notify_event', self.on_hover)

    def plot_chart(self):
        self.ax.clear()
        # Prepare data
        df = self.df.copy()
        df['Month'] = df['date'].dt.month
        grouped = df.groupby('Month')['amount'].sum()
        months = [month for month in range(1, 13)]
        values = [grouped.get(m, 0) for m in months]
        labels = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']

        bars = self.ax.bar(labels, values, color='#000000', width=0.7, zorder=3)
        self.bar_containers = bars

        self.ax.set_title('Expenses by month', fontsize=16, fontweight='bold', color='#000000', loc='left')
        self.ax.set_facecolor('#FFFFFF')
        self.ax.grid(axis='y', color='#E0E0E0', linewidth=1, zorder=0)
        self.ax.tick_params(axis='x', colors='#000000', labelsize=12)
        self.ax.tick_params(axis='y', colors='#888888', labelsize=12)
        self.ax.spines['top'].set_visible(False)
        self.ax.spines['right'].set_visible(False)
        self.ax.spines['left'].set_color('#E0E0E0')
        self.ax.spines['bottom'].set_color('#E0E0E0')
        self.fig.tight_layout()
        self.draw()

    def on_hover(self, event):
        if event.inaxes != self.ax:
            if self.last_hovered is not None:
                self.last_hovered.set_width(0.7)
                self.draw()
                self.last_hovered = None
            return
        for bar in self.bar_containers:
            if bar.contains(event)[0]:
                if self.last_hovered is not None and self.last_hovered != bar:
                    self.last_hovered.set_width(0.7)
                bar.set_width(0.9)
                self.last_hovered = bar
                self.draw()
                break
        else:
            if self.last_hovered is not None:
                self.last_hovered.set_width(0.7)
                self.draw()
                self.last_hovered = None 