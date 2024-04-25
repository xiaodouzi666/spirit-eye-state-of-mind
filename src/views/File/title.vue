<template>
    <div class="section-title">
        <div class="section-title-icon">
            <slot name="icon"></slot>
        </div>
        <div class="section-title-text">
            <slot name="title"></slot>
        </div>
    </div>
</template>


<style lang="less" scoped>
.section-title{
    display: flex;
    align-items: center;
    margin: 0 0 20px 0;

    &-icon {
        width: 25px;
        height: 25px;
        line-height: 0;
        :deep(img){
            width: 100%;
            height: 100%;
        }
    }

    &-text{
        font-size: 20px;
        color: #fff;
        margin: 0 0 0 10px;
    }
}
</style>