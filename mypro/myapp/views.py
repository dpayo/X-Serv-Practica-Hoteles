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
from django.template.loader import get_template
from django.template import Context
from django.template import RequestContext
from django.shortcuts import render_to_response
# Create your views here.
mini=0;
maxi=10;

def show_aloj_id_frances(reuqest,id):
    fil = urllib2.urlopen( 'http://www.esmadrid.com/opendata/alojamientos_v1_fr.xml')
    tree = ET.parse(fil)
    root = tree.getroot()
    hotel=Hotel.objects.get(id=id)

    encontrado = False
    for child in root.iter('basicData'):
        name=child.find('name').text
        if name == hotel.name:
                print name
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
    fil = urllib2.urlopen( 'http://www.esmadrid.com/opendata/alojamientos_v1_en.xml')
    tree = ET.parse(fil)
    root = tree.getroot()
    hotel=Hotel.objects.get(id=id)
    print hotel.name
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
            print url
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
def show_aloj_id(request,id):
    pathf=request.path+"/xmlfrances"
    pathi=request.path+"/xmlingles"
    hotel=Hotel.objects.get(id=id)
    listimages=Image.objects.filter(hid=hotel.id)
    listcoms=""
    if request.method =='POST':
        value = request.POST.get('comentarios', "")
        comment=Comment(hid=hotel.id,com=hotel,text=value)
        comment.save()
    listcoms=Comment.objects.filter(hid=hotel.id)

    context = {'lista':listimages[0:5],'condicion':"",'url':hotel.url,'name':hotel.name,'address':hotel.address,'body':hotel.body,'comentarios':listcoms,'type':hotel.tipo,'stars':hotel.stars,'pathf':pathf,'pathi':pathi}
    return render_to_response('alojid.html', context,context_instance = RequestContext(request))

def show_aloj(request):
    lista=Hotel.objects.all()
    valuestars=""
    valuetype=""
    if request.method =='POST':
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


def show_hotels(request,usuario):
    value=""
    siz=""
    listhotels=HotelsUser.objects.filter(user=usuario)

    if len(listhotels)==0:
        return HttpResponse(" 404 Not Found ")

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
    context={'lista':listhotels,'color':value,'usuario':usuario,'size':siz}
    return render_to_response('user.html', context, context_instance = RequestContext(request))

def more(request):
    respuesta=""
    global maxi
    global mini
    maxi+=10
    mini+=10
    lista=Hotel.objects.all()
    listauser=PagUser.objects.all()
    context = {'lista':lista[0:10],'user':request.user.username,'listausers':listauser,'condicion':""}
    if request.user.is_authenticated():
            try:
                us=PagUser.objects.get(user=request.user.username)
            except PagUser.DoesNotExist:
                context = {'lista':lista[0:10],'user':request.user.username}
                return render_to_response('index.html', context, context_instance = RequestContext(request))
            context = {'lista':lista[0:10],'user':request.user.username,'listausers':listauser,'condicion':"",'color':us.color,'size':us.size}
    return render_to_response('index.html', context, context_instance = RequestContext(request))



def main(request):

    respuesta=""
    salida=""
    lista=Hotel.objects.all()
    listauser=PagUser.objects.all()

    for hotel in lista:
        print hotel.id
        if hotel.name== "Hilton Madrid Airport":
            print "fr "+str(hotel.id)
    if len(lista) == 0:
        print("Parsing....")
        theParser = make_parser()
        theHandler = myContentHandler()
        theParser.setContentHandler(theHandler)
        fil = urllib2.urlopen( 'http://www.esmadrid.com/opendata/alojamientos_v1_es.xml')
        theParser.parse(fil)

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
