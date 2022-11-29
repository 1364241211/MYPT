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
