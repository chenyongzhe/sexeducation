from django.http import JsonResponse
from django.shortcuts import render
#wangchaojun
# Create your views here.
from django.shortcuts import  HttpResponse
from django.shortcuts import redirect
import os
import json
from article import models
from django.core.cache import cache
##from alipay import AliPay
from django.conf import settings
import datetime
import time
from django.db.models import Q

def addscore(myrequest,num):
    name = myrequest.COOKIES.get('username')
    if name:
        user = models.ArticleUserinfor.objects.filter(username=name).first()
        score=int(user.score)+num
        models.ArticleUserinfor.objects.filter(id=user.id).update(score=score)



def  index1(request):
    #result = models.Userinfor.objects.filter(username="chen").first()
    result1=models.Article.objects.filter(article_id=750).first()
    result=models.Article.objects.raw("select * from article where title like '%%男生%%'")
    return render(request, 'index1.html', {'article':result})


def index(request):
    addscore(request,2)
    #cache.set("name","陈永喆")
    #myname=cache.get("name")
    #print(myname)
    result = models.Article.objects.all()
    count=len(result)
    num="总共"+str(count)+"篇文章"
    current_page = request.GET.get("p", 1)
    print(current_page)
    current_page = int(current_page)
    start = (current_page - 1) * 10
    end = current_page * 10
    print(result[1].title)
    result.reverse()
    print(result[1].title)
    data1 = result[count-end:count-start]
    data=list(data1)
    data.reverse()
    print(data[1].title)
    all_count = count
    total_count, y = divmod(all_count, 10)
    if y:
        total_count += 1
    page_list = []
    nav = """<nav aria-label= "Page navigation" >
        <ul class ="pagination" >"""
    page_list.append(nav)
    page_num = 7
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
    addscore(request, 2)
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
    page_num = 7
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
    addscore(request, 2)
    myid=request.GET.get("id",None)
    myarticle=models.Article.objects.filter(article_id=myid ).first()
    #print(myarticle.title)
    comment=[]
    mycommtent = models.Comment.objects.filter(article_id=myid)
    for cc in mycommtent:
        user=models.ArticleUserinfor.objects.filter(id=cc.user_id).first()
        comment_tamp={}
        comment_tamp["username"]=user.username
        comment_tamp["user_id"]=user.id
        comment_tamp["comment_content"]=cc.comment_content
        comment_tamp["nickname"]=user.nickname
        comment.append(comment_tamp)
    comment_cookie=""
    comment_cookie = request.COOKIES.get('comment_cookie',None)

    if comment_cookie !=None and comment_cookie !="N":
      comment_cookie = json.loads(comment_cookie)
      #print(comment_cookie)
    if comment_cookie ==None or comment_cookie =='N':
             comment_cookie=""
    print(comment_cookie)
    name = request.COOKIES.get('username')
    myclass="fa fa-thumbs-o-up"
    if name:
      user = models.ArticleUserinfor.objects.filter(username=name).first()
      sp=models.Support.objects.filter(user_id=user.id, article_id=myid).first()
      if sp:
          myclass="fa fa-thumbs-up"
    myrender=render(request,'article.html',{'article':myarticle,'comment':comment,'comment_cookie':comment_cookie,'supportcount':myarticle.supportcount,'myclass':myclass})
    myrender.set_cookie('comment_cookie',"N")
    return myrender

def player(request):
    addscore(request, 2)
    url='http://player.youku.com/embed/'
    id = request.GET.get("id", None)
    url=url+str(id)
    video_list = models.Video.objects.filter(video_id=id).first()
    title=video_list.title
    return render(request,'youkuvideo.html',{'url':url,'title':title})
def videoeducation(request):
    addscore(request, 2)
    video_list = models.Video.objects.all()
    return render(request,'videoeducation.html',{'video_list':video_list})

