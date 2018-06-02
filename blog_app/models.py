from django.contrib.auth.models import *

# class Uzytkownik(models.Model):
#     imie = models.CharField(max_length = 50)
#     nazwisko = models.CharField(max_length = 50)
#     email = models.EmailField(null = True, blank = True)
#     login = models.CharField(max_length = 50)
#     haslo = models.CharField(max_length = 50)

class Artykul(models.Model):
    nazwa = models.CharField(max_length = 50)
    autor = models.ForeignKey(User, on_delete = models.CASCADE)
    tresc = models.TextField(null = True, blank = True)
    #komentarz = models.ForeignKey(Komentarz, on_delete = models.CASCADE, null = True, blank = True)
    dataUtworzenia = models.DateTimeField('Data utworzenia')

    def __str__(self):
        return self.nazwa + " by " + self.autor.username

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
