import { RouteRecordRaw } from "vue-router";

const routes: RouteRecordRaw[] = [
  {
    path: "/",
    redirect: "/index",
  },
  {
    path: "/index",
    name: "index", // components: { indexVue: () => import("../views/Index.vue") }
    component: () => import("../views/Index.vue"),
    meta: {
      requireAuth: false,
    },
  },
  {
    path: "/success",
    name: "success",
    // components: { indexVue: () => import("../views/CommitSuccess.vue") }
    component: () => import("../views/CommitSuccess.vue"),
    meta: {
      requireAuth: false,
    },
  },
  {
    path: "/admin/",
    name: "admin",
    redirect: "/admin/login",
    // component: () => import("../views/Login.vue"),
  },
  {
    path: "/admin/login",
    name: "login",
    // components: { indexVue: () => import("../views/Login.vue") },
    component: () => import("../views/Login.vue"),
    meta: {
      requireAuth: false,
    },
  },
  {
    path: "/admin/controlPanel",
    name: "customerControlPanel",
    components: { adminVue: () => import("../views/CustomerControlPanel.vue") },
    redirect: { name: "customers" },
    children: [
      {
        path: "/admin/controlPanel/customers",
        name: "customers",
        component: () => import("../components/Customers.vue"),
      },
      {
        path: "/admin/controlPanel/adDesign",
        name: "adDesign",
        component: () => import("../components/AdDesign.vue"),
      },
      {
        path: "/admin/controlPanel/rechargeNotice",
        name: "rechargeNotice",
        component: () => import("../components/ReChargeMd.vue"),
      },
      {
        path: "/admin/controlPanel/moderateUsers",
        name: "moderateUsers",
        component: () => import("../components/ValidateCustomers.vue"),
      },
      {
        path: "/admin/controlPanel/classesControl",
        name: "classesControl",
        component: () => import("../components/ClassesControl.vue"),
      },
      {
        path: "/admin/controlPanel/exportAvatar",
        name: "exportAvatar",
        component: () => import("../components/ExportAvatar.vue"),
      },
      {
        path: "/admin/controlPanel/importOperations",
        name: "importOperations",
        component: () => import("../components/ImportOperations.vue"),
      },
      {
        path: "/admin/controlPanel/teachers",
        name: "teachers",
        component: () => import("../components/Teachers.vue"),
      },
      {
        path: "/admin/controlPanel/moderateTeachers",
        name: "moderateTeachers",
        component: () => import("../components/VaildateTeachers.vue"),
      },
    ],
    meta: {
      requireAuth: true,
    },
  },
];

export default routes;
