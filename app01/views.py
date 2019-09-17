from django.shortcuts import render, HttpResponse, redirect

# Create your views here.

from app01.models import Book, Publish, Author, AuthorDetail, Emp


def addrecord(request):
    '''
    添加记录

    '''

    # 一对多的添加方式：
    # pub_obj=Publish.objects.filter(name="橙子出版社").first()

    # book=Book.objects.create(
    #     title="python",
    #     price=120,
    #     pub_date="2012-12-12",
    #     publish_id=1,
    #     #publish=pub_obj
    #
    # )

    # 多对多的添加方式:

    # 方式1
    # alex=Author.objects.filter(name="alex").first()
    # egon=Author.objects.filter(name="egon").first()
    # book.authors.add(alex,egon)
    # 方式2：
    # book.authors.add(1,2)
    # 方式3：
    # book.authors.add(*[1,2])

    #######

    # egon=Author.objects.filter(name="egon").first()
    # book=Book.objects.filter(nid=4).first()
    # #book.authors.remove(1)
    # book.authors.clear()

    ###### 解除再绑定
    book = Book.objects.filter(nid=3).first()
    book.authors.clear()
    book.authors.add(1)

    book.authors.set(1)

    '''
        app01_book_authors
              id     book_id   author_id
               1        3          1
               2        3          2
    
    '''

    return HttpResponse("添加成功")


def query(request):
    ######################### 基于对象的跨表查询 #############################
    ####### 一对多 ##########
    '''
    正向查询：关联属性所在的表查询关联表记录
    反向查询

        ----正向查询按字段：book.publish
    Book------------------------------------>Publish
         <-----------------------------------
          反向查询表名小写_set.all()：pub_obj.book_set.all()

    '''

    # 1 查询python这本书出版社的名字和邮箱
    # book=Book.objects.filter(title="python").first()
    # pub_obj=Publish.objects.filter(nid=book.publish_id).first()
    # print(pub_obj.name)
    # print(pub_obj.email)
    ########################
    # book = Book.objects.filter(title="python").first()
    # print(book.publish) #  与book这本书关联出版社对象
    # print(book.publish.name) #  与book这本书关联出版社对象
    # print(book.publish.email) #  与book这本书关联出版社对象

    # 2 查询苹果出版社出版的所有的书籍的名称
    # pub_obj=Publish.objects.get(name="苹果出版社")
    # print(pub_obj.book_set.all())  # queryset
    # print(pub_obj.book_set.all().values("title"))  # queryset

    ####### 多对多 ##########
    '''
                正向查询按字段 book.authors.all()
       Book  -------------------------------------->Author
             <--------------------------------------
                反向查询按表名小写_set.all()： alex.book_set.all()
    '''

    # 查询python这本书籍的作者的年龄
    book = Book.objects.filter(title="python").first()
    ret = book.authors.all().values("age")  # 与这本书关联的左右作者的queryset的集合
    print(ret)
    # #查询alex出版过的所有的书籍名称
    # alex=Author.objects.filter(name="alex").first()
    # print(alex.book_set.all())
    ####### 一对一 ##########
    '''
                     正常查询安字段：alex.ad
        Author -----------------------------------------> AuthorDetail
               <------------------------------------------
                     反向查询按表名小写  ad.author
    '''
    # 查询alex的手机号
    # alex = Author.objects.filter(name="alex").first()
    # print(alex.ad.tel)
    # # 查询手机号为110的作者的名字
    # ad=AuthorDetail.objects.filter(tel=110).first()
    # print(ad.author.name)

    return HttpResponse("查询成功")


