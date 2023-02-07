#pylint: disable=C0114, C0116, W0311, W0212
import pytest
from snowiecaster import SnowieCaster, Subscription


@pytest.mark.asyncio
@pytest.mark.usefixtures("create_test_caster_noauto")
async def test_subscription_init(create_test_caster_noauto):
	caster, _ = create_test_caster_noauto()
	await caster.astart()
	subscription = await caster.asubscribe("channel")
	assert isinstance(subscription, Subscription), "Bad subscription datatype"
	assert isinstance(subscription.updater, SnowieCaster)

@pytest.mark.asyncio
@pytest.mark.usefixtures("create_test_caster_noauto")
async def test_update_no_sub(create_test_caster_noauto):
	caster, _ = create_test_caster_noauto()
	await caster.astart()
	assert await caster._update_subscriptions("channel") is False, "Bad return value"

@pytest.mark.asyncio
@pytest.mark.usefixtures("create_test_caster_noauto")
async def test_caster_delete(create_test_caster_noauto):
	caster, _ = create_test_caster_noauto()
	await caster.astart()
	del caster

@pytest.mark.asyncio
@pytest.mark.usefixtures("create_test_caster_noauto")
async def test_caster_stop(create_test_caster_noauto):
	caster, _ = create_test_caster_noauto()
	assert caster.stop() is False, "Bad stop method"
	assert await caster.astop() is False, "Bad stop method"

@pytest.mark.asyncio
@pytest.mark.usefixtures("create_test_caster_noauto")
async def test_update_no_start(create_test_caster_noauto):
	caster, _ = create_test_caster_noauto()
	assert await caster._update_subscriptions("channel") is False, "Bad return value"

@pytest.mark.asyncio
@pytest.mark.usefixtures("create_test_caster_noauto")
async def test_caster_start(create_test_caster_noauto):
	caster, _ = create_test_caster_noauto()
	assert await caster.astart() is None
	assert caster.start() is False
	assert await caster.astart() is False
