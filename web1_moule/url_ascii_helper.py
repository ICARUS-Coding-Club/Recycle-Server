"""
url 퍼센트 인코딩을 한글로 변환하거나 한글을 퍼센트 인코딩으로 변환하는 유틸 프로그램

"""
from urllib.parse import quote
from urllib.parse import unquote


class PercentStrHelper:

    @staticmethod
    def percent_encode(input_string: str, encoding='cp949') -> str:
        """
        한글을 url 퍼센트 인코딩 문자열로 인코딩합니다.
        :param input_string: 한글
        :param encoding:
        :return:
        """

        return quote(input_string, encoding=encoding)

    @staticmethod
    def percent_decode(input_string: str, encoding='cp949') -> str:
        """
        url 퍼센트 인코딩 문자열을 한글로 디코딩합니다.
        :param input_string: url 퍼센트 인코딩 문자열
        :param encoding:
        :return:
        """

        return unquote(input_string, encoding=encoding)
