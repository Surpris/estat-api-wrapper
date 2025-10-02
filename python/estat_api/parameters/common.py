"""common

Common parameters for the e-Stat API.
"""

from dataclasses import dataclass
from typing import Literal

@dataclass
class CommonParameters:
    """
    e-Stat APIの全機能に共通するパラメータを管理するクラスです。 [cite: 74]

    このクラスは、APIリクエストに必要な共通パラメータであるアプリケーションIDと言語設定を保持します。 

    Attributes:
        app_id (str): 必須パラメータ。利用登録によって取得したアプリケーションID。 
        lang (Literal['J', 'E']): 任意パラメータ。取得データの言語を指定します。
                                'J'は日本語（デフォルト）、'E'は英語です。 
    """

    def __init__(self, app_id: str, lang: Literal['J', 'E'] = 'J'):
        """
        CommonParametersのインスタンスを初期化します。

        Args:
            app_id (str): 取得したアプリケーションIDを指定します。 
            lang (Literal['J', 'E'], optional): 取得するデータの言語を指定します。
                                                デフォルトは 'J' (日本語)です。 
        """
        self.app_id: str = app_id
        self.lang: Literal['J', 'E'] = lang


# --- 使用例 ---
if __name__ == '__main__':
    # アプリケーションIDを指定してインスタンスを作成（langはデフォルトの'J'）
    params_jp = CommonParameters(app_id="YOUR_APPLICATION_ID")
    print(f"app_id: {params_jp.app_id}, lang: {params_jp.lang}")

    # 言語を英語に指定してインスタンスを作成
    params_en = CommonParameters(app_id="YOUR_APPLICATION_ID", lang='E')
    print(f"app_id: {params_en.app_id}, lang: {params_en.lang}")
