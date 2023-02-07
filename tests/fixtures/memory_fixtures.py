#pylint: disable=C0114, C0116, W0311, W0212, W0621
import pytest
from snowiecaster.backends.memory import MemoryBackend
from snowiecaster import SnowieCaster

@pytest.fixture
def create_memory_backend():
	def memory_backend_creator():
		return MemoryBackend()
	return memory_backend_creator

@pytest.fixture
def create_caster(create_memory_backend):
	def caster_creator(requests_delay=None, requests_delay_limit=None):
		memory_backend = create_memory_backend()
		memory_backend._request_delay_limit = requests_delay_limit
		caster = SnowieCaster(memory_backend, requests_delay=requests_delay, auto_start=True)
		return (caster, memory_backend)
	return caster_creator
