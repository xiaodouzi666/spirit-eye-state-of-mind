<template>
    <div class="process">
        <div class="process-container">
            <div :class="[
                    'process-item',
                    process >= index ? 'active' : ''
                 ]" v-for="(label, index) in list" :key="index">
                <div class="process-item-index">{{ index + 1 }}</div>
                <div class="process-item-label">{{ label }}</div>
                <div :class="[
                    'process-item-line',
                    index < process  ? 'line-active' : ''
                ]" v-show="index < list.length - 1"></div>
            </div>
        </div>
    </div>
</template>

<script setup>
import { defineProps } from 'vue'

const props = defineProps({
    list: {
        type: Array,
        default: () => ([])
    },
    process: {
        type: Number,
        default: 0
    }
})


</script>

<style scoped>
.process{
    
}

.process-container,
.process-item{
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 14px;
}
.process-item-index{
    display: flex;
    align-items: center;
    justify-content: center;
    width: 28px;
    height: 28px;
    background: #E5E7EB;
    border-radius: 50%;
    font-weight: 500;
    font-size: 16px;
    color: #606266;
    
}

.process-item-label{
    height: 19px;
    font-family: PingFang SC, PingFang SC;
    font-weight: 800;
    font-size: 16px;
    color: #606266;
    /* line-height: 40px; */
    text-align: left;
    font-style: normal;
    text-transform: none;
}

.process-item-line{
    width: 360px;
    height: 0px;
    border: 1px solid rgba(51,51,51,0.2);
}
.active .process-item-index{
    background: #2570FF;
    color: #fff;
}
.active .process-item-label{
    color: #333333;
}
.line-active{
   border-color: #2570FF;
}
</style>