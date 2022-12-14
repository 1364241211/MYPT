import time
from hashlib import md5

from django.conf import settings
from jwt import decode
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer, TokenVerifySerializer

from .models import Admin, Customers, Class, Resources, ZipfilesInfo, Teacher


# admin用户序列化器
class adminSerializer(serializers.ModelSerializer):
    admin_account = serializers.RegexField(regex=r"\d{6}", required=True)
    password = serializers.RegexField(regex=r'[A-Za-z0-9]{32}', required=True)
    admin_name = serializers.CharField(required=True, max_length=10)

    def create(self, validated_data):
        password = validated_data['password']
        fisrtEncryption = md5(password.encode()).hexdigest()
        validated_data['password'] = fisrtEncryption
        return Admin.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.admin_account = validated_data.get(instance, 'admin_account')
        instance.admin_password = validated_data.get(
            instance, 'admin_password')
        instance.admin_name = validated_data.get(instance, 'admin_name')
        instance.save()
        return instance


class Meta:
    model = Admin
    fields = '__all__'
    read_only_fields = ('admin_id', 'admin_account',
                        'admin_name', 'admin_logtime')


# customer用户序列化器
class customerSerializer(serializers.ModelSerializer):
    # 身份证验证
    customer_id = serializers.RegexField(
        regex=r"^[1-9]\d{5}(18|19|20)\d{2}((0[1-9])|(1[0-2]))(([0-2][1-9])|10|20|30|31)\d{3}[0-9Xx]$")
    customer_name = serializers.CharField(max_length=5)
    # 手机号验证
    # apartment_name = serializers.RegexField(regex=r"^1[35678]\d{9}$")
    student_id = serializers.CharField()
    customer_photo = serializers.CharField()
    class_id = serializers.IntegerField()
    class_name = serializers.CharField()
    is_valided = serializers.IntegerField()
    department_name = serializers.CharField()
    apartment = serializers.CharField()
    grade = serializers.CharField()
    apartment_id = serializers.CharField()

    def create(self, validated_data):
        return Customers.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.customer_id = validated_data.get("customer_id")
        instance.student_id = validated_data.get("student_id")
        instance.customer_name = validated_data.get("customer_name")
        instance.department_name = validated_data.get("department_name")
        instance.apartment = validated_data.get("apartment")
        instance.apartment_id = validated_data.get("apartment_id")
        instance.grade = validated_data.get("grade")
        instance.customer_photo = validated_data.get("customer_photo")
        instance.class_id = validated_data.get("class_id")
        instance.class_name = validated_data.get("class_name")
        instance.is_valided = validated_data.get("is_valided")
        instance.save()
        return instance

    class Meta:
        model = Customers
        fields = '__all__'
        read_only_fields = ('customer_logtime', 'id')


# 教师序列化器
class teacherSerializer(serializers.ModelSerializer):
    # 身份证验证
    teacher_name = serializers.CharField(max_length=5)
    # 手机号验证
    teacher_phone = serializers.RegexField(regex=r"^1[35678]\d{9}$")
    teacher_id = serializers.CharField()
    teacher_photo = serializers.CharField()
    teacher_department = serializers.CharField()
    is_valided = serializers.IntegerField()

    def create(self, validated_data):
        return Teacher.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.teacher_id = validated_data.get("teacher_id")
        instance.teacher_name = validated_data.get("teacher_name")
        instance.teacher_department = validated_data.get("teacher_department")
        instance.teacher_photo = validated_data.get("teacher_photo")
        instance.teacher_phone = validated_data.get("teacher_phone")
        instance.is_vailded = validated_data.get("is_vailded")
        instance.save()
        return instance

    class Meta:
        model = Teacher
        fields = '__all__'
        read_only_fields = ('id',)


# class 班级序列化器
class classSerializer(serializers.ModelSerializer):
    class_name = serializers.CharField()
    class_group = serializers.IntegerField()

    def create(self, validated_data):
        return Class.objects.create(**validated_data)

    class Meta:
        model = Class
        fields = '__all__'
        read_only_field = ('id',)


class mdResSerializer(serializers.ModelSerializer):
    res_name = serializers.CharField(max_length=255)

    def create(self, validated_data):
        return Resources.objects.create(**validated_data)

    class Meta:
        model = Resources
        fields = '__all__'
        read_only_field = ('id',)


class zipFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = ZipfilesInfo
        fields = '__all__'


# admin用户token序列化器
class adminTokenObtainSerializer(TokenObtainPairSerializer):

    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        # 添加用户到token中
        token['admin_account'] = user.admin_account
        token['admin_name'] = user.admin_name
        token['is_active'] = True
        return token


class customerTokenObtainSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['customer_id'] = int(time.time())
        token['is_customer'] = True
        return token


class adminClearAllDataSerializer(TokenVerifySerializer):
    """
    获取token信息,用于验证
    """

    def validate(self, attrs):
        """
        attr['token']: 请求token
        settings.SECRET_KEY: settings.py 中的加密字符
        algorithms: 加密算法
        """
        decode_data = decode(
            attrs['token'], settings.SECRET_KEY, algorithms=['HS256'])
        return decode_data
