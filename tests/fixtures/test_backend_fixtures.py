#pylint: disable=C0114, C0116, W0311, W0212, W0621, C0115, R0903
from typing import Any
import pytest
from SnowieCaster import SnowieCaster, abstract


class TestBackend(abstract.AbstractBackend):
	async def _astart(self, *args, **kwargs) -> None:
		pass

	async def _astop(self) -> None:
		pass

	async def _apublish(self, channel: str, message: Any, *args, **kwargs) -> None:
		pass

	async def _aget_all(self, channel: str):
		pass


@pytest.fixture
def create_test_caster_noauto():
	def caster_creator():
		memory_backend = TestBackend()
		caster = SnowieCaster(memory_backend)
		return (caster, memory_backend)
	return caster_creator
