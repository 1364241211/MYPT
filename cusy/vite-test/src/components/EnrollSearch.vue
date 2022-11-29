<template>
  <div>
    <van-form>
      <van-search
        v-model="searchValue"
        show-action
        placeholder="请输入身份号码或者工号"
        @search="search"
      >
        <template #action>
          <div @click="search(searchType)">搜索</div>
        </template>
      </van-search>
      <van-field
        v-model="searchTypeV"
        is-link
        readeonly
        label="查询类型"
        placeholder="学生"
        @click="showSearchTypePicker = true"
      >
      </van-field>
      <van-popup
        v-model:show="showSearchTypePicker"
        round
        position="bottom"
        teleport="body"
      >
        <van-picker
          title="查询类型"
          :columns="searchTypes"
          @confirm="confirmSearchType"
          @change="changeSearchType"
          @cancel="cancelSearchType"
        >
        </van-picker>
      </van-popup>
    </van-form>
    <van-empty image="error" description="查询用户不存在" v-if="!isExist" />
    <van-empty image="network" description="网络错误" v-if="netError" />
    <div class="user-group" v-if="isExist && searchType == 0">
      <div class="avatar">
        <!-- :src="'/static/avatar/' + userInfo.customer_photo" -->
        <van-image
          width="80px"
          height="100px"
          :src="'http:127.0.0.1/static/avatar/' + userInfo.customer_photo"
          fit="cover"
          position="center"
        />
      </div>
      <div class="user-info-div">
        <van-form>
          <van-field
            v-model="userInfo.customer_name"
            readonly
            label="学生姓名"
          ></van-field>
          <van-field
            v-model="userInfo.customer_id"
            readonly
            label="学生身份证"
          ></van-field>
          <van-field
            v-model="userInfo.student_id"
            readonly
            label="家长电话"
          ></van-field>
          <van-field
            v-model="userInfo.class_name"
            readonly
            label="学生班级"
          ></van-field>
          <van-field
            v-model="userInfo.is_valided"
            type="textarea"
            autosize
            readonly
            label="审核结果"
          ></van-field>
        </van-form>
      </div>
    </div>
    <div class="teacher-group" v-if="isExist && searchType == 1">
      <!-- :src="'/static/avatar/' + teacherInfo.teacher_photo" -->
      <div class="avatar">
        <van-image
          width="80px"
          height="100px"
          :src="'http://127.0.0.1/static/avatar/' + teacherInfo.teacher_photo"
          fit="cover"
          position="center"
        />
      </div>
      <div class="teacher-info-div">
        <van-form>
          <van-field
            v-model="teacherInfo.teacher_id"
            readonly
            label="教师工号"
          ></van-field>
          <van-field
            v-model="teacherInfo.teacher_name"
            readonly
            label="教师名称"
          ></van-field>
          <van-field
            v-model="teacherInfo.teacher_department"
            readonly
            label="教师职称"
          ></van-field>
          <van-field
            v-model="teacherInfo.teacher_phone"
            readonly
            label="联系方式"
          ></van-field>
          <van-field
            v-model="teacherInfo.is_valided"
            type="textarea"
            autosize
            readonly
            label="审核结果"
          ></van-field>
        </van-form>
      </div>
    </div>
  </div>
</template>

<script lang="ts" setup>
import { AxiosResponse } from "axios";
import { reactive, ref } from "vue";

import { customer, teacher } from "../types/index";
import service from "../util/api";

