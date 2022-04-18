#pylint: disable=C0114, C0116, W0311, W0212, E0110
import pytest
from SnowieCaster import abstract

@pytest.mark.asyncio
async def test_subscription_updater():
	abstract.SubscriptionUpdater.__abstractmethods__ = set()
	updater = abstract.SubscriptionUpdater()
	updater.get_request_delay()
	await updater._update_subscriptions("channel")

@pytest.mark.asyncio
async def test_abstract_backend():
	abstract.AbstractBackend.__abstractmethods__ = set()
	backend = abstract.AbstractBackend()
	try:
		backend._start()
		assert False, "Bad start abstract method"
	except NotImplementedError:
		pass
	try:
		backend._stop()
		assert False, "Bad stop abstract method"
	except NotImplementedError:
		pass
	await backend._astart()
	await backend._astop()
	await backend._apublish("channel", "message")
	await backend._aget_all("channel")

@pytest.mark.asyncio
async def test_backend_interface():
	abstract.ISyncBackend.__abstractmethods__ = set()
	backend = abstract.ISyncBackend()
	try:
		await backend._astart()
		assert False, "Bad start abstract method"
	except NotImplementedError:
		pass
	try:
		await backend._astop()
		assert False, "Bad stop abstract method"
	except NotImplementedError:
		pass
