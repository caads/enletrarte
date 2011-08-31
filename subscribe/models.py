#coding:utf-8
from django.db.models import Q
from django.db import models
from django.core.mail import send_mail


class Choices():

    vinculo = (
        ('PR', 'Professor'),
        ('AG', 'Aluno de Graduação'),
        ('AE', 'Aluno de Especialização/Aperfeiçoamento'),
        ('AM', 'Aluno de Mestrado'),
        ('AD', 'Aluno de Doutorado'),
        ('OU', 'Outro'),
    )

    titulacao = (
        (u'DT', u'Doutor'),
        (u'MT', u'Mestre'),
        (u'ES', u'Especialista'),
        (u'GR', u'Graduado'),
        (u'GN', u'Graduando'),
        (u'OU', u'Outro'),
    )

    participacao = (
        ('AO', 'Apenas Ouvinte'),
        ('AC', 'Apresentador de Comunicação'),
        ('AP', 'Apresentador de Pôster'),
    )

    sem_apresentacao = (
        ('AO', 'Apenas Ouvinte'),
    )

    situacao = (
        (u'Aprovado', u'Aprovado'),
        (u'Reprovado', u'Reprovado'),
        (u'Pendente', u'Pendente'),
    )

    publicar = (
        (u'SIM', u'Sim'),
        (u'NAO', u'Não'),
    )


class MiniCursos(models.Model):
    class Meta:
        verbose_name = 'Mini-Curso'
        verbose_name_plural = 'Mini-Cursos'

    id_minicurso = models.AutoField(primary_key=True)
    nome = models.CharField("Titulo", max_length=100)
    inscritos = models.IntegerField("Inscritos", default= 0)
    max_inscritos = models.IntegerField("Máximo Inscritos", default=40)
    cheio = models.IntegerField("Lotação", default =0, editable=False)    
    
    def __unicode__(self):
        return self.nome

class Inscricoes (models.Model):
    class Meta:
        verbose_name = 'Inscrição'
        verbose_name_plural = 'Inscrições'
    id_inscritos = models.AutoField("id", primary_key=True)
    nome = models.CharField("Nome", max_length=100)
    cpf = models.CharField ("CPF", max_length=14, unique=True)
    endereco = models.CharField ("Endereço", max_length=150)
    bairro = models.CharField ("Bairro", max_length=100)
    cep = models.CharField ("CEP", max_length=9)
    cidade = models.CharField("Cidade", max_length=100)
    uf = models.CharField("UF", max_length=2)
    telefone = models.CharField ("Telefone", max_length=14)
    celular = models.CharField("Celular", max_length=14)
    email = models.EmailField("Email",max_length=50)
    instituicao = models.CharField("Instituição", max_length=50)
    vinculo = models.CharField("Vínculo com a instituição", max_length=2, choices=Choices.vinculo)
    outro_1 = models.CharField("Qual", max_length=100, blank=True, null=True)
    titulacao = models.CharField("Titulação máxima", max_length=2, choices=Choices.titulacao)
    outro_2 = models.CharField('Qual', max_length=100, blank=True, null=True)
    participacao = models.CharField("Tipo de participação", max_length=2, choices=Choices.participacao)
    pub = models.CharField('Deseja ter seu trabalho completo publicado no cd dos Anais?', max_length=3, choices=Choices.publicar, help_text="Acréscimo de R$ 10,00 no valor da inscrição", blank=True, null=True)
    minicurso = models.ForeignKey(MiniCursos, related_name = 'Primeira Opção', verbose_name = 'Minicurso (Primeira Opção)')
    minicurso_2 = models.ForeignKey(MiniCursos, related_name = 'Segunda Opção',verbose_name = 'Minicurso (Segunda Opção)')
    data_inscricao = models.DateField("Data de Inscrição", auto_now_add=True)
    situacao = models.CharField("Situação", max_length=9, blank=True, choices = Choices.situacao, default='Pendente')
    reserva = models.CharField("Reserva", max_length=3, blank=True, choices=Choices.publicar, default='NAO')
    emails_env = models.IntegerField("Email enviado", default=0, editable=False)




    def __unicode__(self):
        return '%s - (%s)' %(self.nome, self.data_inscricao)

    

    def save(self, *args, **kwargs):
        a = self.minicurso
        b = self.minicurso_2
        preencher_vaga = MiniCursos.objects.get(nome=a)
        preencher_vaga_2 = MiniCursos.objects.get(nome=b)
        super(Inscricoes, self).save(*args, **kwargs)
    ## PREENCHE AS VAGAS SOMENTE COM OS CADASTROS APROVADOS ##
        preencher_vaga.inscritos = 0
        preencher_vaga_2.inscritos = 0
        minicurso1 = False
        minicurso2 = False

        for i in Inscricoes.objects.filter(minicurso=a, situacao='Aprovado'):
            preencher_vaga.inscritos +=1
        preencher_vaga.save()
        for i in Inscricoes.objects.filter(minicurso=b, situacao='Aprovado'):
            preencher_vaga_2.inscritos +=1
        preencher_vaga_2.save()

    ## ENVIA 1 EMAIL SOMENTE SE FOI APROVADO O CADASTRO ##
        if self.situacao == 'Aprovado' and self.reserva == 'NAO':
            send_mail('V - ENLETRARTE: Aprovação de Inscrição', 
                      'Prezado(a) %s,\n Sua inscrição foi aceita no V - ENLETRARTE para o minicurso: %s' %(self.nome, self.minicurso),
                      '',#email do evento
                      [self.email],
                      fail_silently=False)
            self.emails_env += 1

        if self.situacao == 'Reprovado':
            send_mail('V - ENLETRARTE: Aprovação de Inscrição', 
                      'Prezado(a) %s,\n Sua inscrição não foi aceita, porque não houve pagamento a sua inscrição.' %(self.nome),
                      '',#email do evento
                      [self.email],
                      fail_silently=False)
            self.emails_env += 1
