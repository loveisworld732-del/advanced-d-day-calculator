# Import necessary modules and libraries (필요한 모듈 및 라이브러리 임포트)
import sys
from datetime import timedelta, date
import holidays
from PySide6.QtWidgets import (QApplication, QWidget, QVBoxLayout, QHBoxLayout, 
                                QLabel, QDateEdit, QCheckBox, QPushButton, QFrame, QLineEdit)
from PySide6.QtCore import QDate, Qt

# Define stylesheet for cute UI design (귀여운 파스텔톤 UI 디자인을 위한 QSS 스타일시트 정의)
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
    font-size: 15px;
    font-weight: bold;
    color: #FF6B8B;
}

QLabel#sectionLabel {
    font-size: 11px;
    font-weight: bold;
    color: #7B61FF;
}

QLineEdit#titleInput {
    background-color: #F0F4FF;
    border: 2px solid #ADC4FF;
    border-radius: 10px;
    padding: 5px 8px;
    font-size: 11px;
    font-weight: bold;
    color: #4A4A4A;
}

QDateEdit {
    background-color: #F0F4FF;
    border: 2px solid #ADC4FF;
    border-radius: 10px;
    padding: 5px 8px;
    font-size: 11px;
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
    font-size: 10px;
    font-weight: bold;
    color: #555555;
    spacing: 5px;
}

QCheckBox::indicator {
    width: 13px;
    height: 13px;
    border-radius: 4px;
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
    font-size: 13px;
    font-weight: bold;
    border-radius: 12px;
    padding: 7px;
    border: none;
}

QPushButton#calcBtn:hover {
    background-color: #FF8FAB;
}
 
QFrame#resultCard {
    background-color: #E8F8F5;
    border-radius: 12px;
    border: 2px solid #A3E4D7;
}