def query2(request):
    ################基于双下划线的跨表查询（基于join实现的）################

    # KEY：正向查询按字段，反向查询按表明小写

    # 1 查询python这本书出版社的名字

    # ret=Book.objects.filter(title="python").values("price")
    # ret=Book.objects.filter(title="python").values("publish__name")
    # print(ret)
    # ret=Publish.objects.filter(book__title="python").values("name")
    # print(ret)

    # 2 查询苹果出版社出版的所有的书籍的名称
    # ret=Publish.objects.filter(name="苹果出版社").values("book__title")
    # ret=Book.objects.filter(publish__name="苹果出版社")

    # 3 查询python这本书籍的作者的年龄

    # ret=Book.objects.filter(title="python").values("authors__age")
    # print(ret)
    # ret=Author.objects.filter(book__title="python").values("age")
    #
    # # 4 查询alex出版过的所有的书籍名称
    # ret1=Book.objects.filter(authors__name="alex").values("title")
    # ret2=Author.objects.filter(name="alex").values("book__title")
    # print(ret1,ret2)

    # 5 查询alex的手机号

    # ret=Author.objects.filter(name="alex").values("ad__tel")
    # ret=AuthorDetail.objects.filter(author__name="alex").values("tel")

    # 6 查询手机号为110的作者的名字

    # ret=AuthorDetail.objects.filter(tel=110).values("author__name")
    # ret=Author.objects.filter(ad__tel=110).values("name")

    ########### 连续跨表  ###############

    # 查询苹果出版社出版过的所有书籍的名字以及作者的姓名

    # ret=Publish.objects.filter(name="苹果出版社").values("book__title","book__authors__name")
    # ret=Book.objects.filter(publish__name="苹果出版社").values("title","authors__name")
    # ret=Book.objects.filter(publish__name="苹果出版社").values("title","authors__name")
    # print(ret)

    # 手机号以110开头的作者出版过的所有书籍名称以及出版社名称
    # 方式1:
    # ret=Author.objects.filter(ad__tel__startswith=110).values_list("book__title","book__publish__name")
    # print(ret)

    # 方式2：
    # ret=AuthorDetail.objects.filter(tel__startswith=110).values("author__book__title","author__book__publish__name")
    #
    # # 方式3：
    # ret=Book.objects.filter(authors__ad__tel__startswith=110).values("title","publish__name")

    ################ 聚合 分组 ################

    '''
    emp
       id  name    dep      pro  salary
        1  alex   教学部   山东    1000
        2  mjj    教学部   山东    3000
        3  林海峰 保安部    山东   5000
        4  peiqi  人事部   河北   10000

        select Count(id) from emp;
        select AVG(salary) from emp;

        select dep,AVG(salary) from emp group by dep
        select pro,Count(1) from emp group by pro


    '''
    # 聚合
    # 查询所有书籍的平均价格
    from django.db.models import Avg, Max, Sum, Min, Count
    # ret=Book.objects.all().aggregate(priceAvg=Avg("price"))
    # print(ret) # {'priceAvg': 142.0}
    # # 查询所有书籍的个数
    # ret=Book.objects.all().aggregate(c=Count(1))
    # print(ret) # {'c': 4}

    # 分组

    # 单表分组查询

    # 查询书籍表每一个出版社id以及对应的书籍个数
    # key： annotate()前values哪一个字段就按哪一个字段group by
    # ret=Book.objects.values("publish_id").annotate(c=Count(1))
    # print(ret)
    #
    # # 查询每一个部门的名称以及对应员工的平均薪水
    # ret=Emp.objects.values("dep").annotate(avg_salary=Avg("salary"))
    # print(ret) # [{'dep': '教学部', 'avg_salary': 2500.0}, {'dep': '保洁部', 'avg_salary': 3500.0}, {'dep': '保安部', 'avg_salary': 4000.0}]>
    #
    # # 查询每一个省份的名称以及对应的员工最大年龄
    #
    # ret=Emp.objects.values("pro").annotate(max_age=Max("age"))
    # print(ret) # <QuerySet [{'pro': '山东省', 'max_age': 123}, {'pro': '河南省', 'max_age': 23}, {'pro': '河北省', 'max_age': 56}]>

    # 单表按主键分组没有意义
    Emp.objects.values("id").annotate()

    # 跨表分组查询
    """
    `select app01_publish.name,COUNT(1) from app01_book INNER JOIN app01_publish ON app01_book.publish_id=app01_publish.nid
        GROUP BY app01_publish.nid
    """

    # 查询每一个出版社的名称以及对应的书籍平均价格
    # ret=Publish.objects.values("name","email").annotate(avg_price=Avg("book__price"))
    # print(ret) # <QuerySet [{'name': '苹果出版社', 'avg_price': 117.0}, {'name': '橙子出版社', 'avg_price': 112.0}, {'name': '西瓜出版社', 'avg_price': 222.0}]>

    # 查询每一个作者的名字以及出版的书籍的最高价格

    # ret=Author.objects.values("pk","name").annotate(max_price=Max("book__price"))
    # print(ret)

    # 查询每一个书籍的名称以及对应的作者的个数
    ret = Book.objects.values("title").annotate(c=Count("authors"))
    print(ret)  # <QuerySet [{'title': 'python', 'authors__count': 2}, {'title': 'linux', 'authors__count': 1}, {'title': 'go', 'authors__count': 1}, {'title': 'java', 'authors__count': 0}]>

    return HttpResponse("查询成功")


