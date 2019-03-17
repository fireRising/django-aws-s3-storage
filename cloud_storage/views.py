from django.shortcuts import render, redirect
from .forms import FileForm, FolderForm
from .models import File, FolderInFolder, SharedFile, Folder
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required


def home(request):
    count = User.objects.count()
    return render(request, 'cloud_storage/home.html', {
        'count': count
    })


@login_required
def list_files(request):
    # путь по папкам в виде элементов списка
    filter_folders = [folder for folder in request.path.split('/') if folder]

    # задаем корневой каталог
    url_string = '/' + filter_folders[0] + '/'
    url_parent_id = 1

    # проверяем правильность запрошенного content URL и узнаем ID запрашиваемой папки
    for ind, filter_folder in enumerate(filter_folders):
        folders = FolderInFolder.objects.filter(parent_folder__user=request.user.id,
                                                parent_folder__name=filter_folder)
        for next_folder in folders:
            if len(filter_folders) - 1 > ind and filter_folders[ind + 1] == next_folder.child_folder.name:
                url_string += next_folder.child_folder.name + '/'
                url_parent_id = next_folder.child_folder.id
                break

    error = False if url_string == request.path else True

    files = None
    folders = None
    file_form = None
    folder_form = None
    if not error:
        files = File.objects.filter(user=request.user.id, folder__id=url_parent_id)
        folders = FolderInFolder.objects.filter(parent_folder__user=request.user.id,
                                                parent_folder__id=url_parent_id)
        file_form = FileForm()
        folder_form = FolderForm()

    return render(request, 'cloud_storage/list_files.html', {
        'files': files,
        'folders': folders,
        'file_form': file_form,
        'folder_form': folder_form,
        'error': error,
        'url_parent_id': url_parent_id,
    })


@login_required
def shared_files(request):

    files_shared = SharedFile.objects.filter(to_user=request.user.id)

    return render(request, 'cloud_storage/shared_files.html', {
        'files_shared': files_shared,
    })


@login_required
def shared_files_post(request, file_id):
    if request.method == 'POST':
        to_user = User.objects.get(username=request.POST['username'])

        shared_file = SharedFile()
        shared_file.file_id = file_id
        shared_file.to_user = to_user
        shared_file.from_user = request.user
        shared_file.save()
    return redirect('home')


@login_required
def upload_file(request, folder_id):
    if request.method == 'POST':
        file_form = FileForm(request.POST, request.FILES)
        if file_form.is_valid():
            file = file_form.save(commit=False)
            file.user = request.user
            file.folder = Folder.objects.get(user=request.user, id=folder_id)
            file.size = int(file.content.size)
            file.type = str(file.content).split('.')[-1]
            file.save()
            return redirect('list_files')


@login_required
def delete_file(request, pk):
    if request.method == 'POST':
        file = File.objects.get(pk=pk)
        file.delete()
    return redirect('list_files')


@login_required
def create_folder(request, folder_id):
    if request.method == 'POST':
        folder_form = FolderForm(request.POST)
        if folder_form.is_valid():
            folder = folder_form.save(commit=False)
            folder.user = request.user
            folder.save()

            # заполняем связь между путями в FolderInFolder table
            parent_folder = Folder.objects.get(id=folder_id)
            child_folder = Folder.objects.get(id=folder.pk)
            new_folder = FolderInFolder(parent_folder=parent_folder, child_folder=child_folder)
            new_folder.save()
    return redirect('list_files')


@login_required
def delete_folder(request, pk):
    if request.method == 'POST':
        folder = Folder.objects.get(pk=pk)
        folder.delete()
    return redirect('list_files')


def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'cloud_storage/registration/signup.html', {
        'form': form
    })
