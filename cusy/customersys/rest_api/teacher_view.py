import os.path
import re
import time
from django.conf import settings
from uuid import uuid1
from django.db.models import Q
from django.http.response import HttpResponse
from django.middleware.csrf import get_token
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from .aliMessage import aliMessage
from .authentication import isLoginJWTAuthentication
from .message import message
from .base64Tobyte import base64ToImage
from .models import Customers, Class, Teacher, ZipfilesInfo
from .customersOperation import customersOp
from .pagination import teachersPagination
from .resources import teachersMTResources, teachersResources
from .serializer import (
    customerSerializer, classSerializer, teacherSerializer, zipFileSerializer)
from .thread import threadPool, futureInfo, singleEnum


class teacherApiViewSet(ModelViewSet):
    """
    教师用户视图集合，包含查询所有教师，查询单个教师，创建教师，删除教师，更改教师
    需要admin用户登录才能使用以上功能
    """
    serializer_class = teacherSerializer
    queryset = Teacher.objects.filter(is_valided=1).order_by("id")
    pagination_class = teachersPagination
    authentication_classes = [isLoginJWTAuthentication]

    def list(self, request, *args, **kwargs):
        if "ex_is_valided" in request.GET:
            ex_is_valided = request.GET.get("ex_is_valided")
            self.queryset = Teacher.objects.exclude(
                is_valided=ex_is_valided).order_by("id")
        return super().list(request)

    def create(self, request, *args, **kwargs):
        try:
            self.get_queryset().get(teacher_id=request.data.get('teacher_id'))
            return Response(message('failed', 403, message="teaher is existed"))
        except Exception as e:
            serializer = teacherSerializer(data=request.data)
            if not serializer.is_valid():
                return Response(
                    message('failed', 400, message="teahcer failed to create!", kwargs={"info": serializer.errors}))
            serializer.save()
            serializer = teacherSerializer(self.get_queryset().get(
                teacher_id=request.data.get('teacher_id')))
            return Response(
                message('success', 200, message="create a new teacher", kwargs={"info": serializer.data}))

    def retrieve(self, request, param, *args, **kwargs):
        try:
            if "ex_is_valided" in request.GET:
                ex_is_valided = request.GET.get("ex_is_valided")
                self.queryset = Teacher.objects.all().exclude(is_valided=ex_is_valided).filter(
                    Q(teacher_id__icontains=param) | Q(
                        teacher_name__icontains=param) | Q(teacher_phone__icontains=param))
            else:
                self.queryset = self.get_queryset().filter(Q(teacher_id__icontains=param) | Q(
                    teacher_name__icontains=param) | Q(teacher_phone__icontains=param))
        except Exception as e:
            return Response(message('failed', 404, e.args[0]), status=200)
        return super(teacherApiViewSet, self).list(request)

    def update(self, request, *args, **kwargs):
        if "teacher_id" not in request.GET:
            return Response(message(status="failed", code=404, message="教师工号是必须的!"))
        teacher_id = request.GET.get("teacher_id")
        request.data.update({"is_valided": 0})
        newData = request.data
        try:
            teacher = self.get_queryset().get(teacher_id=teacher_id)
        except Exception as e:
            return Response(message('failed', 404, e.args[0]), status=200)
        if teacher is not None:
            serializer = teacherSerializer(teacher, newData)
            if not serializer.is_valid():
                return Response(message(status='failed', code=403, message=serializer.errors), status=200)
            serializer.save()
            return Response(
                message("success", code=200, message="teacher update successfully ", kwargs={"info": serializer.data}))

    def destroy(self, request, *args, **kwargs):
        id = request.query_params.get('id')
        try:
            teacher = self.get_queryset().get(pk=id)
        except Exception as e:
            return Response(message(status='failed', code=404, message=e.args[0]), status=200)
        content = {"teacher_id": teacher.teacher_id,
                   "teacher_name": teacher.teacher_name}
        try:
            teacher.delete()
            return Response(
                message(message="teacher already delete", kwargs={"info": content}), status=200)
        except Exception as e:
            return Response(
                message(status='failed', code=403, message=e.args[0], kwargs={"info": content}), status=200)

    def updateAll(self, request):
        if "status" not in request.GET:
            return Response(message("failed", code=403, message="status字段是必须的!"))
        status = request.GET.get("status")
        dataList = request.data.get("idList")
        messageList = list()
        # try:
        if dataList:
            for data in dataList:
                teacher = Teacher.objects.get(pk=data)
                teacher.is_valided = status
                teacher.save()
                # 获取对应id的电话号码
                # teacher_phone = teacher.teacher_phone
                # 发送短信
                # aliMessage.main([teacher_phone], ["四川信管"])
                # newMessage = message(
                # status="success", code=200, message="OK")
                # messageList.append(newMessage)
            return Response(message(status="success", code=200, message="Ok", kwargs={"results": messageList}),
                            status=200)
        # except Exception as e:
            # return Response(message(status="failed", code=400, message="短信发送失败", kwargs={"info": e.args[0]}),
            # status = 200)


