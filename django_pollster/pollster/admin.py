"""
Pollster Admin Module

Description:
    - This module contains the admin configuration for the pollster app.

"""

from typing import Any

from django.contrib import admin
from django.contrib.auth.admin import GroupAdmin
from django.contrib.auth.models import Group
from django.forms.models import ModelForm
from django.http import HttpRequest, HttpResponse
from django.utils.translation import gettext_lazy


# Subclass the Group model to change verbose name
class Role(Group):
    """
    Role Model

    Description:
        - This model is a subclass of the Group model.
        - It is used to represent the different roles that users can have.
        - The Group model is used to represent the different groups that users
        can belong to.
        - The Role model is a proxy model, meaning it doesn't create a new
        table in the database.
        - The Role model is used to change the verbose name of the Group model
        to "Role".
        - This is done to make the admin interface more user-friendly.

    Attributes:
        - `None`

    Methods:
        - `None`

    """

    class Meta:
        """
        Meta Class

        Description:
            - This class is used to define metadata options for the Role model.

        Attributes:
            - `proxy (bool)`: Proxy model means it won't create a new table.
            - `verbose_name (_StrPromise)`: Verbose name for the Role model.
            - `verbose_name_plural (_StrPromise)`: Verbose name for the Role
            model in plural form.

        Methods:
            - `None`

        """

        proxy = True  # Proxy model means it won't create a new table
        verbose_name = gettext_lazy("Role")
        verbose_name_plural = gettext_lazy("Roles")


# Unregister the original Group admin
if admin.site.is_registered(Group):
    admin.site.unregister(Group)


# Register the Role model with the custom RoleAdmin
@admin.register(Role)
class RoleAdmin(GroupAdmin):
    """
    Role Admin

    Description:
        - This class is used to configure the admin interface for the Role
        model.

    Attributes:
        - `None`

    Methods:
        - `changelist_view(self, request, extra_context=None) -> HttpResponse`:
            - Description:
                - This method is used to render the change list view for the
                Role model.

            - Args:
                - `request (HttpRequest)`: The request object.  **(Required)**
                - `extra_context (dict[str, str])`: Extra context to pass to
                the template. **(Optional)**

            - Returns:
                - `HttpResponse`: The response object.

        - `changeform_view(self, request, object_id=None, form_url='',
        extra_context=None) -> HttpResponse`:
            - Description:
                - This method is used to render the change form view for the
                Role model.

            - Args:
                - `request (HttpRequest)`: The request object.  **(Required)**
                - `object_id (str)`: The id of the object to change.
                **(Optional)**
                - `form_url (str)`: The form URL. **(Optional)**
                - `extra_context (dict[str, bool])`: Extra context to pass to
                the template. **(Optional)**

            - Returns:
                - `HttpResponse`: The response object.

        - `get_form(self, request, obj=None, **kwargs)`:
            - Description:
                - This method is used to get the form for the Role model.

            - Args:
                - `request (HttpRequest)`: The request object.  **(Required)**
                - `obj (Role)`: The Role object. **(Optional)**
                - `**kwargs`: Additional keyword arguments. **(Optional)**

            - Returns:
                - `RoleForm (ModelForm)`: The Role form.

    """

    def changelist_view(  # type: ignore
        self,
        request: HttpRequest,
        extra_context: dict[str, str] | None = None,
    ) -> HttpResponse:
        """
        Change List View

        Description:
            - This method is used to render the change list view for the Role
            model.

        Args:
            - `request (HttpRequest)`: The request object.  **(Required)**
            - `extra_context (dict[str, str])`: Extra context to pass to the
            template. **(Optional)**

        Returns:
            - `HttpResponse`: The response object.

        """

        extra_context = extra_context or {}
        extra_context["title"] = gettext_lazy(  # type: ignore
            "Select Role to change"
        )

        return super().changelist_view(
            request=request, extra_context=extra_context
        )

    def changeform_view(  # type: ignore
        self,
        request: HttpRequest,
        object_id: str | None = None,
        form_url: str = "",
        extra_context: dict[str, bool] | None = None,
    ) -> HttpResponse:
        """
        Change Form View

        Description:
            - This method is used to render the change form view for the Role
            model.

        Args:
            - `request (HttpRequest)`: The request object.  **(Required)**
            - `object_id (str)`: The id of the object to change. **(Optional)**
            - `form_url (str)`: The form URL. **(Optional)**
            - `extra_context (dict[str, bool])`: Extra context to pass to the
            template. **(Optional)**

        Returns:
            - `HttpResponse`: The response object.

        """

        extra_context = extra_context or {}
        if object_id:
            extra_context["title"] = gettext_lazy(  # type: ignore
                "Change Role"
            )

        else:
            extra_context["title"] = gettext_lazy("Add Role")  # type: ignore

        return super().changeform_view(
            request, object_id, form_url, extra_context=extra_context
        )

    def get_form(
        self,
        request: HttpRequest,
        obj: Any | None = None,
        change: bool = False,
        **kwargs: Any,
    ) -> type[ModelForm]:
        """
        Get Form

        Description:
            - This method is used to get the form for the Role model.

        Args:
            - `request (HttpRequest)`: The request object.  **(Required)**
            - `obj (Role)`: The Role object. **(Optional)**
            - `**kwargs`: Additional keyword arguments. **(Optional)**

        Returns:
            - `RoleForm (ModelForm)`: The Role form.

        """

        form = super().get_form(request, obj, **kwargs)

        form.base_fields["name"].label = gettext_lazy("Role name")
        return form

    list_display = ("name",)
    search_fields = ("name",)
