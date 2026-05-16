from __future__ import absolute_import, division, print_function
__metaclass__ = type

"""Unit tests for slxos_vcs_fabric module."""

from unittest.mock import MagicMock


TestCreate:
    def test_create_returns_resource(self):
        client = MagicMock()
        client.create.return_value = dict(id="123", name="test")
        result = client.create("vcs_fabric", dict(name="test"))
        assert result["id"] == "123"
        client.create.assert_called_once()

    def test_create_with_name(self):
        client = MagicMock()
        client.create.return_value = dict(id="456", name="prod")
        result = client.create("vcs_fabric", dict(name="prod"))
        assert result["name"] == "prod"


TestDelete:
    def test_delete_existing(self):
        client = MagicMock()
        client.delete("vcs_fabric", "123")
        client.delete.assert_called_once_with("vcs_fabric", "123")

    def test_delete_not_found(self):
        client = MagicMock()
        client.delete.return_value = None
        result = client.delete("vcs_fabric", "nonexistent")
        assert result is None


TestList:
    def test_list_returns_items(self):
        client = MagicMock()
        client.list.return_value = [dict(id="1"), dict(id="2")]
        result = client.list("vcs_fabric")
        assert len(result) == 2

    def test_list_empty(self):
        client = MagicMock()
        client.list.return_value = []
        result = client.list("vcs_fabric")
        assert len(result) == 0


TestGet:
    def test_get_existing(self):
        client = MagicMock()
        client.get.return_value = dict(id="123", name="test")
        result = client.get("vcs_fabric", "123")
        assert result["name"] == "test"

    def test_get_not_found(self):
        client = MagicMock()
        client.get.return_value = None
        result = client.get("vcs_fabric", "nonexistent")
        assert result is None


TestUpdate:
    def test_update_returns_updated(self):
        client = MagicMock()
        client.update.return_value = dict(id="123", name="updated")
        result = client.update("vcs_fabric", "123", dict(name="updated"))
        assert result["name"] == "updated"
