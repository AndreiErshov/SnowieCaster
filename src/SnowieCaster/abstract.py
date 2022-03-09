"""
This script is used to access an abstract class for other backends
"""

# pylint: disable=W0311, W0107, R0903
from abc import ABC, abstractmethod
from typing import AsyncIterator, Any
from enum import Enum


class Results(Enum):
	"""This class is using in SnowieCaster code for update_subscriptions method"""
	NO_DATA = 1
	NONE_DATA = 2


class SubscriptionUpdater(ABC):
	"""Abstract wrapper around SnowieCaster class for typization"""
	@abstractmethod
	async def _update_subscriptions(self, channel: str):
		"""Abstract method for typization"""
		pass


class AbstractBackend(ABC):
	"""Abstract class that created for multibackend support"""
	def _start(self, *args, **kwargs) -> None:
		raise NotImplementedError()

	def _stop(self) -> None:
		raise NotImplementedError()

	def _publish(self, channel: str, message: Any, *args, **kwargs) -> None:
		raise NotImplementedError()

	@abstractmethod
	async def _astart(self, *args, **kwargs) -> None:
		pass

	@abstractmethod
	async def _astop(self) -> None:
		pass

	@abstractmethod
	async def _apublish(self, channel: str, message: Any, *args, **kwargs) -> None:
		pass

	@abstractmethod
	async def _asubscribe(self, channel: str) -> AsyncIterator[Any]:
		pass


class ISyncBackend(AbstractBackend):
	"""Class that wraps sync methods to async"""

	async def _astart(self, *args, **kwargs) -> None:
		return self._start(*args, **kwargs)

	async def _astop(self) -> None:
		return self._stop()

	async def _apublish(self, channel: str, message: Any, *args, **kwargs) -> None:
		return self._publish(channel, message, *args, **kwargs)

