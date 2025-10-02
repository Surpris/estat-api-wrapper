"""dataset_registration

Parameters for the e-Stat API that registers a dataset.
"""

from dataclasses import dataclass


@dataclass
class DatasetRegistrationUrlParams:
    """
    e-Stat API「データセット登録」機能のURLパラメータを管理するクラスです。

    Attributes:
        stats_data_id (str): 必須パラメータ。統計表IDを指定します。
                             「統計表情報取得」APIで取得した@idの値を設定します。
    """

    def __init__(self, stats_data_id: str):
        """
        DatasetRegistrationUrlParamsのインスタンスを初期化します。

        Args:
            stats_data_id (str): 統計表ID（@idの値）を指定します。
        """
        self.stats_data_id: str = stats_data_id
