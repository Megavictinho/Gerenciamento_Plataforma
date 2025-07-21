from django.db import models

class Plataforma(models.Model):
    nome = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.nome


class Pessoa(models.Model):
    nome = models.CharField(max_length=150)
    cpf = models.CharField(max_length=14, unique=True)  # formato 000.000.000-00 (com ou sem máscara)
    data_entrada = models.DateField()
    data_saida = models.DateField()
    foto = models.ImageField(upload_to='fotos_pessoas/', blank=True, null=True)

    def __str__(self):
        return f"{self.nome} ({self.cpf})"


class Log(models.Model):
    pessoa = models.ForeignKey(Pessoa, on_delete=models.CASCADE)
    plataforma = models.ForeignKey(Plataforma, on_delete=models.CASCADE)
    data_entrada = models.DateField()
    data_saida = models.DateField()
    
    @property
    def duracao(self):
        return (self.data_saida - self.data_entrada).days

    def __str__(self):
        return f"Log: {self.pessoa.nome} - {self.plataforma.nome} ({self.data_entrada} a {self.data_saida})"
