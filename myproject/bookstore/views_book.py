# coding:utf-8
import json
import time

from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.db import transaction
from django.core.paginator import Paginator
from bookstore.models import Book
from bookstore.models import Author
from bookstore.models import Publisher



# Create your views here.
@csrf_exempt
def query(request):
    global books

    result = {
        'books': [],
        'pagination': {
            'total': None,
            'pageNo': None,
            'pageSize': None
        }
    }
    # get查询，默认查询所有
    if request.method == 'GET':
        print(request)

        defaultPageNo = 1
        defaultPageSize = 5

        booksInDbPager = Paginator(Book.objects.all(), defaultPageSize)

        result['books'] = bookInfos2Json(booksInDbPager.page(defaultPageNo).object_list)
        result['pagination']['total'] = booksInDbPager.count
        result['pagination']['pageNo'] = defaultPageNo
        result['pagination']['pageSize'] = defaultPageSize
        print('result: %s' % result)
        response = HttpResponse(json.dumps(result), content_type="application/json")

    #post查询，根据查询条件过滤
    elif request.method == 'POST':
        # request infos
        # print(request)

        # 请求方式是接送的，不能直接从request.POST里面拿，里面是空的；在request.body里面
        # print(request.POST)

        postBody = request.body
        # print(postBody)
        # print(type(postBody))
        postJson = json.loads(postBody)
        # print(type(postJson))
        # print(postJson)

        for key in postJson:
            print('req json key:%s, value:%s'%(key, postJson[key]))

        #查询请求里面的查询条件和分页控制信息
        bookName = ''
        if 'param' in postJson and 'bookName' in postJson['param']:
            bookName = postJson['param']['bookName']
        publishYear = ''
        if 'param' in postJson and 'publishYear' in postJson['param']:
            publishYear = postJson['param']['publishYear']
        authorName = ''
        if 'param' in postJson and 'authorName' in postJson['param']:
            authorName = postJson['param']['authorName']
        currentPage = 1
        pageSize = 5
        if 'pagination' in postJson:
            currentPage = postJson['pagination']['pageNo']
            pageSize = postJson['pagination']['pageSize']
        print('pagination:%s, %s' % (currentPage, pageSize))


        print('###############################匹配数据库################################')
        # 数据库动态查询条件
        dbQueryArgs = {}
        if bookName:
            dbQueryArgs['name__contains'] = bookName
        if publishYear:
            dbQueryArgs['publishDay__year'] = publishYear
        if authorName:
            dbQueryArgs['author__name'] = authorName
        print('查询条件%s' % dbQueryArgs)

        booksInDbPager = Paginator(Book.objects.filter(**dbQueryArgs).order_by('id'), pageSize)
        # 翻页前增加了查询条件，则翻页时的查询结果可能变少了，翻页页码可能超过了总页数
        if booksInDbPager.num_pages < currentPage:
            currentPage = booksInDbPager.num_pages
        result['books'] = bookInfos2Json(booksInDbPager.page(currentPage).object_list)
        result['pagination']['total'] = booksInDbPager.count
        result['pagination']['pageNo'] = currentPage
        result['pagination']['pageSize'] = pageSize
        print('result: %s' % result)


        #################### 返回查询结果，内存全局books里面的，或者数据库里面的 #####################
        # response = HttpResponse(json.dumps(bookMatchResByAuthorName), content_type="application/json")
        response = HttpResponse(json.dumps(result), content_type="application/json")

    else:
        response = HttpResponse('only accept GET/POST request, but got %s' % request.method)

    response["Access-Control-Allow-Origin"] = "*"
    response["Access-Control-Allow-Methods"] = "POST, GET, OPTIONS"
    response["Access-Control-Allow-Headers"] = "*"
    return response



