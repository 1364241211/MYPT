<template>
  <div class="cascaderComp-div">
    <h2>{{ props.title }}</h2>
    <div class="main-panel">
      <label for="cascader-grade">请选择你的专业和年级</label>
      <select
        ref="Tselect"
        name=""
        id="cascader-grade"
        class="cascader-select"
        required
        @change="selectChange"
      >
        <optgroup
          ref="Gselect"
          v-for="COption in props.options"
          :label="COption.text"
        >
          <option v-for="C1Option in COption.children" :value="C1Option.text">
            {{ C1Option.text }}
          </option>
        </optgroup>
      </select>
      <label for="cascader-class">请选择你的班级</label>
      <select
        ref="Fselect"
        name=""
        id="cascader-class"
        class="cascader-select"
        required
        @select=""
      >
        <option v-for="COption in Locate" :value="COption.text">
          {{ COption.text }}
        </option>
      </select>
    </div>
    <div>
      <button @click.prevent="onEnter">确认</button>
    </div>
  </div>
</template>

<script setup lang="ts">
import type { CascaderOption } from "vant";
import { onMounted, ref } from "vue";

interface Props {
  title: string;
  options: Array<CascaderOption>;
}
const props = defineProps<Props>();

// 获取当前年级信息
const NowDepartment = ref();
// 获取当前年级信息
const NowGrad = ref();
// 获取当前的年级
const Tselect = ref<HTMLSelectElement>();
// 最后班级
const Fselect = ref<HTMLSelectElement>();
// 班级列表
const Locate = ref<CascaderOption[]>();
// 选择的专业和班级发生变化时出发事件
const selectChange = () => {
  // 获取选择专业的下标
  let i = Tselect.value?.selectedIndex;
  // 获取选择年级的下标
  let t = i! % 3;
  i = Math.floor(i! / 3);

  NowDepartment.value = props.options[i]?.text;
  NowGrad.value = props.options[i]?.children![t]?.text;
  Locate.value = props.options[i]?.children![t]?.children as [];
};

const emit = defineEmits<{
  (
    e: "onFinish",
    selectedValue: { department: string; grade: string; class: string }
  ): void;
}>();

const onEnter = () => {
  emit("onFinish", {
    department: NowDepartment.value,
    grade: NowGrad.value,
    class: Locate.value![Fselect.value?.selectedIndex!].text!,
  });
};
onMounted(() => {
  // 班级列表初始化
  NowDepartment.value = props.options[0]?.text;
  NowGrad.value = props.options[0]?.children![0].text;
  Locate.value = props.options[0]?.children![0].children as [];
});
</script>

<style scoped lang="scss">
.cascaderComp-div {
  width: 100%;
  height: 100%;
  display: flex;
  flex-direction: column;
  justify-content: space-around;
  align-items: center;
  .main-panel {
    height: 40%;
    width: 100%;
    padding-left: calc(4%);
    display: flex;
    flex-direction: column;
    align-items: flex-start;
    justify-content: space-around;
    .cascader-select {
      width: 90%;
      height: calc(40% - 10px);
      font-size: medium;
    }
  }
  button {
    color: whitesmoke;
    background-color: #71b6a2;
    border: none;
  }
}
</style>
