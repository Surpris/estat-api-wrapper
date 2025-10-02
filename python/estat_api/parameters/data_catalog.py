"""data_catalog

Parameters for the e-Stat API that retrieves data catalog.
"""

from dataclasses import dataclass
from typing import Optional


@dataclass
class DataCatalogParameters:
    """
    e-Stat API「データカタログ情報取得」機能のパラメータを管理するクラスです。

    Attributes:
        search_word (Optional[str]): 任意パラメータ。検索キーワードをUTF-8でURLエンコードして指定します。
        start_position (Optional[int]): 任意パラメータ。データの取得開始位置を1からの連番で指定します。
        limit (Optional[int]): 任意パラメータ。データの取得件数を指定します。
    """

    def __init__(
        self,
        search_word: Optional[str] = None,
        start_position: Optional[int] = None,
        limit: Optional[int] = None,
    ):
        """
        DataCatalogParametersのインスタンスを初期化します。

        Args:
            search_word (Optional[str], optional): 検索キーワード。Defaults to None.
            start_position (Optional[int], optional): データの取得開始位置。Defaults to None.
            limit (Optional[int], optional): データの取得件数。Defaults to None.
        """
        self.search_word = search_word
        self.start_position = start_position
        self.limit = limit


# --- 使用例 ---
if __name__ == '__main__':
    # パラメータを指定せずにインスタンスを作成（全件取得の意図）
    params1 = DataCatalogParameters()
    print(
        f"search_word: {params1.search_word}, "
        f"start_position: {params1.start_position}, "
        f"limit: {params1.limit}"
    )

    # 全てのパラメータを指定してインスタンスを作成
    params2 = DataCatalogParameters(
        search_word="国勢調査",
        start_position=1,
        limit=50
    )
    print(
        f"search_word: {params2.search_word}, "
        f"start_position: {params2.start_position}, "
        f"limit: {params2.limit}"
    )
