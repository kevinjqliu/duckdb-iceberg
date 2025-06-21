import pytest
import os
import datetime
import duckdb

pyice = pytest.importorskip("pyiceberg")
pa = pytest.importorskip("pyarrow")
pyice_rest = pytest.importorskip("pyiceberg.catalog.rest")


@pytest.fixture()
def bearer_token():
    if hasattr(bearer_token, "cached_token"):
        return bearer_token.cached_token

    import requests

    CATALOG_HOST = "http://127.0.0.1:8181"

    CLIENT_ID = "admin"
    CLIENT_SECRET = "password"

    token_url = f"{CATALOG_HOST}/v1/oauth/tokens"
    payload = {
        "grant_type": "client_credentials",
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "scope": "PRINCIPAL_ROLE:ALL",
    }

    response = requests.post(token_url, data=payload)

    assert response.status_code == 200
    access_token = response.json().get("access_token")
    print("Token:", access_token)
    bearer_token.cached_token = access_token
    return access_token


@pytest.fixture()
def rest_catalog(bearer_token):
    catalog = pyice_rest.RestCatalog(
        "rest",
        **{
            "uri": "http://127.0.0.1:8181",
            "token": bearer_token,
            "warehouse": "",
            "s3.endpoint": "http://127.0.0.1:9000",
            "s3.access-key-id": "admin",
            "s3.secret-access-key": "password",
            "s3.path-style-access": "true",
            "s3.ssl.enabled": "false",
        },
    )
    return catalog


@pytest.fixture()
def duckdb_connection(bearer_token):
    conn = duckdb.connect()
    # Create S3 secret
    conn.execute("""
        CREATE SECRET (
            TYPE S3,
            KEY_ID 'admin',
            SECRET 'password',
            ENDPOINT '127.0.0.1:9000',
            URL_STYLE 'path',
            USE_SSL 0
        );
    """)

    # Attach Iceberg catalog
    conn.execute(f"""
        ATTACH '' AS my_datalake (
            TYPE ICEBERG,
            ENDPOINT 'http://127.0.0.1:8181',
            TOKEN '{bearer_token}',
        );
    """)
    return conn


@pytest.mark.skipif(
    os.getenv("ICEBERG_SERVER_AVAILABLE", None) == None,
    reason="Test data wasn't generated, run 'make data' first",
)
class TestPyIcebergRead:
    def test_pyiceberg_read(self, rest_catalog, duckdb_connection):
        # read from pyiceberg
        table = rest_catalog.load_table("default.insert_test")
        pyiceberg_arrow_table: pa.Table = table.scan().to_arrow()
        res = pyiceberg_arrow_table.to_pylist()
        assert len(res) == 6
        assert res == [
            {"col1": datetime.date(2010, 6, 11), "col2": 42, "col3": "test"},
            {
                "col1": datetime.date(2020, 8, 12),
                "col2": 45345,
                "col3": "inserted by con1",
            },
            {"col1": datetime.date(2020, 8, 13), "col2": 1, "col3": "insert 1"},
            {"col1": datetime.date(2020, 8, 14), "col2": 2, "col3": "insert 2"},
            {"col1": datetime.date(2020, 8, 15), "col2": 3, "col3": "insert 3"},
            {"col1": datetime.date(2020, 8, 16), "col2": 4, "col3": "insert 4"},
        ]

        # read from duckdb
        duckdb_arrow_table = duckdb_connection.execute("SELECT * FROM my_datalake.default.insert_test").arrow()
        assert pyiceberg_arrow_table.equals(duckdb_arrow_table)
