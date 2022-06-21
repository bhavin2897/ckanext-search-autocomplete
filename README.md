[![Tests](https://github.com/mutantsan/ckanext-search-autocomplete/workflows/Tests/badge.svg?branch=main)](https://github.com/mutantsan/ckanext-search-autocomplete/actions)

# ckanext-search-autocomplete

This extension provides an autocomplete for /datasets page search.
Autocomplete search by dataset titles and facets.

The default facets:
```
{
    'organization': _('Organisations'),
    'tags': ('Tags'),
    'res_format': _('Formats'),
}
```

You can redefine this by implementing the ISearchAutocomplete interface.


## Requirements

Compatibility with core CKAN versions:

| CKAN version    | Compatible? |
|-----------------|-------------|
| 2.6 and earlier | not tested  |
| 2.7             | not tested  |
| 2.8             | not tested  |
| 2.9             | yes         |
| 2.10            | yes         |

## Installation

To install ckanext-search-autocomplete:

1. Clone the source and install it on the virtualenv

    git clone https://github.com/mutantsan/ckanext-search-autocomplete.git
    cd ckanext-search-autocomplete
    pip install -e .
	pip install -r requirements.txt

2. Add `search_autocomplete` to the `ckan.plugins` setting in your CKAN
   config file.


## Config settings
TODO:

	# The item limit to show
	# (optional, default: 6).
	ckanext.search_autocomplete.autocomplete_limit = 10


	# Enable basic(example) template with the autocomplete widget.
    # You can use it for testing, but it's better to implement your own template,
    # because basic one is neither configurable, nor fancy-looking
	# (optional, default: false).
	ckanext.search_autocomplete.enable_default_implementation = yes

	# Space-separated list of CKAN endpoints(Flask endpoints in form `blueprint.view`).
    # It can be used if you want to enable autocomplete for non-standard dataset types, or on
    # the organization/group page.
	# (optional, default: dataset.search group.read organization.read).
	ckanext.search_autocomplete.dataset_search_endpoints = dataset.search custom_dataset_type.search

## Developer installation

To install ckanext-search-autocomplete for development, activate your CKAN virtualenv and
do:

    git clone https://github.com/mutantsan/ckanext-search-autocomplete.git
    cd ckanext-search-autocomplete
    python setup.py develop
    pip install -r dev-requirements.txt


## Tests

To run the tests, do:

    pytest --ckan-ini=test.ini

## License

[AGPL](https://www.gnu.org/licenses/agpl-3.0.en.html)
