from ckan.plugins.interfaces import Interface


class ISearchAutocomplete(Interface):
    def get_categories(self):
        '''
        Allows to redefine the default autocompletable categories

        Default: 
        categories = {
            'organization': _('Organisations'),
            'tags': ('Tags'),
            'res_format': _('Formats'),
        }

        '''
        pass
