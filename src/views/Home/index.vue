<template>
    <div class="home">
        <div class="home-title">User Portrait Selection</div>

        <div class="home-section">
            <div class="home-section-flex">

                <!--Sex Selection-->
                <div class="home-section-item">
                    <div class="home-section-item-title">Sex Selection</div>
                    <div class="home-section-item-content">
                        <Radio :list="RadioList"/>
                    </div>
                </div>

                <!--Permanent Residence Selection-->
                <div class="home-section-item home-section-item-center">
                    <div class="home-section-item-title home-section-item-two">Permanent Residence Selection</div>
                    <div class="flex align-center">
                        <el-select
                            v-model="province"
                            placeholder=""
                            size="large"
                            @change="getCity"
                        >
                            <el-option
                                v-for="item in provinces"
                                :key="item.value"
                                :label="item.label"
                                :value="item.value"
                            />
                        </el-select>
                        <span class="home-section-item-select-label">Provinces</span>

                        <el-select
                            v-model="city"
                            placeholder=""
                            size="large"
                        >
                            <el-option
                                v-for="item in citys"
                                :key="item.value"
                                :label="item.label"
                                :value="item.value"
                            />
                        </el-select>
                        <span class="home-section-item-select-label">City</span>
                    </div>
                </div>

                <!--Competitive vehicle models-->
                <div class="home-section-item">
                    <!-- <div class="flex align-center home-section-item-three"> -->
                        <div class="home-section-item-title home-section-item-three">Competitive vehicle models</div>
                        <el-input v-model="vehicleModel"  placeholder="Please input" />
                    <!-- </div> -->
                    
                </div>
            </div>
        </div>

        <div class="home-section home-section-two">

        </div>

        <div class="home-bottom">
            <div class="home-bottom-btn home-bottom-btn-reset">Reset</div>
            <div class="home-bottom-btn home-bottom-btn-confirm">Confirm</div>
        </div>
    </div>
</template>

<script setup>
import { ref } from 'vue';
import Radio from './radio.vue'
import api from '@/api/audio'

const RadioList = ref([
    { label: 'Male', value: 1},
    { label: 'Female', value: 2},
    { label: 'All', value: 2}
])
const sex = ref(1)
const vehicleModel = ref('')
const province = ref('')
const provinces = ref([])
const city = ref('')
const citys = ref([])


const getProvice = async () => {
    const res = await api.getProvinces()

    if(res?.length) {
        provinces.value = res;
    }
}
getProvice()

const getCity = async(province) => {
    
    const res = await api.getCitysBy(province)
    console.log(res, 'getCity ==== args', province)

    if(res?.length) {
        citys.value = res;
    }
}

</script>


<style>
.home .el-input{
    --el-input-text-color: #fff;
}
.home .el-select,
.home .el-select--large .el-select__wrapper {
    background: #44546A;
    width: 212px;
    border-radius: 9px;
    color: #fff;
    --el-input-text-color: #fff;
}
.home .el-select--large .el-select__wrapper {
    height: 36px;
}

.home .el-input__wrapper{
    width: 320px;
    height: 45px;
    background: #44546A;
}

</style>

<style lang="less" scoped>
.home {
    /* padding: 0 51px; */
    box-sizing: border-box;
}
.home-title{
    font-size: 24px;
    font-weight: bold;
    color: #fff;
    line-height: 34px;
}
.home-section {
    width: 100%;
    height: 257px;
    background: #44546A;
    color: #fff;
    font-size: 16px;
    padding: 27px 48px;
    box-sizing: border-box;
}
.home-section-two{
    margin: 30px 0 0 0;
    height: 503px;
}
.home-section-flex{
    display: flex;
    justify-content: space-around;
}
.home-section-item{
    flex: 1;
    &-center{
        flex: 2;
    }
}
.home-section-item-two,
.home-section-item-three{
    margin: 0 0 20px 0;
}
.home-section-item-three{
    
}
.home-section-item-select-label{
    padding: 0 20px;
    /* font-size: 14px; */
}
.home-section-item-title{
    white-space: nowrap;
}

.home-bottom{
    display: flex;
    justify-content: center;
    align-items: center;
    gap: 40px;
}
.home-bottom-btn{
    margin: 26px 0 0 0;
    display: flex;
    justify-content: center;
    align-items: center;
    width: 142px;
    height: 60px;
    border-radius: 10px;
    cursor: pointer;
    color: #fff;
    font-size: 18px;
    font-weight: bold;
}
.home-bottom-btn-reset{
    background: #F0803F;
}
.home-bottom-btn-confirm{
    background: #4472C4;
}
</style>