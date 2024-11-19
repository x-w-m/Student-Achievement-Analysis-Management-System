from django.core.files.storage import FileSystemStorage
import os
from django.conf import settings


class UploadStorage(FileSystemStorage):
    def __init__(self, sub_path='uploads', *args, **kwargs):
        """
        初始化时可以动态设置子路径。
        :param sub_path: 相对于 MEDIA_ROOT 的子路径
        """
        location = os.path.join(settings.MEDIA_ROOT, sub_path)
        super().__init__(location=location, *args, **kwargs)
