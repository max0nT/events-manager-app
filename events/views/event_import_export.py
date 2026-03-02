import import_export_extensions.api.views as import_export_views

from ..resources import EventResource


class EventExportViewSet(import_export_views.ExportJobViewSet):
    """Export api view class for `Event` models."""

    resource_class = EventResource


class EventImportViewSet(import_export_views.ImportJobViewSet):
    """Import api view class for `Event` models."""

    resource_class = EventResource
