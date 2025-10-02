"""meta_info

Parameters for the e-Stat API that retrieves meta information.
"""

from dataclasses import dataclass


@dataclass
class MetaInfoParameters:
    """
    e-Stat APIの「メタ情報取得」機能のパラメータを管理するクラスです。

    この機能では、統計表ID（statsDataId）を指定して、
    当該統計表のメタ情報（定義情報）を取得します。

    Attributes:
        stats_data_id (str): 必須パラメータ。統計表IDを指定します。
                             「統計表情報取得」APIで取得した@idの値を設定します。
    """

    def __init__(self, stats_data_id: str):
        """
        MetaInfoParametersのインスタンスを初期化します。

        Args:
            stats_data_id (str): 統計表ID（@idの値）を指定します。
        """
        self.stats_data_id: str = stats_data_id


# --- 使用例 ---
if __name__ == '__main__':
    # 必須パラメータである統計表IDを指定してインスタンスを作成
    # このIDは、事前に「統計表情報取得」APIを呼び出して取得しておく必要があります。
    meta_params = MetaInfoParameters(stats_data_id="0003411678")

    print(f"stats_data_id: {meta_params.stats_data_id}")