def login(request):
    msg={}
    error = ""
    msg['username']=""
    msg['password']=""
    isredict=False
    username = request.GET.get('aid', None)
    if request.method=='GET':
        username = request.GET.get('username', None)
        password = request.GET.get('p', None)

        if username ==None and password==None:
            print("没问题")
            return render(request, 'login.html',{'error': error,'msg':msg})
        else:
            msg['username'] = username
            msg['password'] = password
            return render(request, 'login.html',{'error': error,'msg':msg})

    if(request.method=='POST'):
        username=request.POST.get('username',None)
        password=request.POST.get('password',None)
        if username == "" or password == "":
            error = "账号密码不能为空"
            return render(request, "login.html", {'error': error,'msg':msg})
        else:
          user= models.ArticleUserinfor.objects.filter(username=username).first()
          if not user :
              error="该用户不存在"
              return render(request, "login.html", {'error': error,'msg':msg})

          if user.password==password :
              res = redirect('/userinfor/')
              res.set_cookie('username', username)
              aid = request.COOKIES.get('aid')
              print(aid)
              if aid !=None and (aid !='N'):
                  res1 = redirect('/article?id='+aid)
                  res1.set_cookie('aid', "N")
                  res1.set_cookie('username', username)
                  return res1
              return res
          error = "密码错误"
          return  render(request, "login.html", {'error': error,'msg':msg})

    else:

      return render(request,'login.html',{'error': error,'msg':msg})

def userinfor(request):
    name = request.COOKIES.get('username')
    if not name:
        return redirect('/login/')
    user=models.ArticleUserinfor.objects.filter(username=name).first()
    myarticle= models.Article.objects.filter(user_id=user.id)
    sex=""
    csssex=""
    if user.gender==0:
        sex='fa fa-mars'
        csssex="color:blue"
    else:
        sex = 'fa fa-venus'
        csssex = "color:pink"
    return render(request,'userinfor.html',{'user':user,'myarticle':myarticle,"imgurl":user.imgurl,"sex":sex,"csssex":csssex,"score":user.score})

def sent_aritcle(request):
    name = request.COOKIES.get('username')
    if not name:
        return redirect('/login/')
    user = models.ArticleUserinfor.objects.filter(username=name).first()
    return render(request,'sent_article.html',{'user':user})

def insert_article(request):
    addscore(request, 20)
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
           nickname = request.POST.get('nickname', None)
           if username=="":
               error=error+"账号不能为空"
               return render(request, 'register.html', {'error': error})
           if not ( (username.isalpha() or username.isdigit()) and username.isalnum()):
               error = error + " 账号只能是字母和数字"
               return render(request, 'register.html', {'error': error})
           if nickname=="":
               error = error + " 昵称不能为空"
               return render(request, 'register.html', {'error': error})

           user =  models.ArticleUserinfor.objects.filter(username=username).first()
           if user:
               print("该用户已存在")
               error="该账号已存在"
               return render(request,'register.html',{'error':error})
           if password1=="" or password2=="" :
                error="密码或确认密码不能为空"
                return render(request, 'register.html', {'error': error})
           if password2 !=password1 :
                error="确认密码与密码不一致"
                return render(request, 'register.html', {'error': error})
           if not phonenumber:
               phonenumber=None
           models.ArticleUserinfor.objects.create(username=username,password=password1,phone_number=phonenumber,email=email,nickname=nickname)
           return  redirect('/login/?username='+username+'&p='+password1)
        except :
            error = "出现异常"
            return render(request, 'register.html', {'error': error})
     return  render(request,'register.html')

def showhtml(request,id):
     addscore(request, 2)
     return render(request,id+'.html')
def picedu(request):
    # result = models.Article.objects.all()
    # article=[]
    # for myre in result:
    #     a={}
    #     a['article_id']=myre.article_id
    #     a['title']=myre.title
    #     a['content']=myre.content
    #     a['type_id']=myre.type_id
    #     a['user_id']=myre.user_id
    #     cache.set('article:'+str(myre.article_id), json.dumps(a))
    # #print(json.loads(cache.get('article:*')))
    # it=cache.keys("article:*")
    # for i in it:
    #     print(i)

    #cache.set('article',json.dumps(article))
    addscore(request, 2)
    return  render(request,'picedu.html')
def manbody(request):
    addscore(request, 2)
    return render(request,'manbody.html')
def womanbody(request):
    addscore(request, 2)
    return render(request,'womenbody.html')
def insert_comment(request):
    addscore(request, 10)
    name = request.COOKIES.get('username')
    response={}
    response['islogin']='True'
    if not name:
        print("空")
        response['islogin']='False'
        response=HttpResponse(json.dumps(response))
        article_id = request.POST.get('article_id', None)
        mycomment = request.POST.get('mycomment', None)
        response.set_cookie('aid', article_id)
        if mycomment !=None:
           response.set_cookie('comment_cookie', json.dumps(mycomment))
        return response
    response['state']=True
    try:
        ##title = request.POST.get('myconment', None)
        mycomment = request.POST.get('mycomment', None)
        article_id=request.POST.get('article_id',None)
        #print(mycomment)

        user = models.ArticleUserinfor.objects.filter(username=name).first()
        models.Comment.objects.create(comment_content=mycomment, article_id=article_id, user_id=user.id)

    except:
        response['state'] = False
    return HttpResponse(json.dumps(response))

