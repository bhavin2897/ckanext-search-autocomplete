from __future__ import annotations
from typing import Iterable

import pytest

from ckan.tests import factories
from ckan.tests.helpers import call_action

import ckan.plugins as p
import ckanext.datapusher.interfaces as interfaces

from ckanext.search_autocomplete.interfaces import ISearchAutocomplete
from ckanext.search_autocomplete.utils import get_categories, CONFIG_IGNORE_SYNONYMS


def _tags(tags: Iterable[str]) -> list[dict[str, str]]:
    return [{"name": tag} for tag in tags]


class TestPlugin(p.SingletonPlugin):
    p.implements(ISearchAutocomplete)

    def get_categories(self):
        """
        Allows to redefine the default autocompletable categories

        Default:
        _facet_type_to_label = {
            'organization': 'Organisations',
            'tags': 'Tags',
            'res_format': 'Formats',
        }
        """
        return {"tags": "Tags"}


@pytest.mark.usefixtures("with_request_context", "with_plugins", "clean_db", "clean_index")
class TestSearchAutocomplete:
    ds_title = "Vegetation of the Mallee Cliffs National Park"

    def test_tags(self):
        factories.Dataset(tags=_tags(["fresh", "water", "fresh water"]))
        factories.Dataset(tags=_tags(["green", "water"]))
        results = call_action("search_autocomplete", q="fresh water")

        assert [t["label"] for t in results["categories"]] == [
            "fresh water",
            "water",
            "fresh",
        ]

    def test_tags_empty(self):
        factories.Dataset(tags=_tags(["fresh", "water", "fresh water"]))
        results = call_action("search_autocomplete", q="yellow car")

        assert not results["categories"]

    def test_org(self):
        group = factories.Organization(title="IBM")
        factories.Dataset(owner_org=group["id"])

        results = call_action("search_autocomplete", q="IBM")

        assert len(results["categories"]) == 1
        assert results["categories"][0]["label"] == "IBM"

    def test_org_empty(self):
        group = factories.Organization(title="IBM")
        factories.Dataset(owner_org=group["id"])

        results = call_action("search_autocomplete", q="Apple")

        assert not results["categories"]

    def test_res_format(self):
        dataset = factories.Dataset()
        factories.Resource(package_id=dataset["id"], format="XML")

        results = call_action("search_autocomplete", q="XML")

        assert len(results["categories"]) == 1
        assert results["categories"][0]["label"] == "XML"

    def test_res_format_empty(self):
        dataset = factories.Dataset()
        factories.Resource(package_id=dataset["id"], format="XML")

        results = call_action("search_autocomplete", q="ZIP")

        assert not results["categories"]

    def test_default_categories(self):
        group = factories.Organization(title="EXAMPLE")
        dataset = factories.Dataset(
            tags=_tags(
                [
                    "EXAMPLE",
                ]
            ),
            owner_org=group["id"],
        )
        factories.Resource(package_id=dataset["id"], format="EXAMPLE")

        results = call_action("search_autocomplete", q="EXAMPLE")

        assert len(results["categories"]) == len(get_categories())

    def test_deleted_dataset(self):
        factories.Dataset(state="deleted", title=self.ds_title)
        results = call_action("search_autocomplete", q="Park")

        assert not results["categories"]

    @pytest.mark.ckan_config("ckan.plugins", "search_autocomplete test_plugin")
    def test_custom_categories(self):
        group = factories.Organization(title="EXAMPLE")
        dataset = factories.Dataset(
            tags=_tags(
                [
                    "EXAMPLE",
                ]
            ),
            owner_org=group["id"],
        )
        factories.Resource(package_id=dataset["id"], format="EXAMPLE")

        results = call_action("search_autocomplete", q="EXAMPLE")

        assert len(results["categories"]) == 1
        assert results["categories"][0]["type"] == "Tags"

    def test_synonyms_applied_by_default(self):
        # "gib" is default test synonym, that is available out of the box
        # and expanded to "gigabyte"
        factories.Dataset(title="gib")
        result = call_action("search_autocomplete", q="gigabyte")
        assert len(result["datasets"]) == 1
        full = result["datasets"][0]

        result = call_action("search_autocomplete", q="gib")
        assert len(result["datasets"]) == 1
        short = result["datasets"][0]
        assert short == full

    @pytest.mark.ckan_config(CONFIG_IGNORE_SYNONYMS, "yes")
    def test_synonyms_ignored(self):
        # "gib" is default test synonym, that is available out of the box
        # and expanded to "gigabyte"
        factories.Dataset(title="gib")
        result = call_action("search_autocomplete", q="gigabyte")
        assert len(result["datasets"]) == 0

        result = call_action("search_autocomplete", q="gib")
        assert len(result["datasets"]) == 1
