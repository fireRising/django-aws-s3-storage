from django.db import models
from django.contrib.auth.models import User
from diplom.storage_backends import PrivateMediaStorage
from cloud_storage.storage import OverwriteStorage


def user_directory_path(instance, filename):
    return 'user_{0}/{1}'.format(instance.user.id, filename)


class Folder(models.Model):
    name = models.CharField(max_length=90)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class FolderInFolder(models.Model):
    parent_folder = models.ForeignKey(Folder, on_delete=models.CASCADE, related_name='parent_folder_in_folder')
    child_folder = models.ForeignKey(Folder, on_delete=models.CASCADE, related_name='child_folders_in_folder')


class File(models.Model):
    # content = models.FileField(upload_to=user_directory_path, storage=PrivateMediaStorage())
    content = models.FileField(upload_to=user_directory_path, storage=OverwriteStorage())
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    folder = models.ForeignKey(Folder, on_delete=models.CASCADE)
    date_load = models.DateTimeField(auto_now_add=True)
    type = models.CharField(max_length=10)
    size = models.BigIntegerField()

    def __str__(self):
        return self.content

    def delete(self, *args, **kwargs):
        self.content.delete()
        super().delete(*args, **kwargs)


class SharedFile(models.Model):
    file = models.ForeignKey(File, on_delete=models.CASCADE)  # какой файл
    to_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='to_user_sharedfile')  # с каким пользователем поделен
    from_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='from_user_sharedfile')  # кто поделился
