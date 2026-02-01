from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from .models import Task
from django.db import connection

@login_required
def task_list(request):
    status = request.GET.get('status')
    title = request.GET.get('title')

    sql = f"""
        SELECT * FROM tasks_task
        WHERE owner_id = {request.user.id}
    """

    if status == 'done':
        sql += " AND is_done = 1"
    elif status == 'pending':
        sql += " AND is_done = 0"

    if title:
        # SQL Injection direta
        sql += f" AND title LIKE '%{title}%'"

    with connection.cursor() as cursor:
        cursor.execute(sql)
        rows = cursor.fetchall()

    tasks = Task.objects.raw(sql)

    return render(request, 'tasks/list.html', {'tasks': tasks})

@login_required
def create_task(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description', '')
        if title:
            Task.objects.create(owner=request.user, title=title, description=description)
            return redirect('task_list')
    return render(request, 'tasks/create.html')

@login_required
def edit_task(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    if request.method == 'POST':
        task.title = request.POST.get('title', task.title)
        task.description = request.POST.get('description', task.description)
        task.save()
        return redirect('task_list')
    return render(request, 'tasks/edit.html', {'task': task})

@login_required
def delete_task(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    if request.method == 'POST':
        task.delete()
        return redirect('task_list')
    return render(request, 'tasks/delete.html', {'task': task})

@login_required
def toggle_task(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    task.is_done = not task.is_done
    task.save()
    return redirect('task_list')
