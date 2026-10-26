from django import forms
from .models import Checklist, Action


class ChecklistForm(forms.ModelForm):
    class Meta:
        model = Checklist
        fields = ["name"]

class ActionForm(forms.ModelForm):
    class Meta:
        model = Action
        fields = ["name","comment"]

    def clean_name(self):
        name = self.cleaned_data["name"]
        doublon = (Action.objects
                   .filter(checklist_id=self.instance.checklist_id, name=name)
                   .exclude(pk=self.instance.pk)
                   .exists())
        if doublon:
            raise forms.ValidationError("Une action porte déjà ce nom dans cette checklist.")
        return name