<template>
    <div class="tabs-info">
        <div class="tabs-info-item">
            <div class="tabs-info-item-type">导入总数</div>
            <div class="tabs-info-item-num">
                <div>{{ total }}</div>
            </div>
        </div>
        &nbsp;&nbsp;
        <div class="tabs-info-item">
            <div class="tabs-info-item-type"><el-button type="success" text>成功</el-button></div>
            <div class="tabs-info-item-num">
                <div><el-button type="success" text>{{ success }}</el-button></div>
            </div>
        </div>
        &nbsp;&nbsp;
        <div class="tabs-info-item">
            <div class="tabs-info-item-type"><el-button type="danger" text>失败</el-button></div>
            <div class="tabs-info-item-num">
                <div><el-button type="danger" text> {{ fail }}</el-button></div>
            </div>
        </div>
    </div>
</template>

<script setup>
import { defineProps } from 'vue';

const props = defineProps({
    total: {
        type: Number,
        default: 0
    },
    success: {
        type: Number,
        default: 0
    },
    fail: {
        type: Number,
        default: 0
    }
})

</script>

<style scoped>
.tabs-info{
    display: flex;
    margin: 30px 0;
}

.tabs-info-item{
    display: flex;
    align-items: center;
    width: 200px;
    height: 44px;
    line-height: 44px;
    
    border-radius: 6px 0px 0px 6px;
    border: 1px solid #DBE3FF;
}
.tabs-info-item-type{
    background: #F5F7FE;
    width: 100px;
    text-align: center;
    font-size: 14px;
}
.tabs-info-item-num{
    flex: 1;
    display: flex;
    align-items: center;
}
.tabs-info-item-num > div:first-child{
    width: 80%;
    text-align: center;
    font-size: 14px;
    color: #333333;
}
.tabs-info-item-num > div:last-child{
    font-size: 14px;
    color: #2570FF;
}
</style>