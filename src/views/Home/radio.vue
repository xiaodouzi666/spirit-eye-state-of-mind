<template>
    <div class="radio-list">
        <div class="radio-item" v-for="(item,index) in list" :key="index" @click="() => handleRadio(item, index)">
            <div class="radio-item-label">{{ item.label }}</div>
            <div :class="['radio-item-cicle', activeIdx === index ? 'active' : '']">
                <div class="radio-item-cicle-inner" v-show="activeIdx === index"></div>
            </div>
        </div>
    </div>
</template>

<script setup>
import { ref, defineProps, defineEmits } from 'vue';

const props = defineProps({
    list: {
        type: Array,
        default: () =>([])
    },
    modelValue: {
        type: String,
        default: ''
    },
    // defaultValue: () => list?.[0]?.value
})

const emits = defineEmits(['update:modelValue'])

const activeIdx = ref(0)



const handleRadio = (item, index) => {
    activeIdx.value = index
    emits('update:modelValue', item.value)
}
</script>

<style scoped>
.radio-list{
    display: flex;
}
.radio-item{
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    cursor: pointer;
    margin: 0 30px 0 0;
}
.radio-item-label{
    font-size: 14px;
    color: #fff;
    margin: 20px 0;
}
.radio-item-cicle{
    display: flex;
    align-items: center;
    justify-content: center;
    width: 17px;
    height: 17px;
    border-radius: 50%;
    border: 1px solid #fff;
}
.radio-item-cicle-inner{
    width: 9px;
    height: 9px;
    border-radius: 50%;
    background: #F0803F;
}
.active{
    border-color: #F0803F;
}
</style>