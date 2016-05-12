from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
from xml.sax.handler import ContentHandler
from xml.sax import make_parser
from xmlparser import myContentHandler
import urllib2
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

    hotel=Hotel.objects.get(id=id)
    listimages=Image.objects.filter(hid=hotel.id)
    listcoms=""
    if request.method =='POST':
        value = request.POST.get('comentarios', "")
        comment=Comment(hid=hotel.id,com=hotel,text=value)
        comment.save()
    listcoms=Comment.objects.filter(hid=hotel.id)

    context = {'lista':listimages[0:5],'condicion':"",'url':hotel.url,'name':hotel.name,'address':hotel.address,'comentarios':listcoms,'type':hotel.tipo,'stars':hotel.stars}
    return render_to_response('alojid.html', context,context_instance = RequestContext(request))

def show_aloj(request):
    lista=Hotel.objects.all()
    context = {'lista':lista}
    if request.method =='POST':
        valuetype = request.POST.get('filtrotipo', "")
        valuestars=request.POST.get('filtrostars',"")
        if valuetype != "" and valuestars != "":
            lista=Hotel.objects.filter(tipo=valuetype,stars=valuestars)
        elif valuestars == "" and valuetype != "":
            lista=Hotel.objects.filter(tipo=valuetype)
        elif valuetype == "" and valuestars != "":
            lista=Hotel.objects.filter(stars=valuestars)
        context = {'lista':lista}
    return render_to_response('aloj.html', context, context_instance = RequestContext(request))


def show_hotels(request,usuario):
    value=""
    siz=""
    listhotels=HotelsUser.objects.filter(user=usuario)
    if len(listhotels)==0:
        return HttpResponse(" 404 Not Found ")
    us=PagUser.objects.get(user=usuario)

    print us.color
    if request.method =='POST':
        value = request.POST.get('css', "")
        siz= request.POST.get('size', "")
        print siz
        us=PagUser.objects.get(user=usuario)
        if value != "" :
            us.color=value;
        if siz != "":
            us.size=siz;
    us.save()
    value=us.color
    siz=us.size
    print "value "+value
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
    context = {'lista':lista[mini:maxi],'user':request.user.username,'listausers':listauser,'condicion':""}
    return render_to_response('index.html', context, context_instance = RequestContext(request))


def main(request):

    respuesta=""
    salida=""
    lista=Hotel.objects.all()

    listauser=PagUser.objects.all()

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
        us=PagUser.objects.get(user=request.user.username)
        context = {'lista':lista[0:10],'user':request.user.username,'listausers':listauser,'condicion':"",'color':us.color,'size':us.size}

    return render_to_response('index.html', context, context_instance = RequestContext(request))
