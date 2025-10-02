"""bulk_stats_data

Parameters for the e-Stat API that retrieves the bulk of stats data.
"""

from dataclasses import dataclass
from typing import Literal, Optional


@dataclass
class BulkStatsDataParameters:
    """
    e-Stat API「統計データ一括取得」機能のパラメータを管理するクラスです。

    Attributes:
        dataset_id (str): 必須パラメータ。データセットIDを指定します。
        start_position (Optional[int]): 任意パラメータ。データの取得開始位置を1からの連番で指定します。
        limit (Optional[int]): 任意パラメータ。データの取得件数を指定します。
        meta_get_flg (Literal['Y', 'N']): 任意パラメータ。'Y'を指定するとメタ情報を取得します。
        cnt_get_flg (Literal['Y', 'N']): 任意パラメータ。'Y'を指定するとデータ件数を取得します。
        section_header_flg (Literal['1', '2']): 任意パラメータ。CSV出力時のセクションヘッダ出力指定。
                                               '1': 出力しない（デフォルト）、'2': 出力する
        explanation_get_flg (Literal['Y', 'N']): 任意パラメータ。解説情報取得フラグ。
                                                'Y' を指定すると、統計表の解説情報を取得します。
    """

    def __init__(
        self,
        dataset_id: str,
        start_position: Optional[int] = None,
        limit: Optional[int] = None,
        meta_get_flg: Literal['Y', 'N'] = 'N',
        cnt_get_flg: Literal['Y', 'N'] = 'N',
        section_header_flg: Literal['1', '2'] = '1',
        explanation_get_flg: Literal['Y', 'N'] = 'N',
    ):
        """
        BulkStatsDataParametersのインスタンスを初期化します。

        Args:
            dataset_id (str): データセットIDを指定します。
            start_position (Optional[int]): データの取得開始位置。
            limit (Optional[int]): データの取得件数。
            meta_get_flg (Literal['Y', 'N']): メタ情報有無フラグ。
            cnt_get_flg (Literal['Y', 'N']): 件数取得フラグ。
            section_header_flg (Literal['1', '2']): CSVヘッダ出力フラグ。
            explanation_get_flg (Literal['Y', 'N']): 解説情報取得フラグ。
        """
        self.dataset_id = dataset_id
        self.start_position = start_position
        self.limit = limit
        self.meta_get_flg = meta_get_flg
        self.cnt_get_flg = cnt_get_flg
        self.section_header_flg = section_header_flg
        self.explanation_get_flg = explanation_get_flg


# --- 使用例 ---
if __name__ == '__main__':
    # 必須パラメータであるデータセットIDのみを指定
    params1 = BulkStatsDataParameters(dataset_id="DS00000123")
    print(f"dataset_id: {params1.dataset_id}")

    # 複数の任意パラメータを指定
    params2 = BulkStatsDataParameters(
        dataset_id="DS00000123",
        limit=100,
        meta_get_flg='Y',
        explanation_get_flg='Y'
    )
    print(
        f"dataset_id: {params2.dataset_id}, "
        f"limit: {params2.limit}, "
        f"meta_get_flg: {params2.meta_get_flg}, "
        f"explanation_get_flg: {params2.explanation_get_flg}"
    )
