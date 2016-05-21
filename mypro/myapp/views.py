from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
from xml.sax.handler import ContentHandler
from xml.sax import make_parser
from xmlparser import myContentHandler
import urllib2
import xml.etree.ElementTree as ET
from django.http import HttpResponse,HttpResponseNotFound
from models import Hotel
from models import PagUser
from models import HotelsUser
from models import Image
from models import Comment
from django.contrib.auth.models import User
from django.template.loader import get_template
from django.template import Context
from django.template import RequestContext
from django.shortcuts import render_to_response
# Create your views here.
mini=0;
maxi=10;

def add_hotels(request,us,id):
    hotel=Hotel.objects.get(id=id)
    record =HotelsUser(user=us,hotel=hotel)
    record.save()
    context={'title':hotel.name}
    return render_to_response('hoteladd.html', context)

def about(request):
    context={}
    return render_to_response('about.html')
def show_aloj_id_frances(reuqest,id):
    fil = urllib2.urlopen( 'http://cursosweb.github.io/etc/alojamientos_fr.xml')
    tree = ET.parse(fil)
    root = tree.getroot()
    hotel=Hotel.objects.get(id=id)

    encontrado = False
    for child in root.iter('basicData'):
        name=child.find('name').text
        if name == hotel.name:
                encontrado=True;
                body=child.find('body').text
                phone=child.find('phone').text
                web=child.find('web').text
                if body == None:
                    body="Info no disponible"
                if phone == None:
                    phone= "Telefono no disponible"
                if web == None:
                    web= " Web no disponible"
                break;
    if not encontrado:
        return HttpResponse(" Hotel no disponible en este idioma")
    for child in root.iter('geoData'):
        address=child.find('address').text
        if address==hotel.address:
            country=child.find('country').text
            break;
    for child in root.iter('media'):
        url=child.find('url').text

        if url == hotel.source:
            break;
    if url == None:
        url= " imagen nos disponible"
    return HttpResponse("<h1>"+name+"</h1>"+body+phone+"<a href="+web+">"+name+"</a>"+"</br>"+address+"</br>"+country+"</br><img src="+url+"></img>")

def show_aloj_id_ingles(reuqest,id):
    encontrado=False;
    fil = urllib2.urlopen( 'http://cursosweb.github.io/etc/alojamientos_en.xml')
    tree = ET.parse(fil)
    root = tree.getroot()
    hotel=Hotel.objects.get(id=id)

    for child in root.iter('basicData'):
        name=child.find('name').text

        if name == hotel.name:
                encontrado=True;
                body=child.find('body').text
                phone=child.find('phone').text
                web=child.find('web').text
                if body == None:
                    body="Info no disponible"
                if phone == None:
                    phone= "Telefono no disponible"
                if web == None:
                    web= " Web no disponible"
                break;
    if not encontrado:
        return HttpResponse(" Hotel no disponible en este idioma")
    for child in root.iter('geoData'):
        address=child.find('address').text
        if address==hotel.address:
            country=child.find('country').text
            break;
    for child in root.iter('media'):
        url=child.find('url').text

        if url == hotel.source:
            break;

    return HttpResponse("<h1>"+name+"</h1>"+body+phone+"<a href="+web+">"+name+"</a>"+"</br>"+address+"</br>"+country+"</br><img src="+url+"></img>")

def show_userxml(request,usuario):
    if usuario == "Diego":
        f = open('userdiego.xml', 'r')

    elif usuario =="Luis":
        f = open('userluis.xml', 'r')

    elif usuario =="Isra":
        f = open('userisra.xml', 'r')
    xml=f.read()
    return HttpResponse(xml,content_type='text/xml')

def show_aloj_id(request,ide):
    pathf=request.path+"/xmlfrances"
    pathi=request.path+"/xmlingles"
    try:
        hotel=Hotel.objects.get(id=ide)
    except Hotel.DoesNotExist:
            context={'name': ""}
            return render_to_response('alojid.html',context);
    listimages=Image.objects.filter(hid=hotel.id)
    listcoms=""
    if request.method =='POST':
        value = request.POST.get('comentarios', "")

        n= hotel.numbercom+1;
        hotel.numbercom=n
        hotel.save()
        comment=Comment(hid=hotel.id,com=hotel,text=value)
        comment.save()
    listcoms=Comment.objects.filter(hid=hotel.id)
    us=PagUser.objects.get(user=request.user.username)
    context = {'lista':listimages[0:5],'condicion':"",'url':hotel.url,'name':hotel.name,'address':hotel.address,'body':hotel.body,'comentarios':listcoms,'type':hotel.tipo,'stars':hotel.stars,'pathf':pathf,'pathi':pathi,'id':ide,'email':hotel.email,
                'phone':hotel.phone,'color':us.color,'size':us.size}
    return render_to_response('alojid.html', context,context_instance = RequestContext(request))

