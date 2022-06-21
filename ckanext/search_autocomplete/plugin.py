import ckan.plugins as plugins
import ckan.plugins.toolkit as toolkit

from .logic.action import get_actions
from .helpers import get_helpers


class SearchAutocompletePlugin(plugins.SingletonPlugin):
    plugins.implements(plugins.IConfigurer)
    plugins.implements(plugins.IActions)
    plugins.implements(plugins.ITemplateHelpers)

    # ITemplateHelpers

    def get_helpers(self):
        return get_helpers()

    # IConfigurer

    def update_config(self, config_):
        toolkit.add_template_directory(config_, "templates")
        toolkit.add_public_directory(config_, "public")
        toolkit.add_resource("fanstatic", "search_autocomplete")
        toolkit.add_resource("assets", "search_autocomplete")

    # IActions

    def get_actions(self):
        return get_actions()
