<template>
  <div class="cascaderComp-div">
    <h2>{{ props.title }}</h2>
    <div class="main-panel">
      <label for="cascader-grade">请选择你的寝室楼栋</label>
      <select
        ref="SelectApartment"
        name=""
        id="cascader-grade"
        class="cascader-select"
        required
      >
        <option v-for="COption in props.options" :value="COption.text">
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
import { ref } from "vue";

interface Props {
  title: string;
  options: Array<CascaderOption>;
}
const props = defineProps<Props>();

// 选择的寝室实例
const SelectApartment = ref<HTMLSelectElement>();

// 获取当前寝室楼栋
const NowApartment = ref();
NowApartment.value = SelectApartment.value?.selectedIndex;

const emit = defineEmits<{
  (e: "onFinish", selectedValue: string): void;
}>();

const onEnter = () => {
  emit(
    "onFinish",
    SelectApartment.value?.selectedOptions.item(NowApartment.value)?.innerText!
  );
};
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
