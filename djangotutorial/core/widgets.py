from django.forms import PasswordInput
from django.forms import CheckboxSelectMultiple

class UserTableWidget(CheckboxSelectMultiple):
    template_name = "core/partials/widgets/_user_table_widget.html"

class TogglePassInput(PasswordInput):
    template_name = "core/partials/widgets/_toggle_pass_widget.html"