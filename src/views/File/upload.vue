<template>
    <div class="file-upload">
        <el-upload action="#" :show-file-list="false" :auto-upload="false" v-show="!isShowProgress">
            <div class="file-upload-container">
                <img class="file-upload-container-icon" src="@/assets/img/icons/icon-upload.png"/>
                <div class="file-upload-container-text">Click to add or drag the text to this area</div>
            </div>
        </el-upload>

        <div class="file-upload-progress" v-show="isShowProgress">
            <el-progress type="circle" :percentage="25" width="63" :show-text="false" color="#4472C4"/>
            <div class="file-upload-progress-text">
                uploading... 50%
            </div>
        </div>
        
    </div>
</template>


<script setup>
import { ref } from 'vue'


const isShowProgress = ref(true)

</script>


<style>
.file-upload .el-upload{
    width: 100%;
}
</style>
<style lang="less" scoped>
.file-upload{
    width: 100%;
    height: 60%;
    text-align: center;
    overflow: hidden;
    padding: 0 0 20px 0;

    &-container{
        text-align: center;
        margin: 267px 0 0 0;
        &-icon{
            width: 75px;
            height: 75px;
        }

        &-text{
            font-size: 24px;
            text-align: center;
        }
    }

    &-progress{
        margin: 267px 0 0 0;
        &-text{
            font-size: 24px;
            font-weight: bold;
            margin: 20px 0 0 0;
        }
    }
    
}
</style>