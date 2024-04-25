<template>
    <div class="table-empty">
        <div class="table-nodata">
            <img class="table-nodata-img" src="@/assets/img/noData.png" />
        </div>
        <span class="table-empty-text">
            <slot name='text'>暂无数据</slot>
        </span>
        <div class="table-empty-button" >
            <slot name="button"></slot>
        </div>
    </div>
</template>


<style scoped>
.table-nodata {
    margin: 275px auto 0;
}
.table-nodata-img{
    width: 300px;
    height: 300px;
}

.table-empty{
    position: relative;
    text-align: center;
}
.table-empty-button{
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 10px;
    /* height: 400px; */
    margin: 0 0 120px 0;
}
.table-empty-text{
    position: absolute;
    bottom: 60px;
    left: 50%;
    transform: translateX(-50%);
    font-size: 16px;
}
</style>