"""
Analytics window UI for Face Recognition Attendance System.
"""

import pandas as pd
from datetime import datetime
from PyQt5.QtWidgets import (
    QWidget, QLabel, QVBoxLayout, QPushButton,
    QTableWidget, QTableWidgetItem, QHBoxLayout,
    QLineEdit, QFileDialog, QDateEdit, QFrame,
    QGridLayout, QHeaderView, QSizePolicy,
    QComboBox, QScrollArea
)
from PyQt5.QtCore import QDate, Qt
from PyQt5.QtGui import QIcon, QColor, QBrush
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.pyplot as plt

from src.database.db_manager import DatabaseManager
from src.ui.style import MAIN_STYLE, TITLE_STYLE, CARD_STYLE, SECONDARY_BUTTON_STYLE, SUCCESS_BUTTON_STYLE, MAIN_BUTTON_STYLE
from src.ui.icons import get_chart_icon, get_save_icon

class AnalyticsWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Attendance Analytics")
        self.setMinimumSize(1000, 700)
        self.setStyleSheet(MAIN_STYLE)

        self.db_manager = DatabaseManager()
        
        # Main layout
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(15)
        
        # Title
        title_layout = QHBoxLayout()
        title_label = QLabel("Attendance Analytics")
        title_label.setStyleSheet(TITLE_STYLE)
        title_layout.addWidget(title_label)
        
        main_layout.addLayout(title_layout)
        
        # Separator line
        line = QFrame()
        line.setFrameShape(QFrame.HLine)
        line.setFrameShadow(QFrame.Sunken)
        line.setStyleSheet("background-color: #d1d1d1;")
        main_layout.addWidget(line)

        # Filter section
        filter_container = QWidget()
        filter_container.setStyleSheet(CARD_STYLE)
        filter_layout = QGridLayout(filter_container)
        filter_layout.setVerticalSpacing(10)
        filter_layout.setHorizontalSpacing(15)
        
        # Date filter
        date_label = QLabel("Date:")
        filter_layout.addWidget(date_label, 0, 0)
        
        self.date_filter = QDateEdit(calendarPopup=True)
        self.date_filter.setDate(QDate.currentDate())
        self.date_filter.setMinimumHeight(30)
        filter_layout.addWidget(self.date_filter, 0, 1)
        
        # Student ID filter
        id_label = QLabel("Student ID:")
        filter_layout.addWidget(id_label, 0, 2)
        
        self.id_filter = QLineEdit()
        self.id_filter.setPlaceholderText("Enter ID (optional)")
        self.id_filter.setMinimumHeight(30)
        filter_layout.addWidget(self.id_filter, 0, 3)
        
        # Chart type selector
        chart_type_label = QLabel("Chart Type:")
        filter_layout.addWidget(chart_type_label, 0, 4)
        
        self.chart_type_combo = QComboBox()
        self.chart_type_combo.addItems(["Bar Chart", "Line Chart", "Pie Chart"])
        self.chart_type_combo.setMinimumHeight(30)
        filter_layout.addWidget(self.chart_type_combo, 0, 5)
        
        # Buttons
        self.filter_btn = QPushButton()
        self.filter_btn.setIcon(get_chart_icon())
        self.filter_btn.setText("Apply Filter")
        self.filter_btn.setMinimumHeight(35)
        self.filter_btn.setStyleSheet(MAIN_BUTTON_STYLE)
        filter_layout.addWidget(self.filter_btn, 1, 1)
        
        self.export_btn = QPushButton()
        self.export_btn.setIcon(get_save_icon())
        self.export_btn.setText("Export to CSV")
        self.export_btn.setMinimumHeight(35)
        self.export_btn.setStyleSheet(MAIN_BUTTON_STYLE)
        filter_layout.addWidget(self.export_btn, 1, 3)
        
        self.chart_btn = QPushButton()
        self.chart_btn.setIcon(get_chart_icon())
        self.chart_btn.setText("Generate Chart")
        self.chart_btn.setMinimumHeight(35)
        self.chart_btn.setStyleSheet(MAIN_BUTTON_STYLE)
        filter_layout.addWidget(self.chart_btn, 1, 5)
        
        main_layout.addWidget(filter_container)
        
        # Data section split into table and chart
        data_layout = QHBoxLayout()
        
        # Table section
        table_container = QWidget()
        table_container.setStyleSheet(CARD_STYLE)
        table_layout = QVBoxLayout(table_container)
        
        table_title = QLabel("Attendance Records")
        table_title.setStyleSheet("font-weight: bold; font-size: 14px;")
        table_layout.addWidget(table_title)
        
        self.record_count_label = QLabel("No records found")
        table_layout.addWidget(self.record_count_label)
        
        self.table = QTableWidget()
        self.table.setAlternatingRowColors(True)
        self.table.setStyleSheet("alternate-background-color: #f5f5f5; background-color: white;")
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table.setEditTriggers(QTableWidget.NoEditTriggers)  # Make table read-only
        table_layout.addWidget(self.table)
        
        data_layout.addWidget(table_container)
        
        # Chart section
        chart_container = QWidget()
        chart_container.setStyleSheet(CARD_STYLE)
        chart_layout = QVBoxLayout(chart_container)
        
        chart_title = QLabel("Attendance Visualization")
        chart_title.setStyleSheet("font-weight: bold; font-size: 14px;")
        chart_layout.addWidget(chart_title)
        
        # Create a figure for plotting
        plt.style.use('ggplot')  # Use a nicer style
        self.chart = FigureCanvas(Figure(figsize=(5, 4)))
        self.ax = self.chart.figure.subplots()
        chart_layout.addWidget(self.chart)
        
        data_layout.addWidget(chart_container)
        main_layout.addLayout(data_layout)
        
        # Status bar
        status_bar = QFrame()
        status_bar.setFrameShape(QFrame.StyledPanel)
        status_bar.setStyleSheet("background-color: #f0f0f0; border-radius: 4px; padding: 5px;")
        status_layout = QHBoxLayout(status_bar)
        status_layout.setContentsMargins(10, 5, 10, 5)
        
        self.status_label = QLabel("Ready to analyze attendance data")
        status_layout.addWidget(self.status_label)
        
        main_layout.addWidget(status_bar)
        
        # Connect signals
        self.filter_btn.clicked.connect(self.load_data)
        self.export_btn.clicked.connect(self.export_csv)
        self.chart_btn.clicked.connect(self.plot_chart)
        
        # Load initial data
        self.load_data()

    def load_data(self):
        """Load attendance data based on filters."""
        self.status_label.setText("Loading data...")
        
        try:
            date_str = self.date_filter.date().toString("yyyy-MM-dd")
            student_id = self.id_filter.text().strip()
            
            # Get data from database
            records = self.db_manager.get_attendance_records(
                date=date_str if date_str else None,
                user_id=student_id if student_id else None
            )
            
            # Display data in table
            self.table.setRowCount(len(records))
            self.table.setColumnCount(4)
            self.table.setHorizontalHeaderLabels(["ID", "Name", "Date", "Time"])
            
            for row_idx, row_data in enumerate(records):
                for col_idx, col_data in enumerate(row_data):
                    item = QTableWidgetItem(str(col_data))
                    # Center align the text
                    item.setTextAlignment(Qt.AlignCenter)
                    self.table.setItem(row_idx, col_idx, item)
            
            # Convert to DataFrame for further processing
            self.df = pd.DataFrame(records, columns=["ID", "Name", "Date", "Time"])
            
            # Update record count label
            record_count = len(records)
            self.record_count_label.setText(f"Found {record_count} attendance record(s)")
            
            # Update status
            self.status_label.setText(f"Loaded {record_count} records" + 
                                     (f" for date: {date_str}" if date_str else "") +
                                     (f" and ID: {student_id}" if student_id else ""))
            
            # Generate chart automatically if we have data
            if not self.df.empty:
                self.plot_chart()
            else:
                self.clear_chart()
                
        except Exception as e:
            self.status_label.setText(f"Error loading data: {str(e)}")
            print(f"Error loading data: {e}")

    def export_csv(self):
        """Export the current data to a CSV file."""
        if not hasattr(self, "df") or self.df.empty:
            self.status_label.setText("No data to export")
            return
            
        # Set default filename with current date
        default_name = f"attendance_{datetime.now().strftime('%Y%m%d')}.csv"
        
        path, _ = QFileDialog.getSaveFileName(
            self, "Save CSV", default_name, "CSV Files (*.csv)"
        )
        
        if path:
            try:
                self.df.to_csv(path, index=False)
                self.status_label.setText(f"Data exported to {path}")
            except Exception as e:
                self.status_label.setText(f"Error exporting data: {str(e)}")

    def plot_chart(self):
        """Plot attendance statistics chart."""
        if not hasattr(self, "df") or self.df.empty:
            self.status_label.setText("No data to visualize")
            return
            
        try:
            chart_type = self.chart_type_combo.currentText()
            
            self.ax.clear()
            
            # Group by date and count attendance
            if chart_type == "Pie Chart":
                if 'Name' in self.df.columns:
                    # Count attendance by student name
                    summary = self.df['Name'].value_counts()
                    summary.plot(kind="pie", ax=self.ax, autopct='%1.1f%%', startangle=90)
                    self.ax.set_ylabel('')  # Hide ylabel
                    self.ax.set_title("Attendance by Student")
            else:
                # Default to date-based charts
                summary = self.df.groupby("Date").size()
                
                if chart_type == "Line Chart":
                    summary.plot(kind="line", marker='o', ax=self.ax)
                    self.ax.set_title("Attendance Trend")
                else:  # Bar Chart (default)
                    summary.plot(kind="bar", ax=self.ax)
                    self.ax.set_title("Attendance Count by Date")
                
                self.ax.set_xlabel("Date")
                self.ax.set_ylabel("Count")
            
            # Improve appearance
            self.chart.figure.tight_layout()
            self.chart.draw()
            
            self.status_label.setText(f"Generated {chart_type}")
            
        except Exception as e:
            self.status_label.setText(f"Error creating chart: {str(e)}")
            print(f"Error creating chart: {e}")
    
    def clear_chart(self):
        """Clear the current chart."""
        self.ax.clear()
        self.ax.set_title("No data to display")
        self.chart.draw()
        
    def closeEvent(self, event):
        """Handle window close event."""
        self.db_manager.close()
        event.accept()