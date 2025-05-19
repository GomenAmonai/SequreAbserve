import httpx, pytest
BASE = "http://localhost:8000"

@pytest.mark.parametrize("path", ["/health", "/nodes/best"])
def test_paths(path):
    r = httpx.get(BASE + path)
    assert r.status_code in (200, 404)   # 404 ожидаем, если нет нод