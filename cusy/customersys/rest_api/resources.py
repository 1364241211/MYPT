from import_export import resources
from import_export.fields import Field

from .models import Customers, Teacher


class customersResources(resources.ModelResource):
    student_id = Field(attribute="student_id", column_name="学（工）号")
    customer_name = Field(attribute="customer_name", column_name="学生姓名")
    customer_id = Field(attribute="customer_id", column_name="学生身份证号码")
    department_name = Field(attribute="department_name", column_name="专业")
    grade = Field(attribute="grade", column_name="年级")
    class_name = Field(attribute="class_name", column_name="班级")
    custoemr_logtime = Field(attribute="customer_logtime", column_name="学生登记时间")
    is_valided = Field(attribute="is_valided", column_name="审核结果")

    class Meta:
        model = Customers
        exclude = ("customer_photo", "apartment_id", "class_id")
        export_order = ("id",)

    def dehydrate_is_valided(self, customer):
        is_valided = customer.is_valided
        if is_valided == 0:
            return "审核中"
        elif is_valided == 1:
            return "已通过"
        elif is_valided == 2:
            return "已驳回"


class customersMTResources(resources.ModelResource):
    customer_name = Field(attribute="customer_name", column_name="客户姓名")
    customer_id = Field(attribute="customer_id", column_name="学（工）号")

    class Meta:
        model = Customers
        exclude = ("parent_phone", "customer_photo", "customer_logtime",
                   "class_id", "class_name", "id", "is_valided")


class teachersResources(resources.ModelResource):
    teacher_id = Field(attribute="teacher_id", column_name="学（工）号")
    teacher_name = Field(attribute="teacher_name", column_name="教师姓名")
    teacher_department = Field(
        attribute="teacher_department", column_name="教师职称")
    teacher_phone = Field(attribute="teacher_phone", column_name="教师联系方式")
    is_valided = Field(attribute="is_valided", column_name="审核结果")

    class Meta:
        model = Teacher
        exclude = ("teacher_photo",)
        export_order = ("id",)

    def dehydrate_is_valided(self, customer):
        is_valided = customer.is_valided
        if is_valided == 0:
            return "审核中"
        elif is_valided == 1:
            return "已通过"
        elif is_valided == 2:
            return "已驳回"


class teachersMTResources(resources.ModelResource):
    teacher_name = Field(attribute="teacher_name", column_name="教师姓名")
    teacher_id = Field(attribute="teacher_id", column_name="学（工）号")

    class Meta:
        model = Teacher
        exclude = ("id", "teacher_department", "teacher_phone",
                   "is_valided", "teacher_logtime")
