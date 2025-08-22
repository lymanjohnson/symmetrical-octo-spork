# tests/test_order_views.py
import datetime
import pytest
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from interview.order.models import Order
from interview.inventory.models import Inventory, InventoryType, InventoryLanguage


@pytest.fixture
def client():
    return APIClient()


@pytest.fixture
def inventory_items(db):
    """Create some Inventory items with required fields."""
    _type = InventoryType.objects.create(
        id=1,
        name="Movie",
    )
    _language = InventoryLanguage.objects.create(
        id=1,
        name="English",
    )
    _inventory_item = Inventory.objects.create(
        name="Item 1",
        created_at=datetime.datetime(2025, 8, 20, 12, 0),
        metadata={},
        language_id=1,
        type_id=1,
    )
    # Inventory.objects.create(
    #     name="Item 2",
    #     created_at=datetime.datetime(2025, 8, 22, 12, 0),
    #     metadata={},
    #     language_id=1,
    #     type_id=1,
    # )
    # Inventory.objects.create(
    #     name="Item 3",
    #     created_at=datetime.datetime(2025, 8, 25, 12, 0),
    #     metadata={},
    #     language_id=1,
    #     type_id=1,
    # )
    # Inventory.objects.filter(name="Item 1").update(created_at=datetime.datetime(2025, 8, 20, 12, 0))
    # Inventory.objects.filter(name="Item 2").update(created_at=datetime.datetime(2025, 8, 22, 12, 0))
    # Inventory.objects.filter(name="Item 3").update(created_at=datetime.datetime(2025, 8, 25, 12, 0))


@pytest.fixture
def active_order(db):
    _type = InventoryType.objects.create(
        id=1,
        name="Movie",
    )
    _language = InventoryLanguage.objects.create(
        id=1,
        name="English",
    )
    _inventory_item = Inventory.objects.create(
        name="Item 1",
        created_at=datetime.datetime(2025, 8, 20, 12, 0),
        metadata={},
        language_id=1,
        type_id=1,
    )
    """Create an active order for testing."""
    return Order.objects.create(
        inventory_id=1,
        start_date=datetime.datetime(2025, 8, 25, 12, 0).date(),
        embargo_date=datetime.datetime(2025, 8, 25, 12, 0).date(),
        is_active=True,  # initially active
        # add any other required fields here
    )


@pytest.mark.django_db
@pytest.mark.parametrize("new_status", [True, False])
def test_deactivate_order(client, active_order, new_status):
    """PUT request should set is_active=False or is_active=True."""
    url = reverse("order-deactivate", kwargs={"pk": active_order.pk})

    # Send PUT request with JSON body containing the new status
    response = client.put(url, {"is_active": new_status}, format="json")

    # Refresh from DB to get updated value
    active_order.refresh_from_db()

    assert response.status_code == status.HTTP_200_OK
    assert active_order.is_active is new_status
    assert response.data["is_active"] == new_status
