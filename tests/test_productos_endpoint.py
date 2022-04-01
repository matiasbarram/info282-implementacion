import pytest


def test_get_productos(client):
    response = client.get('/productos/')
    assert response.status_code == 200
    prod_list = response.json['items']
    assert prod_list
    barcode = prod_list[0]['codigoBarra']
    assert barcode == '7613033458507'
    pytest.barcode = barcode


def test_get_producto_id(client):
    response = client.get('/productos/7')
    assert response.status_code == 200