QLabel#resultLabel {
    font-size: 11px;
    font-weight: bold;
    color: #16A085;
}
"""

# Main D-Day Calculator Widget Class (메인 D-Day 계산기 위젯 클래스)
class CuteDDayCalculator(QWidget):
    def __init__(self):
        # Initialize widget and layout setup (위젯 초기화 및 UI 설정 함수 호출)
        super().__init__()
        self.initUI()
        
    def initUI(self):
        # Set window properties and layout (창 기본 속성 및 메인 레이아웃 설정)
        self.setObjectName("mainWindow")
        self.setWindowTitle('(D-Day Calculator)\nD-Day 계산기')
        self.setFixedSize(460, 690)
        self.setStyleSheet(CUTE_STYLE)
        
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(16, 16, 16, 16)
        
        # Create card frame container (콘텐츠 배치를 위한 카드 프레임 생성)
        card = QFrame()
        card.setObjectName("card")
        card_layout = QVBoxLayout(card)
        card_layout.setContentsMargins(16, 16, 16, 16)
        card_layout.setSpacing(6)
        
        # Title label widget (앱 타이틀 라벨 생성)
        title_label = QLabel('(D-Day Calculator)\nD-Day 계산기')
        title_label.setObjectName("titleLabel")
        title_label.setAlignment(Qt.AlignCenter)
        card_layout.addWidget(title_label)
        
        # Title input section (D-Day 제목 입력 섹션)
        title_input_label = QLabel('(D-Day Title)\nD-Day 제목')
        title_input_label.setObjectName("sectionLabel")
        card_layout.addWidget(title_input_label)
        
        self.title_input = QLineEdit()
        self.title_input.setObjectName("titleInput")
        self.title_input.setPlaceholderText('Ex: Midterm, Vacation, Couple (예: 중간고사, 방학, 커플 기념일)')
        card_layout.addWidget(self.title_input)
        
        # Start date selection section (시작 날짜 선택 섹션)
        start_title = QLabel('(Start Date)\n시작 날짜')
        start_title.setObjectName("sectionLabel")
        card_layout.addWidget(start_title)
        
        start_layout = QHBoxLayout()
        self.start_date_edit = QDateEdit()
        self.start_date_edit.setCalendarPopup(True)
        self.start_date_edit.setDate(QDate.currentDate())
        start_layout.addWidget(self.start_date_edit)
        card_layout.addLayout(start_layout)
        
        # Today start checkbox option (오늘부터 시작 체크박스 옵션)
        self.today_check = QCheckBox('(Start from today!)\n오늘부터 시작할래요!')
        self.today_check.setChecked(True)
        self.today_check.toggled.connect(self.toggle_start_date)
        card_layout.addWidget(self.today_check)
        self.start_date_edit.setEnabled(False)
        
        # End date selection section (끝낼 날짜 선택 섹션)
        end_title = QLabel('(End Date)\n끝낼 날짜')
        end_title.setObjectName("sectionLabel")
        card_layout.addWidget(end_title)
        
        end_layout = QHBoxLayout()
        self.end_date_edit = QDateEdit()
        self.end_date_edit.setCalendarPopup(True)
        self.end_date_edit.setDate(QDate.currentDate().addDays(7))
        end_layout.addWidget(self.end_date_edit)
        card_layout.addLayout(end_layout)
        
        # Option checkboxes for calculation rules (계산 규칙 설정 체크박스들)
        self.no_end_date_check = QCheckBox('(No target date - Calculate elapsed days)\n목표 날짜 없음 (오늘까지 경과일 계산)')
        self.no_end_date_check.toggled.connect(self.toggle_end_date)
        card_layout.addWidget(self.no_end_date_check)
        
        self.include_first_day_check = QCheckBox('(Include start date as day 1 - Anniversary style)\n시작한 날짜부터 1일로 포함하기 (기념일 방식)')
        card_layout.addWidget(self.include_first_day_check)
        
        self.exclude_weekend_check = QCheckBox('(Exclude weekends)\n주말 제외')
        self.exclude_holiday_check = QCheckBox('(Exclude holidays)\n공휴일 제외')
        card_layout.addWidget(self.exclude_weekend_check)
        card_layout.addWidget(self.exclude_holiday_check)
        
        # Calculation button widget (D-Day 계산 실행 버튼)
        self.calc_btn = QPushButton('(Calculate D-Day)\nD-Day 계산하기')
        self.calc_btn.setObjectName("calcBtn")
        self.calc_btn.setCursor(Qt.PointingHandCursor) 
        self.calc_btn.clicked.connect(self.calculate_dday)
        card_layout.addWidget(self.calc_btn)
        
        # Result display card frame (계산 결과 표시 카드 프레임)
        result_card = QFrame()
        result_card.setObjectName("resultCard")
        result_layout = QVBoxLayout(result_card)
        result_layout.setContentsMargins(10, 8, 10, 8)
        
        self.result_label = QLabel('(Click the button to check D-Day.)\n버튼을 눌러 D-Day를 확인해보세요.')
        self.result_label.setObjectName("resultLabel")
        self.result_label.setAlignment(Qt.AlignCenter)
        self.result_label.setWordWrap(True)
        result_layout.addWidget(self.result_label)
        
        card_layout.addWidget(result_card)
        main_layout.addWidget(card)
        self.setLayout(main_layout)
        
    # Toggle start date edit enabled status based on checkbox (체크박스 상태에 따른 시작 날짜 활성화/비활성화 토글 메서드)
    def toggle_start_date(self, checked):
        if checked:
            self.start_date_edit.setDate(QDate.currentDate())
            self.start_date_edit.setEnabled(False)
        else:
            self.start_date_edit.setEnabled(True)

    # Toggle end date edit enabled status based on checkbox (체크박스 상태에 따른 종료 날짜 활성화/비활성화 토글 메서드)
    def toggle_end_date(self, checked):
        if checked:
            self.end_date_edit.setEnabled(False)
        else:
            self.end_date_edit.setEnabled(True)
            
    # Calculate effective days excluding weekends and holidays if checked (주말 및 공휴일을 제외한 유효 일수 계산 헬퍼 메서드)
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

    # Main D-Day calculation logic triggered by button click (버튼 클릭 시 실행되는 메인 D-Day 계산 로직 메서드)
    def calculate_dday(self):
        start_date = self.start_date_edit.date().toPython()
        title_text = self.title_input.text().strip()
        title_prefix = f"[{title_text}] " if title_text else ""
        
        include_first_day = self.include_first_day_check.isChecked()
        exclude_weekend = self.exclude_weekend_check.isChecked()
        exclude_holiday = self.exclude_holiday_check.isChecked()
        no_end_date = self.no_end_date_check.isChecked()
        
        # Set end date based on whether end date is specified (종료일 지정 여부에 따른 end_date 변수 설정)
        if no_end_date:
            end_date = date.today()
        else:
            end_date = self.end_date_edit.date().toPython()
            
        if start_date > end_date:
            self.result_label.setText("(Oops! Start date cannot be after end date 🥺)\n앗! 시작 날짜가 끝나는 날짜보다 이후일 수 없어요 🥺")
            return
            
        total_days = self._calculate_effective_days(start_date, end_date, exclude_weekend, exclude_holiday)
        
        if no_end_date:
            if include_first_day:
                count_day = total_days
                self.result_label.setText(f"({title_prefix}Today is day {count_day}! (D+{count_day}))\n{title_prefix}오늘로 {count_day}일째입니다! (D+{count_day})")
            else:
                count_day = total_days - 1
                self.result_label.setText(f"({title_prefix}{count_day} days passed since start! (D+{count_day}))\n{title_prefix}시작일로부터 {count_day}일 지났습니다! (D+{count_day})")
        else:
            if include_first_day:
                d_day = total_days
                self.result_label.setText(f"({title_prefix}Total {d_day} days remaining!)\n{title_prefix}총 {d_day}일 남았습니다!")
            else:
                d_day = total_days - 1
                if d_day == 0:
                    self.result_label.setText(f"({title_prefix}Today is the D-Day!)\n{title_prefix}오늘이 바로 D-Day입니다!")
                else:
                    self.result_label.setText(f"({title_prefix}{d_day} days left.)\n{title_prefix}D-{d_day}일 남았습니다.")

# Application execution entry point (파이썬 애플리케이션 실행 진입점)
if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = CuteDDayCalculator()
    ex.show()
    sys.exit(app.exec())
