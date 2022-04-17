#pylint: disable=C0114, C0116, W0311, W0212
from asyncio import Queue
import string
import random
import pytest

@pytest.mark.asyncio
@pytest.mark.usefixtures("create_memory_backend")
async def test_store_none(create_memory_backend):
	memory_backend = create_memory_backend()
	try:
		await memory_backend._apublish("channel", "message")
		assert False, "No exception"
	except AssertionError:
		pass

@pytest.mark.asyncio
@pytest.mark.usefixtures("create_memory_backend")
async def test_stop(create_memory_backend):
	memory_backend = create_memory_backend()
	memory_backend._stop()
	assert hasattr(memory_backend, 'store'), 'store is not defined, mb u call start?'
	assert isinstance(memory_backend.store, dict), \
	"store's datatype is not Dict[str, Queue]"

@pytest.mark.asyncio
@pytest.mark.usefixtures("create_caster")
async def test_get_all(create_caster):
	_, memory_backend = create_caster()
	result = await memory_backend._aget_all("channel")
	assert len(result) == 0, "Bad return"
	assert isinstance(memory_backend.store["channel"], Queue)

@pytest.mark.asyncio
@pytest.mark.usefixtures("create_caster")
async def test_subscription_iteration(create_caster):
	caster, _ = create_caster()
	subscription = await caster.asubscribe("channel")
	subscription._queue = None
	async for _ in subscription:
		assert False, "No data in subscription, but it's called"
	await caster._update_subscriptions("channel")
	assert len(caster._channel_subs["channel"]) == 0, "Bad length of channel subs list"

@pytest.mark.asyncio
@pytest.mark.usefixtures("create_caster")
async def test_update_no_data(create_caster):
	caster, _ = create_caster()
	await caster.asubscribe("channel")
	assert await caster._update_subscriptions("channel") is False, "Bad return value"

def generate_random(symbols):
	return ''.join(random.choices(
					string.ascii_uppercase + string.ascii_lowercase + string.digits, k=symbols
				))

@pytest.mark.asyncio
@pytest.mark.usefixtures("create_caster")
async def test_memory_caster(create_caster):
	caster, _ = create_caster()
	channel = generate_random(3000)
	channel2 = generate_random(3000)
	msgs = [generate_random(3000) for i in range(1000)]
	msgs2 = [generate_random(3000) for i in range(1000)]
	for msg in msgs:
		await caster.apublish(channel, msg)
	for msg in msgs2:
		await caster.apublish(channel2, msg)
	handler1 = await caster.asubscribe(channel)
	handler2 = await caster.asubscribe(channel)
	for i in range(2):
		times = 0
		if i == 0:
			handler = handler1
		elif i == 1:
			handler = handler2
		async with handler as data:
			async for data_value in data:
				if data_value is None:
					continue
				assert data_value == msgs[times]
				times += 1
				if times >= 1000:
					break
	await caster.astop()