def showuser(request):
    user_id=request.GET.get('user_id', None)
    user = models.ArticleUserinfor.objects.filter(id=user_id).first()
    name = request.COOKIES.get('username')
    me=None
    followlist=[]
    followerlist = []
    #followerlist = []
    followees = []
    if True:
        if name:
           me = models.ArticleUserinfor.objects.filter(username=name).first()
        follows = models.Follow.objects.filter(follower=user_id)
        followlist=[]

        for ff in follows:
            followee=models.ArticleUserinfor.objects.filter(id=ff.followee).first()
            followees.append(followee)
            followlist.append(ff.followee)
        followers = models.Follow.objects.filter(followee=user_id)

        for ff in followers:
            follower = models.ArticleUserinfor.objects.filter(id=ff.follower).first()
            followerlist.append(follower)
    myarticle = models.Article.objects.filter(user_id=user_id)
    sex = ""
    csssex = ""
    if user.gender == 0:
        sex = 'fa fa-mars'
        csssex = "color:blue"
    else:
        sex = 'fa fa-venus'
        csssex = "color:pink"

    return render(request, 'user.html', {'user': user,"me":me,"followeelist":followees,"followerlist":followerlist,"followId_list":followlist,"me":me, 'myarticle': myarticle,'imgurl':user.imgurl,"sex":sex,"csssex":csssex})

def zhan(request):
    name = request.COOKIES.get('username')
    response = {'state': True}
    response['islogin'] = 'True'
    if not name:
        response['islogin'] = 'False'
        myresponse = HttpResponse(json.dumps(response))
        article_id = request.POST.get('article_id', None)
        #mycomment = request.POST.get('mycomment', None)
        #print(article_id+"id")
        myresponse.set_cookie('aid', article_id)

        return myresponse
    try:
        article_id = request.POST.get('article_id', None)
        add = request.POST.get('add', None)
        user = models.ArticleUserinfor.objects.filter(username=name).first()
        myarticle=models.Article.objects.filter(article_id=article_id).first()
        count=int(myarticle.supportcount)
        if(add=="1"):
            count = count + 1
            models.Article.objects.filter(article_id=article_id).update(supportcount=count)
            models.Support.objects.create(user_id=user.id,article_id=article_id)
        else:
            count=count-1
            models.Article.objects.filter(article_id=article_id).update(supportcount=count)
            models.Support.objects.filter(user_id=user.id,article_id=article_id).delete()
        #models.Article.objects.filter(article_id=article_id).update(supportcount=count)
        response['count']=str(count)
        print(user.username)
    except:
        response['state'] = False

    return   HttpResponse(json.dumps(response))

# def create_alipay():
#     ali_pay = AliPay(
#         appid=settings.ALIPAY_APPID,
#         app_notify_url=None,
#         app_private_key_path=os.path.join(settings.BASE_DIR, 'static\\s2048.txt'),
#         alipay_public_key_path=os.path.join(settings.BASE_DIR, 'static\\g2048.txt'),
#         sign_type='RSA2',
#         debug=True)
#     return ali_pay
#
#
#
# def get_alipay_page():
#     ali_pay = AliPay(
#         appid=settings.ALIPAY_APPID,
#         app_notify_url=None,
#         app_private_key_path=os.path.join(settings.BASE_DIR, 'static\\s2048.txt'),
#         alipay_public_key_path=os.path.join(settings.BASE_DIR, 'static\\g2048.txt'),
#         sign_type='RSA2',
#         debug=True)
#     order_string = ali_pay.api_alipay_trade_page_pay(
#         out_trade_no="20161112123",
#         total_amount=0.01,
#         subject="计科162王狗蛋的狗头",
#         #return_url="http://",
#         #notify_url="https://openapi.alipay.com/gateway.do"  # this is optional
#     )
#
#     print(order_string)
#     return settings.ALIPAY_URL + order_string
#
#
#
#
# def get_alipay_query(order_id):
#      """查询订单状态"""
#      alipay = create_alipay()
#      result = alipay.api_alipay_trade_query(out_trade_no=order_id)
#      print(result)
#      if result.get("trade_status", "") == "TRADE_SUCCESS":
#           return True
#      else:
#        return False
#
#
# def zhifu(request):
#     u=get_alipay_page()
#     return redirect(u)