class teacherGeneralApi(ModelViewSet):
    """
    开放给提交用户的api接口不用验证token
    """
    queryset = Teacher.objects.all().order_by("id")
    serializer_class = teacherSerializer

    def retrieve(self, request, *args, **kwargs):
        if len(request.GET) == 0:
            get_token(request)
            return Response(message(status="success", code=200, message="OK"))
        else:
            teacher_id = request.GET.get('teacher_id')
            try:
                teacher = Teacher.objects.get(teacher_id=teacher_id)
            except Exception as e:
                return Response(message(status="failed", code=404, message="don't exist"))
            teacher = teacherSerializer(teacher).data
            print(teacher)
            return Response(message(status="success", code=200, message="exist", kwargs={"info": teacher}))

    def create(self, request, *args, **kwargs):
        try:
            self.get_queryset().get(teacher_id=request.data.get('teacher_id'))
            # return Response(message('failed', 403, message="customer is existed"))
            return self.update(request, *args, **kwargs)
        except Exception as e:
            # 为用户添加未验证字段
            request.data.update({"is_valided": 0})
            serializer = teacherSerializer(data=request.data)
            if not serializer.is_valid():
                return Response(
                    message('failed', 400, message="teacher failed to create!", kwargs={"info": serializer.errors}))
            serializer.save()
            serializer = teacherSerializer(self.get_queryset().get(
                teacher_id=request.data.get('teacher_id')))
            return Response(
                message('success', 200, message="create a new teacher", kwargs={"info": serializer.data}))

    def update(self, request, *args, **kwargs):
        try:
            teacher = self.get_queryset().get(teacher_id=request.data.get('teacher_id'))
        except Exception as e:
            return Response(message('failed', 404, e.args[0]), status=200)
        if teacher is not None:
            request.data.update({"is_valided": teacher.is_valided})
            serializer = customerSerializer(teacher, request.data)
            if not serializer.is_valid():
                return Response(message(status='failed', code=403, message=serializer.errors), status=200)
            serializer.save()
            return Response(
                message("success", code=200, message="teacher update successfully ", kwargs={"info": serializer.data}))


class classGeneralApi(APIView):
    """
    为普通用户开放的班级接口，不需要验证
    """

    def get(self, request):
        return Response(classSerializer(Class.objects.all(), many=True).data)


