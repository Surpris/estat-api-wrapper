"""stats_table_info

Parameters for the e-Stat API that retrieves statistical table information.
"""

from dataclasses import dataclass
from typing import Literal, Optional


@dataclass
class StatsTableParameters:
    """
    e-Stat APIの「統計表情報取得」機能のパラメータを管理するクラスです。

    Attributes:
        stats_code (Optional[str]): 任意パラメータ。政府統計コード（5桁）を指定します。
        search_word (Optional[str]): 任意パラメータ。検索キーワードをUTF-8でURLエンコードして指定します。
        search_kind (Literal['1', '2']): 任意パラメータ。検索種別を '1'（AND）または '2'（OR）で指定します。
                                      デフォルトは '1' です。
        start_position (Optional[int]): 任意パラメータ。データの取得開始位置を1からの連番で指定します。
        limit (Optional[int]): 任意パラメータ。データの取得件数を指定します。
        updated_date (Optional[str]): 任意パラメータ。更新日を "YYYYMM" または "YYYYMMDD" 形式で指定します。
        stats_field (Optional[str]): 任意パラメータ。統計分野（大分類）コードを指定します。
        collect_area (Optional[str]): 任意パラメータ。統計作成地域コードを指定します。
        explanation_get_flg (Literal['Y', 'N']): 任意パラメータ。解説情報取得フラグ。
                                                'Y' を指定すると、統計表の解説情報を取得します。
        survey_years (Optional[str]): 任意パラメータ。調査年月を "YYYY" または "YYYYMM" 形式で指定します。
        open_years (Optional[str]): 任意パラメータ。公開年月日を "YYYY" または "YYYYMM" 形式で指定します。
        report_type (Literal['D', 'H', 'M', 'Y']): 任意パラメータ。統計の報告種類を指定します。
                                                 'D': 日次, 'H': 半期, 'M': 月次, 'Y': 年次
    """

    def __init__(
        self,
        stats_code: Optional[str] = None,
        search_word: Optional[str] = None,
        search_kind: Literal['1', '2'] = '1',
        start_position: Optional[int] = None,
        limit: Optional[int] = None,
        updated_date: Optional[str] = None,
        stats_field: Optional[str] = None,
        collect_area: Optional[str] = None,
        explanation_get_flg: Literal['Y', 'N'] = 'N',
        survey_years: Optional[str] = None,
        open_years: Optional[str] = None,
        report_type: Optional[Literal['D', 'H', 'M', 'Y']] = None,
    ):
        self.stats_code = stats_code
        self.search_word = search_word
        self.search_kind = search_kind
        self.start_position = start_position
        self.limit = limit
        self.updated_date = updated_date
        self.stats_field = stats_field
        self.collect_area = collect_area
        self.explanation_get_flg = explanation_get_flg
        self.survey_years = survey_years
        self.open_years = open_years
        self.report_type = report_type


# --- 使用例 ---
if __name__ == '__main__':
    # 検索キーワードを指定してインスタンスを作成
    params1 = StatsTableParameters(search_word="労働力調査")
    print(f"search_word: {params1.search_word}")

    # 複数のパラメータを指定してインスタンスを作成
    params2 = StatsTableParameters(
        stats_code="00200531",
        start_position=1,
        limit=100,
        explanation_get_flg='Y'
    )
    print(
        f"stats_code: {params2.stats_code}, "
        f"start_position: {params2.start_position}, "
        f"limit: {params2.limit}, "
        f"explanation_get_flg: {params2.explanation_get_flg}"
    )
