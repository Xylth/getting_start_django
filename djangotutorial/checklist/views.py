from django.db import transaction
from django.db.models import F, Q, Count
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST

from .models import Checklist, Action
from .forms import ChecklistForm, ActionForm


# Create your views here.
def index(request):
    checklists = Checklist.objects.annotate(
        nb_actions = Count("actions"),
        nb_done = Count("actions", filter=Q(actions__status=True)),
    )
    return render(request, "checklist/index.html", {"checklists": checklists})

def checklist_detail(request,checklist_id):
    checklist = get_object_or_404(
        Checklist.objects.annotate(
            nb_actions=Count("actions"),
            nb_done=Count("actions", filter=Q(actions__status=True)),
        ),
        pk=checklist_id,
    )
    actions = Action.objects.filter(checklist_id = checklist_id).order_by("rank")
    return render(request, "checklist/checklist_detail.html", {"checklist": checklist, "actions": actions})

def new_checklist(request):
    if request.method == "POST":
        form = ChecklistForm(request.POST)
        if form.is_valid():
            checklist = form.save()
            return redirect( "checklist:checklist_detail", checklist_id = checklist.id )
    else:
        form = ChecklistForm()
    return render(request, "checklist/new_checklist.html",{"form": form},)

def update_checklist(request,checklist_id):
    checklist = get_object_or_404(Checklist, pk=checklist_id)
    if request.method == "POST":
        form = ChecklistForm(request.POST, instance=checklist)
        if form.is_valid():
            form.save()
            return redirect( "checklist:checklist_detail", checklist_id = checklist_id)
    else:
        form = ChecklistForm(instance=checklist)
    return render(request,"checklist/update_checklist.html",{"form": form, "checklist" : checklist})


def confirm_delete_checklist(request, checklist_id):
    checklist = get_object_or_404(
        Checklist.objects.annotate(
            nb_actions=Count("actions"),
            nb_done=Count("actions", filter=Q(actions__status=True)),
        ),
        pk=checklist_id,
    )
    actions = Action.objects.filter(checklist_id=checklist_id).order_by("rank")
    return render(request,"checklist/confirm_delete_checklist.html",{"checklist":checklist, "actions": actions})

@require_POST
def delete_checklist(request,checklist_id):
    checklist = get_object_or_404(Checklist,pk=checklist_id)
    checklist.delete()
    return redirect( "checklist:index")

def new_action(request, checklist_id):
    checklist = get_object_or_404(Checklist,pk=checklist_id)
    action = Action(checklist = checklist)
    if request.method == "POST":
        form = ActionForm(request.POST,instance=action)
        if form.is_valid():
            action = form.save(commit=False)
            action.rank =Action.objects.filter(checklist = checklist).count()
            action.save()
            return redirect("checklist:checklist_detail", checklist_id=checklist_id)
    else:
        form = ActionForm(instance=action)
    return render(request, "checklist/new_action.html", {"form": form,"checklist": checklist})

def action_detail(request, action_id):
    action = get_object_or_404(Action, pk= action_id)
    form = ActionForm(instance=action)
    return render(request, "checklist/action_detail.html", {"form": form,"action": action})

@require_POST
def toggle_action(request, action_id):
    action = get_object_or_404(Action, pk= action_id)
    action.status = not action.status
    action.save()
    return redirect( "checklist:checklist_detail", checklist_id = action.checklist_id)

@require_POST
def up_action(request, action_id):
    action = get_object_or_404(Action, pk= action_id)
    previous_action = Action.objects.filter(checklist_id = action.checklist_id, rank__lt= action.rank).order_by("-rank").first()
    if previous_action:
        with transaction.atomic():
            action.rank , previous_action.rank = previous_action.rank , action.rank
            action.save(update_fields=["rank"])
            previous_action.save(update_fields=["rank"])
    return redirect( "checklist:checklist_detail", checklist_id = action.checklist_id)

@require_POST
def down_action(request, action_id):
    action = get_object_or_404(Action, pk= action_id)
    next_action = Action.objects.filter(checklist_id = action.checklist_id, rank__gt= action.rank).order_by("rank").first()
    if next_action:
        with transaction.atomic():
            action.rank , next_action.rank = next_action.rank , action.rank
            action.save(update_fields=["rank"])
            next_action.save(update_fields=["rank"])
    return redirect( "checklist:checklist_detail", checklist_id = action.checklist_id)

@require_POST
def delete_action(request, action_id):
    action = get_object_or_404(Action, pk= action_id)
    with transaction.atomic():
        Action.objects.filter(checklist_id = action.checklist_id, rank__gt = action.rank).update(rank = F("rank") - 1)
        action.delete()
    return redirect( "checklist:checklist_detail", checklist_id = action.checklist_id)

def update_action(request,action_id):
    action = get_object_or_404(Action, pk= action_id)
    if request.method == "POST":
        form = ActionForm(request.POST, instance=action)
        if form.is_valid():
            action = form.save()
            return redirect("checklist:checklist_detail", checklist_id = action.checklist.id)
    else:
        form = ActionForm(instance=action)
    return render(request,"checklist/update_action.html",{"form" : form, "action":action},)

