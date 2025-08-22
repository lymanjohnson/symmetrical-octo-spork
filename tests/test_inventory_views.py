import datetime
import pytest
from rest_framework import status
from rest_framework.test import APIClient
from django.urls import reverse
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
    Inventory.objects.create(
        name="Item 1",
        created_at=datetime.datetime(2025, 8, 20, 12, 0),
        metadata={},
        language_id=1,
        type_id=1,
    )
    Inventory.objects.create(
        name="Item 2",
        created_at=datetime.datetime(2025, 8, 22, 12, 0),
        metadata={},
        language_id=1,
        type_id=1,
    )
    Inventory.objects.create(
        name="Item 3",
        created_at=datetime.datetime(2025, 8, 25, 12, 0),
        metadata={},
        language_id=1,
        type_id=1,
    )
    Inventory.objects.filter(name="Item 1").update(created_at=datetime.datetime(2025, 8, 20, 12, 0))
    Inventory.objects.filter(name="Item 2").update(created_at=datetime.datetime(2025, 8, 22, 12, 0))
    Inventory.objects.filter(name="Item 3").update(created_at=datetime.datetime(2025, 8, 25, 12, 0))


@pytest.mark.django_db
def test_requires_query_params(client):
    """Should return 400 if no query params are provided."""
    url = reverse("inventory-list-after-date")
    response = client.get(url)
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "detail" in response.data
    assert response.data["detail"] == "You must provide 'after' or 'before' query parameters."


@pytest.mark.django_db
def test_filters_by_after_date(client, inventory_items):
    """Should return items on/after the 'after' date."""
    url = reverse("inventory-list-after-date")
    response = client.get(url, {"after": "2025-08-22"})
    assert response.status_code == status.HTTP_200_OK
    names = [item["name"] for item in response.data]
    assert "Item 1" not in names
    assert "Item 2" in names
    assert "Item 3" in names


@pytest.mark.django_db
def test_filters_by_before_date(client, inventory_items):
    """Should return items on/before the 'before' date."""
    url = reverse("inventory-list-after-date")
    response = client.get(url, {"before": "2025-08-22"})
    assert response.status_code == status.HTTP_200_OK
    names = [item["name"] for item in response.data]
    assert "Item 1" in names
    assert "Item 2" in names
    assert "Item 3" not in names


@pytest.mark.django_db
def test_filters_between_dates(client, inventory_items):
    """Should return items between 'after' and 'before' dates."""
    url = reverse("inventory-list-after-date")
    response = client.get(url, {"after": "2025-08-21", "before": "2025-08-24"})
    assert response.status_code == status.HTTP_200_OK
    names = [item["name"] for item in response.data]
    # Only Item 2 (22nd) falls in this range
    assert names == ["Item 2"]


@pytest.mark.django_db
def test_invalid_date_format(client):
    """Should return 400 if the date format is invalid."""
    url = reverse("inventory-list-after-date")
    response = client.get(url, {"after": "08-22-2025"})
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "after" in response.data
    assert response.data["after"] == "Invalid date format. Use YYYY-MM-DD."