class exportTeacherResources(APIView):
    """
    导出模版数据1
    """
    authentication_classes = [isLoginJWTAuthentication]

    def get(self, request):
        if ("page" or "pageSize") not in request.GET:
            return Response(message("failed", 404, "请求参数不全，请检查"))
        try:
            page = int(request.GET.get("page"))
            pageSize = int(request.GET.get("pageSize"))
            querySet = Teacher.objects.filter(
                is_valided=1)[(page - 1) * pageSize:page * pageSize]
            teacherData = teachersResources().export(queryset=querySet)
            response = HttpResponse(teacherData.xlsx,
                                    content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
            response["Content-Disposition"] = "attachment;filename=\"teachers({}).xls\"".format(
                page)
            return response
        except Exception as e:
            return Response(message("failed", 403, "参数不合法", kwargs={"info": e.args[0]}))

    def post(self, request):
        data = teachersResources().export()
        response = HttpResponse(data.xlsx,
                                content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
        response["Content-Disposition"] = "attachment;filename=\"teachers.xlsx\""
        return response


class exportTeacherMTResources(APIView):
    """
    导出模版数据2
    """
    authentication_classes = [isLoginJWTAuthentication]

    def get(self, request):
        if ("page" or "pageSize") not in request.GET:
            return Response(message("failed", 404, "请求参数不全，请检查"))
        try:
            page = int(request.GET.get("page"))
            pageSize = int(request.GET.get("pageSize"))
            querySet = Customers.objects.filter(
                is_valided=1)[(page - 1) * pageSize:page * pageSize]
            teacherData = teachersMTResources().export(queryset=querySet)
            response = HttpResponse(teacherData.xlsx,
                                    content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
            response["Content-Disposition"] = "attachment;filename=\"teachers({}).xls\"".format(
                page)
            return response
        except Exception as e:
            return Response(message("failed", 403, "参数不合法", kwargs={"info": e.args[0]}))

    def post(self, request):
        customersMTData = teachersMTResources().export()
        response = HttpResponse(customersMTData.xlsx,
                                content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
        response["Content-Disposition"] = "attachment;filename=\"teachers.xlsx\""
        return response


class uploadTeacherAvatar(APIView):
    def post(self, request):
        if "avatarSize" in request.data and request.data.get("avatarSize") != 0:
            base64ToImage(request.data.get("avatar"),
                          request.data.get("avatarName"), 'png').toImage()
            return Response(message("success", 200, message="OK"))
        return Response(message("failed", 404, message="上传头像失败"))


class exportTeacherAvatarRes(APIView):
    # authentication_classes = [isLoginJWTAuthentication]
    teachersList = Teacher.objects.filter(is_valided=1)

    def get(self, request):
        thread: threadPool = settings.GLOBAL_THREAD_POOL
        uuid = request.GET.get("uuid")

        # 如果uuid在url请求链接中，执行查询
        if uuid or len(str(uuid).strip()) == 0:
            is_running, future = thread.is_running(uuid)
            if is_running:
                return Response(message("success", 200, "请求成功",
                                        kwargs={
                                            "info": {"uuid": str(uuid), "running": is_running}}))
            else:
                return Response(message("failed", 401, "请求失败",
                                        kwargs={
                                            "info": {"uuid": str(uuid), "running": is_running}}))
        else:
            zipFileInfoList = ZipfilesInfo.objects.all()
            zipSerializer = zipFileSerializer(zipFileInfoList, many=True)
            return Response(message("success", 200, "请求成功",
                                    kwargs={
                                        "info": zipSerializer.data}))

    def patch(self, request):
        zipinfoType = request.GET.get("zipInfoType")
        if not zipinfoType:
            zipinfoType = 1
        thread: threadPool = settings.GLOBAL_THREAD_POOL
        future_uuid = str(uuid1().int)
        future = thread.pool.submit(customersOp("").readAvatarZip, future_uuid,
                                    [c.teacher_photo for c in self.teachersList], zipinfoType)

        thread.future_dict.update(
            {future_uuid: futureInfo(future, singleEnum.RUNNING)})
        return Response(message("success", 200, "请求成功",
                                kwargs={
                                    "info": {"uuid": future_uuid, "zipName": "{}.zip".format(future_uuid)}}))

    def post(self, request):
        if not request.headers.__contains__("range"):
            return Response(400, message("failed", 400, "参数不合法", kwargs={"info": "range头缺失"}))
        if not request.GET.__contains__("uuid"):
            return Response(400, message("failed", 400, "参数不合法", kwargs={"info": "uuid缺失"}))
        try:
            uuid = request.GET.get("uuid")
            rangeB = request.headers.get("range")
            starts = re.findall(r"\d+", rangeB)
            start, end = map(lambda x: int(x), starts)
            zipFileName = os.path.join(
                settings.STATICFILES_DIRS[0], "zipFile/{}.zip".format(uuid))
            with open(zipFileName, "rb") as f:
                f.seek(start)
                sliceF = f.read(end - start + 1)
            resp = HttpResponse(sliceF)
            resp['content-type'] = 'application/octet-stream'
            resp['Content-Range'] = "bytes {0}-{1}/*".format(start, end)
            resp['accept-Ranges'] = "bytes"
            return resp
        except ValueError as ve:
            return Response(416, message("failed", 416, "参数不合法", kwargs={"info": ve.args[0]}))
        except FileNotFoundError:
            return Response(status=404, data=message("failed", 404, "参数不合法", kwargs={"info": "文件不存在，请重新添加任务"}))
        except Exception as e:
            return Response(400, message("failed", 400, "参数不合法", kwargs={"info": e.args[0]}))

    def delete(self, request):
        thread: threadPool = settings.GLOBAL_THREAD_POOL
        uuid = request.GET.get("uuid")
        if uuid:
            thread.destroy_task(uuid)
            is_running, future = thread.is_running(uuid)
            if not future:
                return Response(
                    message("success", 200, "请求成功", kwargs={"info": {"uuid": str(uuid), "closed": not is_running}}))
            else:
                return Response(
                    message("failed", 500, "请求失败", kwargs={"info": {"uuid": str(uuid), "closed": is_running}}))
