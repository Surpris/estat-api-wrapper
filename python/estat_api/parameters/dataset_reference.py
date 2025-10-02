"""dataset_reference

Parameters for the e-Stat API that retrieves dataset reference.
"""

from dataclasses import dataclass
from typing import Optional


@dataclass
class DatasetReferenceParameters:
    """
    e-Stat API「データセット参照」機能のパラメータを管理するクラスです。

    この機能は、登録したデータセットの情報を一覧で取得します。
    特定のデータセットIDを指定することで、個別の情報を取得することも可能です。

    Attributes:
        dataset_id (Optional[str]): 任意パラメータ。データセットIDを指定します。
                                    指定しない場合は、登録されているデータセットの一覧を取得します。
    """

    def __init__(self, dataset_id: Optional[str] = None):
        """
        DatasetReferenceParametersのインスタンスを初期化します。

        Args:
            dataset_id (Optional[str], optional): データセットIDを指定します。
                                                   省略した場合はNoneになります。
                                                   Defaults to None.
        """
        self.dataset_id: Optional[str] = dataset_id


# --- 使用例 ---
if __name__ == '__main__':
    # パラメータを指定せずにインスタンスを作成（全データセット参照）
    params_all = DatasetReferenceParameters()
    print(f"List all datasets - dataset_id: {params_all.dataset_id}")

    # データセットIDを指定してインスタンスを作成（個別参照）
    params_specific = DatasetReferenceParameters(dataset_id="DS00000123")
    print(f"Get specific dataset - dataset_id: {params_specific.dataset_id}")
