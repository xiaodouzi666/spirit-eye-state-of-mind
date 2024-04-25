<template>
    <div class="file">
        <div class="file-title">User Portrait Selection</div>
        <div class="content flex">
            <div class="content-left">
                <div class="content-left-top">
                    <Title>
                        <template #icon> <img src="@/assets/img/icons/icon-recentFile.png"/></template>
                        <template #title> Recent Files </template>
                    </Title>
                    <Table :list="RecentFiles" />
                </div>

                <div class="content-left-bottom">
                    <Title>
                        <template #icon> <img src="@/assets/img/icons/icon-runningfile.png"/></template>
                        <template #title> Running files </template>
                    </Title>
                    <div class="content-left-bottom-list">
                        <div :class="[
                            'content-left-bottom-item',
                            index === runningIndex ? 'content-left-bottom-item-active' : ''
                        ]"
                        v-for="(item, index) in runningList"
                        :key="index"
                        @click="() => handleRunning(index)"
                    >
                            <div class="content-left-bottom-item-label">{{ item.label }}</div>
                            <div class="content-left-bottom-item-audio">{{ item.type }}</div>
                            <el-popconfirm title="是否确定删除？" @confirm="() => handleDelete(index)">
                                <template #reference>
                                    <div class="content-left-bottom-item-delete">x</div>
                                </template>
                            </el-popconfirm>
                            
                        </div>
                    </div>
                </div>

            </div>
            <div class="content-right">
                <Title>
                    <template #icon> <img src="@/assets/img/icons/icon-fileprocessing.png"/></template>
                    <template #title> File processing </template>
                </Title>

                <div class="right-container">
                    <Player v-show="isShowPlaying"/>
                    <Upload v-show="!isShowPlaying"/>
                    <div class="content-right-buttons flex">
                        <el-upload action="#" :show-file-list="false" :auto-upload="false">
                            <div class="content-right-buttons-upload flex">
                                <img src="@/assets/img/icons/icon-upload-up.png"/>
                            </div>
                        </el-upload>
                        
                        <div :class="['content-right-buttons-record flex', isRecording ? 'record-active' : '']" @click="handleRecord">
                            <img src="@/assets/img/icons/icon-record.png"/>
                        </div>
                    </div>
                </div>

                <div class="content-right-footer flex">
                    <div class="content-right-footer-btn flex" @click="handleRemove">Remove</div>
                    <div class="content-right-footer-btn flex" @click="uploadRecording">Submit</div>
                </div>
            </div>
        </div>
    </div>
    <!-- <audio ref="audioElement" :src="audioUrl" @loadeddata="onAudioLoaded" controls></audio> -->
</template>

<script setup>
import Title from './title.vue';
import Table from './table.vue';
import Player from './player.vue';
import Upload from './upload.vue';
import { RecentFiles, RunningFiles } from './data';
import { ElMessage } from 'element-plus';
import { useAudioStore } from '@/store/audio'

import { ref, onMounted, onUnmounted } from 'vue';


const store = useAudioStore()
// =============== state ================

const audioElement = ref()
const audioRef = ref()
const audioUrl = ref('')

const runningList = ref(RunningFiles)

const runningIndex = ref(0);
const isRecording = ref(false);

const isShowPlaying = ref(true);
const hasRecording = ref(false);  
const mediaRecorder = ref(null);  
const audioChunks = ref([]);  

// =============== methods ===============

const handleRunning = (index) => {
    runningIndex.value = index;
}

const handleDelete = (index) => {
    runningList.value.splice(index, 1)
}
 
const handleRecord = () => {
    // 正在录音，停止录音
    if(isRecording.value) {
        // isRecording.value = false; //!isRecording.value
        console.log('停止录音')
        stopRecording()
        
    } else {
        console.log('开始录音')
        startRecording()
        // isRecording.value = true; //!isRecording.value
    }
    
}


const startRecording = async () => {  
    try {
        console.log('mediaRecorder.value.state--start', mediaRecorder.value.state)
        const stream = await navigator.mediaDevices.getUserMedia({ audio: true });  
        mediaRecorder.value = new MediaRecorder(stream);  
        
        const handleDataAvailable = (event) => {  
            if (event.data.size > 0) {  
                audioChunks.value.push(event.data);  
            }
        };  

        mediaRecorder.value.ondataavailable = handleDataAvailable;  
        mediaRecorder.value.start();
        isRecording.value = true;  
    } catch (err) {  
        console.error('无法获取录音权限:', err);  
        ElMessage.error('无法获取录音权限！')
    }  
};  

const stopRecording = () => {
    console.log('mediaRecorder.value.state--stop', mediaRecorder.value.state)
    if (mediaRecorder.value) {
        console.log('stopRecording--停止录音')
        mediaRecorder.value.stop();  
        isRecording.value = false;
        setTimeout(() => {
            getBlob(); 
        }, 0)
        
        console.log('mediaRecorder.value.state--stop--2', mediaRecorder.value.state)
    }  
};  
    
const getBlob = () => {

    const blob = new Blob(audioChunks.value, { type: 'audio/ogg; codecs=opus' });  
    hasRecording.value = true;
    audioUrl.value = URL.createObjectURL(blob);

    store.setAudioUrl(audioUrl.value)
    audioChunks.value = []

    // // 如果需要播放录音，可以创建一个audio元素并设置其src为blob URL  
    // const audioElement = document.createElement('audio');  
    // audioElement.src = URL.createObjectURL(blob);  
    // audioElement.load();
    // audioElement.onloadeddata = () => {
    //     console.log('录音加载完成')
    //     audioElement.play();
    // }
    
    // document.body.appendChild(audioElement)
};

