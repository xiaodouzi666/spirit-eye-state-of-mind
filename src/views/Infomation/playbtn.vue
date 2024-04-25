<template>
    <div class="playbtn flex">
        <div class="playbtn-btn flex" v-show="playing" @click="handleStop">
            <img class="playbtn-btn-stop" src="@/assets/img/icons/icon-info-stop.png" draggable="false"/>
            <img class="playbtn-btn-stop" src="@/assets/img/icons/icon-info-stop.png" draggable="false"/>
        </div>
        <div class="playbtn-btn playbtn-btn-alt" v-show="!playing" @click="handleStart">
            <img class="playbtn-btn-start" src="@/assets/img/icons/icon-info-start.png" draggable="false"/>
        </div>
    </div>
</template>

<script setup>
import { defineProps, defineEmits } from 'vue'

const emits = defineEmits(['play'])

const props = defineProps({
    playing: {
        type: Boolean,
        default: false
    }
})


const handleStart = () => emits('play', true)

const handleStop = () => emits('play', false)


</script>

<style lang="less" scoped>
.playbtn{
    width: 100%;
    height: 100%;
    align-items: center;
    justify-content: center;
    cursor: pointer;
    &-btn{
        gap: 5px;
        &-start{
            // width: 32px;
            height: 27px;

        }

        &-stop{
            width: 7px;
            height: 24px;
        }
        &-alt{
        margin: 0 0 0 5px;
    }
    }
    
}
</style>