def gettip(request):
    key=request.POST.get("key",None)
    response = {'state': True}
    st=""
    if  key :
        result = models.Article.objects.raw("select distinct * from article where title like '%%"+key+"%%'")
        for rr in result:
            st=st+rr.title+"//"
    else :
       pass
    response['result']=st
    print(key)
    return HttpResponse(json.dumps(response))

def modify(request):

    mesg=""
    if request.method=="POST":
        name = request.COOKIES.get('username')
        if not name:
            return redirect('/login/')
        try:
              user = models.ArticleUserinfor.objects.filter(username=name).first()
              nickname= request.POST.get("nickname")
              if nickname!="":
                  #print("提交了昵称")
                  models.ArticleUserinfor.objects.filter(id=user.id).update( nickname=nickname)
                  mesg =mesg+ "昵称修改成功 "
              else:
                  pass
              gender = request.POST.get("gender")
              if gender!="":
                  # print("提交了昵称")
                  models.ArticleUserinfor.objects.filter(id=user.id).update(gender=gender)
                  mesg = mesg+"性别修改成功 "
              else:
                  pass
              desc = request.POST.get("desc")
              if desc!="":
                  # print("提交了昵称")
                  models.ArticleUserinfor.objects.filter(id=user.id).update(desc=desc)
                  mesg = mesg + "简介修改成功 "
              else:
                  pass
              f = request.FILES.get("head")
              if  f:

                 filename = f.name
                 last = filename.split('.')[1]
                 filepath = os.path.join("article/static/headimg", str(user.id)+ "."+last)
                 loadfile = open(filepath, mode="wb")
                 for fi in f.chunks():
                    loadfile.write(fi)
                 loadfile.close()
                 mesg = mesg+"头像修改成功"
                 models.ArticleUserinfor.objects.filter(id=user.id).update(imgurl="/static/headimg/"+str(user.id)+ "."+last)
        except:
              mesg = "修改失败"
        addscore(request, 15)
        return  render(request,"modify.html",{"isupload":mesg})
    return render(request,"modify.html",{"isupload":mesg})


def exit_login(request):
    name = request.COOKIES.get('username')
    if not name:
        return redirect('/login/')
    else:
        res1 = redirect('/login')
        res1.set_cookie('username', "")
        return res1
def sendmessage(request):
       return render(request, "sendtomanager.html")

def insert_message(request):
    name = request.COOKIES.get('username')
    response = {'state': True}
    try:
        content = request.POST.get('content', None)
        if name:
            user = models.ArticleUserinfor.objects.filter(username=name).first()
            print("user.id",user.id)
            models.Message.objects.create(content=content,userid=user.id)
            print("插入成功")
        else:
            models.Message.objects.create(content=content)
        #print(title)
    except:
        response['state'] = False
    return HttpResponse(json.dumps(response))
def managerlogin(request):
    msg = {}
    error = ""
    msg['username'] = ""
    msg['password'] = ""
    if(request.method == 'GET'):
        return render(request,"managerlogin.html",{'error': error, 'msg': msg})
    if (request.method == 'POST'):
        username = request.POST.get('username', None)
        password = request.POST.get('password', None)
        if username == "" or password == "":
            error = "账号密码不能为空"
            return render(request, "managerlogin.html", {'error': error, 'msg': msg})
        else:
            user = models.Manager.objects.filter(username=username).first()
            if not user:
                error = "该用户不存在"
                return render(request, "managerlogin.html", {'error': error, 'msg': msg})

            if user.password == password:
                res = redirect('/manageruserinfor/')
                res.set_cookie('manageusername', username)
                return res
            error = "密码错误"
            return render(request, "managerlogin.html", {'error': error, 'msg': msg})

