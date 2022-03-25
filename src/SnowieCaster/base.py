#pylint: disable=W0311, W0212

# плохо кнч задокументировал, ну да ладно

"""
A general script for contacting with this library
"""

from asyncio import Queue
from typing import Any, Dict, Optional, List, AsyncGenerator
from .abstract import AbstractBackend, Results, SubscriptionUpdater


class Subscription:
	"""This class allows you to iterate through messages"""

	def __init__(self, channel: str, updater: SubscriptionUpdater):
		assert isinstance(channel, str), "channel's datatype is str"
		assert isinstance(updater, SubscriptionUpdater), "caster's datatype is SnowieCaster"
		self.channel = channel
		self.updater = updater
		self._queue = Queue()

	async def __aiter__(self) -> Optional[AsyncGenerator]:
		while True:
			if not isinstance(self._queue, Queue):
				break
			assert isinstance(self.channel, str), "channel's datatype is str"
			if self._queue.empty():
				await self.updater._update_subscriptions(self.channel)
			yield await self._queue.get()

	async def __aenter__(self):
		return self

	async def __aexit__(self, *args, **kwargs):
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
		if channel not in self._channel_subs:
			return False
		subs: List[Subscription] = self._channel_subs[channel]
		assert isinstance(subs, list)

		subs_length = len(subs)
		if subs_length < 1:
			return False

		result = Results.NONE_DATA
		async def get_result():
			nonlocal result
			if result is Results.NONE_DATA:
				result = await self._backend.aget_next(channel)
			return result


		for i in range(subs_length):
			sub = subs[i]
			assert isinstance(sub, Subscription), "sub's datatype isn't Subscription"
			if not isinstance(sub._queue, Queue):
				# here is mb bug
				sub._queue = None
				del subs[i]
				continue
			data = await get_result()
			if data is Results.NO_DATA:
				return False
			await sub._queue.put(data)
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
		if self._is_started:
			return False
		result = self._backend._start(*args, **kwargs)
		self._is_started = True
		return result

	def stop(self) -> None:
		"""try to stop backend synchronously"""
		if not self._is_started:
			return False
		result = self._backend._stop()
		self._is_started = False
		return result

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
		result = await self._backend._apublish(channel, message, *args, **kwargs)
		await self._update_subscriptions(channel)
		return result
