"""stats_data

Parameters for the e-Stat API that retrieves statistical table.
"""

from dataclasses import dataclass
from typing import Literal, Optional, Any


@dataclass
class StatsDataParameters:
    """
    e-Stat APIの「統計データ取得」機能のパラメータを管理するクラスです。

    Attributes:
        stats_data_id (str): 必須パラメータ。統計表IDを指定します。
        start_position (Optional[int]): 任意パラメータ。データの取得開始位置を1からの連番で指定します。
        limit (Optional[int]): 任意パラメータ。データの取得件数を指定します。
        meta_get_flg (Literal['Y', 'N']): 任意パラメータ。'Y'を指定するとメタ情報を取得します。
        cnt_get_flg (Literal['Y', 'N']): 任意パラメータ。'Y'を指定するとデータ件数を取得します。
        section_header_flg (Literal['1', '2']): 任意パラメータ。CSV出力時のセクションヘッダ出力指定。
                                               '1': 出力しない（デフォルト）、'2': 出力する
        cd_area (Optional[str]): 任意パラメータ。絞り込み条件（地域コード）。
        cd_time (Optional[str]): 任意パラメータ。絞り込み条件（時間軸コード）。
        cd_tab (Optional[str]): 任意パラメータ。絞り込み条件（表章項目コード）。
        cd_cat (Dict[str, Any]): 任意パラメータ。絞り込み条件（カテゴリコード）。
                                 'cdCat01', 'cdCat02'などをキーとして指定します。
    """

    def __init__(
        self,
        stats_data_id: str,
        start_position: Optional[int] = None,
        limit: Optional[int] = None,
        meta_get_flg: Literal['Y', 'N'] = 'N',
        cnt_get_flg: Literal['Y', 'N'] = 'N',
        section_header_flg: Literal['1', '2'] = '1',
        cd_area: Optional[str] = None,
        cd_time: Optional[str] = None,
        cd_tab: Optional[str] = None,
        **kwargs: Any
    ):
        """
        StatsDataParametersのインスタンスを初期化します。

        Args:
            stats_data_id (str): 統計表IDを指定します。
            start_position (Optional[int]): データの取得開始位置。
            limit (Optional[int]): データの取得件数。
            meta_get_flg (Literal['Y', 'N']): メタ情報有無フラグ。
            cnt_get_flg (Literal['Y', 'N']): 件数取得フラグ。
            section_header_flg (Literal['1', '2']): CSVヘッダ出力フラグ。
            cd_area (Optional[str]): 絞り込み条件（地域コード）。
            cd_time (Optional[str]): 絞り込み条件（時間軸コード）。
            cd_tab (Optional[str]): 絞り込み条件（表章項目コード）。
            **kwargs: cdCat01, cdCat02などのカテゴリ絞り込み条件をキーワード引数として指定します。
        """
        self.stats_data_id = stats_data_id
        self.start_position = start_position
        self.limit = limit
        self.meta_get_flg = meta_get_flg
        self.cnt_get_flg = cnt_get_flg
        self.section_header_flg = section_header_flg
        self.cd_area = cd_area
        self.cd_time = cd_time
        self.cd_tab = cd_tab
        # 'cdCat'で始まるキーワード引数のみを抽出して辞書に格納
        self.cd_cat = {k: v for k,
                       v in kwargs.items() if k.startswith('cdCat')}


# --- 使用例 ---
if __name__ == '__main__':
    # 必須パラメータと、いくつかの任意パラメータを指定
    params1 = StatsDataParameters(
        stats_data_id="0003411678",
        limit=10,
        meta_get_flg='Y'
    )
    print(
        f"stats_data_id: {params1.stats_data_id}, limit: {params1.limit}, cd_cat: {params1.cd_cat}")

    # カテゴリ絞り込み条件(cdCat01, cdCat02)を含む例
    params2 = StatsDataParameters(
        stats_data_id="0003411678",
        cdCat01="010",  # 例: カテゴリ01のコード
        cdCat02=["020", "030"]  # 例: カテゴリ02のコード（複数指定）
    )
    print(f"stats_data_id: {params2.stats_data_id}, cd_cat: {params2.cd_cat}")
