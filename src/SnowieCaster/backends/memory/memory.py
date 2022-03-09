"""
Memory backend class
"""
#pylint: disable=W0311, R0903, W0221, W0201

from asyncio import Queue
from typing import Any, Dict, AsyncIterator
from ...abstract import ISyncBackend, Results


class MemoryBackend(ISyncBackend):
	"""This class allows you to use pub/sub in-memory"""
	def _check_instance_vars(self):
		"""This method checks is class vars are valid"""
		assert hasattr(self, 'store'), 'store is not defined, mb u call start?'
		assert isinstance(self.store, dict), \
		"store's datatype is not Dict[str, Queue]"

	def _start(self, store: Dict[str, Queue] = None):
		self.store: Dict[str, Queue] = {} if store is None else store
		self._check_instance_vars()

	def _stop(self):
		self.store = {}

	async def _apublish(self, channel: str, message: Any) -> None:
		self._check_instance_vars()
		assert isinstance(channel, str), "channel's datatype is not str"
		if channel not in self.store:
			self.store[channel] = Queue()
		sub = self.store[channel]
		assert isinstance(sub, Queue), \
		"store's datatype is not Dict[str, Queue]"
		await sub.put(message)


	async def _asubscribe(self, channel: str) -> AsyncIterator[Any]:
		self._check_instance_vars()
		assert isinstance(channel, str), "channel's datatype is not str"
		if channel not in self.store:
			self.store[channel] = Queue()
		while isinstance(self.store[channel], Queue):
			channel_queue = self.store[channel]
			if channel_queue.empty():
				yield Results.NO_DATA
			else:
				yield await channel_queue.get()
