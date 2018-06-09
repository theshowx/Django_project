from django.contrib.auth.models import *
from django.conf import settings
import os

class ImageField(models.ImageField):

    def save_form_data(self, instance, data):
        if data is not None:
            file = getattr(instance, self.attname)
            if file != data:
                file.delete(save=False)
        super(ImageField, self).save_form_data(instance, data)

class Artykul(models.Model):
    nazwa = models.CharField(max_length = 50)
    autor = models.ForeignKey(User, on_delete = models.CASCADE)
    obraz = models.ImageField(upload_to='blog_app/', null = True, blank = True)
    tresc = models.TextField(null = True, blank = True)
    dataUtworzenia = models.DateTimeField('Data utworzenia')

    def __str__(self):
        return self.nazwa + " by " + self.autor.username

    def delete(self, *args, **kwargs):
        if self.obraz:
            os.remove(os.path.join(settings.MEDIA_ROOT, self.obraz.name))
        super(Artykul,self).delete(*args,**kwargs)

class Komentarz(models.Model):
    tresc = models.TextField(null = True, blank = True)
    autor = models.ForeignKey(User, on_delete = models.CASCADE)
    dataZamieszczenia = models.DateTimeField("Data zamieszczenia")
    artykul = models.ForeignKey(Artykul, on_delete = models.CASCADE, null = True, blank = True)
    czyOdpowiedz = models.BooleanField(default=False)

    def __str__(self):
        return "Komentarz " + self.autor.username + " w " + self.artykul.__str__()

class Komentarz_odpowiedz(models.Model):
    komentarz = models.ForeignKey(Komentarz, on_delete = models.CASCADE)
    odpowiedz = models.OneToOneField(Komentarz, on_delete = models.CASCADE, related_name='Odpowiedz')
    artykul = models.ForeignKey(Artykul, on_delete = models.CASCADE, null = True, blank = True)
    dataZamieszczenia = models.DateTimeField("Data zamieszczenia", null = True, blank = True)

    @classmethod
    def create(cls, komentarz, odpowiedz, artykul):
        komentarz_odpowiedz = cls(komentarz=komentarz, odpowiedz=odpowiedz, artykul=artykul)
        return komentarz_odpowiedz


