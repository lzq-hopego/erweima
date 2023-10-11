'''
作者: 李展旗
Date: 2023-10-11 12:43:41
文件最后编辑者: 李展旗
LastEditTime: 2023-10-11 20:58:26
'''
from django.shortcuts import render,HttpResponse,redirect
from datetime import datetime
from qr.models import info
from qr.models import usr_log
from django import forms
from qr.utils import paginator
from qr.utils import settings
import qrcode
# Create your views here.


class InfoModelFrom(forms.ModelForm):
    class Meta:
        model=info
        fields=['title','info_text','url','info_type']
    def __init__(self,*args, **kwargs):
        super().__init__(*args, **kwargs)
        for i,field in self.fields.items():
            field.widget.attrs={'class':'form-control'}

def chakan(request,id):
    data=info.objects.filter(id=id).first()
    try:
        type=data.info_type
    except:
        return HttpResponse("无数据")

    ua=request.META.get('HTTP_USER_AGENT')

    if 'HTTP_X_FORWARDED_FOR' in request.META: 
         ip = request.META.get('HTTP_X_FORWARDED_FOR') 
    else:
         ip = request.META.get('REMOTE_ADDR')

    usr_log.objects.create(title_info=data.title,time=datetime.now(),ip=ip,ua=ua)

    if type==1:
        print(data.info_text)
        return render(request,'view_page.html',{'type':1,'info':str(data.info_text)})
    else:
        return render(request,'view_page.html',{'type':2,'info':str(data.url)})



def root(request):
    data_dict={}
    value=request.GET.get('q','')
    if value:
        data_dict["title__contains"]=value
    queryset=info.objects.filter(**data_dict).all().order_by("-id") 
    pag=paginator.paginator(queryset,request,4)
    page_data=pag.get_data(pag.page)
    html_data=pag.get_html(pag.page)
    # queryset=info.objects.all()
    return render(request,'info_ls.html',{'queryset':page_data,'html_data':html_data,'value':value})

def add(request):
    if request.method=='GET':
        form=InfoModelFrom()
        return render(request,'info_add.html',{'form':form})
    form=InfoModelFrom(data=request.POST)
    if form.is_valid():
        form.save()
        return redirect('/root/')
    return render(request,'info_add.html',{'form':form})

def delete(request,id):
    info.objects.filter(id=id).delete()
    return redirect('/root/')

def edit(request,id):
    data=info.objects.filter(id=id).first()
    if request.method=='GET':
        form=InfoModelFrom(instance=data)
        return render(request,'info_add.html',{'form':form})
    form=InfoModelFrom(data=request.POST,instance=data) #更新数据
    if form.is_valid():
        form.save()
        return redirect('/root/')
    return render(request,'info_add.html',{'form':form})

def view_log(request):
    data_dict={}
    value=request.GET.get('q','')
    if value:
        data_dict["title_info__contains"]=value
    queryset=usr_log.objects.filter(**data_dict).all().order_by("-id") 
    pag=paginator.paginator(queryset,request,5)
    page_data=pag.get_data(pag.page)
    html_data=pag.get_html(pag.page)
    # queryset=info.objects.all()
    return render(request,'views_ls.html',{'queryset':page_data,'html_data':html_data,'value':value})

def usr_log_delete(request,id):
    usr_log.objects.filter(id=id).delete()
    return redirect('/view/log/')

def qr(request,id):
    data=info.objects.filter(id=id).first()
    try:
        type=data.info_type
    except:
        return HttpResponse("失败")
    

    qr = qrcode.QRCode(version=1, box_size=10, border=5)
    

    data=settings.host+'/viwe/'+str(id)+"/"
    qr.add_data(data)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    img.save("qrcode.png")

    
    response = HttpResponse(content_type='application/png')
    response['Content-Disposition'] = 'attachment; filename="filename.png"'

    # 设置响应内容
    with open('qrcode.png','rb') as f:
        response.write(f.read())

    return response