def manageruserinfor(request):
     name = request.COOKIES.get('manageusername')
     if not name:
        return redirect('/managerlogin/')
     message= models.Message.objects.all()
     mymessage=[]
     for cc in message:
         comment_tamp = {}
         if cc.userid:
             user = models.ArticleUserinfor.objects.filter(id=cc.userid).first()

             comment_tamp["username"] = user.username
             comment_tamp["user_id"] = user.id
             comment_tamp["content"] = cc.content
             comment_tamp["nickname"] = user.nickname
             comment_tamp["message_id"] = cc.id
             mymessage.append(comment_tamp)

         else:
             print("userid为空")
             comment_tamp["content"] = cc.content
             comment_tamp["nickname"] = "匿名用户"
             comment_tamp["message_id"] = cc.id
             mymessage.append(comment_tamp)
     return   render(request,"managerinfor.html",{"mymessage":mymessage})
def message(request):
    id=request.GET.get("id",None)
    mes = models.Message.objects.filter(id=id).first()
    return  render(request,"showmessage.html",{"content":mes.content})

def sendto(request):
    if  request.method=="GET":
         to_userid=request.GET.get("id",None)
         from_name=request.COOKIES.get('username')
         if  from_name :
                user = models.ArticleUserinfor.objects.filter(username=from_name).first()
                user2 = models.ArticleUserinfor.objects.filter(id=to_userid).first()
                from_id=user.id
                return  render(request,"sendto.html",{"from_id":from_id,"to_id":to_userid,"tonickname":user2.nickname})
         else:
                return  redirect("/login")
    from_name = request.COOKIES.get('username')
    if request.method=="POST":
      response = {'state': True}
      if from_name:
        #response = {'state': True}
        response['islogin']=True
        try:
            user = models.ArticleUserinfor.objects.filter(username=from_name).first()
            content = request.POST.get("content", None)
            from_id = user.id
            to_id = request.POST.get("to_id", None)
            nowTime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')  # 现在
            models.Usermessage.objects.create(content=content,from_id=from_id,to_id=to_id,time=nowTime)

            # print(title)
        except:
            response['state'] = False
        return HttpResponse(json.dumps(response))
      else :
          response['islogin'] = False
          return HttpResponse(json.dumps(response))


def mymessage(request):
    name = request.COOKIES.get('username')
    if not name:
        return redirect('/login/')
    user=models.ArticleUserinfor.objects.filter(username=name).first()
    message = models.Usermessage.objects.filter(Q(to_id=user.id )|Q(from_id=user.id)).order_by('-time')
    mymessage = []
    for cc in message:
        comment_tamp = {}

        user3 = models.ArticleUserinfor.objects.filter(id=cc.from_id).first()
        user4= models.ArticleUserinfor.objects.filter(id=cc.to_id).first()
        #comment_tamp["myusername"] = user.username
        comment_tamp["myuser_id"] = user.id
        comment_tamp["content"] = cc.content
        comment_tamp["mynickname"] = user.nickname
        comment_tamp["message_id"] = cc.id
        comment_tamp["from_nickname"] = user3.nickname
        comment_tamp["from_id"] = user3.id
        comment_tamp["to_id"]=cc.to_id
        comment_tamp["to_nickname"] = user4.nickname
        comment_tamp["time"] = cc.time
        comment_tamp["from_img"] = user3.imgurl
        mymessage.append(comment_tamp)
    return render(request, "mymessage.html", {"mymessage": mymessage,"mynickname":user.nickname,"myimg":user.imgurl,"user":user})

def usermessage(request):
    id=request.GET.get("id",None)
    message = models.Usermessage.objects.filter(id=id).first()
    return  render(request,"showusermessage.html",{"content":message.content})

def testedit(request):
    return render(request,"edittest.html")
def  upload_img(request):
    files = request.FILES.get("imgFile", None)
    print(files.name)
    filename=files.name
    t = time.time()
    last=filename.split('.')[1]
    picname=str(int(round(t * 1000)))+"."+last
    filepath="article/static/image/" + picname
    loadfile = open(filepath, mode="wb")
    for fi in files.chunks():
        loadfile.write(fi)
    loadfile.close()
    result = {"error": 0, "url": "/static/image/"+picname}
    return  HttpResponse(json.dumps(result), content_type="application/json")


def follow(request):
    follower_id=request.POST.get("follower_id",None)
    followee_id = request.POST.get("followee_id",None)
    follow_tip=request.POST.get("follow_tip",None)

    if  follow_tip=="ok":
         models.Follow.objects.create(follower=follower_id,followee=followee_id)
         return HttpResponse("focused")
    if   follow_tip=="cancel":
        models.Follow.objects.filter(follower=follower_id,followee=followee_id).first().delete()
        return HttpResponse("canceled")
