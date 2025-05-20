from PyQt6.QtWidgets import QVBoxLayout
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import pandas as pd

class DrilldownBarChartWidget(FigureCanvas):
    def __init__(self, df, parent=None):
        self.df = df
        self.level = 'month'  # can be 'month', 'week', 'day'
        self.current = None   # stores current month or week for drilldown
        self.fig = Figure(figsize=(6, 3))
        super().__init__(self.fig)
        self.setParent(parent)
        self.plot_month()
        self.mpl_connect('button_press_event', self.on_click)

    def plot_month(self):
        self.fig.clear()
        ax = self.fig.add_subplot(111)
        df_month = self.df.copy()
        df_month['YearMonth'] = df_month['Date'].dt.to_period('M')
        grouped = df_month.groupby('YearMonth')['Amount'].sum()
        bars = ax.bar([str(p) for p in grouped.index], grouped.values, color='#4a90e2')
        ax.set_title('Total by Month')
        ax.set_ylabel('Amount')
        ax.set_xlabel('Month')
        ax.tick_params(axis='x', rotation=45)
        self.level = 'month'
        self.current = None
        self.fig.tight_layout()
        self.draw()
        self.bars = bars
        self.bar_labels = list(grouped.index)

    def plot_week(self, yearmonth):
        self.fig.clear()
        ax = self.fig.add_subplot(111)
        df_month = self.df[self.df['Date'].dt.to_period('M') == yearmonth]
        df_month['Week'] = df_month['Date'].dt.isocalendar().week
        grouped = df_month.groupby('Week')['Amount'].sum()
        bars = ax.bar([f"Week {w}" for w in grouped.index], grouped.values, color='#50e3c2')
        ax.set_title(f'Total by Week: {yearmonth}')
        ax.set_ylabel('Amount')
        ax.set_xlabel('Week')
        self.level = 'week'
        self.current = yearmonth
        self.fig.tight_layout()
        self.draw()
        self.bars = bars
        self.bar_labels = list(grouped.index)

    def plot_day(self, yearmonth, week):
        self.fig.clear()
        ax = self.fig.add_subplot(111)
        df_month = self.df[self.df['Date'].dt.to_period('M') == yearmonth]
        df_week = df_month[df_month['Date'].dt.isocalendar().week == week]
        grouped = df_week.groupby(df_week['Date'].dt.day)['Amount'].sum()
        bars = ax.bar([str(d) for d in grouped.index], grouped.values, color='#f5a623')
        ax.set_title(f'Total by Day: {yearmonth}, Week {week}')
        ax.set_ylabel('Amount')
        ax.set_xlabel('Day')
        self.level = 'day'
        self.current = (yearmonth, week)
        self.fig.tight_layout()
        self.draw()
        self.bars = bars
        self.bar_labels = list(grouped.index)

    def on_click(self, event):
        if event.inaxes is None or not hasattr(self, 'bars'):
            return
        for i, bar in enumerate(self.bars):
            if bar.contains(event)[0]:
                if self.level == 'month':
                    yearmonth = self.bar_labels[i]
                    self.plot_week(yearmonth)
                elif self.level == 'week':
                    week = self.bar_labels[i]
                    yearmonth = self.current
                    self.plot_day(yearmonth, week)
                elif self.level == 'day':
                    self.plot_month()
                break 