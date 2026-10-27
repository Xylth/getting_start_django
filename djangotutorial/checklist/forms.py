from django import forms
from .models import Checklist, Action


class ChecklistForm(forms.ModelForm):
    class Meta:
        model = Checklist
        fields = ["name"]
        labels = {"name": "Nom"}
        widgets = {
            "name": forms.Textarea(attrs={
                "rows": 1,
            }),
        }

class ActionForm(forms.ModelForm):
    class Meta:
        model = Action
        fields = ["name","comment"]
        labels = {
            "name": "Nom",
            "comment": "Commentaire"
        }
        widgets = {
            "name": forms.Textarea(attrs={
                "rows": 1,
            }),
            "comment": forms.Textarea(attrs={
                "rows": 5,
            })
        }
    def clean_name(self):
        name = self.cleaned_data["name"]
        doublon = (Action.objects
                   .filter(checklist_id=self.instance.checklist_id, name=name)
                   .exclude(pk=self.instance.pk)
                   .exists())
        if doublon:
            raise forms.ValidationError("Une action porte déjà ce nom dans cette checklist.")
        return name