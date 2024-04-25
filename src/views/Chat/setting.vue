<template>

    <div class="setting">
        <div class="setting-mask"></div>
        <div class="setting-bg">
            <div class="setting-title">设置提醒日期</div>
            <div class="setting-picker-list">
                <van-date-picker
                    v-model="currentDate"
                    title=""
                    :show-toolbar="false"
                    :option-height="22"
                    :visible-option-num="3"
                />
            </div>
            <div class="setting-footer">
                <img class="setting-footer-button" src="@/assets/setting-confirm.png" @click="handleClick"/>
                <img class="setting-footer-button" src="@/assets/setting-cancel.png" @click="handleClick"/>
            </div>
        </div>
        
    </div>
</template>

<script setup>
import { ref, defineEmits } from 'vue'

const emits = defineEmits(['update:modelValue'])

const currentDate = ref([])

const handleClick = () => {
    emits('update:modelValue', false)
}

</script>


<style>
:root,
.van-picker,
.van-date-picker__cell,
.van-date-picker__header{
    --van-picker-background: '#7530E3';
    --van-picker-mask-color: linear-gradient(90deg, rgba(225,175,204,.6), rgba(117,48,227,0.6));
    /* linear-gradient(0deg, rgba(255, 255, 255, .9), rgba(255, 255, 255, .4)); */
}

</style>
<style lang="less" scoped>
.setting {
    position: relative;
    width: 375px;
    height: 100vh;
    &-mask{
        position: absolute;
        width: 375px;
        height: 100%;
        background: rgba(0,0,0,.8);
    }
    &-bg{
        position: absolute;
        left: 50%;
        top: 50%;
        transform: translate(-50%, -50%);
        width: 245px;
        height: 291px;
        background-image: url('@/assets/calendar.png');
        background-size: 245px 291px;
        background-repeat: no-repeat;
    }
    &-title{
        font-size: 18px;
        color: #fff;
        margin: 87px 0 0;
        text-align: center;
    }
    &-picker-list{
        height: 60px;
        margin: 35px 25px;
    }

    &-footer{
        display: flex;
        gap: 27px;
        justify-content: center;
        &-button{
            width: 92px;
            height: 40px;
            cursor: pointer;
        }
    }
}
</style>