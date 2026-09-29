import sys
from datetime import timedelta, date
import holidays
from PySide6.QtWidgets import (QApplication, QWidget, QVBoxLayout, QHBoxLayout, 
                                QLabel, QDateEdit, QCheckBox, QPushButton, QFrame, QLineEdit)
from PySide6.QtCore import QDate, Qt

CUTE_STYLE = """
QWidget#mainWindow {
    background-color: #FFF2F5;
    font-family: 'Malgun Gothic', 'Apple SD Gothic Neo', sans-serif;
}

QFrame#card {
    background-color: #FFFFFF;
    border-radius: 20px;
    border: 2px solid #FFD1DC;
}

QLabel#titleLabel {
    font-size: 20px;
    font-weight: bold;
    color: #FF6B8B;
}

QLabel#sectionLabel {
    font-size: 13px;
    font-weight: bold;
    color: #7B61FF;
}

QLineEdit#titleInput {
    background-color: #F0F4FF;
    border: 2px solid #ADC4FF;
    border-radius: 10px;
    padding: 6px 10px;
    font-size: 13px;
    font-weight: bold;
    color: #4A4A4A;
}

QDateEdit {
    background-color: #F0F4FF;
    border: 2px solid #ADC4FF;
    border-radius: 10px;
    padding: 6px 10px;
    font-size: 13px;
    font-weight: bold;
    color: #4A4A4A;
}

QDateEdit:disabled {
    background-color: #EAEAEA;
    border: 2px solid #CCCCCC;
    color: #999999;
}

QCalendarWidget {
    min-width: 320px;
    min-height: 260px;
}

QCalendarWidget QWidget#qt_calendar_navigationbar {
    background-color: #FFD1DC;
    min-height: 36px;
}

QCalendarWidget QToolButton {
    color: #4A4A4A;
    font-weight: bold;
    border: none;
    background-color: transparent;
    padding: 0px 8px;
}

QCalendarWidget QSpinBox {
    background-color: #FFFFFF;
    border: 1px solid #000000;
    border-radius: 4px;
    font-weight: bold;
    color: #000000;
    min-width: 85px;
    max-width: 85px;
    height: 26px;
    padding-right: 20px;
    margin-left: 5px;
}

QCalendarWidget QSpinBox::up-button, QCalendarWidget QSpinBox::down-button {
    width: 18px;
}

QCheckBox {
    font-size: 12px;
    font-weight: bold;
    color: #555555;
    spacing: 6px;
}

QCheckBox::indicator {
    width: 16px;
    height: 16px;
    border-radius: 5px;
    border: 2px solid #FFB7B2;
    background-color: #FFFFFF;
}

QCheckBox::indicator:checked {
    background-color: #FF8E9E;
    border: 2px solid #FF8E9E;
}

QPushButton#calcBtn {
    background-color: #FFB3C6;
    color: #FFFFFF;
    font-size: 15px;
    font-weight: bold;
    border-radius: 14px;
    padding: 10px;
    border: none;
}

QPushButton#calcBtn:hover {
    background-color: #FF8FAB;
}

QFrame#resultCard {
    background-color: #E8F8F5;
    border-radius: 14px;
    border: 2px solid #A3E4D7;
}

QLabel#resultLabel {
    font-size: 14px;
    font-weight: bold;
    color: #16A085;
}
"""

