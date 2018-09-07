from django.shortcuts import render

# Create your views here.
from django.shortcuts import  HttpResponse
from django.shortcuts import redirect
import os
import json
from article import models

def  index1(request):
    #result = models.Userinfor.objects.filter(username="chen").first()
    result1=models.Article.objects.filter(article_id=750).first()
    result=models.Article.objects.raw("select * from article where title like '%%男生%%'")
    return render(request, 'index1.html', {'article':result})


def index(request):
    result = models.Article.objects.all()
    count=len(result)
    num="总共"+str(count)+"篇文章"
    current_page = request.GET.get("p", 1)
    print(current_page)
    current_page = int(current_page)
    start = (current_page - 1) * 10
    end = current_page * 10
    data = result[start:end]
    all_count = count
    total_count, y = divmod(all_count, 10)
    if y:
        total_count += 1
    page_list = []
    nav = """<nav aria-label= "Page navigation" >
        <ul class ="pagination" >"""
    page_list.append(nav)
    page_num = 11
    start_index = 1
    end_index = 0
    if total_count < page_num:
        start_index = 1
        end_index = total_count + 1
    else:
        if current_page <= ((page_num + 1) / 2):
            start_index = 1
            end_index = page_num + 1
        else:
            start_index = current_page - (page_num - 1) / 2
            end_index = current_page + (page_num + 1) / 2
            if (current_page + (page_num - 1) / 2) > total_count:
                end_index = total_count + 1
                start_index = total_count - page_num + 1
    pre = ""
    if current_page == 1:
        pre = """<li>
            <a href="#" aria-label = "Previous" >
            <span aria-hidden = "true" > &laquo; </span></a>
           </li>"""

        # pre = '<a class="page" href="#">上一页</a>'
    else:
        pre = '<li>  <a href = "/'
        pre2 = """?p=%s" aria-label="Previous" >
                   <span aria-hidden="true" > &laquo; </span></a>
                  </li>""" % (current_page - 1)
        pre = pre + pre2
        #        print(pre)
    page_list.append(pre)

    for i in range(int(start_index), int(end_index)):
        if i == current_page:
            temp = '<li class ="active" > <a href="/?&p=%s">%s</a></li>' % (i, i)
            # temp = '<a class="page isactive" href="/s/?keyword='+keyword+'&p=%s">%s</a>' % (i, i)
        else:
            # temp = '<a class="page" href="/s/?keyword='+keyword+'&p=%s">%s</a>' % (i, i)
            temp = '<li> <a href="/?p=%s">%s</a></li>' % (i, i)
        page_list.append(temp)
    afterpage = ""
    if current_page == total_count:
        # afterpage = '<a class="page" href="#">下一页</a>'
        afterpage = """<li>
                    <a href="#" aria-label="Next">
                    <span aria-hidden="true">&raquo;</span></a>
                   </li>"""
    else:
        afterpage = '<li>  <a href = "/?'
        afterpage2 = """p=%s" aria-label="Next" >
                           <span aria-hidden ="true">&raquo;</span></a>
                          </li>""" % (current_page + 1)
        afterpage = afterpage + afterpage2
        # afterpage = '<a class="page" href="/s/?keyword='+keyword+'&p=%s">下一页</a>' % (current_page + 1)
        page_list.append(afterpage)
    nav2 = '</ul> </nav>'
    page_list.append(nav2)
    page_str = "".join(page_list)
    return render(request, 'index.html', {'article': data, 'num': num, 'page_str': page_str})



