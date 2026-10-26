from django.urls import path

from . import views

app_name = "checklist"
urlpatterns = [
    path("", views.index, name="index"),
    path("list/<int:checklist_id>", views.checklist_detail , name="checklist_detail"),
    path("new_checklist", views.new_checklist, name="new_checklist"),
    path("confirm_delete_checklist/<int:checklist_id>", views.confirm_delete_checklist , name="confirm_delete_checklist"),
    path("delete_checklist/<int:checklist_id>", views.delete_checklist , name="delete_checklist"),
    path("update_checklist/<int:checklist_id>", views.update_checklist , name="update_checklist"),
    path("new_action/<int:checklist_id>", views.new_action, name="new_action"),
    path("action/<int:action_id>", views.action_detail , name="action_detail"),
    path("toggle_action/<int:action_id>", views.toggle_action , name="toggle_action"),
    path("up_action/<int:action_id>", views.up_action , name="up_action"),
    path("down_action/<int:action_id>", views.down_action , name="down_action"),
    path("delete_action/<int:action_id>", views.delete_action , name="delete_action"),
    path("update_action/<int:action_id>", views.update_action , name="update_action"),
]