// getAudioDuration
// const getAudioDuration = (audioUrl) => {
//     // 创建一个新的Audio对象  
//     const audio = new Audio(audioUrl);  
    
//     // 监听metadata loaded事件，该事件在音频元数据（包括时长）加载完成后触发  
//     audio.onloadedmetadata = function() {  
//         const duration = audio.duration; // 音频时长，以秒为单位  
//         console.log('音频时长:::duration::', duration);  
//     };  
        
//     // 加载音频文件  
//     audio.load();
// }
const playRecording = () => {  
    // if (!hasRecording.value) return;  

    const audio = audioElement.value;
    console.log('获取播放音频的时长', audio?.duration)
    audio.currentTime = 0; // 重置播放位置到开头  
    audio.play();  
};  

const onAudioLoaded = (...event) => {
    console.log(event, '加载完成，播放音频', mediaRecorder.value.state)
    playRecording()
}

const onAudioLoadedMeta = () => {
    setTimeout(() => {
        const audio = audioElement.value;
        console.log('audio.duration时长--metadata', audio.duration)
    }, 5000)
    
    // getAudioDuration(audioUrl.value)
}

// 上传音频
const uploadRecording = async () => {
    if (!hasRecording.value) {  
        ElMessage.error('请选择需要上传的文件！')
        return;  
    }  

    const formData = new FormData();  
    formData.append('audioFile', new Blob(audioChunks.value, { type: 'audio/ogg; codecs=opus' }), 'recording.ogg');  

    // 假设你使用axios作为HTTP客户端  
    try {  
        const response = await axios.post('/your-upload-endpoint', formData, {  
            headers: {  
                'Content-Type': 'multipart/form-data'  
            }  
        });  
        if (response.data.success) {  
            ElMessage.success('录音上传成功！');  
            // 清除录音数据  
            audioChunks.value = [];  
            hasRecording.value = false;  
        } else {  
            alert('录音上传失败：' + response.data.message);  
        }  
    } catch (error) {  
        console.error('录音上传出错:', error);  
    }  
}; 

// 删除音频
const handleRemove = () => {
    isShowPlaying.value = false;
    audioChunks.value = [];
    const audio = store.audioEle;
    if (audio && audio.paused === false) {  
        audio.pause();  
    }
}

// 在组件挂载时添加媒体设备变化的监听器，以便在权限变化时重新尝试录音  
onMounted(async () => {
    const stream = await navigator.mediaDevices.getUserMedia({ audio: true });  
    mediaRecorder.value = new MediaRecorder(stream);


    navigator.mediaDevices.addEventListener('devicechange', () => {  
        console.log('媒体设备已更改，可以尝试重新录音');  
    });  
});  

// 在组件卸载时移除监听器  
onUnmounted(() => {  
    navigator.mediaDevices.removeEventListener('devicechange', () => {});
    // 释放Blob URL占用的内存  
    URL.revokeObjectURL(audioUrl.value)  
});  

</script>

<style lang="less" scoped>
.file{
    color: #fff;
}

.flex{
    display: flex;
}
.record-active{
    border-color: #F06473 !important;
}
.content{
    &-left{
        width: 570px;
        margin: 0 28px 0 0;
        // &-top{
        //     height: 428px;
        //     overflow-y: scroll;
        // }
        // &-top::-webkit-scrollbar {
        //     width: 5px;
        //     height: 73px;
        // }
        // &-top::-webkit-scrollbar-thumb{
        //     background: #4472C4;
        //     border-radius: 5px;
        // }

        &-bottom{
            margin: 30px 0 0 0;

            &-list{
                height: 300px;
                overflow-y: scroll;
            }
            &-list::-webkit-scrollbar {
                width: 5px;
                height: 73px;
            }
            &-list::-webkit-scrollbar-thumb{
                background: #4472C4;
                border-radius: 5px;
            }
            &-item{
                display: flex;
                align-items: center;
                justify-content: space-between;
                font-size: 16px;
                height: 50px;
                cursor: pointer;
                padding: 0 40px 0 70px;

                &-label{
                    width: 185px;
                    box-sizing: border-box;
                    overflow: hidden;
                    text-overflow: ellipsis;
                    white-space: nowrap;
                }
                
                &-active{
                    background: #4472C4;
                }

                &-delete{
                    font-size: 26px;
                }
            }
        }
    }

    &-right{
        &-buttons{
            align-items: center;
            justify-content: center;
            gap: 30px;
            margin: 100px 0 0 0;

            &-upload{
                box-sizing: border-box;
                width: 65px;
                height: 65px;
                border-radius: 9px;
                background: #4472C4;
                cursor: pointer;
                align-items: center;
                justify-content: center;
                img{
                    width: 40px;
                    height: 40px;
                }
            }
            &-record{
                width: 65px;
                height: 65px;
                border-radius: 9px;
                border: 1px solid #fff;
                cursor: pointer;
                align-items: center;
                justify-content: center;
                box-sizing: border-box;
                img{
                    width: 46px;
                    height: 46px;
                }
            }
        }

        &-footer{
            justify-content: center;
            align-items: center;
            gap: 30px;
            &-btn{
                width: 142px;
                height: 60px;
                border-radius: 10px;
                justify-content: center;
                align-items: center;
                font-size: 18px;
                font-weight: bold;
                color: #fff;
                margin: 30px 0;
                cursor: pointer;
                &:first-child{
                    background: #F0803F;
                }
                &:last-child{
                    background: #4472C4;
                }
            }
            
        }
    }
}
.right-container{
    width: 1216px;
    height: 677px;
    background: #44546A;
}
</style>