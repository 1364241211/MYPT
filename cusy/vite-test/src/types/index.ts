// 用户结构
export interface customer {
  id: number;
  customer_id: string;
  customer_name: string;
  customer_photo: string;
  student_id: string;
  class_name: string;
  class_id: number;
  customer_logtime: string;
  is_valided: string;
  department_name: string;
  apartment: string;
  grade: string;
  apartment_id: number;
}
// 教师结构
export interface teacher {
  id: number;
  teacher_id: string;
  teacher_name: string;
  teacher_photo: string;
  teacher_phone: string;
  is_valided: string;
  teacher_department: string;
  teacher_logtime: string;
}
// 分页数据结构
export interface pagnationData {
  count: number;
  next: string;
  previous: string;
}
// 班级组结构
export interface classGroup {
  group_id: number;
  group_name: string;
  groups: Array<classType>;
}
// 班级数据结构
export interface classType {
  id: number;
  class_group: number;
  class_name: string;
}
// 列表数据结构
export interface tabType {
  title: string;
}
// 网络请求方法枚举
export enum METHOD {
  GET = "GET",
  POST = "POST",
  UPDATE = "UPDATE",
  DELETE = "DELETE",
  PATCH = "PATCH",
}
// 网络响应信息
interface messageInfo {
  [props: string]: any;
}
// 网路响应格式
export interface resMessage {
  code?: number;
  message?: string;
  status?: string;
  info?: string | Array<any> | number;
}
export interface ListMessage<T> {
  count?: number;
  next?: string;
  previous?: string;
  results?: Array<T>;
}
export interface zipFileInfo {
  zip_name?: string;
  zip_size?: number;
  last_modified_time?: string;
  download?: number;
  zipinfo_type?: string;
}
export const options = [
  {
    text: "烹饪系",
    vale: "1",
    children: [
      {
        text: "20级",
        value: "120",
        children: [
          {
            text: "烹饪20级本实班",
            value: "1201",
          },
          {
            text: "中餐20级1班",
            value: "1202",
          },
          {
            text: "军预20级1班",
            value: "1203",
          },
        ],
      },
      {
        text: "21级",
        value: "121",
        children: [
          {
            text: "烹饪21级本实班",
            value: "1211",
          },
          {
            text: "中餐21级1班",
            value: "1212",
          },
          {
            text: "中餐21级2班",
            value: "1213",
          },
          {
            text: "西餐21级1班",
            value: "1214",
          },
          {
            text: "西餐21级2班",
            value: "1215",
          },
          {
            text: "军预21级1班",
            value: "1216",
          },
          {
            text: "军预21级2班",
            value: "1217",
          },
        ],
      },
      {
        text: "22级",
        value: "122",
        children: [
          {
            text: "烹饪22级本实班",
            value: "1221",
          },

          {
            text: "中餐22级1班",
            value: "1222",
          },
          {
            text: "西餐22级1班",
            value: "1223",
          },
          {
            text: "西餐22级2班",
            value: "1224",
          },
          {
            text: "军预22级1班",
            value: "1225",
          },
        ],
      },
    ],
  },
  {
    text: "机电系",
    value: "2",
    children: [
      {
        text: "20级",
        value: "220",
        children: [
          {
            text: "机电20本实班",
            value: "2201",
          },
          {
            text: "汽修20级1班",
            value: "2202",
          },
          {
            text: "汽修20级2班",
            value: "2203",
          },
          {
            text: "数控20级1班",
            value: "2204",
          },
          {
            text: "水建20级1班",
            value: "2205",
          },
        ],
      },
      {
        text: "21级",
        value: "221",
        children: [
          {
            text: "机电21级本实班",
            value: "2211",
          },
          {
            text: "汽修21级1班",
            value: "2212",
          },
          {
            text: "汽修21级2班",
            value: "2213",
          },
          {
            text: "数控21级1班",
            value: "2214",
          },
          {
            text: "数控21级2班",
            value: "2215",
          },
          {
            text: "水建21级1班",
            value: "2216",
          },
          {
            text: "水建21级2班",
            value: "2217",
          },
        ],
      },
      {
        text: "22级",
        value: "222",
        children: [
          {
            text: "机电22级本实班",
            value: "2221",
          },
          {
            text: "汽修22级1班",
            value: "2222",
          },
          {
            text: "汽修22级2班",
            value: "2223",
          },
          {
            text: "数控21级1班",
            value: "2214",
          },
          {
            text: "数控22级1班",
            value: "2215",
          },
          {
            text: "数控22级2班",
            value: "2216",
          },
          {
            text: "水建22级1班",
            value: "2217",
          },
          {
            text: "水建22级2班",
            value: "2218",
          },
        ],
      },
    ],
  },
  {
    text: "民旅科",
    value: "3",
    children: [
      {
        text: "20级",
        value: "320",
        children: [
          {
            text: "民旅20级本实班",
            value: "3201",
          },
          {
            text: "铁旅20级1班",
            value: "3202",
          },
          {
            text: "铁旅20级2班",
            value: "3203",
          },
          {
            text: "电商20级1班",
            value: "3204",
          },
          {
            text: "北大青鸟计算机20级1班",
            value: "3205",
          },
          {
            text: "北大青鸟计算机20级2班",
            value: "3206",
          },
        ],
      },
      {
        text: "21级",
        value: "321",
        children: [
          {
            text: "民旅21级本实班",
            value: "3211",
          },
          {
            text: "铁旅21级1班",
            value: "3212",
          },
          {
            text: "铁旅21级2班",
            value: "3213",
          },
          {
            text: "电商21级1班",
            value: "3214",
          },
          {
            text: "电商21级2班",
            value: "3215",
          },
          {
            text: "北大青鸟计算机21级1班",
            value: "3216",
          },
          {
            text: "北大青鸟计算机21级2班",
            value: "3217",
          },
        ],
      },
      {
        text: "22级",
        value: "322",
        children: [
          {
            text: "电商22级合班",
            value: "3221",
          },
          {
            text: "铁旅22级1班",
            value: "3222",
          },
          {
            text: "铁旅22级2班",
            value: "3223",
          },
          {
            text: "电商22级1班",
            value: "3224",
          },
          {
            text: "电商22级2班",
            value: "3225",
          },
          {
            text: "北大青鸟计算机22级1班",
            value: "3226",
          },
          {
            text: "北大青鸟计算机22级2班",
            value: "3227",
          },
        ],
      },
    ],
  },
  {
    text: "学艺科",
    value: "4",
    children: [
      {
        text: "20级",
        value: "420",
        children: [
          {
            text: "学前20级本实班",
            value: "4201",
          },
          {
            text: "学前20级1班",
            value: "4202",
          },
          {
            text: "学前20级2班",
            value: "4203",
          },
          {
            text: "学前20级3班",
            value: "4204",
          },
          {
            text: "学前20级4班",
            value: "4205",
          },
          {
            text: "学前20级5班",
            value: "42026",
          },
        ],
      },
      {
        text: "21级",
        value: "421",
        children: [
          {
            text: "幼儿保育21级本实班",
            value: "4211",
          },
          {
            text: "幼儿保育21级1班",
            value: "4212",
          },
          {
            text: "幼儿保育21级2班",
            value: "4213",
          },
          {
            text: "幼儿保育21级3班",
            value: "4214",
          },
          {
            text: "幼儿保育21级4班",
            value: "4215",
          },
          {
            text: "幼儿保育21级5班",
            value: "4216",
          },
          {
            text: "形设21级1班",
            value: "4217",
          },
        ],
      },
      {
        text: "22级",
        value: "422",
        children: [
          {
            text: "幼儿保育22级本实班",
            value: "4221",
          },
          {
            text: "幼儿保育22级1班",
            value: "4222",
          },
          {
            text: "幼儿保育22级2班",
            value: "4223",
          },
          {
            text: "幼儿保育22级3班",
            value: "4224",
          },
          {
            text: "幼儿保育22级4班",
            value: "4225",
          },
          {
            text: "形设22级1班",
            value: "4226",
          },
        ],
      },
    ],
  },
  {
    text: "艺术科",
    value: "5",
    children: [
      {
        text: "20级",
        value: "520",
        children: [
          {
            text: "美术20级1班",
            value: "5201",
          },
          {
            text: "美术20级2班",
            value: "5202",
          },
          {
            text: "体育20级1班",
            value: "5203",
          },
          {
            text: "舞蹈20级1班",
            value: "5204",
          },
          {
            text: "声乐20级1班",
            value: "5205",
          },
        ],
      },
      {
        text: "21级",
        value: "521",
        children: [
          {
            text: "美术21级1班",
            value: "5211",
          },
          {
            text: "美术21级2班",
            value: "5212",
          },
          {
            text: "体育21级1班",
            value: "5213",
          },
          {
            text: "舞蹈声乐20级1班",
            value: "5214",
          },
        ],
      },
      {
        text: "22级",
        value: "522",
        children: [
          {
            text: "美术22级1班",
            value: "5221",
          },
          {
            text: "体育22级1班",
            value: "5222",
          },
          {
            text: "舞蹈22级1班",
            value: "5223",
          },
          {
            text: "声乐22级1班",
            value: "5224",
          },
        ],
      },
    ],
  },
];

export const apratment = [
  { text: "男生宿舍", value: "1" },
  { text: "女生宿舍", value: "2" },
  { text: "男女混合宿舍", value: "3" },
];
