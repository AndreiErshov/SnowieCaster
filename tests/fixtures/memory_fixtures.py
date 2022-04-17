#pylint: disable=C0114, C0116, W0311, W0212, W0621
import pytest
from SnowieCaster.backends.memory import MemoryBackend
from SnowieCaster import SnowieCaster

@pytest.fixture
def create_memory_backend():
	def memory_backend_creator():
		return MemoryBackend()
	return memory_backend_creator

@pytest.fixture
def create_caster(create_memory_backend):
	def caster_creator():
		memory_backend = create_memory_backend()
		caster = SnowieCaster(memory_backend, auto_start=True)
		return (caster, memory_backend)
	return caster_creator
