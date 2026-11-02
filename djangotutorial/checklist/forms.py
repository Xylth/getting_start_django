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

    def clean(self):
        cleaned_data = super().clean()
        name = cleaned_data.get("name")
        if name:
            doublon = (Checklist.objects
                       .filter(user_id=self.instance.user_id, name=name)
                       .exclude(pk=self.instance.pk)
                       .exists())
            if doublon:
                self.add_error("name", "Une liste porte déjà ce nom.")
        return cleaned_data


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
    def clean(self):
        cleaned_data = super().clean()
        name = cleaned_data.get("name")
        doublon = (Action.objects
                   .filter(checklist_id=self.instance.checklist_id, name=name)
                   .exclude(pk=self.instance.pk)
                   .exists())
        if doublon:
            self.add_error("name", "Une action porte déjà ce nom dans cette checklist.")
        return cleaned_data