from django.db import models


class Usuario(models.Model):
    nome = models.CharField(max_length=30)
    email = models.EmailField()
    senha = models.CharField(max_length=64)

    def __str__(self) -> str:
        return self.nome


class Empresa(models.Model):
    # empresa
    # razao_social
    # CNPJ
    # logradouro
    # complemento
    # CEP
    # bairro
    # cidade
    # estado

    pass

    def __str__(self):
        return self.empresa


class Processo(models.Model):
    # processo
    # empresa
    # valor
    # unidade
    # data_entrada
    # assunto
    # observacao
    # tipo
    # objeto
    # data_inicial
    # data_final
    # fiscal1
    # fiscal2
    # relatório1
    # relatorio2

    pass

    def __str__(self):
        return self.processo


class Notas(models.Model):
    # processo
    # numero_nota
    # emissao
    # valor
    # período
    # atesto1
    # atesto2
    # programa_trabalho
    # elemento_despesa
    # fonte

    pass

    def __str__(self):
        return self.numero_nota


class Unidade(models.Model):
    # codigo
    # nome da unidade
    # endereço
    pass

    def __str__(self):
        return self.nome_unidade


class Fiscais(models.Model):
    # nome_fiscal
    # Matrícula
    pass

    def __str__(self):
        return self.nome_fiscal
