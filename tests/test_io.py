"""test.test_io.py"""
import string

import pytest

import app.io

IO_PARAMS = (
    "name, content, kwargs",
    [
        ("test_file.txt", string.ascii_lowercase, {}),
        ("test_json_file.json", {"a": 0, "b": 1, "c": 2}, {}),
        ("test_custom_json.json", {"z": -1, "b": 1, "y": -2, "a": 0}, {"indent": 4, "sort_keys": True}),
    ],
)


@pytest.mark.parametrize(*IO_PARAMS)
def test_save(tmp_path, name, content, kwargs):
    test_path = tmp_path / name
    assert not test_path.exists()

    result = app.io.save(test_path, content, **kwargs)
    assert result == test_path
    assert test_path.exists()


@pytest.mark.parametrize(*IO_PARAMS)
def test_round_trip(tmp_path, name, content, kwargs):
    test_path = tmp_path / name
    assert not test_path.exists()

    app.io.save(test_path, content, **kwargs)
    assert app.io.load(test_path) == content


@pytest.mark.asyncio
@pytest.mark.parametrize(*IO_PARAMS)
async def test_async_save(tmp_path, name, content, kwargs):
    test_path = tmp_path / name
    assert not test_path.exists()

    result = await app.io.AIO.save(test_path, content, **kwargs)
    assert result == test_path
    assert test_path.exists()


@pytest.mark.asyncio
@pytest.mark.parametrize(*IO_PARAMS)
async def test_async_round_trip(tmp_path, name, content, kwargs):
    test_path = tmp_path / name
    assert not test_path.exists()

    await app.io.AIO.save(test_path, content, **kwargs)
    load_results = await app.io.AIO.load(test_path)
    assert load_results == content
