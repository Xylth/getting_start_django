from django.db import transaction
from django.db.models import F, Q, Count
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required

from .models import Checklist, Action
from .forms import ChecklistForm, ActionForm


# Create your views here.
@login_required
def index(request):
    checklists = Checklist.objects.annotate(
        nb_actions = Count("actions"),
        nb_done = Count("actions", filter=Q(actions__status=True)),
    ).filter(user=request.user)
    return render(request, "checklist/index.html", {"checklists": checklists})

@login_required
def checklist_detail(request,checklist_id):
    checklist = get_object_or_404(
        Checklist.objects.annotate(
            nb_actions=Count("actions"),
            nb_done=Count("actions", filter=Q(actions__status=True)),
        ),
        pk=checklist_id,
        user=request.user,
    )
    actions = Action.objects.filter(checklist_id = checklist_id).order_by("rank")
    return render(request, "checklist/checklist_detail.html", {"checklist": checklist, "actions": actions})

@login_required
def new_checklist(request):
    default_new_checklist = ChecklistForm()
    if request.method == "POST":
        form = ChecklistForm(request.POST)
        form.instance.user = request.user
        if form.is_valid():
            checklist = form.save(commit=False)
            checklist.user = request.user
            checklist.save()
            return redirect( "checklist:checklist_detail", checklist_id = checklist.id )
        else:
            form.data = default_new_checklist.data.copy()
    else:
        form = default_new_checklist
    return render(request, "checklist/new_checklist.html",{"form": form},)

@login_required
def update_checklist(request,checklist_id):
    checklist = get_object_or_404(Checklist, pk=checklist_id, user=request.user)
    initial = ChecklistForm(instance=checklist).initial
    if request.method == "POST":
        form = ChecklistForm(request.POST, instance=checklist)
        if form.is_valid():
            form.save()
            return redirect( "checklist:checklist_detail", checklist_id = checklist_id)
        form.data = initial
        checklist.refresh_from_db()
    else:
        form = ChecklistForm(instance=checklist)
    return render(request,"checklist/update_checklist.html",{"form": form, "checklist" : checklist})

@login_required
def confirm_delete_checklist(request, checklist_id):
    checklist = get_object_or_404(
        Checklist.objects.annotate(
            nb_actions=Count("actions"),
            nb_done=Count("actions", filter=Q(actions__status=True)),
        ),
        pk=checklist_id, user=request.user,
    )
    actions = Action.objects.filter(checklist_id=checklist_id).order_by("rank")
    return render(request,"checklist/confirm_delete_checklist.html",{"checklist":checklist, "actions": actions})

@login_required
@require_POST
def delete_checklist(request,checklist_id):
    checklist = get_object_or_404(Checklist,pk=checklist_id, user=request.user)
    checklist.delete()
    return redirect( "checklist:index")

@login_required
def new_action(request, checklist_id):
    checklist = get_object_or_404(Checklist,pk=checklist_id, user=request.user)
    if request.method == "POST":
        form = ActionForm(request.POST)
        form.instance.checklist = checklist
        if form.is_valid():
            action = form.save(commit=False)
            action.rank =Action.objects.filter(checklist = checklist).count()
            action.save()
            return redirect("checklist:checklist_detail", checklist_id=checklist_id)
        form.data = {}
    else:
        form = ActionForm()
    return render(request, "checklist/new_action.html", {"form": form,"checklist": checklist})

@login_required
def action_detail(request, action_id):
    action = get_object_or_404(Action, pk= action_id, checklist__user = request.user)
    form = ActionForm(instance=action)
    return render(request, "checklist/action_detail.html", {"form": form,"action": action})

@login_required
@require_POST
def toggle_action(request, action_id):
    action = get_object_or_404(Action, pk= action_id, checklist__user = request.user)
    action.status = not action.status
    action.save()
    return redirect( "checklist:checklist_detail", checklist_id = action.checklist_id)

@login_required
@require_POST
def up_action(request, action_id):
    action = get_object_or_404(Action, pk= action_id, checklist__user = request.user)
    previous_action = Action.objects.filter(checklist_id = action.checklist_id, rank__lt= action.rank).order_by("-rank").first()
    if previous_action:
        with transaction.atomic():
            action.rank , previous_action.rank = previous_action.rank , action.rank
            action.save(update_fields=["rank"])
            previous_action.save(update_fields=["rank"])
    return redirect( "checklist:checklist_detail", checklist_id = action.checklist_id)

@login_required
@require_POST
def down_action(request, action_id):
    action = get_object_or_404(Action, pk= action_id, checklist__user = request.user)
    next_action = Action.objects.filter(checklist_id = action.checklist_id, rank__gt= action.rank).order_by("rank").first()
    if next_action:
        with transaction.atomic():
            action.rank , next_action.rank = next_action.rank , action.rank
            action.save(update_fields=["rank"])
            next_action.save(update_fields=["rank"])
    return redirect( "checklist:checklist_detail", checklist_id = action.checklist_id)

@login_required
@require_POST
def delete_action(request, action_id):
    action = get_object_or_404(Action, pk= action_id, checklist__user = request.user)
    with transaction.atomic():
        Action.objects.filter(checklist_id = action.checklist_id, rank__gt = action.rank).update(rank = F("rank") - 1)
        action.delete()
    return redirect( "checklist:checklist_detail", checklist_id = action.checklist_id)

@login_required
def update_action(request, action_id):
    action = get_object_or_404(Action, pk=action_id, checklist__user=request.user)
    initial = ActionForm(instance=action).initial   # avant is_valid()

    if request.method == "POST":
        form = ActionForm(request.POST, instance=action)
        if form.is_valid():
            form.save()
            return redirect("checklist:checklist_detail", checklist_id=action.checklist_id)
        form.data = initial
        action.refresh_from_db()   # annule les modifs faites par is_valid()
    else:
        form = ActionForm(instance=action)

    return render(request, "checklist/update_action.html", {"form": form, "action": action})