##################### 图书管理系统 视图函数 ##################


def book_view(request):
    book_list = Book.objects.all()
    return render(request, "book_view.html", {"book_list": book_list})


def book_add(request):
    if request.method == "GET":
        publish_list = Publish.objects.all()
        author_list = Author.objects.all()
        return render(request, "book_add.html", {"publish_list": publish_list, "author_list": author_list})
    else:
        title = request.POST.get("title")
        price = request.POST.get("price")
        pub_date = request.POST.get("pub_date")
        publish_id = request.POST.get("publish_id")
        authors = request.POST.getlist("authors")
        print(request.POST)
        print(authors)

        book = Book.objects.create(title=title, price=price, pub_date=pub_date, publish_id=publish_id)
        book.authors.add(*authors)

        return redirect("/books/")


def book_edit(request, edit_book_id):
    edit_book = Book.objects.filter(pk=edit_book_id).first()
    if request.method == "GET":
        publish_list = Publish.objects.all()
        author_list = Author.objects.all()
        return render(request, "book_edit.html",
                      {"edit_book": edit_book, "publish_list": publish_list, "author_list": author_list})

    else:
        title = request.POST.get("title")
        price = request.POST.get("price")
        pub_date = request.POST.get("pub_date")
        publish_id = request.POST.get("publish_id")
        authors = request.POST.getlist("authors")
        print(request.POST)
        print(authors)
        Book.objects.filter(pk=edit_book_id).update(title=title, price=price, pub_date=pub_date, publish_id=publish_id)
        edit_book.authors.set(authors)

        return redirect("/books/")


def book_del(request, del_book_id):
    Book.objects.filter(pk=del_book_id).delete()

    return redirect("/books/")