def show_aloj(request):
    lista=Hotel.objects.all()
    valuestars=""
    valuetype=""

    if request.method == 'POST':
        valuetype = request.POST.get('filtrotipo', "")
        valuestars=request.POST.get('filtrostars',"")
        if valuetype != "" and valuestars != "":
            lista=Hotel.objects.filter(tipo=valuetype,stars=valuestars)
        elif valuestars == "" and valuetype != "":
            lista=Hotel.objects.filter(tipo=valuetype)
        elif valuetype == "" and valuestars != "":
            lista=Hotel.objects.filter(stars=valuestars)
    try:
        us=PagUser.objects.get(user=request.user.username)
    except PagUser.DoesNotExist:
            context = {'lista':lista,'stars':valuestars,'tipo':valuetype}
            return render_to_response('aloj.html', context, context_instance = RequestContext(request))
    context = {'lista':lista,'color':us.color,'size':us.size,'stars':valuestars,'tipo':valuetype}
    return render_to_response('aloj.html', context, context_instance = RequestContext(request))

def moreuser(request,usuario):
    value=""
    siz=""
    global maxi
    global mini
    maxi+=10
    mini+=10
    listhotels=HotelsUser.objects.filter(user=usuario)


    if request.method =='POST':
        value = request.POST.get('css', "")
        siz= request.POST.get('size', "")
        title=request.POST.get('titulo',"")
        try:
            us=PagUser.objects.get(user=usuario)
            if value != "" :
                us.color=value;
            if siz != "":
                us.size=siz;
            if title != "":
                us.title=title;
            us.save()
        except PagUser.DoesNotExist:
            record=PagUser(user=usuario,title=title,color=value,size=siz)
            record.save()

    try:
        us=PagUser.objects.get(user=usuario)
        us.save()
        value=us.color
        siz=us.size
        titel=us.title
    except PagUser.DoesNotExist:
            value =""
            siz=""
            title=""
    l=len(listhotels)
    context={'lista':listhotels[mini:maxi],'color':value,'usuario':usuario,'size':siz,'list_len':l}
    return render_to_response('user.html', context, context_instance = RequestContext(request))

def show_hotels(request,usuario):
    value=""
    siz=""
    try:
        username=User.objects.get(username=usuario)
    except User.DoesNotExist:
        usuario='Este usuario no existe '
        context={'usuario':usuario}
        return render_to_response('user.html', context, context_instance = RequestContext(request))
    listhotels=HotelsUser.objects.filter(user=usuario)


    if request.method =='POST':
        value = request.POST.get('css', "")
        siz= request.POST.get('size', "")
        title=request.POST.get('titulo',"")
        try:
            us=PagUser.objects.get(user=usuario)
            if value != "" :
                us.color=value;
            if siz != "":
                us.size=siz;
            if title != "":
                us.title=title;
            us.save()
        except PagUser.DoesNotExist:
            record=PagUser(user=usuario,title=title,color=value,size=siz)
            record.save()

    try:
        us=PagUser.objects.get(user=usuario)
        us.save()
        value=us.color
        siz=us.size
        titel=us.title
    except PagUser.DoesNotExist:
            value =""
            siz=""
            title=""


    context={'lista':listhotels[0:2],'color':value,'usuario':usuario,'size':siz}
    return render_to_response('user.html', context, context_instance = RequestContext(request))

def more(request):
    respuesta=""
    global maxi
    global mini
    maxi+=10
    mini+=10
    lista=Hotel.objects.all()
    listauser=PagUser.objects.all()
    context = {'lista':lista[mini:maxi],'user':request.user.username,'listausers':listauser,'condicion':""}
    if request.user.is_authenticated():
            try:
                us=PagUser.objects.get(user=request.user.username)
            except PagUser.DoesNotExist:
                context = {'lista':lista[mini:maxi],'user':request.user.username}
                return render_to_response('index.html', context, context_instance = RequestContext(request))
            context = {'lista':lista[mini:maxi],'user':request.user.username,'listausers':listauser,'condicion':"",'color':us.color,'size':us.size}
    return render_to_response('index.html', context, context_instance = RequestContext(request))



def main(request):
    listhotcoms=[]
    respuesta=""
    salida=""

    lista=Hotel.objects.all().order_by('-numbercom')
    listauser=PagUser.objects.all()
    users=User.objects.all()

    for user in users:
        try:
            name=PagUser.objects.get(user=user.username).title
        except PagUser.DoesNotExist:
            record=PagUser(user=user.username,title="",color="",size="")
            record.save()

    if len(lista) == 0:
        print("Parsing....")
        theParser = make_parser()
        theHandler = myContentHandler()
        theParser.setContentHandler(theHandler)
        fil = urllib2.urlopen( 'http://cursosweb.github.io/etc/alojamientos_es.xml')
        theParser.parse(fil)
    listauser=PagUser.objects.all()
    template = get_template("index.html")
    context = {'lista':lista[0:10],'user':request.user.username,'listausers':listauser,'condicion':""}
    if request.user.is_authenticated():
            try:
                us=PagUser.objects.get(user=request.user.username)
            except PagUser.DoesNotExist:
                context = {'lista':lista[0:10],'user':request.user.username}
                return render_to_response('index.html', context, context_instance = RequestContext(request))
            context = {'lista':lista[0:10],'user':request.user.username,'listausers':listauser,'condicion':"",'color':us.color,'size':us.size}
    return render_to_response('index.html', context, context_instance = RequestContext(request))