@transaction.atomic
@csrf_exempt
def addBook(request):
    print('add book: %s' % request)

    # global books
    if request.method == 'POST':
        print('book info:%s' % request.POST)

        book = generateBook(request)
        #插入数据库
        newAuthor = Author(name = book['author']['name'],
                           nickName = book['author']['nickName'],
                           mobile = book['author']['mobile'],
                           gender = book['author']['gender'],
                           birthday = book['author']['birthday'],
                           address = book['author']['address'],
                           phone = book['author']['phone'],
                           email = book['author']['email'])
        newAuthor.save()

        newPublisher = Publisher(name = book['publish']['name'],
                                 address = book['publish']['address'],
                                 phone = book['publish']['phone'],
                                 email = book['publish']['email'])
        newPublisher.save()

        newBook = Book(type = book['type'],
                        name = book['name'],
                        location = book['location'],
                        price = book['price'],
                        thumbnail = book['thumbnail'],
                        publishDay = book['publishDay'],
                        author = newAuthor,
                        publisher = newPublisher)
        newBook.save()

        # books.append(book)
        # print(books)

        response = HttpResponse('OK', content_type="application/json")

    else:
        response = HttpResponse('only accept POST request, but got %s' % request.method)

    response["Access-Control-Allow-Origin"] = "*"
    response["Access-Control-Allow-Methods"] = "POST, GET, OPTIONS"
    response["Access-Control-Allow-Headers"] = "*"
    return response


@csrf_exempt
def queryOneBook(request, bookId):
    #print(request)

    if request.method == 'GET':
        # global books
        if bookId:
            bookById = Book.objects.get(id__exact = int(bookId))
            if bookById:
                response = HttpResponse(json.dumps(bookInfo2Json(bookById)), content_type="application/json")
            else:
                response = HttpResponse(json.dumps({}), content_type="application/json")
        else:
            response = HttpResponse('book id cannot be empty.')

    else:
        response = HttpResponse('only accept GET request, but got %s' % request.method)

    response["Access-Control-Allow-Origin"] = "*"
    response["Access-Control-Allow-Methods"] = "POST, GET, OPTIONS"
    response["Access-Control-Allow-Headers"] = "*"
    return response


@transaction.atomic
@csrf_exempt
def delBook(request, bookId):
    print('delete book id: %s' % bookId)

    if request.method == 'GET':
        if bookId:
            bookInDb = Book.objects.get(id__exact = int(bookId))
            if bookInDb:
                bookInDb.author.delete()
                bookInDb.publisher.delete()
                bookInDb.delete()
            response = HttpResponse('OK', content_type="application/json")

        else:
            response = HttpResponse('book id cannot be empty.')

    else:
        response = HttpResponse('only accept GET request, but got %s' % request.method)

    response["Access-Control-Allow-Origin"] = "*"
    response["Access-Control-Allow-Methods"] = "POST, GET, OPTIONS"
    response["Access-Control-Allow-Headers"] = "*"
    return response


@transaction.atomic
@csrf_exempt
def edit(request):

    if request.method == 'POST':
        print('request info in POST:%s' % request.POST)
        # print('request info in payload:%s' % request.body)

        if request.POST:
            id = request.POST.get('id')
            if not id:
                response = HttpResponse('ERROR', content_type="application/json")
                response["Access-Control-Allow-Origin"] = "*"
                response["Access-Control-Allow-Methods"] = "POST, GET, OPTIONS"
                response["Access-Control-Allow-Headers"] = "*"

                return response

            print("book to update, id:%s" % id)

            # update book info
            bookToUpdate = generateBook(request)
            #查询数据库记录
            bookInDb = Book.objects.get(id__exact = id)
            print('book in db: %s' % bookInDb)

            #更新书籍信息
            bookInDb.type = bookToUpdate['type']
            bookInDb.name = bookToUpdate['name']
            bookInDb.location = bookToUpdate['location']
            bookInDb.price = bookToUpdate['price']
            bookInDb.thumbnail = bookToUpdate['thumbnail']
            bookInDb.publishDay = bookToUpdate['publishDay']
            bookInDb.save()

            #更新作者信息
            bookAuthor = Author.objects.get(id__exact = bookInDb.author.id)
            bookAuthor.name = bookToUpdate['author']['name']
            bookAuthor.nickName = bookToUpdate['author']['nickName']
            bookAuthor.mobile = bookToUpdate['author']['mobile']
            bookAuthor.gender = bookToUpdate['author']['gender']
            bookAuthor.birthday = bookToUpdate['author']['birthday']
            bookAuthor.address = bookToUpdate['author']['address']
            bookAuthor.phone = bookToUpdate['author']['phone']
            bookAuthor.email = bookToUpdate['author']['email']
            bookAuthor.save()

            #更新出版社信息
            bookPublisher = Publisher.objects.get(id__exact = bookInDb.publisher.id)
            bookPublisher.name = bookToUpdate['publish']['name']
            bookPublisher.address = bookToUpdate['publish']['address']
            bookPublisher.phone = bookToUpdate['publish']['phone']
            bookPublisher.email = bookToUpdate['publish']['email']
            bookPublisher.save()

        response = HttpResponse('SUCCESS', content_type="application/json")
        response["Access-Control-Allow-Origin"] = "*"
        response["Access-Control-Allow-Methods"] = "POST, GET, OPTIONS"
        response["Access-Control-Allow-Headers"] = "*"

    else:
        # print('edit book . %s' % request)
        response = HttpResponse('<h1>only accept POST request, but got GET.</h1>')
        response["Access-Control-Allow-Origin"] = "*"
        response["Access-Control-Allow-Methods"] = "POST, GET, OPTIONS"
        response["Access-Control-Allow-Headers"] = "*"

    return response