def search(request):
    keyword=request.GET.get("keyword",None)
    result=None
    if  keyword :
        result = models.Article.objects.raw("select distinct * from article where title like '%%"+keyword+"%%'")
    else :
       pass
    count=0
    for i in result:
        count=count+1
    num="查询到"+str(count)+"篇文章"
    #num=len(list(result))

    ###
    ##分页
    ##
    current_page = request.GET.get("p", 1)
    print(current_page)
    current_page = int(current_page)
    start = (current_page - 1) * 10
    end = current_page * 10
    data = result[start:end]
    all_count = count
    total_count, y = divmod(all_count, 10)
    if y:
        total_count += 1
    page_list = []
    nav="""<nav aria-label= "Page navigation" >
    <ul class ="pagination" >"""
    page_list.append(nav)
    page_num = 11
    start_index = 1
    end_index = 0
    if total_count < page_num:
        start_index = 1
        end_index = total_count + 1
    else:
        if current_page <= ((page_num + 1) / 2):
            start_index = 1
            end_index = page_num + 1
        else:
            start_index = current_page - (page_num - 1) / 2
            end_index = current_page + (page_num + 1) / 2
            if (current_page + (page_num - 1) / 2) > total_count:
                end_index = total_count + 1
                start_index = total_count - page_num + 1
    pre = ""
    if current_page == 1:
        pre="""<li>
        <a href="#" aria-label = "Previous" >
        <span aria-hidden = "true" > &laquo; </span></a>
       </li>"""



        #pre = '<a class="page" href="#">上一页</a>'
    else:
        pre = '<li>  <a href = "/s/?keyword='
        pre2="""&p=%s" aria-label="Previous" >
               <span aria-hidden="true" > &laquo; </span></a>
              </li>"""% (current_page - 1)
        pre = pre+keyword+pre2
        print(pre)
    page_list.append(pre)

    for i in range(int(start_index), int(end_index)):
        if i == current_page:
            temp='<li class ="active" > <a href="/s/?keyword='+keyword+'&p=%s">%s</a></li>' % (i, i)
            #temp = '<a class="page isactive" href="/s/?keyword='+keyword+'&p=%s">%s</a>' % (i, i)
        else:
            #temp = '<a class="page" href="/s/?keyword='+keyword+'&p=%s">%s</a>' % (i, i)
            temp = '<li> <a href="/s/?keyword=' + keyword + '&p=%s">%s</a></li>' % (i, i)
        page_list.append(temp)
    afterpage = ""
    if current_page == total_count:
        #afterpage = '<a class="page" href="#">下一页</a>'
        afterpage = """<li>
                <a href="#" aria-label="Next">
                <span aria-hidden="true">&raquo;</span></a>
               </li>"""
    else:
        afterpage = '<li>  <a href = "/s/?keyword='
        afterpage2 = """&p=%s" aria-label="Next" >
                       <span aria-hidden ="true">&raquo;</span></a>
                      </li>"""% (current_page + 1)
        afterpage = afterpage + keyword + afterpage2
        #afterpage = '<a class="page" href="/s/?keyword='+keyword+'&p=%s">下一页</a>' % (current_page + 1)
        page_list.append(afterpage)
    nav2='</ul> </nav>'
    page_list.append(nav2)
    page_str = "".join(page_list)
    return   render(request, 'index.html',{'article':data,'num':num,'page_str':page_str})
def article(request):
    id=request.GET.get("id",None)
    myarticle=models.Article.objects.filter(article_id=id ).first()
    return render(request,'article.html',{'article':myarticle})

def player(request):
    url='http://player.youku.com/embed/'
    id = request.GET.get("id", None)
    url=url+str(id)
    video_list = models.Video.objects.filter(video_id=id).first()
    title=video_list.title
    return render(request,'youkuvideo.html',{'url':url,'title':title})
def videoeducation(request):

    video_list = models.Video.objects.all()
    return render(request,'videoeducation.html',{'video_list':video_list})

def login(request):
    error=""
    if(request.method=='POST'):
        username=request.POST.get('username',None)
        password=request.POST.get('password',None)
        if username == "" or password == "":
            error = "账号密码不能为空"
            return render(request, "login.html", {'error': error})
        else:
          user= models.ArticleUserinfor.objects.filter(username=username).first()
          if not user :
              error="该用户不存在"
              return render(request, "login.html", {'error': error})

          if user.password==password :
              res = redirect('/userinfor/')
              res.set_cookie('username', username)
              return res
          error = "密码错误"
          return  render(request, "login.html", {'error': error})

    else:

      return render(request,'login.html')

def userinfor(request):
    name = request.COOKIES.get('username')
    if not name:
        return redirect('/login/')
    user=models.ArticleUserinfor.objects.filter(username=name).first()
    return render(request,'userinfor.html',{'user':user})

def sent_aritcle(request):
    name = request.COOKIES.get('username')
    if not name:
        return redirect('/login/')
    user = models.ArticleUserinfor.objects.filter(username=name).first()
    return render(request,'sent_article.html',{'user':user})

def insert_article(request):
    name = request.COOKIES.get('username')
    response = {'state': True}
    try:
       title = request.POST.get('title', None)
       content = request.POST.get('content', None)
       user=user = models.ArticleUserinfor.objects.filter(username=name).first()
       models.Article.objects.create(title=title, content=content,type_id='9',user_id=user.id)
       print(title)
    except :
        response['state'] = False
    return HttpResponse(json.dumps(response))

def register(request):
     error=""

     if request.method=='POST':
        try:
           username = request.POST.get('username', None)
           password1 = request.POST.get('password1', None)
           password2 = request.POST.get('password2', None)
           email = request.POST.get('email', None)
           phonenumber = request.POST.get('phonenumber', None)

           if username=="":
               error=error+"用户名不能为空"
           user =  models.ArticleUserinfor.objects.filter(username=username).first()
           if user:
               print("该用户已存在")
               error="该用户已存在"
               return render(request,'register.html',{'error':error})
           if password1=="" or password2=="" :
                error="密码或确认密码不能为空"
                return render(request, 'register.html', {'error': error})
           if password2 !=password1 :
                error="确认密码与密码不一致"
                return render(request, 'register.html', {'error': error})
           if not phonenumber:
               phonenumber=None
           models.ArticleUserinfor.objects.create(username=username,password=password1,phone_number=phonenumber,email=email)
           return  redirect('/login/')
        except :
            error = "出现异常"
            return render(request, 'register.html', {'error': error})
     return  render(request,'register.html')

def showhtml(request,id):
     return render(request,id+'.html')
def picedu(request):
    return  render(request,'picedu.html')
def manbody(request):
    return render(request,'manbody.html')
def womanbody(request):
    return render(request,'womenbody.html')