from typing import Dict
from ckan.plugins.interfaces import Interface


class ISearchAutocomplete(Interface):
    def get_categories(self) -> Dict[str, str]:
        """
        Allows to redefine the default autocompletable categories

        Default:
        categories = {
            'organization': _('Organisations'),
            'tags': ('Tags'),
            'res_format': _('Formats'),
        }

        """
        return {}
