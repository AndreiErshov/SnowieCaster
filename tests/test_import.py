#pylint: disable=C0114, C0116, W0311, W0212, C0415, W0611
import pytest

@pytest.mark.order(1)
def test_import():
    try:
        from SnowieCaster.backends.memory import MemoryBackend
        from SnowieCaster import SnowieCaster, __version__
    except ModuleNotFoundError as exc:
        raise ModuleNotFoundError("Can't find SnowieCaster build! Run: make build") from exc
