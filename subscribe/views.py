# coding: utf-8

from django.shortcuts import render_to_response,get_object_or_404
from django.template import RequestContext
from django.http import HttpResponse, HttpResponseRedirect
from models import *
from emails import *
from forms import InscricoesForm, InscritosForm, CadastroForm
from django.core.mail import send_mail, get_connection, EmailMessage
from datetime import *
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist

def inscrever(request):
#Condição de datas (para alterar os valores e liberar inscrição)
    if date.today() <= date(2011, 10, 19):
        form = InscricoesForm()
        if request.method == 'POST':
            form = InscricoesForm(request.POST)
            if form.is_valid():
                success = True
                nome = request.POST.get('nome')
                part = request.POST.get('participacao')
                pub = request.POST.get('pub')
                vinculo = request.POST.get('vinculo')
                email = request.POST.get('email')
                if date.today() <= date(2011, 9, 19) and part == 'AC' or part == 'AP':
                    inscricao = 'R$ 70,00'
                    if pub == 'SIM':
                        valor_cd = 'R$ 10,00'
                        total = 'R$ 80,00' 
                    else:
                        valor_cd = 'R$ 0,00'
                        total = 'R$ 70,00'
                    conteudo_email = conteudo %(nome, inscricao, valor_cd, total)

                elif date.today() <= date(2011, 8, 31) and part != 'AC' or part != 'AP':
                    if vinculo == 'AG':
                        valor = 'R$ 40,00'
                    else:
                        valor = 'R$ 50,00'
                    conteudo_email = conteudo_2 %(nome, valor, valor)



                elif date.today() > date(2011, 8, 31) and date.today() <= date(2011, 10,18):
                    if vinculo == 'AG':
                        valor = 'R$ 50,00'
                    else:
                        valor = 'R$ 60,00'
                    conteudo_email = conteudo_2 %(nome, valor, valor)


                elif date.today() == date(2011, 10,19):
                    valor = 'R$ 70,00'
                    conteudo_email = conteudo_2 %(nome, valor, valor)

                    
                form.save()
    #           ENVIA O EMAIL DE CONFIRMAÇÃO DE INSCRIÇÃO
                send_mail('Inscrição Enletrarte', 
                          '%s' %conteudo_email,
                          '',#email do evento
                          [email],
                          fail_silently=False) 
                form = InscricoesForm()
                return render_to_response(
                    'inscrever.html',
                    {'success': success, 'form': form, 'email':email},
                    context_instance = RequestContext(request)
                )

        return render_to_response(
            'inscrever.html',
            {'form': form},
            context_instance=RequestContext(request),
        )
    else:
        expirou = True
        return render_to_response('expirou.html', {'expirou':expirou}, context_instance = RequestContext(request))



def resultado_esqueci(request):
    if request.method == 'POST':
        try:
            email = request.POST['email']
            consulta = User.objects.get(email=email) 
            random = User.objects.make_random_password(length=10, allowed_chars='abcdefghjkmnpqrstuvwxyzABCDEFGHJKLMNPQRSTUVWXYZ23456789')
            consulta.set_password(random)
            subject = 'V - ENLETRARTE: Nova Senha'
            message = ('Sua nova senha é:' + random)   
            from_email = ''#email do remetente
            connection = get_connection(username = '', password ='')#email e senha de conexão
            send_email = EmailMessage(subject, message , from_email, [consulta.email], connection = connection)
            send_email.content_subtype = "html"
            send_email.send()
            success = True
            consulta.save()  
        except ObjectDoesNotExist:
            consulta = ''
            mensagem = 'Este email não está cadastrado em nosso sistema!'
        return render_to_response('esqueci_email.html',{'success': success}, context_instance = RequestContext(request))
    else: 
        return render_to_response('esqueci_email.html', context_instance = RequestContext(request))

@login_required
def principal(request):
    inscritos = Inscricoes.objects.all()
    minicursos = MiniCursos.objects.all()
    return render_to_response('principal.html',{'inscritos':inscritos, 'minicursos':minicursos},context_instance=RequestContext(request)) 

@login_required
def listar_inscritos(request, codigo):
    inscritos = Inscricoes.objects.filter(minicurso=codigo, situacao='Aprovado')
    minicurso = MiniCursos.objects.get(pk=codigo)
    nome = minicurso.nome
    vagas = minicurso.max_inscritos
    tinscritos = minicurso.inscritos
    return render_to_response('listar_inscritos.html',{'inscritos':inscritos,'minicurso':nome, 'vagas':vagas, 'tinscritos':tinscritos },context_instance=RequestContext(request)) 

    

    

@login_required
def editar_inscrito(request, codigo):
    inscrito = get_object_or_404(Inscricoes, pk=codigo)
    mini_1 = get_object_or_404(MiniCursos, nome=inscrito.minicurso)
    insc_1 = mini_1.inscritos
    vagas_1 = mini_1.max_inscritos
    rest_1 = vagas_1 - insc_1
    mini_2 = get_object_or_404(MiniCursos, nome=inscrito.minicurso_2)
    insc_2 = mini_2.inscritos
    vagas_2 = mini_2.max_inscritos
    rest_2 = vagas_2 - insc_2
    if rest_1 == 0 and rest_2 > 0:
        inscrito.minicurso = inscrito.minicurso_2
        insc_1 = insc_2
        vagas_1 = vagas_2
        rest_1 = rest_2
    elif rest_1 <= 0 and rest_2 <= 0:
        inscrito.reserva = 'SIM'
        rest_1 = 0
        rest_2 = 0

    if request.method == "POST":
        a = InscritosForm(request.POST, instance=inscrito)
        if a.is_valid():
            c = a.save()
            return HttpResponseRedirect('/principal')
        else:
            return render_to_response('erro.html')
    else:
        a = InscritosForm(instance=inscrito)
        return render_to_response('editar_inscrito.html', {'a':a, 'inscrito':inscrito, 'codigo':codigo, 'insc_1': insc_1, 'insc_2': insc_2, 'vagas_1':vagas_1, 'vagas_2':vagas_2, 'rest_1':rest_1, 'rest_2':rest_2}, context_instance = RequestContext(request))

@login_required
def mostrar_aprovado(request, codigo):
    inscrito = get_object_or_404(Inscricoes, pk=codigo)
    return render_to_response('mostrar_aprovado.html', {'inscrito':inscrito}, context_instance = RequestContext(request))


