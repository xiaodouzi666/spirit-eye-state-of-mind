<template>
    <div class="info">
        <div class="info-section">
            <div class="info-section-title">Rating information</div>
            <div class="info-section-container">
                <div class="info-section-radar">
                    <Radar />
                </div>
                <div class="info-section-right">
                    <div class="info-section-right-title flex">
                        <div class="info-section-right-title-label">The name of this file</div>
                        <div class="info-section-right-title-label">MP4</div>
                        <div class="info-section-right-title-label">2024/09/05  12:10:12</div>
                        <div class="info-section-right-title-label info-section-right-title-label--score">Score:96</div>
                    </div>
                    <div class="info-section-right-content">
                        It's a description of the evaluation information. This is a description of the evaluation information. This is a description of the evaluation information. This is a description of the evaluation information
                    </div>

                    <div class="info-section-right-buttons flex">
                        <div class="info-section-right-buttons-btn flex">Collection</div>
                        <div class="info-section-right-buttons-btn flex">Download</div>
                        <div class="info-section-right-buttons-btn flex">Back</div>
                    </div>
                </div>
            </div>
        </div>
        
        <div class="info-section-two">
            <Title>
                <template #icon> <img src="@/assets/img/icons/icon-info-user.png"/></template>
                <template #title> Matching user profiles </template>
            </Title>
            <div class="info-section-two-banner flex">
                <div class="info-section-two-banner-label">Gender: Male</div>
                <div class="info-section-two-banner-label">Age range: 30-24 years old</div>
                <div class="info-section-two-banner-label">Favorite model: sports car</div>
                <div class="info-section-two-banner-label">Favorite style: lively</div>
            </div>
        </div>


        <div class="info-section-three">
            <Title>
                <template #icon> <img src="@/assets/img/icons/icon-info-yinpin.png"/></template>
                <template #title> Competitive Audio </template>
            </Title>

            <List />
        </div>
    </div>
</template>


<script setup>
import Radar from './radar.vue'
import List from './list.vue'
import Title from "@/views/File/title.vue"

</script>


<style lang="less" scoped>
.info{
    width: 1226px;
    margin: auto;
    
    &-section{
        width: 1226px;
        background: #44546A;
        padding: 30px;
        margin: auto;
        box-sizing: border-box;
        &-title{
            color: #fff;
            font-size: 20px;
        }

        &-container{
            display: flex;
            gap: 10px;
        }

        &-radar{
            width: 580px;
            height: 352px;
            margin-left: -30px;
        }

        &-right{
            &-title{
                font-size: 16px;
                line-height: 22px;
                color: #fff;
                align-items: center;
                justify-content: start;
                gap: 40px;
                margin: 0 0 40px 0;
                &-label{
                    
                    &--score{
                        font-size: 24px;
                        color: #F06473;
                    }
                    
                }
            }
            &-content{
                width: 621px;
                height: 144px;
                line-height: 20px;
                border: 1px solid #fff;
                box-sizing: border-box;
                font-size: 14px;
                color: #fff;
                padding: 10px 20px;
                // overflow-y: scroll;
            }

            &-buttons{
                gap: 40px;
                margin: 40px 0 0 0;
                &-btn{
                    width: 142px;
                    height: 60px;
                    align-items: center;
                    justify-content: center;
                    background: #4472C4;
                    color: #fff;
                    font-size: 18px;
                    border-radius: 10px;
                    cursor: pointer;
                }
            }
        }
    }

    &-section-two{
        width: 1226px;
        box-sizing: border-box;
        margin: 40px auto 0;
        // &-title{
        //     margin: 0 0 0 10px;
        // }
        &-banner{
            height: 74px;
            background: #44546A;
            margin: auto;
            font-size: 16px;
            color: #fff;

            align-items: center;
            gap: 30px;
            padding: 0 60px;
        }
    }

    &-section-three {
        margin: 40px auto 0;
        width: 1226px;
        box-sizing: border-box;
    }
}
</style>