def query3(request):
    """
    :param request:
    :return:
    """
    ################基于双下划线的跨表查询（基于join实现的）################

    # KEY：正向查询按字段，反向查询按表明小写

    # 1 查询天龙八部这本书出版社的名字
    # 正向
    # ret = Book.objects.filter(title="天龙八部").values("publish__name")
    # print(ret)# <QuerySet [{'publish__name': '人民出版社'}]>
    # 反向
    # ret = Publish.objects.filter(book__title="天龙八部").values("name")
    # print(ret)# <QuerySet [{'name': '人民出版社'}]>

    # 2 查询人民出版社出版的所有的书籍的名称
    # ret = Publish.objects.filter(name="人民出版社").values("book__title")
    # print(ret)# <QuerySet [{'book__title': '天龙八部'}]
    # ret = Book.objects.filter(publish__name="人民出版社").values("title")
    # print(ret)# <QuerySet [{'title': '天龙八部'}]>

    # 3 查询python这本书籍的作者的年龄
    # 正向
    # ret = Book.objects.filter(title="斗罗大陆").values("authors__age")
    # print(ret)# <QuerySet [{'authors__age': 30}]>
    # 反向
    # ret = Author.objects.filter(book__title="斗罗大陆").values("age")
    # print(ret)# <QuerySet [{'age': 30}]>

    # # 4 查询alex出版过的所有的书籍名称
    # ret = Author.objects.filter(name="金庸").values("book__title")
    # print(ret)# <QuerySet [{'book__title': '天龙八部'}, {'book__title': '神雕侠侣'}]>
    # ret = Book.objects.filter(authors__name="金庸").values("title")
    # print(ret)# <QuerySet [{'book__title': '天龙八部'}, {'book__title': '神雕侠侣'}]>

    # 5 查询金庸的手机号
    # ret = Author.objects.filter(name="金庸").values("ad__tel")
    # print(ret)# <QuerySet [{'ad__tel': 1608030}]>
    # ret = AuthorDetail.objects.filter(author__name="金庸").values("tel")
    # print(ret)# <QuerySet [{'tel': 1608030}]>

    # 6 查询手机号为110的作者的名字
    # ret = AuthorDetail.objects.filter(tel=1376084).values("author__name")
    # print(ret)# <QuerySet [{'author__name': '天蚕土豆'}]>
    # ret = Author.objects.filter(ad__tel=1376084).values("name")
    # print(ret)# <QuerySet [{'name': '天蚕土豆'}]>

    ########### 连续跨表  ###############
    # 查询人民出版社出版过的所有书籍的名字以及作者的姓名
    # 方式一
    # ret = Publish.objects.filter(name="人民出版社").values("book__title","book__authors__name")
    # print(ret)# <QuerySet [{'book__title': '天龙八部', 'book__authors__name': '金庸'}]>
    # 方式二
    # ret = Book.objects.filter(publish__name="人民出版社").values("title","authors__name")
    # print(ret)# <QuerySet [{'title': '天龙八部', 'authors__name': '金庸'}]>
    #
    # # 方式三
    # ret = Author.objects.filter(book__publish__name="人民出版社").values("book__title","book__authors__name")
    # print(ret)# <QuerySet [{'book__title': '天龙八部', 'book__authors__name': '金庸'}]>

    # 手机号以110开头的作者出版过的所有书籍名称以及出版社名称
    # 方式一
    # ret = AuthorDetail.objects.filter(tel__startswith="13").values("author__book__publish__name","author__book__title")
    # print(ret)# <QuerySet [{'author__book__publish__name': '广东出版社', 'author__book__title': '斗破苍穹'}]>
    # # 方式二
    # ret = Book.objects.filter(authors__ad__tel__startswith="13").values("title","publish__name")
    # print(ret)# <QuerySet [{'title': '斗破苍穹', 'publish__name': '广东出版社'}]>
    # 方式三
    # 略

    ################ 聚合 分组 ################

    '''
    emp
       id  name    dep      pro  salary
        1  alex   教学部   山东    1000
        2  mjj    教学部   山东    3000
        3  林海峰 保安部    山东   5000
        4  peiqi  人事部   河北   10000

        select Count(id) from emp;
        select AVG(salary) from emp;

        select dep,AVG(salary) from emp group by dep
        select pro,Count(1) from emp group by pro
    '''

    # 聚合   aggregate()
    # 查询所有书籍的平均价格
    from django.db.models import Avg,Max,Sum,Min,Count
    '''
        # select AVG(app01_book.price) as priceAvg from app01_book;
    '''
    # ret=Book.objects.all().aggregate(priceAvg=Avg("price"))# aggregate聚合
    # print(ret) # {'priceAvg': 92.75}


    # # 查询所有书籍的个数
    # ret=Book.objects.all().aggregate(c=Count(1))
    # print(ret) # {'c': 4}

    ########
    # 分组  annotate()

    # 单表分组查询

    # 查询书籍表每一个出版社id以及对应的书籍个数
    # key： annotate()前values哪一个字段就按哪一个字段group by
    # sql:select publish_id,Count(1) from app01_book group by publish_id;
    # ret=Book.objects.values("publish_id").annotate(c=Count(1),p=Avg("price"))
    # print(ret)# <QuerySet [{'publish_id': 1, 'c': 1, 'p': 99.0}, {'publish_id': 2, 'c': 2, 'p': 94.0}, {'publish_id': 3, 'c': 1, 'p': 84.0}]>


    # # 查询每一个部门的名称以及对应员工的平均薪水
    # select dep,Avg(salary) as avg_salary from EMP group by dep
    # ret=Emp.objects.values("dep").annotate(avg_salary=Avg("salary"))
    # print(ret) # [{'dep': '教学部', 'avg_salary': 2500.0}, {'dep': '保洁部', 'avg_salary': 3500.0}, {'dep': '保安部', 'avg_salary': 4000.0}]>


    # # 查询每一个省份的名称以及对应的员工最大年龄
    #select pro,Max(age) as max_age from app01_emp group by pro
    # ret=Emp.objects.values("pro").annotate(max_age=Max("age"))
    # print(ret) # <QuerySet [{'pro': '山东省', 'max_age': 123}, {'pro': '河南省', 'max_age': 23}, {'pro': '河北省', 'max_age': 56}]>

    # 单表按主键分组没有意义
    # Emp.objects.values("id").annotate()

    # 跨表分组查询
    """
    `select app01_publish.name,COUNT(1) from app01_book INNER JOIN app01_publish ON app01_book.publish_id=app01_publish.nid
        GROUP BY app01_publish.nid
    """

    # 查询每一个出版社的名称以及对应的书籍平均价格
    #SELECT `app01_publish`.`name`, AVG(`app01_book`.`price`) AS `avg_price` FROM `app01_publish` LEFT OUTER JOIN `app01_book` ON (`app01_publish`.`nid` = `app01_book`.`publish_id`) GROUP BY `app01_publish`.`name` ORDER BY NULL  LIMIT 21;
    # 方式一
    # ret=Publish.objects.values("name").annotate(avg_price=Avg("book__price"))
    # print(ret) # <QuerySet [{'name': '人民出版社', 'avg_price': 99.0}, {'name': '广东出版社', 'avg_price': 94.0}, {'name': '北京出版社', 'avg_price': 84.0}]>
    # 方式二
    # ret=Publish.objects.all().annotate(avg_price=Avg("book__price")).values("name","avg_price")
    # print(ret)#<QuerySet [{'name': '人民出版社', 'avg_price': 99.0}, {'name': '广东出版社', 'avg_price': 94.0}, {'name': '北京出版社', 'avg_price': 84.0}]>

    # 方式三-->常用
    # ret = Publish.objects.annotate(avg_price=Avg("book__price")).values("name","avg_price")
    # print(ret)# <QuerySet [{'name': '人民出版社', 'avg_price': 99.0}, {'name': '广东出版社', 'avg_price': 94.0}, {'name': '北京出版社', 'avg_price': 84.0}]>
    # for i in ret:
    #     print(i)


    # 查询每一个作者的名字以及出版的书籍的最高价格
    #
    # ret=Author.objects.values("pk","name").annotate(max_price=Max("book__price"))
    # print(ret)


    # <QuerySet [{'pk': 1, 'name': '金庸', 'max_price': Decimal('99.00')}, {'pk': 3, 'name': '唐家三少', 'max_price': Decimal('84.00')}, {'pk': 2, 'name': '天蚕土豆', 'max_price': Decimal('100.00')}]>

    # 查询每一个书籍的名称以及对应的作者的个数
    # SELECT `app01_book`.`title`, COUNT(`app01_book_authors`.`author_id`) AS `c` FROM `app01_book` LEFT OUTER JOIN `app01_book_authors` ON (`app01_book`.`nid` = `app01_book_authors`.`book_id`) GROUP BY `app01_book`.`title` ORDER BY NULL  LIMIT 21; args=()
    ret = Book.objects.values("title").annotate(c=Count("authors"))
    print(ret)
    # <QuerySet [{'title': '天龙八部', 'c': 1}, {'title': '神雕侠侣', 'c': 1}, {'title': '斗罗大陆', 'c': 1}, {'title': '斗破苍穹', 'c': 1}]>

    # ret = Book.objects.values("title").annotate(c=Count("authors"))
    # print(ret)  # <QuerySet [{'title': 'python', 'authors__count': 2}, {'title': 'linux', 'authors__count': 1}, {'title': 'go', 'authors__count': 1}, {'title': 'java', 'authors__count': 0}]>



    return HttpResponse("查询成功！")