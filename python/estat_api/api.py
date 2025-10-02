"""api.py
"""

import json
import requests

TIMEOUT_SEC: int = 30


class EstatAPI:
    """
    政府統計の総合窓口(e-Stat) APIのPythonラッパークラス。

    e-Stat API仕様書 バージョン3.0に基づいています。
    - 参考資料: https://www.e-stat.go.jp/api/sites/default/files/uploads/2019/07/API-specVer3.0.pdf
    """

    def __init__(self, app_id, version="3.0", use_https=True):
        """
        EstatAPIクラスのコンストラクタ。

        Args:
            app_id (str): e-Statから取得したアプリケーションID。
            version (str, optional): APIのバージョン。デフォルトは "3.0"。
            use_https (bool, optional): HTTPSプロトコルを使用するかどうか。デフォルトは True。
        """
        if not app_id:
            raise ValueError("アプリケーションID (app_id) は必須です。")
        self.app_id = app_id
        protocol = "https" if use_https else "http"
        self.base_url = f"{protocol}://api.e-stat.go.jp/rest/{version}/app"

    def _build_endpoint(self, path, data_format):
        """
        データ形式に基づいてAPIのエンドポイントURLを構築します。
        """
        # CSV形式の場合、パスが'getSimple...'という形式になります
        if data_format == "csv":
            if "List" in path:
                path = path.replace("List", "SimpleStatsList")
            elif "Info" in path:
                path = path.replace("Info", "SimpleMetaInfo")
            elif "Data" in path and "Datas" not in path:
                path = path.replace("Data", "SimpleStatsData")
            elif "Datas" in path:
                path = path.replace("Datas", "SimpleStatsDatas")
            return f"{self.base_url}/{path}"

        # JSON/JSONP形式の場合
        if data_format in ("json", "jsonp"):
            return f"{self.base_url}/{data_format}/{path}"

        # XML形式 (デフォルト)
        return f"{self.base_url}/{path}"

    def _make_request(self, method, path, data_format="json", params=None):
        """
        APIにHTTPリクエストを送信する内部メソッド。

        Args:
            method (str): 'GET' または 'POST'。
            path (str): APIのエンドポイントのパス。
            data_format (str, optional): レスポンスのデータ形式 ('json', 'xml', 'csv', 'jsonp')。
            params (dict, optional): APIに送信するパラメータ。

        Returns:
            dict or str: APIからのレスポンス。JSONの場合は辞書、それ以外はテキスト。
        """
        endpoint = self._build_endpoint(path, data_format)

        all_params = params.copy() if params else {}
        all_params["appId"] = self.app_id

        headers = {}
        # データセット登録APIはContent-Typeの指定が必要です
        if path == 'postDataset':
            headers['Content-Type'] = 'application/x-www-form-urlencoded'

        try:
            if method.upper() == 'GET':
                response = requests.get(
                    endpoint, timeout=TIMEOUT_SEC, params=all_params
                )
            elif method.upper() == 'POST':
                response = requests.post(
                    endpoint, timeout=TIMEOUT_SEC, data=all_params, headers=headers
                )
            else:
                raise ValueError(f"サポートされていないHTTPメソッドです: {method}")

            response.raise_for_status()

            if data_format == "json" or data_format == "jsonp":
                return response.json()
            else:
                response.encoding = 'utf-8'
                return response.text

        except requests.exceptions.HTTPError as e:
            print(
                f"HTTPエラーが発生しました: {e.response.status_code} {e.response.reason}")
            print(f"レスポンス: {e.response.text}")
            return None
        except requests.exceptions.RequestException as e:
            print(f"リクエストエラーが発生しました: {e}")
            return None

    def get_stats_list(self, data_format="json", **kwargs):
        """
        2.1. 統計表情報取得 (getStatsList)

        e-Statで提供している統計表の情報を取得します。

        Args:
            data_format (str, optional): レスポンス形式 ('json', 'xml', 'csv', 'jsonp')。
            **kwargs: surveyYears, openYears, statsField, statsCode, searchWord など、
                      仕様書に記載されているパラメータ。
        """
        return self._make_request('GET', 'getStatsList', data_format, params=kwargs)

    def get_meta_info(self, statsDataId, data_format="json", **kwargs):
        """
        2.2. メタ情報取得 (getMetaInfo)

        指定した統計表IDに対応するメタ情報（表章事項、分類事項など）を取得します。

        Args:
            statsDataId (str): 統計表ID。
            data_format (str, optional): レスポンス形式 ('json', 'xml', 'csv', 'jsonp')。
            **kwargs: explanationGetFlg などのパラメータ。
        """
        params = kwargs
        params['statsDataId'] = statsDataId
        return self._make_request('GET', 'getMetaInfo', data_format, params=params)

    def get_stats_data(self, data_format="json", **kwargs):
        """
        2.3. 統計データ取得 (getStatsData)

        指定した統計表IDまたはデータセットIDに対応する統計データを取得します。

        Args:
            data_format (str, optional): レスポンス形式 ('json', 'xml', 'csv', 'jsonp')。
            **kwargs: statsDataId または dataSetId のいずれかが必須。
                      その他、lvTab, cdArea, startPosition などの絞り込みパラメータ。
        """
        if 'statsDataId' not in kwargs and 'dataSetId' not in kwargs:
            raise ValueError("'statsDataId' または 'dataSetId' のいずれか一つは必須です。")
        return self._make_request('GET', 'getStatsData', data_format, params=kwargs)

    def post_dataset(self, **kwargs):
        """
        2.4. データセット登録 (postDataset)

        統計データを取得する際の取得条件をデータセットとして登録・更新・削除します。
        このAPIはPOSTリクエストを使用します。レスポンスはXMLまたはJSONです。

        Args:
            **kwargs: processMode, statsDataId, dataSetName などのパラメータ。
        """
        # このAPIのレスポンス形式はXMLかJSONのみ
        return self._make_request('POST', 'postDataset', data_format="json", params=kwargs)

    def ref_dataset(self, data_format="json", **kwargs):
        """
        2.5. データセット参照 (refDataset)

        登録されているデータセットの情報を参照します。

        Args:
            data_format (str, optional): レスポンス形式 ('json', 'xml', 'jsonp')。CSVは非対応。
            **kwargs: dataSetId などのパラメータ。
        """
        return self._make_request('GET', 'refDataset', data_format, params=kwargs)

    def get_data_catalog(self, data_format="json", **kwargs):
        """
        2.6. データカタログ情報取得 (getDataCatalog)

        統計表ファイルや統計データベースの情報を取得します。

        Args:
            data_format (str, optional): レスポンス形式 ('json', 'xml', 'jsonp')。CSVは非対応。
            **kwargs: searchWord, dataType, updatedDate などのパラメータ。
        """
        return self._make_request('GET', 'getDataCatalog', data_format, params=kwargs)

    def get_stats_datas(self, statsDatasSpec, data_format="json", **kwargs):
        """
        2.7. 統計データ一括取得 (getStatsDatas)

        複数の統計表IDまたはデータセットIDを指定して、一括で統計データを取得します。
        このAPIはPOSTリクエストを使用します。

        Args:
            statsDatasSpec (list): 取得したい統計データの条件を辞書のリストで指定します。
                                   例: [{"statsDataId": "000..."}, {"dataSetId": "..."}]
            data_format (str, optional): レスポンス形式 ('json', 'xml', 'csv')。
            **kwargs: metaGetFlg, explanationGetFlg などの共通パラメータ。
        """
        if not isinstance(statsDatasSpec, list):
            raise TypeError("'statsDatasSpec' は辞書のリストである必要があります。")

        params = kwargs
        # リストをJSON文字列に変換します
        params['statsDatasSpec'] = json.dumps(
            statsDatasSpec, ensure_ascii=False)
        return self._make_request('POST', 'getStatsDatas', data_format, params=params)
