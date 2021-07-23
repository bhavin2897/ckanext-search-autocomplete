from typing import Dict

import ckan.plugins.toolkit as tk

from ckanext.search_autocomplete.utils import (
    _autocomplete_datasets,
    _autocomplete_categories,
)


@tk.side_effect_free
def search_autocomplete(context, data_dict):
    q = tk.get_or_bust(data_dict, "q")
    words = q.lower().split()

    if not words:
        return {
            "datasets": [],
            "categories": [],
        }

    # use only first two words. Otherwise we'll mess with
    # distributions of relevant suggestions per word
    datasets = _autocomplete_datasets(words)
    categories = _autocomplete_categories(words)

    return {
        "datasets": datasets,
        "categories": categories,
    }
