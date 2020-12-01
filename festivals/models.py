from django.db import models
from django.contrib.auth.models import User


# User model extension
class Additional(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    display_name = models.CharField(max_length=255)


# user permission groups:
#     organiser - edit event
#     admin - edit users
# add with: https://gist.github.com/bee-keeper/9857973


"""
class t_uzivatel(models.Model):
    # id is automatic PK
    email = models.EmailField()
    meno = models.CharField(max_length=255)
    priezvisko = models.CharField(max_length=255)
    heslo = models.CharField(max_length=255)

    # row identification
    def __str__(self):
        return self.meno[0] + ". " + self.priezvisko
"""


class t_festival(models.Model):
    # id is automatic PK
    nazov = models.CharField(max_length=255)
    rocnik = models.SmallIntegerField()
    zaciatok = models.DateField()
    koniec = models.DateField()
    miesto = models.CharField(max_length=255)
    kapacita = models.PositiveIntegerField()
    obrazok = models.CharField(max_length=255, default="https://images.unsplash.com/photo-1533174072545-7a4b6ad7a6c3?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=1950&q=80")
    popis = models.TextField()

    vytvoril = models.ForeignKey(User, on_delete=models.CASCADE)

    # model permissions
    class Meta:
        permissions = [
            ('edit_festival', 'Can create, edit and delete festivals')
        ]

    # row identification
    def __str__(self):
        return self.nazov + " " + self.rocnik + " - " + self.miesto


class t_stage(models.Model):
    # id is automatic PK
    nazov = models.CharField(max_length=255)
    popis = models.TextField(blank=True)

    festival_id = models.ForeignKey(t_festival, on_delete=models.CASCADE)

    # model permissions
    class Meta:
        permissions = [
            ('edit_stage', 'Can create, edit and delete stages')
        ]

    # row identification
    def __str__(self):
        return self.nazov + " @ " + self.festival_id.nazov + " " + self.festival_id.rocnik + " - " + self.festival_id.miesto


class t_interpret(models.Model):
    # id is automatic PK
    nazov = models.CharField(max_length=255)
    datum_vzniku = models.DateField()
    clenovia = models.TextField()
    albumy = models.TextField(blank=True)

    # model permissions
    class Meta:
        permissions = [
            ('edit_interpret', 'Can create, edit and delete inteprets')
        ]

    # row identification
    def __str__(self):
        return self.nazov


class t_rezervacia(models.Model):
    # id is automatic PK
    stav = models.CharField(max_length=50)
    email = models.EmailField(max_length=254)
    majitel = models.ForeignKey(User, on_delete=models.CASCADE, blank=True,null=True)
    
    # row identification
    def __str__(self):
        return self.majitel.meno[0] + ". " + self.majitel.priezvisko + ": " + self.typ


class t_listok(models.Model):
    # id is automatic PK
    typ = models.CharField(max_length=10)
    cena = models.SmallIntegerField()
    pocet = models.SmallIntegerField()
    popis = models.TextField(blank=True)

    id_festival = models.ForeignKey(t_festival, on_delete=models.CASCADE)


class r_rezervacia_na(models.Model):
    id_rezervacie = models.ForeignKey(t_rezervacia, on_delete=models.CASCADE)
    id_listku = models.ForeignKey(t_listok, on_delete=models.CASCADE)


class r_zucastni_sa(models.Model):
    id_festival = models.ForeignKey(t_festival, on_delete=models.CASCADE)
    id_interpret = models.ForeignKey(t_interpret, on_delete=models.CASCADE)


class r_vystupuje_na(models.Model):
    zaciatok = models.DateTimeField()
    koniec = models.DateTimeField()

    id_stage = models.ForeignKey(t_stage, on_delete=models.CASCADE)
    id_interpret = models.ForeignKey(t_interpret, on_delete=models.CASCADE)

