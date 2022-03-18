#pylint: disable=W0311, W0212

# плохо кнч задокументировал, ну да ладно

"""
A general script for contacting with this library
"""

from asyncio import Queue
from typing import Any, Dict, Optional, List, AsyncIterator
from .abstract import AbstractBackend, Results, SubscriptionUpdater


class Subscription:
	"""This class allows you to iterate through messages"""

	def __init__(self, channel: str, updater: SubscriptionUpdater):
		assert isinstance(channel, str), "channel's datatype is str"
		assert isinstance(updater, SubscriptionUpdater), "caster's datatype is SnowieCaster"
		self.channel = channel
		self.updater = updater
		self._queue = Queue()

	async def __aenter__(self):
		async def iterator_func():
			nonlocal self
			while isinstance(self._queue, Queue):
				assert isinstance(self.channel, str), "channel's datatype is str"
				if self._queue.empty():
					await self.updater._update_subscriptions(self.channel)
					if self._queue.empty():
						yield None
				else:
					yield await self._queue.get()
		return iterator_func()

	async def __aexit__(self, *args, **kwargs):
		self._queue = None

	def __del__(self):
		self._queue = None


class SnowieCaster(SubscriptionUpdater):
	"""A general class for contacting with this library"""
	def _check_instance_vars(self):
		"""This method checks is class vars are valid"""
		assert isinstance(self._channel_subs, dict)
		assert isinstance(self._backend, AbstractBackend)

	async def _update_subscriptions(self, channel: str):
		"""This method inherits from SubscriptionUpdater and updates Subscription's class Queries"""
		self._check_instance_vars()
		assert isinstance(channel, str), "channel's datatype is str"
		assert channel in self._channel_subs, "can't find channel"
		backend_iterator: AsyncIterator[Any] = self._backend._asubscribe(channel)
		subs: List[Subscription] = self._channel_subs[channel]
		assert isinstance(subs, list)

		subs_length = len(subs)
		if subs_length < 1:
			return False

		result = Results.NONE_DATA
		async def get_result():
			nonlocal result
			if result is Results.NONE_DATA:
				result = await backend_iterator.__anext__()
			return result


		for i in range(subs_length):
			sub = subs[i]
			if not isinstance(sub._queue, Queue):
				# here is mb bug
				subs._queue = None
				del subs[i]
				continue
			data = await get_result()
			if data is Results.NO_DATA:
				return False
			await sub._queue.put(result)
		return True

	# what a stupid warning in pylint
	def __init__(self, backend: AbstractBackend, auto_start: Optional[bool] = False, *args, **kwargs): #pylint: disable=W1113
		"""Class init method"""
		assert isinstance(backend, AbstractBackend), "This is not a backend class instance"
		assert isinstance(auto_start, bool), "auto_start's datatype is Optional[bool]"
		self._backend = backend
		self._channel_subs: Dict[str, List[Subscription]] = {}
		self._is_started = False

		if auto_start:
			self.start(*args, **kwargs)

	def __del__(self):
		"""try to stop backend correctly"""
		try:
			self.stop()
		except NotImplementedError:
			pass

	def start(self, *args, **kwargs) -> None:
		"""try to start backend synchronously"""
		result = self._backend._start(*args, **kwargs)
		self._is_started = True
		return result

	def stop(self) -> None:
		"""try to stop backend synchronously"""
		result = self._backend._stop()
		self._is_started = False
		return result

	def publish(self, channel: str, message: Any, *args, **kwargs) -> None:
		"""A method that publishes message to channel"""
		self._check_instance_vars()
		assert not isinstance(message, Results), "message can't be this datatype"
		assert message == None, "message can't be None"
		assert isinstance(channel, str), "channel's datatype is str"
		assert self._is_started, "Backend is not started, SnowieCaster.start()"
		return self._backend._publish(channel, message, *args, **kwargs)

	async def asubscribe(self, channel: str) -> None:
		"""Subscribe to channel updates asynchronously"""
		self._check_instance_vars()
		assert isinstance(channel, str), "channel's datatype is str"
		assert self._is_started, "Backend is not started, SnowieCaster.start()"
		sub = Subscription(channel, self)
		if channel not in self._channel_subs:
			self._channel_subs[channel]: List[Subscription] = []
		self._channel_subs[channel].append(sub)
		return sub

	async def astart(self, *args, **kwargs) -> None:
		"""Start backend asynchronously"""
		result = await self._backend._astart(*args, **kwargs)
		self._is_started = True
		return result

	async def astop(self, *args, **kwargs) -> None:
		"""Stop backend asynchronously"""
		result = await self._backend._start(*args, **kwargs)
		self._is_started = False
		return result

	async def apublish(self, channel: str, message: Any, *args, **kwargs) -> None:
		"""Publish message to channel asynchronously"""
		self._check_instance_vars()
		assert not isinstance(message, Results), "message can't be SnowieCaster.abstract.Results \
		datatype (don't try import it)"
		assert isinstance(channel, str), "channel's datatype is str"
		assert self._is_started, "Backend is not started, SnowieCaster.start()"
		return await self._backend._apublish(channel, message, *args, **kwargs)
