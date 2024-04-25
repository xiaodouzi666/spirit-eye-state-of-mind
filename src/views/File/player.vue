<template>
    <div class="player">
        <div class="player-title">This is the file name.mp4</div>
        <div class="player-process">
            <img class="player-process-img" src="@/assets/img/file-process-audio.png" />
            <div class="player-process-line" :style="{ left: `${left}%` }">
                <span class="player-process-line-time">{{ format(time) }}</span>
            </div>
            <div class="player-process-start">{{ format(time) }}</div>
            <div class="player-process-end">{{ format(total) }}</div>
        </div>
        <div class="player-control">
            <div class="player-control-left">
                <img class="player-control-left-icon" src="@/assets/img/icons/icon-play-loop.png" />
                <img class="player-control-left-icon" src="@/assets/img/icons/icon-play-jian.png" />
            </div>
            <div class="player-control-center">
                <div class="player-control-prev">
                    <img class="player-control-prev-icon" src="@/assets/img/icons/icon-play-prev.png"></img>
                    <img class="player-control-prev-icon" src="@/assets/img/icons/icon-play-prev.png"></img>
                </div>
                <div class="player-control-start flex" @click="() => handlePlay(false)" v-show="isPlay">
                    <div class="player-control-start-line"></div>
                    <div class="player-control-start-line"></div>
                </div>
                <img class="player-control-stop" v-show="!isPlay"
                src="@/assets/img/icons/icon-play-stop.png" @click="() => handlePlay(true)"></img>
                <div class="player-control-next">
                    <img class="player-control-next-icon" src="@/assets/img/icons/icon-play-next.png"></img>
                    <img class="player-control-next-icon" src="@/assets/img/icons/icon-play-next.png"></img>
                </div>
            </div>
            <div class="player-control-right">
                <img class="player-control-right-icon" src="@/assets/img/icons/icon-play-volume.png" />
                <div class="player-control-right-box pointer">
                    1x
                </div>
            </div>
        </div>
    </div>
</template>

<script setup>
import { ref, watch } from 'vue'
import { useAudioStore } from '@/store/audio';

const store = useAudioStore()

const left = ref(0)
const isPlay = ref(false)
const time = ref(0)
const timer = ref()
const total = ref(100)

const handlePlay = (bool) => {
    isPlay.value = bool
    store.setIsPlay(bool)
    if(!bool) {
        clearTimeout(timer.value)
    } else {
        currentTime()
    }
}



watch(time, (newVal) => {
    if(newVal > total.value) {
        stop()
    }
})

// 开始计时

const currentTime = () => {
        time.value += 1;

        if(time.value <= total.value) {
            left.value = Math.ceil((time.value / total.value) * 100)
        }

        timer.value = setTimeout(() => {
            // if(time.value >= total.value) {
            //     clearTimeout(timer.value)
            //     return;
            // }
            currentTime()
        }, 1000)
    
    
}

const stop = () => {
    time.value = 0;
    left.value = 0;
    handlePlay(false)
}

const format = (time) => {
    const min = `${Math.floor(time / 60)}`;
    const sec = `${time % 60}`
    return `${min.padStart(2, '0')}:${sec.padStart(2, '0')}`
}
</script>

<style lang="less" scoped>
.player{
    padding: 30px 40px;
    box-sizing: border-box;
    
    &-title{
        font-size: 24px;
        font-weight: bold;
        color: #fff;
    }

    &-process{
        position: relative;
        display: flex;
        align-items: center;
        height: 146px;
        border-left: 1px solid #E203A9;
        border-right: 1px solid #E203A9;
        margin: 50px 0 0 0;
        &-img{
            width: 1100px;
        }

        &-line{
            position: absolute;
            left: 0;
            top: -130px;
            width: 1px;
            height: 685px;
            background: #FF0000;
            &-time{
                position: absolute;
                left: 50%;
                top: 100px;
                transform: translateX(-50%);
                font-size: 14px;
            }
        }

        &-start{
            position: absolute;
            left: 0;
            bottom: -30px;
            transform: translateX(-50%);
            font-size: 14px;
        }
        &-end{
            position: absolute;
            right: 0;
            bottom: -30px;
            transform: translateX(50%);
            font-size: 14px;
        }
    }

    &-control{
        display: flex;
        margin: 100px 0 0 0;
        &-left,
        &-right,
        &-center{
            flex: 1;
        }

        &-left{
            display: flex;
            align-items: center;
            gap: 10px;

            &-icon{
                width: 39px;
                height: 36px;
                cursor: pointer;
            }
        }
        &-right{
            display: flex;
            align-items: center;
            justify-content: end;

            &-icon{
                width: 39px;
                height: 36px;
                
            }
            &-box{
                width: 58px;
                height: 36px;
                display: flex;
                align-items: center;
                justify-content: center;
                border-radius: 9px;
                font-size: 16px;
                color: #fff;
                border: 1px solid #fff;
            }
        }
        &-center{
            display: flex;
            align-items: center;
            gap: 150px;
        }

        &-prev{
            display: flex;
            align-items: center;
            cursor: pointer;
            &-icon{
                width: 26px;
                height: 22px;
            }
        }

        &-stop{
            // width: 52px;
            height: 44px;
            cursor: pointer;
        }
        &-start{
            width: 40px;
            height: 44px;
            align-items: center;
            justify-content: center;
            gap: 8px;
            cursor: pointer;
            &-line{
                width: 50%;
                height: 100%;
                border-radius: 10px;
                background: #fff;

            }
        }
        &-next{
            display: flex;
            align-items: center;
            cursor: pointer;
            &-icon{
                width: 26px;
                height: 22px;
            }
        }
    }
}
</style>