from django.http import JsonResponse
import json
# 导入 Customer 
from common.models import Customer

# Create your views here.

def dispatcher(request):
    # 将请求参数同一放入request的params属性中 ，方便后续处理 

    # GET请求参数在url中，通过request对象的GET属性获取
    if request.method == 'GET':
        request.params = request.GET

    # POST/PUT/DELETE 请求参数从request对象的body属性中获取
    elif request.method in ['POST','PUT','DELETE']:
        #根据接口，POST/PUT/DELETE请求的消息都是json格式
        request.params  =  json.loads(request.body)

    # 根据不同的 action分派给不同的函数进行处理
    action = request.params['action']
    if action ==  'list_customer':
        return listcustomers(request)
    elif action == 'add_customer':
        return addcustomer(request)
    elif action == 'modify_customer':
        return modifycustomer(request)
    elif  action  == 'del_customer':
        return deletecustomer(request)

    else:
        return JsonResponse({'ret':1,'msg':'不支持该类型http请求'})
# 列出客户
def listcustomers(request):
    # 返回一个 QuerySet 对象 ，包含所有的表记录
    qs = Customer.objects.values()

    # 将 QuerySet 对象 转化为 list 类型
    # 否则不能 被 转化为 JSON 字符串
    retlist = list(qs)

    return JsonResponse({'ret': 0, 'retlist': retlist})

# 添加客户
def addcustomer(request):
    info = request.params['data']
    # 从请求消息中获取添加客户的信息
    # 并且插入到数据库中
    # 返回值就是对应插入记录的对象
    record = Customer.objects.create(name = info['name'],
                            phonenumber = info['phonenumber'],
                            address = info['address'])
    return JsonResponse({'ret':0,'id':record.id})

# 修改客户信息
def modifycustomer(request):
    # 从请求消息中获取修改用户的信息
    # 找到该客户 ，并且进行修改操作
    customerid =  request.params['id']
    newdata =  request.params['newdata']

    try:
        # 根据id从数据库中找到相应的客户记录
        customer =Customer.objects.get(id = customerid)
    except Customer.DoesNotExist:
        return {
            'ret':1,
            'msg':f'id为`{customerid}`的客户不存在'
        }
    if 'name' in newdata:
        customer.name = newdata['name']
    if 'phonenumber' in newdata:
        customer.phonenumber = newdata['phonenumber']
    if 'address' in newdata:
        customer.address = newdata['address']
    # 注意，一定要执行save才能将修改信息保存到数据库
    customer.save()
    return JsonResponse({'ret': 0})
# 删除客户
def deletecustomer(request):
    customerid = request.params['id']

    try:
        # 根据id从数据库中找到相应的客户记录
        customer = Customer.objects.get(id = customerid)
    except Customer.DoesNotExist:
        return {
                'ret':1,
                'msg':f'id为`{customerid}`的客户不存在'
        }
    # delete方法删除记录后会自动保存
    customer.delete()
    return JsonResponse({'ret':0})
    