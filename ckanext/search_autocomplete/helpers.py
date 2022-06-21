from __future__ import annotations

import ckan.plugins.toolkit as tk


CONFIG_ENABLE_DEFAULT_IMPLEMENTATION = "ckanext.search_autocomplete.enable_default_implementation"
CONFIG_SEARCH_ENDPOINT = "ckanext.search_autocomplete.dataset_search_endpoints"

DEFAULT_ENABLE_DEFAULT_IMPLEMENTATION = False
DEFAULT_SEARCH_ENDPOINT = "dataset.search group.read organization.read"

def get_helpers():
    return {
        "search_autocomplete_enable_default_implementation": enable_default_implementation,
    }


def enable_default_implementation() -> bool:
    return tk.asbool(tk.config.get(
        CONFIG_ENABLE_DEFAULT_IMPLEMENTATION,
        DEFAULT_ENABLE_DEFAULT_IMPLEMENTATION
    ))


def on_dataset_search_page() -> bool:
    endpoint = ".".join(tk.get_endpoint())
    return endpoint in tk.aslist(tk.config.get(
        CONFIG_SEARCH_ENDPOINT,
        DEFAULT_SEARCH_ENDPOINT
    ))
