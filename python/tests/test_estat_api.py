"""test_estat_api.py
"""

import json
import unittest
from unittest.mock import patch, MagicMock
import requests
from estat_api.api import EstatAPI


class TestEstatAPI(unittest.TestCase):
    """EstatAPIクラスのテストコード"""

    def setUp(self):
        """各テストの前に実行されるセットアップ処理"""
        self.app_id = "test_app_id_12345"
        self.api = EstatAPI(app_id=self.app_id)
        self.base_url_v3 = f"https://api.e-stat.go.jp/rest/3.0/app"

    def _create_mock_response(self, status_code, json_data):
        """指定されたステータスコードとJSONデータを持つMockレスポンスオブジェクトを作成するヘルパー関数"""
        mock_res = MagicMock()
        mock_res.status_code = status_code
        mock_res.json.return_value = json_data
        # raise_for_status()がHTTPErrorを投げるように設定
        if status_code >= 400:
            mock_res.raise_for_status.side_effect = requests.exceptions.HTTPError(
                response=mock_res)
        return mock_res

    @patch('estat_api.requests.get')
    def test_get_stats_list_success(self, mock_get):
        """2.1. 統計表情報取得 (getStatsList) の正常系テスト"""
        # モックの戻り値を設定
        expected_response = {"GET_STATS_LIST": {"RESULT": {"STATUS": 0}}}
        mock_get.return_value = self._create_mock_response(
            200, expected_response)

        # テスト対象メソッドの実行
        result = self.api.get_stats_list(searchWord="test")

        # アサーション（検証）
        # 1. requests.getが期待通りに呼ばれたか
        expected_url = f"{self.base_url_v3}/json/getStatsList"
        expected_params = {"appId": self.app_id, "searchWord": "test"}
        mock_get.assert_called_once_with(expected_url, params=expected_params)

        # 2. メソッドの戻り値が期待通りか
        self.assertEqual(result, expected_response)

    @patch('estat_api.requests.get')
    def test_get_meta_info_csv_format(self, mock_get):
        """2.2. メタ情報取得 (getMetaInfo) のCSV形式テスト"""
        # モックの設定
        mock_get.return_value = self._create_mock_response(200, {})

        # メソッド実行
        self.api.get_meta_info(statsDataId="0001", data_format="csv")

        # URLがCSV用の 'getSimpleMetaInfo' になっているか検証
        expected_url = f"{self.base_url_v3}/getSimpleMetaInfo"
        expected_params = {"appId": self.app_id, "statsDataId": "0001"}
        mock_get.assert_called_once_with(expected_url, params=expected_params)

    @patch('estat_api.requests.get')
    def test_get_stats_data_with_http_error(self, mock_get):
        """2.3. 統計データ取得 (getStatsData) の異常系（HTTPエラー）テスト"""
        # モックがHTTPErrorを発生させるように設定
        mock_get.return_value = self._create_mock_response(
            404, {"error": "not found"})

        # メソッド実行
        result = self.api.get_stats_data(statsDataId="invalid_id")

        # エラー時にNoneが返ることを確認
        self.assertIsNone(result)

    @patch('estat_api.requests.post')
    def test_post_dataset_success(self, mock_post):
        """2.4. データセット登録 (postDataset) の正常系テスト"""
        expected_response = {"POST_DATASET": {"RESULT": {"STATUS": 0}}}
        mock_post.return_value = self._create_mock_response(
            200, expected_response)

        params = {
            "processMode": "ADD",
            "statsDataId": "000123",
            "dataSetName": "My Test Dataset"
        }
        result = self.api.post_dataset(**params)

        expected_url = f"{self.base_url_v3}/json/postDataset"
        expected_data = params.copy()
        expected_data["appId"] = self.app_id

        mock_post.assert_called_once_with(
            expected_url,
            data=expected_data,
            headers={'Content-Type': 'application/x-www-form-urlencoded'}
        )
        self.assertEqual(result, expected_response)

    @patch('estat_api.requests.get')
    def test_ref_dataset(self, mock_get):
        """2.5. データセット参照 (refDataset) のテスト"""
        mock_get.return_value = self._create_mock_response(200, {})
        self.api.ref_dataset(dataSetId="DSET001")

        expected_url = f"{self.base_url_v3}/json/refDataset"
        mock_get.assert_called_once_with(
            expected_url, params={"appId": self.app_id, "dataSetId": "DSET001"})

    @patch('estat_api.requests.get')
    def test_get_data_catalog(self, mock_get):
        """2.6. データカタログ情報取得 (getDataCatalog) のテスト"""
        mock_get.return_value = self._create_mock_response(200, {})
        self.api.get_data_catalog(searchWord="catalog")

        expected_url = f"{self.base_url_v3}/json/getDataCatalog"
        mock_get.assert_called_once_with(
            expected_url, params={"appId": self.app_id, "searchWord": "catalog"})

    @patch('estat_api.requests.post')
    def test_get_stats_datas_success(self, mock_post):
        """2.7. 統計データ一括取得 (getStatsDatas) の正常系テスト"""
        expected_response = {"GET_STATS_DATAS": {"RESULT": {"STATUS": 0}}}
        mock_post.return_value = self._create_mock_response(
            200, expected_response)

        spec = [{"statsDataId": "0001"}, {"dataSetId": "DSET002"}]
        result = self.api.get_stats_datas(statsDatasSpec=spec, metaGetFlg="Y")

        expected_url = f"{self.base_url_v3}/json/getStatsDatas"
        expected_data = {
            "appId": self.app_id,
            "statsDatasSpec": json.dumps(spec, ensure_ascii=False),
            "metaGetFlg": "Y"
        }

        mock_post.assert_called_once_with(
            expected_url, data=expected_data, headers={})
        self.assertEqual(result, expected_response)

    def test_init_no_app_id(self):
        """appIdなしで初期化した場合にValueErrorを送出するかのテスト"""
        with self.assertRaises(ValueError):
            EstatAPI(app_id=None)
        with self.assertRaises(ValueError):
            EstatAPI(app_id="")


if __name__ == '__main__':
    # requestsモジュールをインポート（HTTPErrorのために必要）
    import requests
    unittest.main(argv=['first-arg-is-ignored'], exit=False)
