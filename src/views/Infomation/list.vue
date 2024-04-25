<template>
    <div class="audio-list flex">
        <div 
            v-for="(item, index) in list" :key="index"
            :class="['audio-item', isPlaying(index) ? 'audio-item-active' : '']">
        
            <div class="audio-item-title">Audio A</div>

            <div class="audio-item-container flex">
                <div class="audio-item-container-btn">
                    <Playbtn :playing="isPlaying(index)" @play="(isPlay) => handlePlay(isPlay, index)"></Playbtn>
                </div>

                <div class="audio-item-container-right">
                    <div class="audio-item-container-right-top flex" v-show="isPlaying(index)">
                        <img class="audio-item-container-right-top-1" draggable="false" src="@/assets/img/icons/icon-info-progress.png" />
                        <img class="audio-item-container-right-top-2" draggable="false" src="@/assets/img/icons/icon-info-progress2.png" />
                    </div>
                    <div class="audio-item-container-right-top flex" v-show="!isPlaying(index)">
                        <img class="audio-item-container-right-top-1" draggable="false" src="@/assets/img/icons/icon-info-progress-default.png" />
                        <img class="audio-item-container-right-top-2" draggable="false" src="@/assets/img/icons/icon-info-progress2-default.png" />
                    </div>

                    <div class="control flex">
                        <div class="control-line">
                            <div class="control-line-progress" :style="{width: `${progress}%`}"></div>
                            <div class="control-line-dot" :style="{left: `${progress}%`}"></div>
                        </div>
                        <div class="control-time">4:30</div>
                    </div>
                </div>

            </div>
        </div>
    </div>
</template>

<script setup>
import { ref, computed, onMounted , watch } from 'vue'
import Playbtn from './playbtn.vue'
import { useAudioStore } from '@/store/audio'

const store = useAudioStore();

const list = ref([1,2,3,4,5,6]);

const progress = ref(10);
const current = ref(0);


const isPlaying = computed(() => (index) => current.value === index);

const handlePlay = (isplay, index) => {
    if(!isplay) {
        stopPlaying()
    } else {
        //  store.setAudioUrl(list[index]?.file_path)
    }
    current.value = isplay ? index : -1;
}

const stopPlaying = () => {
    const audio = store.audioEle;
    if(audio) {
        audio.pause()
    }
}

const startPlay = () => {
    const audio = store.audioEle;
    if(audio) {
        audio.start()
    } 
}


watch(store, (newVal) => {
    if(newVal.loaded) {
        
    }
}, { deep: true })

onMounted(() => {
    const audioEle = store.audioEle;
    audioEle && audioEle?.pause?.()
})

</script>



<style lang="less" scoped>
.audio-list{
    width: 1226px;
    height: 300px;
    flex-wrap: wrap;
    justify-content: center;
    color: #fff;
    overflow-y: scroll;
    gap: 30px 30px;
    padding: 0 0 200px 0;
    margin: auto;
}
.audio-item{
    width: 587px;
    height: 200px;
    background:#44546A;
    padding: 10px 30px;
    box-sizing: border-box;
    &-title{
        font-size: 16px;
    }
    &-container{
        margin: 20px 0 0 0;
        &-btn{
            width: 60px;
            height: 60px;
            align-items: center;
            justify-content: center;
            background: #fff;
            border-radius: 50%;
            margin: 0 30px 0 0;
        }

        &-right{
            &-top{
                &-1{
                    width: 247px;
                    height: 57px;
                }
                &-2{
                    width: 123px;
                    height: 57px;
                }
            }
        }
    }
}

.audio-item-active{
    background: #4472C4;
}

.control{
    position: relative;
    align-items: center;
    gap: 20px;
    margin: 30px 0 0 0;
    &-line{
        width: 341px;
        height: 3px;
        background: #fff;

        &-dot{
            position: absolute;
            top: 50%;
            transform: translateY(-50%);
            width: 22px;
            height: 22px;
            border-radius: 50%;
            background: #F06473;
            cursor: pointer;
        }

        &-progress{
            position: absolute;
            top: 50%;
            left: 0;
            transform: translateY(-50%);
            height: 3px;
            background: #F06473;
        }
    }

    &-time{
        font-size: 14px;
        color: #fff;
    }
}
</style>