"""
Analytics window UI for Face Recognition Attendance System.
"""

import pandas as pd
from datetime import datetime, timedelta
from PyQt5.QtWidgets import (
    QWidget, QLabel, QVBoxLayout, QPushButton,
    QTableWidget, QTableWidgetItem, QHBoxLayout,
    QLineEdit, QFileDialog, QDateEdit, QFrame,
    QGridLayout, QHeaderView, QSizePolicy,
    QComboBox, QScrollArea, QTabWidget
)
from PyQt5.QtCore import QDate, Qt
from PyQt5.QtGui import QIcon, QColor, QBrush
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
import numpy as np

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
        
        # Create tab widget
        self.tab_widget = QTabWidget()
        
        # Tab 1: Records view
        self.records_tab = QWidget()
        self.create_records_tab()
        self.tab_widget.addTab(self.records_tab, "Attendance Records")
        
        # Tab 2: Statistics view
        self.statistics_tab = QWidget()
        self.create_statistics_tab()
        self.tab_widget.addTab(self.statistics_tab, "Statistics")
        
        # Tab 3: Student Analysis view
        self.student_tab = QWidget()
        self.create_student_analysis_tab()
        self.tab_widget.addTab(self.student_tab, "Student Analysis")
        
        main_layout.addWidget(self.tab_widget)
        
        # Status bar
        status_bar = QFrame()
        status_bar.setFrameShape(QFrame.StyledPanel)
        status_bar.setStyleSheet("background-color: #f0f0f0; border-radius: 4px; padding: 5px;")
        status_layout = QHBoxLayout(status_bar)
        status_layout.setContentsMargins(10, 5, 10, 5)
        
        self.status_label = QLabel("Ready to analyze attendance data")
        status_layout.addWidget(self.status_label)
        
        main_layout.addWidget(status_bar)
        
        # Connect tab change signal
        self.tab_widget.currentChanged.connect(self.on_tab_changed)
        
        # Load initial data
        self.load_data()

    def create_records_tab(self):
        """Create the records tab content."""
        tab_layout = QVBoxLayout(self.records_tab)
        
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
        
        tab_layout.addWidget(filter_container)
        
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
        tab_layout.addLayout(data_layout)
        
        # Connect signals
        self.filter_btn.clicked.connect(self.load_data)
        self.export_btn.clicked.connect(self.export_csv)
        self.chart_btn.clicked.connect(self.plot_chart)

    def create_statistics_tab(self):
        """Create the statistics tab content."""
        tab_layout = QVBoxLayout(self.statistics_tab)
        
        # Period selection
        period_container = QWidget()
        period_container.setStyleSheet(CARD_STYLE)
        period_layout = QHBoxLayout(period_container)
        
        period_label = QLabel("Report Period:")
        period_layout.addWidget(period_label)
        
        self.period_combo = QComboBox()
        self.period_combo.addItems(["Daily", "Monthly", "Total"])
        self.period_combo.setMinimumHeight(30)
        period_layout.addWidget(self.period_combo)
        
        self.refresh_stats_btn = QPushButton("Refresh Statistics")
        self.refresh_stats_btn.setMinimumHeight(35)
        self.refresh_stats_btn.setStyleSheet(MAIN_BUTTON_STYLE)
        self.refresh_stats_btn.clicked.connect(self.load_statistics)
        period_layout.addWidget(self.refresh_stats_btn)
        
        self.export_stats_btn = QPushButton()
        self.export_stats_btn.setIcon(get_save_icon())
        self.export_stats_btn.setText("Export Stats")
        self.export_stats_btn.setMinimumHeight(35)
        self.export_stats_btn.setStyleSheet(MAIN_BUTTON_STYLE)
        self.export_stats_btn.clicked.connect(self.export_statistics)
        period_layout.addWidget(self.export_stats_btn)
        
        tab_layout.addWidget(period_container)
        
        # Statistics content
        stats_layout = QHBoxLayout()
        
        # Stats table
        stats_table_container = QWidget()
        stats_table_container.setStyleSheet(CARD_STYLE)
        stats_table_layout = QVBoxLayout(stats_table_container)
        
        stats_title = QLabel("Attendance Statistics")
        stats_title.setStyleSheet("font-weight: bold; font-size: 14px;")
        stats_table_layout.addWidget(stats_title)
        
        self.stats_table = QTableWidget()
        self.stats_table.setAlternatingRowColors(True)
        self.stats_table.setStyleSheet("alternate-background-color: #f5f5f5; background-color: white;")
        self.stats_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.stats_table.setEditTriggers(QTableWidget.NoEditTriggers)
        stats_table_layout.addWidget(self.stats_table)
        
        stats_layout.addWidget(stats_table_container)
        
        # Stats chart
        stats_chart_container = QWidget()
        stats_chart_container.setStyleSheet(CARD_STYLE)
        stats_chart_layout = QVBoxLayout(stats_chart_container)
        
        stats_chart_title = QLabel("Attendance Trends")
        stats_chart_title.setStyleSheet("font-weight: bold; font-size: 14px;")
        stats_chart_layout.addWidget(stats_chart_title)
        
        self.stats_chart = FigureCanvas(Figure(figsize=(5, 4)))
        self.stats_ax = self.stats_chart.figure.subplots()
        stats_chart_layout.addWidget(self.stats_chart)
        
        stats_layout.addWidget(stats_chart_container)
        
        tab_layout.addLayout(stats_layout)

    def create_student_analysis_tab(self):
        """Create the student analysis tab content."""
        tab_layout = QVBoxLayout(self.student_tab)
        
        # Student selection
        student_filter = QWidget()
        student_filter.setStyleSheet(CARD_STYLE)
        student_filter_layout = QHBoxLayout(student_filter)
        
        student_id_label = QLabel("Student ID:")
        student_filter_layout.addWidget(student_id_label)
        
        self.student_id_input = QLineEdit()
        self.student_id_input.setPlaceholderText("Enter Student ID")
        self.student_id_input.setMinimumHeight(30)
        student_filter_layout.addWidget(self.student_id_input)
        
        self.load_student_btn = QPushButton("Load Student Analysis")
        self.load_student_btn.setMinimumHeight(35)
        self.load_student_btn.setStyleSheet(MAIN_BUTTON_STYLE)
        self.load_student_btn.clicked.connect(self.load_student_analysis)
        student_filter_layout.addWidget(self.load_student_btn)
        
        tab_layout.addWidget(student_filter)
        
        # Student info and attendance summary
        student_info = QWidget()
        student_info.setStyleSheet(CARD_STYLE)
        student_info_layout = QVBoxLayout(student_info)
        
        self.student_name_label = QLabel("Student Name: Not selected")
        self.student_name_label.setStyleSheet("font-weight: bold; font-size: 16px;")
        student_info_layout.addWidget(self.student_name_label)
        
        info_grid = QGridLayout()
        
        self.student_id_label = QLabel("Student ID: -")
        info_grid.addWidget(self.student_id_label, 0, 0)
        
        self.student_enrolled_label = QLabel("Enrolled on: -")
        info_grid.addWidget(self.student_enrolled_label, 0, 1)
        
        self.student_status_label = QLabel("Status: -")
        info_grid.addWidget(self.student_status_label, 0, 2)
        
        self.student_days_present_label = QLabel("Total Days Present: -")
        info_grid.addWidget(self.student_days_present_label, 1, 0)
        
        self.student_first_attendance_label = QLabel("First Attendance: -")
        info_grid.addWidget(self.student_first_attendance_label, 1, 1)
        
        self.student_last_attendance_label = QLabel("Last Attendance: -")
        info_grid.addWidget(self.student_last_attendance_label, 1, 2)
        
        student_info_layout.addLayout(info_grid)
        
        tab_layout.addWidget(student_info)
        
        # Student attendance history
        student_history_container = QWidget()
        student_history_container.setStyleSheet(CARD_STYLE)
        student_history_layout = QVBoxLayout(student_history_container)
        
        history_title = QLabel("Attendance History")
        history_title.setStyleSheet("font-weight: bold; font-size: 14px;")
        student_history_layout.addWidget(history_title)
        
        history_layout = QHBoxLayout()
        
        # History table
        self.student_history_table = QTableWidget()
        self.student_history_table.setAlternatingRowColors(True)
        self.student_history_table.setStyleSheet("alternate-background-color: #f5f5f5; background-color: white;")
        self.student_history_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.student_history_table.setEditTriggers(QTableWidget.NoEditTriggers)
        history_layout.addWidget(self.student_history_table)
        
        # History chart
        self.student_chart = FigureCanvas(Figure(figsize=(5, 4)))
        self.student_ax = self.student_chart.figure.subplots()
        history_layout.addWidget(self.student_chart)
        
        student_history_layout.addLayout(history_layout)
        
        tab_layout.addWidget(student_history_container)

    def on_tab_changed(self, index):
        """Handle tab changes."""
        if index == 0:  # Records tab
            self.status_label.setText("Viewing attendance records")
            self.load_data()
        elif index == 1:  # Statistics tab
            self.status_label.setText("Viewing attendance statistics")
            self.load_statistics()
        elif index == 2:  # Student tab
            self.status_label.setText("Ready for student analysis")
            # Wait for user to enter student ID before loading data

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

    def load_statistics(self):
        """Load attendance statistics based on selected period."""
        try:
            period = self.period_combo.currentText().lower()
            
            # Get statistics from database
            stats = self.db_manager.get_attendance_statistics(period=period)
            
            # Set up table based on period type
            if period == "daily":
                # Daily stats: Date and Student Count
                self.stats_table.setColumnCount(2)
                self.stats_table.setHorizontalHeaderLabels(["Date", "Student Count"])
                self.stats_table.setRowCount(len(stats))
                
                for row_idx, row_data in enumerate(stats):
                    self.stats_table.setItem(row_idx, 0, QTableWidgetItem(str(row_data[0])))
                    self.stats_table.setItem(row_idx, 1, QTableWidgetItem(str(row_data[1])))
                    
                # Plot daily attendance trend
                if stats:
                    dates = [row[0] for row in stats]
                    counts = [row[1] for row in stats]
                    
                    self.stats_ax.clear()
                    self.stats_ax.bar(dates, counts, color='royalblue')
                    self.stats_ax.set_title("Daily Attendance")
                    self.stats_ax.set_ylabel("Student Count")
                    self.stats_ax.tick_params(axis='x', rotation=45)
                    self.stats_chart.figure.tight_layout()
                    self.stats_chart.draw()
                    
            elif period == "monthly":
                # Monthly stats: Month, Unique Students, Total Records
                self.stats_table.setColumnCount(3)
                self.stats_table.setHorizontalHeaderLabels(["Month", "Unique Students", "Total Entries"])
                self.stats_table.setRowCount(len(stats))
                
                for row_idx, row_data in enumerate(stats):
                    self.stats_table.setItem(row_idx, 0, QTableWidgetItem(str(row_data[0])))
                    self.stats_table.setItem(row_idx, 1, QTableWidgetItem(str(row_data[1])))
                    self.stats_table.setItem(row_idx, 2, QTableWidgetItem(str(row_data[2])))
                
                # Plot monthly attendance trend
                if stats:
                    months = [row[0] for row in stats]
                    unique_students = [row[1] for row in stats]
                    total_records = [row[2] for row in stats]
                    
                    self.stats_ax.clear()
                    width = 0.35
                    x = np.arange(len(months))
                    
                    self.stats_ax.bar(x - width/2, unique_students, width, label='Unique Students', color='royalblue')
                    self.stats_ax.bar(x + width/2, total_records, width, label='Total Records', color='lightcoral')
                    
                    self.stats_ax.set_title("Monthly Attendance")
                    self.stats_ax.set_ylabel("Count")
                    self.stats_ax.set_xticks(x)
                    self.stats_ax.set_xticklabels(months)
                    self.stats_ax.legend()
                    self.stats_ax.tick_params(axis='x', rotation=45)
                    self.stats_chart.figure.tight_layout()
                    self.stats_chart.draw()
                    
            else:  # Total
                # Total stats: Total Days, Total Students, Total Records
                if stats:
                    total_days, total_students, total_records = stats[0]
                    
                    self.stats_table.setColumnCount(3)
                    self.stats_table.setHorizontalHeaderLabels(["Total Days", "Total Students", "Total Records"])
                    self.stats_table.setRowCount(1)
                    
                    self.stats_table.setItem(0, 0, QTableWidgetItem(str(total_days)))
                    self.stats_table.setItem(0, 1, QTableWidgetItem(str(total_students)))
                    self.stats_table.setItem(0, 2, QTableWidgetItem(str(total_records)))
                    
                    # Plot total attendance pie chart
                    self.stats_ax.clear()
                    
                    # Total attendance distribution pie chart
                    labels = ['Days Recorded', 'Students Tracked', 'Total Entries']
                    sizes = [total_days, total_students, total_records]
                    colors = ['gold', 'yellowgreen', 'lightcoral']
                    explode = (0.1, 0, 0)  # explode the 1st slice
                    
                    self.stats_ax.pie(sizes, explode=explode, labels=labels, colors=colors,
                            autopct='%1.1f%%', shadow=True, startangle=140)
                    self.stats_ax.axis('equal')  # Equal aspect ratio ensures pie is drawn as a circle
                    self.stats_ax.set_title("Attendance System Summary")
                    self.stats_chart.figure.tight_layout()
                    self.stats_chart.draw()
                
            self.status_label.setText(f"Loaded {period} attendance statistics")
            
        except Exception as e:
            self.status_label.setText(f"Error loading statistics: {str(e)}")
            print(f"Error loading statistics: {e}")

    def load_student_analysis(self):
        """Load analysis for a specific student."""
        student_id = self.student_id_input.text().strip()
        if not student_id:
            self.status_label.setText("Please enter a Student ID")
            return
            
        try:
            # Get student details
            student_details = self.db_manager.get_user_details(student_id)
            if not student_details:
                self.status_label.setText(f"Student ID {student_id} not found")
                return
                
            # Update student info display
            self.student_name_label.setText(f"Student Name: {student_details['name']}")
            self.student_id_label.setText(f"Student ID: {student_details['id']}")
            self.student_enrolled_label.setText(f"Enrolled on: {student_details['enrollment_date']}")
            
            status_text = "Active" if student_details['active'] else "Inactive"
            status_color = "green" if student_details['active'] else "red"
            self.student_status_label.setText(f"Status: <span style='color:{status_color};'>{status_text}</span>")
            
            # Get attendance summary
            summary = self.db_manager.get_user_attendance_summary(student_id)
            if summary:
                self.student_days_present_label.setText(f"Total Days Present: {summary['days_present']}")
                self.student_first_attendance_label.setText(f"First Attendance: {summary['first_attendance'] or 'N/A'}")
                self.student_last_attendance_label.setText(f"Last Attendance: {summary['last_attendance'] or 'N/A'}")
            
            # Get attendance history
            records = self.db_manager.get_attendance_records(user_id=student_id)
            
            # Display in table
            self.student_history_table.setRowCount(len(records))
            self.student_history_table.setColumnCount(4)
            self.student_history_table.setHorizontalHeaderLabels(["ID", "Name", "Date", "Time"])
            
            for row_idx, row_data in enumerate(records):
                for col_idx, col_data in enumerate(row_data):
                    item = QTableWidgetItem(str(col_data))
                    item.setTextAlignment(Qt.AlignCenter)
                    self.student_history_table.setItem(row_idx, col_idx, item)
            
            # Plot attendance chart
            if records:
                df = pd.DataFrame(records, columns=["ID", "Name", "Date", "Time"])
                
                # Convert date strings to datetime objects
                df['Date'] = pd.to_datetime(df['Date'])
                
                # Group by date and count occurrences
                date_counts = df.groupby(df['Date'].dt.strftime('%Y-%m-%d')).size()
                
                # Sort by date
                date_counts = date_counts.sort_index()
                
                self.student_ax.clear()
                date_counts.plot(kind='line', marker='o', ax=self.student_ax)
                self.student_ax.set_title(f"Attendance History: {student_details['name']}")
                self.student_ax.set_xlabel("Date")
                self.student_ax.set_ylabel("Attendance Count")
                self.student_ax.tick_params(axis='x', rotation=45)
                self.student_chart.figure.tight_layout()
                self.student_chart.draw()
            else:
                self.student_ax.clear()
                self.student_ax.set_title("No attendance records found")
                self.student_chart.draw()
            
            self.status_label.setText(f"Loaded data for {student_details['name']} (ID: {student_id})")
            
        except Exception as e:
            self.status_label.setText(f"Error loading student analysis: {str(e)}")
            print(f"Error loading student analysis: {e}")

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
    
    def export_statistics(self):
        """Export the current statistics to a CSV file."""
        if not self.stats_table.rowCount():
            self.status_label.setText("No statistics to export")
            return
            
        # Get current period
        period = self.period_combo.currentText().lower()
        
        # Set default filename with current date and period
        default_name = f"attendance_statistics_{period}_{datetime.now().strftime('%Y%m%d')}.csv"
        
        path, _ = QFileDialog.getSaveFileName(
            self, "Save CSV", default_name, "CSV Files (*.csv)"
        )
        
        if not path:
            return
            
        try:
            # Extract data from table
            data = []
            headers = []
            
            # Get headers
            for col in range(self.stats_table.columnCount()):
                headers.append(self.stats_table.horizontalHeaderItem(col).text())
            
            # Get data
            for row in range(self.stats_table.rowCount()):
                row_data = []
                for col in range(self.stats_table.columnCount()):
                    item = self.stats_table.item(row, col)
                    row_data.append(item.text() if item else "")
                data.append(row_data)
            
            # Create DataFrame and save to CSV
            df = pd.DataFrame(data, columns=headers)
            df.to_csv(path, index=False)
            self.status_label.setText(f"Statistics exported to {path}")
            
        except Exception as e:
            self.status_label.setText(f"Error exporting statistics: {str(e)}")
            print(f"Error exporting statistics: {e}")

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