const isExist = ref(true);
const netError = ref(false);
const errorMessage = ref("");
const validedColor = ref("green");
const userInfo: customer = reactive({
  id: 0,
  customer_name: "",
  customer_id: "",
  student_id: "",
  customer_photo: "",
  class_name: "",
  class_id: 0,
  customer_logtime: "",
  is_valided: "",
  department_name: "",
  apartment: "",
  apartment_id: 0,
  grade: "",
});
const teacherInfo: teacher = reactive({
  id: 0,
  teacher_id: "",
  teacher_name: "",
  teacher_department: "",
  teacher_phone: "",
  teacher_photo: "",
  teacher_logtime: "",
  is_valided: "",
});
const setUserInfo = (res: AxiosResponse) => {
  userInfo.id = res.data.info.id;
  userInfo.customer_name = res.data.info.customer_name;
  userInfo.customer_id = res.data.info.customer_id;
  userInfo.student_id = res.data.info.student_id;
  userInfo.class_name = res.data.info.class_name;
  userInfo.class_id = res.data.info.class_id;
  userInfo.customer_logtime = res.data.info.customer_logtime;
  userInfo.customer_photo = res.data.info.customer_photo;
  switch (res.data.info.is_valided) {
    case 0:
      {
        userInfo.is_valided = "审核中...";
        validedColor.value = "blue";
      }
      break;
    case 1:
      {
        userInfo.is_valided = "审核通过";
        validedColor.value = "green";
      }
      break;
    case 2:
      {
        userInfo.is_valided = "申请被驳回,请联系管理员";
        validedColor.value = "red";
      }
      break;
  }
};
const setTeacherInfo = (res: AxiosResponse) => {
  teacherInfo.id = res.data.info.id;
  teacherInfo.teacher_id = res.data.info.teacher_id;
  teacherInfo.teacher_name = res.data.info.teacher_name;
  teacherInfo.teacher_department = res.data.info.teacher_department;
  teacherInfo.teacher_phone = res.data.info.teacher_phone;
  teacherInfo.teacher_photo = res.data.info.teacher_photo;
  switch (res.data.info.is_valided) {
    case 0:
      {
        teacherInfo.is_valided = "审核中...";
        validedColor.value = "blue";
      }
      break;
    case 1:
      {
        teacherInfo.is_valided = "审核通过";
        validedColor.value = "green";
      }
      break;
    case 2:
      {
        teacherInfo.is_valided = "申请被驳回,请联系管理员";
        validedColor.value = "red";
      }
      break;
  }
};
// 发起查询请求
// 0:学生
// 1:教师
const search = (type: number) => {
  if (searchValue.value !== "") {
    switch (type) {
      case 0:
        {
          service
            .get(`/customerGeneralApi?customer_id=${searchValue.value}`)
            .then((res) => {
              switch (res.data.code) {
                case 200:
                  {
                    isExist.value = true;
                    netError.value = false;
                    setUserInfo(res);
                  }
                  break;
                case 404:
                  {
                    isExist.value = false;
                    netError.value = false;
                  }
                  break;
              }
            })
            .catch((err) => {
              netError.value = true;
              isExist.value = true;
              errorMessage.value = err.config;
            });
        }
        break;
      case 1: {
        service
          .get(`/teacherGeneralApi?teacher_id=${searchValue.value}`)
          .then((res) => {
            switch (res.data.code) {
              case 200:
                {
                  isExist.value = true;
                  netError.value = false;
                  setTeacherInfo(res);
                }
                break;
              case 404:
                {
                  isExist.value = false;
                  netError.value = false;
                }
                break;
            }
          })
          .catch((err) => {
            netError.value = true;
            isExist.value = true;
            errorMessage.value = err.config;
          });
      }
    }
  }
};
const searchTypes = ref(["学生", "教师"]);
const searchValue = ref("");
const searchType = ref(0);
const searchTypeV = ref("");
const showSearchTypePicker = ref(false);
const confirmSearchType = (value: any, index: any) => {
  searchType.value = index;
  searchTypeV.value = value;
  showSearchTypePicker.value = false;
};
const changeSearchType = (value: any, index: any) => {
  searchType.value = index;
  searchTypeV.value = value;
};
const cancelSearchType = () => {
  showSearchTypePicker.value = false;
};
</script>

<style lang="scss" scoped>
.van-search {
  height: 50px;
}
.user-group {
  display: flex;
  background-color: white;
  height: 90vh;
  .avatar {
    width: 25%;
    margin-top: calc(5% + 2px);
    padding: calc(12%) 0;
  }
  .user-info-div {
    width: 75%;
    display: flex;
    flex-direction: column;
    margin-top: 5%;
    padding: 2% 0;
    :deep(.van-field) {
      margin: 10% 0;
      &:last-child {
        margin: 10% 0 5% 0;
        .van-field__control {
          color: v-bind("validedColor");
        }
      }
    }
  }
}
.teacher-group {
  display: flex;
  background-color: white;
  height: 90vh;
  .avatar {
    width: 25%;
    margin-top: calc(5% + 2px);
    padding: calc(12%) 0;
  }
  .teacher-info-div {
    width: 75%;
    display: flex;
    flex-direction: column;
    margin-top: 5%;
    padding: 2% 0;
    :deep(.van-field) {
      margin: 10% 0;
      &:last-child {
        margin: 10% 0 5% 0;
        .van-field__control {
          color: v-bind("validedColor");
        }
      }
    }
  }
}
input[type="search"] {
  color: black;
}
:deep(.van-search__field) {
  margin: 0;
}
.van-empty {
  background: white;
}
</style>