class CuteDDayCalculator(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        
    def initUI(self):
        self.setObjectName("mainWindow")
        self.setWindowTitle('D-Day 계산기')
        self.setFixedSize(420, 600)
        self.setStyleSheet(CUTE_STYLE)
        
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(18, 18, 18, 18)
        
        card = QFrame()
        card.setObjectName("card")
        card_layout = QVBoxLayout(card)
        card_layout.setContentsMargins(18, 18, 18, 18)
        card_layout.setSpacing(10)
        
        title_label = QLabel('D-Day 계산기')
        title_label.setObjectName("titleLabel")
        title_label.setAlignment(Qt.AlignCenter)
        card_layout.addWidget(title_label)
        
        title_input_label = QLabel('D-Day 제목')
        title_input_label.setObjectName("sectionLabel")
        card_layout.addWidget(title_input_label)
        
        self.title_input = QLineEdit()
        self.title_input.setObjectName("titleInput")
        self.title_input.setPlaceholderText('예: 중간고사 남은 일, 방학 남은 일, 커플 된지')
        card_layout.addWidget(self.title_input)
        
        start_title = QLabel('시작 날짜')
        start_title.setObjectName("sectionLabel")
        card_layout.addWidget(start_title)
        
        start_layout = QHBoxLayout()
        self.start_date_edit = QDateEdit()
        self.start_date_edit.setCalendarPopup(True)
        self.start_date_edit.setDate(QDate.currentDate())
        start_layout.addWidget(self.start_date_edit)
        card_layout.addLayout(start_layout)
        
        self.today_check = QCheckBox('오늘부터 시작할래요!')
        self.today_check.setChecked(True)
        self.today_check.toggled.connect(self.toggle_start_date)
        card_layout.addWidget(self.today_check)
        self.start_date_edit.setEnabled(False)
        
        end_title = QLabel('끝낼 날짜')
        end_title.setObjectName("sectionLabel")
        card_layout.addWidget(end_title)
        
        end_layout = QHBoxLayout()
        self.end_date_edit = QDateEdit()
        self.end_date_edit.setCalendarPopup(True)
        self.end_date_edit.setDate(QDate.currentDate().addDays(7))
        end_layout.addWidget(self.end_date_edit)
        card_layout.addLayout(end_layout)
        
        self.no_end_date_check = QCheckBox('목표 날짜 없음 (오늘까지 D+Day 경과일 계산)')
        self.no_end_date_check.toggled.connect(self.toggle_end_date)
        card_layout.addWidget(self.no_end_date_check)
        
        self.include_first_day_check = QCheckBox('시작한 날짜부터 1일로 포함하기 (기념일 방식)')
        card_layout.addWidget(self.include_first_day_check)
        
        self.exclude_weekend_check = QCheckBox('주말 제외')
        self.exclude_holiday_check = QCheckBox('공휴일 제외')
        card_layout.addWidget(self.exclude_weekend_check)
        card_layout.addWidget(self.exclude_holiday_check)
        
        self.calc_btn = QPushButton('D-Day 계산하기')
        self.calc_btn.setObjectName("calcBtn")
        self.calc_btn.setCursor(Qt.PointingHandCursor)
        self.calc_btn.clicked.connect(self.calculate_dday)
        card_layout.addWidget(self.calc_btn)
        
        result_card = QFrame()
        result_card.setObjectName("resultCard")
        result_layout = QVBoxLayout(result_card)
        result_layout.setContentsMargins(12, 10, 12, 10)
        
        self.result_label = QLabel('버튼을 눌러 D-Day를 확인해보세요.')
        self.result_label.setObjectName("resultLabel")
        self.result_label.setAlignment(Qt.AlignCenter)
        self.result_label.setWordWrap(True)
        result_layout.addWidget(self.result_label)
        
        card_layout.addWidget(result_card)
        main_layout.addWidget(card)
        self.setLayout(main_layout)
        
    def toggle_start_date(self, checked):
        if checked:
            self.start_date_edit.setDate(QDate.currentDate())
            self.start_date_edit.setEnabled(False)
        else:
            self.start_date_edit.setEnabled(True)

    def toggle_end_date(self, checked):
        if checked:
            self.end_date_edit.setEnabled(False)
        else:
            self.end_date_edit.setEnabled(True)
            
    def _calculate_effective_days(self, start_date, end_date, exclude_weekend, exclude_holiday):
        kr_holidays = holidays.KR(years=range(start_date.year, end_date.year + 1))
        current_date = start_date
        total_days = 0
        
        while current_date <= end_date:
            is_weekend = current_date.weekday() >= 5
            is_holiday = current_date in kr_holidays
            
            if (exclude_weekend and is_weekend) or (exclude_holiday and is_holiday):
                current_date += timedelta(days=1)
                continue
                
            total_days += 1
            current_date += timedelta(days=1)
        return total_days

    def calculate_dday(self):
        start_date = self.start_date_edit.date().toPython()
        title_text = self.title_input.text().strip()
        title_prefix = f"[{title_text}] " if title_text else ""
        
        include_first_day = self.include_first_day_check.isChecked()
        exclude_weekend = self.exclude_weekend_check.isChecked()
        exclude_holiday = self.exclude_holiday_check.isChecked()
        no_end_date = self.no_end_date_check.isChecked()
        
        # 끝나는 날짜 지정 여부에 따른 end_date 설정
        if no_end_date:
            end_date = date.today()
        else:
            end_date = self.end_date_edit.date().toPython()
            
        if start_date > end_date:
            self.result_label.setText("앗! 시작 날짜가 끝나는 날짜보다 이후일 수 없어요 🥺")
            return
            
        total_days = self._calculate_effective_days(start_date, end_date, exclude_weekend, exclude_holiday)
        
        if no_end_date:
            if include_first_day:
                count_day = total_days
                self.result_label.setText(f"{title_prefix}오늘로 {count_day}일째입니다! (D+{count_day})")
            else:
                count_day = total_days - 1
                self.result_label.setText(f"{title_prefix}시작일로부터 {count_day}일 지났습니다! (D+{count_day})")
        else:
            if include_first_day:
                d_day = total_days
                self.result_label.setText(f"{title_prefix}총 {d_day}일 남았습니다!")
            else:
                d_day = total_days - 1
                if d_day == 0:
                    self.result_label.setText(f"{title_prefix}오늘이 바로 D-Day입니다!")
                else:
                    self.result_label.setText(f"{title_prefix}D-{d_day}일 남았습니다.")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = CuteDDayCalculator()
    ex.show()
    sys.exit(app.exec())