def generateBook(request):
    ############ book info
    bookType = request.POST.get('type')
    # print("request data, type:%s" % type)
    name = request.POST.get('name')
    # print("request data, name:%s" % name)
    location = request.POST.get('location')
    # print("request data, location:%s" % location)
    price = request.POST.get('price')
    # print("request data, price:%s" % price)
    thumbnail = request.POST.get('thumbnail')
    # print("request data, preview:%s" % thumbnail)
    publishDay = request.POST.get('publishDay')
    # print("request data, publish[publishDay]:%s" % publishDay)

    ################ author info
    authorName = request.POST.get('author[name]')
    # print("request data, author[name]:%s" % authorName)
    authorBirthday = request.POST.get('author[birthday]')
    # print("request data, author[authorBirthday]:%s" % authorBirthday)
    authorNickName = request.POST.get('author[nickName]')
    authorGender = request.POST.get('author[gender]')
    authorAddress = request.POST.get('author[address]')
    authorEmail = request.POST.get('author[email]')
    authorMobile = request.POST.get('author[mobile]')
    authorPhone = request.POST.get('author[phone]')

    ################# publisher info
    publisherName = request.POST.get('publish[name]')
    # print("request data, publish[publisher]:%s" % publisher)
    publisherAddress = request.POST.get('publish[address]')
    publisherPhone = request.POST.get('publish[phone]')
    publisherEmail = request.POST.get('publish[email]')

    book = {
        'id': int(time.time()),
        'type': bookType,
        'name': name,
        'location': location,
        'price': price,
        'thumbnail': thumbnail,
        'publishDay': publishDay,
        'author': {
            'name': authorName,
            'nickName': authorNickName,
            'birthday': authorBirthday,
            'gender': authorGender,
            'address': authorAddress,
            'email': authorEmail,
            'mobile': authorMobile,
            'phone': authorPhone,
        },
        'publish': {
            'name': publisherName,
            'address': publisherAddress,
            'phone': publisherPhone,
            'email': publisherEmail,
        }
    }
    return book


def bookInfos2Json(booksInDb):
    result = []

    if booksInDb:
        for i in booksInDb:
            result.append(bookInfo2Json(i))

    return result

def bookInfo2Json(bookInDb):
    return {
        'id': bookInDb.id,
        'type': bookInDb.type,
        'name': bookInDb.name,
        'location': bookInDb.location,
        'price': bookInDb.price,
        'thumbnail': bookInDb.thumbnail,
        'publishDay': bookInDb.publishDay.strftime('%Y-%m-%d'),
        'author': {
            'name': bookInDb.author.name,
            'nickName': bookInDb.author.nickName,
            'birthday': bookInDb.author.birthday.strftime('%Y-%m-%d'),
            'gender': bookInDb.author.gender,
            'address': bookInDb.author.address,
            'email': bookInDb.author.email,
            'mobile': bookInDb.author.mobile,
            'phone': bookInDb.author.phone,
        },
        'publish': {
            'name': bookInDb.publisher.name,
            'address': bookInDb.publisher.address,
            'phone': bookInDb.publisher.phone,
            'email': bookInDb.publisher.email,
        }
    }
