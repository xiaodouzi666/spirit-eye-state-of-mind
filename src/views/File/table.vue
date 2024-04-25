<template>
    <div class="file-table">
        <div class="file-table-header column-color">
            <div class="file-table-header-column">File Name</div>
            <div class="file-table-header-column">Creation time</div>
        </div>
        <div class="file-table-body">
            <div :class="[
                'file-table-body-column',
                index % 2 === 0 ? '' : 'column-color'
            ]" 
            v-for="(item, index) in list" :key="index"
            @click="() => handleCellClick(index)"    
        >
                <div :class="[
                    'file-table-body-column-text',
                    current === index ? 'active' : ''
                ]">{{ item?.label }}</div>
                <div class="file-table-body-column-time">{{ formatTime(item?.time) }}</div>
            </div>
        </div>
    </div>
</template>

<script setup>
import { ref, defineProps } from 'vue';
import { formatTime } from '@/utils/date';

const props = defineProps({
    list: {
        type: Array,
        default: () => ([])
    }
})

const current = ref(-1)


const handleCellClick = (index) => {
    current.value = index
}
</script>

<style lang="less" scoped>
.column-color {
    background: #44546A;
}   
.file-table{
    &-header{
        display: flex;
        align-items: center;
        justify-content: space-between;
        height: 44px;
        font-size: 18px;
        font-weight: bold;
        padding: 0 69px;
    }
}
.file-table-body{
    font-size: 17px;

    height: 378px;
    overflow-y: scroll;
    &::-webkit-scrollbar {
        width: 5px;
        height: 73px;
    }
    &::-webkit-scrollbar-thumb{
        background: #4472C4;
        border-radius: 5px;
    }
    &-column{
        height: 44px;
        display: flex;
        align-items: center;
        justify-content: space-between;
        padding: 0 69px;
        cursor: pointer;

        &-text{}
    }
}

.active{
    color: #5D97FF;
}

</style>