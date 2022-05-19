#  file: api/converters.py
from datetime import datetime

class DateConverter:
    """
    url 파라미터로 날짜{20220519}가 입력되면 {Year/Month/Date}로 파싱하여 datetime 포맷으로 변환
    """
    regex = '\d{4}\d{1,2}\d{1,2}'
    format = '%Y%m%d'

    def to_python(self, value):
        return datetime.strptime(value, self.format).date()

    def to_url(self, value):
        return value.strftime(self.format)