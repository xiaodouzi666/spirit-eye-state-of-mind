<template>
    <div class="chat-container">

        <!--section-->
        <div class="chat-section" v-show="!isShowChatList">
            <img class="chat-section-bg" src="@/assets/bg2.gif" />
            <div class="chat-section-buttons">
                <img class="chat-section-button" @click="handleChat" src="@/assets/button.png" />
                <img class="chat-section-button" src="@/assets/setting.png" @click="showSetting = true"/>
            </div>
            <div class="chat-section-empty"></div>
            <div class="chat-section-footer">
                <img class="chat-section-footer-icon" src="@/assets/audio.png" @click="startRecord"/>
                <div class="chat-section-footer-input">
                    <input class="chat-section-footer-input2" v-model="problemText" placeholder="你今天的心情呢?" v-show="!isStartRecord" @keypress="handleSend"/>
                    <div class="chat-section-footer-audio" v-show="isStartRecord" @click="handleRecord">
                        {{ isRecording ? '结束' : '按住 倾诉' }}
                    </div>
                </div>
            </div>
        </div>

        <!--聊天-->
        <div class="dashboard-chat" v-show="isShowChatList">
            <div>
                <div class="fr dashboard-chat-back-btn" @click="handleBack">返回</div>
            </div>
            <div class="dashboard-chat-video">
                <div class="dashboard-chat-video-outer"></div>
                <video class="dashboard-chat-video-inner" :src="videoUrl" autoplay />
            </div>
            <div class="dashboard-chat-container-wrap" ref="chatContainerRef">
                <div class="dashboard-chat-container" style="margin-top: 10px;">

                    <div v-show="isShowTips" class="dashboard-chat-container-message-item dashboard-chat-container-message-item-reply">
                        <img class="chat-item-avatar" src="@/assets/avatar-man.png" />
                        <div class="chat-item-text-tips">
                            Hi，我的朋友！这周过的怎么样！
                        </div>
                    </div>

                    <div class="dashboard-chat-container-message" v-for="(message, index) in messages" :key="index">

                        <div v-show="message.role === TUTOR_ROLE_USER"
                            class="dashboard-chat-container-message-item fr dashboard-chat-container-message-item-self">
                            <!--文字-->
                            <div class="chat-item-text" v-show="!message.audio_file">{{ message.message }}</div>
                            <!--录音-->
                            <div class="chat-item-text chat-item-text-reply" v-show="message.audio_file" @click="() => playAudio(message, index)">
                                <div :class="['bg', current === index ? 'voicePlay': ''] "></div>
                            </div>
                            <img class="chat-item-avatar" src="@/assets/avatar-women.png" />
                        </div>

                        <div v-show="message.role === TUTOR_ROLE_TUTOR"
                            @click="() => playAudio(message, index)"
                            class="dashboard-chat-container-message-item fl dashboard-chat-container-message-item-reply">
                            <img class="chat-item-avatar" src="@/assets/avatar-man.png" />
                            <div class="chat-item-text chat-item-text-reply">
                                <div :class="['bg', current === index ? 'voicePlay': ''] " v-show="httpLoading !== index"></div>
                                <van-loading class="bg-loading" color="#fff" type="spinner" v-show="httpLoading === index"/>
                            </div>
                        </div>
                    </div>
                </div>
                <!-- <img class="dashboard-chat-scrollToBottom" v-show="isShowScrollToBottom" @click="handleScrollToBottom"/> -->
            </div>
            <div class="chat-section-footer">
                    <img class="chat-section-footer-icon" src="@/assets/audio.png" @click="startRecord"/>
                    <div class="chat-section-footer-input">
                        <input class="chat-section-footer-input2" ref="inputRef" v-model="problemText" placeholder="你今天的心情呢?" v-show="!isStartRecord" @keypress="handleSend"/>
                        <div class="chat-section-footer-audio" v-show="isStartRecord" @click="handleRecord">
                            {{ isRecording ? '结束' : '按住 倾诉' }}
                        </div>
                    </div>
                </div>
        </div>

        <!--音频-->
        <div id="aplayer">
            <audio ref="audioRef" :src="audioUrl" autoplay @loadeddata="handleAudioLoaded" @ended="handleAudioEnded"></audio>
        </div>
        <!--时间设置-->
        <Setting v-model="showSetting" v-show="showSetting"/>

        <!-- <form :action="API_URL_AUDIO" method="post" enctype="multipart/form-data">
            <input type="file" name="audio" />
            <input type="submit" value="Submit" ref="submitRef"/>
        </form> -->
    </div>
</template>

<script setup>
import { ref, watch, onMounted, nextTick } from 'vue'
import * as _ from 'lodash-es'
import { 
    TUTOR_ROLE_USER, 
    TUTOR_ROLE_TUTOR,
    API_URL_CHAT,
    API_URL_VIDEO,
    API_URL_AUDIO,
    IS_SHOW_CHATLIST,
    IS_SHOW_TIPS
} from '@/constants'

import Setting from './setting.vue'

// const submitRef = ref()
const showSetting = ref(false)
const httpLoading = ref(-1)
const isStartRecord = ref(false)
const mediaRecorder = ref()
const isShowTips = ref(localStorage.getItem(IS_SHOW_TIPS))
const isShowChatList = ref(localStorage.getItem(IS_SHOW_CHATLIST))
const audioRef = ref()
const isRecording = ref(false);
const audioChunks = ref([])
const videoUrl = ref('')
const audioUrl = ref('')
// const audioUrl = ref('https://minimax-algeng-chat-tts.oss-cn-wulanchabu.aliyuncs.com/audio%2Ftts-mp3-20240323051811-NJmGmBfB.mp3?Expires=1711257492&OSSAccessKeyId=LTAI5tGLnRTkBjLuYPjNcKQ8&Signature=hMnA4LOZ0bJtD69i4kk4%2FBCPd10%3D');
const chatContainerRef = ref()
const inputRef = ref()
const problem = ref(null)
const problemText = ref('')
const isShowScrollToBottom = ref(false)
const current = ref(0)
const messages = ref([])

// 显示隐藏
const showChatList = () => {
    isShowChatList.value = true;
    localStorage.setItem(IS_SHOW_CHATLIST, true)
}
const hiddenChatList = () => {
    isShowChatList.value = false;
    localStorage.removeItem(IS_SHOW_CHATLIST)
}

const showChatTips = () => {
    isShowTips.value = true
    localStorage.setItem(IS_SHOW_TIPS, true)
}
const hiddenChatTips = () => {
    isShowTips.value = false
    localStorage.removeItem(IS_SHOW_TIPS)
}

const handleRecord = () => {
    // 正在录音，停止录音
    if(isRecording.value) {
        
        console.log('停止录音')
        stopRecording()
        
    } else {
        console.log('开始录音')
        startRecording()
        
    }
    
}

const handleChat = () => {    
    showChatList()
    showChatTips()

    clearChatList()
}

// 清空消息列表
const clearChatList = () =>{
    messages.value = [];
}

const handleBack = () => {
    hiddenChatList()
    hiddenChatTips()
}

const startRecording = async () => {  
    try {
        
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


        mediaRecorder.value.onstop = () => {  
            console.log('关闭录音')
            // const blob = new Blob(audioChunks.value, { type: 'audio/ogg; codecs=opus' });  
            // audioBlob.value = blob;  
            // audioChunks.value = []; // 清空数组以便下次录音  
        }; 

    } catch (err) {  
        console.error('无法获取录音权限:', err);  
        ElMessage.error('无法获取录音权限！')
    }  
};  

const stopRecording = () => {
    
    if (mediaRecorder.value) {
        console.log('stopRecording--停止录音')
        mediaRecorder.value.stop();  
        isRecording.value = false;
        setTimeout(() => {
            getBlob(); 
        }, 0)
    }  
};  
    
const getBlob = () => {

    const blob = new Blob(audioChunks.value, { type: 'audio/ogg; codecs=opus' });  
    // const blob = new Blob(audioChunks.value, { type: 'audio/mpeg' });  
    // hasRecording.value = true;

    audioUrl.value = URL.createObjectURL(blob);
    postRecord(blob)

    audioChunks.value = []
};

// 提交音频
const postRecord = (blob) => {
    // submitRef.value.click()

    console.log('audioUrl.value', audioUrl.value)
    messages.value.push(
        {
            message: '',
            text: '',
            audio_file: audioUrl.value,
            role: TUTOR_ROLE_USER,
        },
        {
            message: '',
            text: '',
            audio_file: '',
            role: TUTOR_ROLE_TUTOR,
        }
    )
    audioUrl.value = ''
    
    current.value = messages.value.length - 1;
    httpLoading.value = messages.value.length - 1;

    showChatList()
    chatScrollBottom()

    const fd = new FormData()
    fd.append('files', blob, 'recording.ogg');

    fetch(API_URL_AUDIO, {
        method: 'POST',
        // headers: {
        //     // 'Content-Type': 'audio/ogg'
        //     'Content-Type': 'multipart/form-data'
        // },
        body: fd
    }).then(res => res.json()).then(res => {
        console.log('音频上传', res)
        handleMessages(res)
    })


}

// 播放音频
const playAudio = (message, index) => {
    // 暂停正在播放的音频
    if(current.value === index) {
        pauseAudio()
        return;
    }

    audioRef.value.play()
    current.value = index;
    audioUrl.value = message?.audio_file;

}

// 暂停音频
const pauseAudio = () => {
    audioRef.value.pause()
    current.value = -1
}

const handleAudioLoaded = () => {
    // current.value = index;
    httpLoading.value = -1
    console.log('播放开始')
}
const handleAudioEnded = () => {
    console.log('播放结束')
    current.value = -1
}

onMounted(async () => {
    const stream = await navigator.mediaDevices.getUserMedia({ audio: true });  
    mediaRecorder.value = new MediaRecorder(stream);

    isShowChatList.value = localStorage.getItem(IS_SHOW_CHATLIST)
})

const startRecord = () => {
    isStartRecord.value = !isStartRecord.value;
}
// 发送文字
const sendText  =(text) => {
    httpLoading.value = messages.value.length - 1;
    console.log('httpLoading.value', httpLoading.value)
    audioRef.value.pause()

    fetch(API_URL_CHAT, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ text: text || '你好，请给我介绍一下chatgpt'})
    }).then(res => res.json()).then(res => {
        if(res.text) {
            handleMessages(res)
        }
        
    }).finally(() => {
        httpLoading.value = -1
    })
}

// 获取视频
const getVideo = (text) => {
    
    fetch(API_URL_VIDEO, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ text: text || '你好，请给我介绍一下chatgpt'})
    }).then(res => res.json()).then(res => {
        if(res.video_url) {
            videoUrl.value = res.video_url
        }
    }).finally(() => {
        // httpLoading.value = -1
    })
}


const chatScrollBottom = () => {
    nextTick(() => {
        chatContainerRef.value?.scrollBy?.(0, 1000)
    })
}
const scrollIntoView = (elm) => {
    elm?.scrollIntoView?.(true)
}

const queryFirstMessagesElm = (len = 0) => {
    return document.querySelectorAll('.dashboard-chat-container-message')[len]
}


const handleMessages = (res) => {
    let len = messages.value.length - 1;
    // if(messages.value[len].role === TUTOR_ROLE_TUTOR) {
    //     messages.value[len].role = TUTOR_ROLE_TUTOR
    // }
    messages.value[len].text = res.text
    messages.value[len].message = res.text
    messages.value[len].audio_file = res.audio_file
    audioUrl.value = res.audio_file
    current.value = len

    chatScrollBottom()
    
}

watch(problem, (newVal) => {
    if(newVal) {
        problemText.value = newVal
    } 
    // else {
    //     inputRef.value.blur()
    // }
})

// const resetProbelm = () => {
//     problem.value = ''
//     problemText.value = ''
// }

// 回车键，发送文字给AI
const handleSend = async (e) => {
    if(e.which === 13) {
        e.preventDefault()

        messages.value.push(
            {
                role: TUTOR_ROLE_USER,
                message: problemText.value,
            },
            {
                role: TUTOR_ROLE_TUTOR,
                message: '',
            }
        )

        // 滚动到页面底部
        nextTick(() => {
            inputRef.value.blur()
            chatScrollBottom()
        })

        showChatList()
        getVideo(problemText.value)
        await sendText(problemText.value)
    }
}


const handleScrollToBottom = () => {
    scrollIntoView(queryFirstMessagesElm(messages.value.length - 1))
    isShowScrollToBottom.value = false
}
const handleLoadingMore = _.throttle(async (e, ...args) => {
    const scrollTop = chatContainerRef.value?.scrollTop;
    const scrollHeight = chatContainerRef.value?.scrollHeight;
    if(scrollTop <= 0) {
        // queryMessageList(pageNum.value + 1)
    }
    // const wrapElm = chatContainerRef.value;
    isShowScrollToBottom.value = (scrollHeight - scrollTop) > 550
}, 300)

</script>

<style>
.el-input__wrapper,
.el-input__wrapper:hover{
    --el-input-bg-color: #3A3A3C;
    box-shadow: none;
    --el-input-text-color: #fff;
    -webkit-tap-highlight-color: transparent; /* 去除点击高亮 */  
    -webkit-text-size-adjust: 100%;
 }
</style>
<style lang="less" scoped>
.loading-wrap{
    position: absolute;
    // left: 0;
    top: 0;
    z-index: 10;
    width: 375px;
    height: 100%;
    background: rgba(0,0,0,.5);
}
.loading{
    position: absolute;
    left: 50%;
    top: 50%;
    transform: translate(-50%, -50%);
}
.chat-item-text{
    padding: 15px;
    border-radius: 14px 0 14px 14px;
    background: #D0E0FE;
    box-shadow: 0px 10px 10px 0px rgba(0, 0, 0, 0.05);
    white-space: wrap;
    word-break: break-word;
    &-tips{
        padding: 10px;
        border-radius: 0 14px 14px 14px;
        background: #D8BBFF;
        box-shadow: 0px 10px 10px 0px rgba(0, 0, 0, 0.05);
        white-space: wrap;
        word-break: break-word;
        color: #2E3553;
    }
}
.chat-item-text-reply{
    position: relative;
    width: 100px;
    height: 4px;
    border-radius: 0 14px 14px 14px;
    background: #D8BBFF;
    margin: 5px 0 0 0;
    cursor: pointer;
}
.chat-item-avatar{
    width: 44px;
    height: 44px;
    border-radius: 50%;
}

.dashboard-chat-video{
    // overflow: hidden;
    position: relative;
    margin: 0 auto 0;
    &-outer{
        // position: absolute;
        // left: 50%;
        // top: 4px;
        // transform: translateX(-50%);
        margin-top: 4px;
        width: 320px;
        height: 180px;
        background: linear-gradient(3deg, #E1AFCC, #7530E3);
        border-radius: 10px;
        border: 1px solid #A091B0;
    }
    &-inner{
        position: absolute;
        left: calc(50% - 4px);
        top: 0px;
        transform: translateX(-50%);
        width: 320px;
        height: 180px;
        margin: auto;
        border-radius: 5px;
        // background: #000;
    }
}
.chat-container{
    width: 375px;
    height: 100%;
    margin: auto;
    background: url('@/assets/chat-bg.gif') right 0 no-repeat;
    background-size: 100%;
    .chat-section{
        position: fixed;
        top: 0;
        // left: 0;
        // right: 0;
        // bottom: 0;
        width: 375px;
        height: 100vh;
        background: #fff;
        display: flex;
        flex-direction: column;
        justify-content: space-between;
        &-bg {
            position: absolute;
            left: 0;
            top: 0;
            width: 375px;
            height: 100vh;
        }
        &-buttons{
            position: absolute;
            top: 437px;
            display: flex;
            justify-content: center;
            gap: 15px;
            width: 100%;
        }
        &-button{
            width: 73px;
            // height: 30px;
            cursor: pointer;
        }

        &-footer{
            display: flex;
            width: 375px;
            height: 68px;
            background: #D8BBFF;
            padding: 14px 20px;
            box-sizing: border-box;
            z-index: 2;
            // margin-bottom: 60px;
            &-icon{
                width: 25px;
                height: 25px;
                margin: 0 23px 0 0;
                cursor: pointer;
            }
            &-input{
                line-height: 0;
                width: 291px;
                height: 25px;
                border: 1px solid #220042;
                border-radius: 5px;
            }
            &-audio,
            &-input2{
                text-indent: 12px;
                width: 291px;
                height: 25px;
                line-height: 25px;
                background: #D8BBFF;
                border:none;
                font-size: 13px;
                color: #2C0159;
                border-radius: 5px;
            }
            &-audio{
                cursor: pointer;
                text-align: center;
            }
        }
    }
}

#aplayer {
    position: fixed;
    bottom: -100%;
    left: 0;
}
.dashboard-chat {
    width: 375px;
    height: 100vh;
    background: linear-gradient(180deg, rgba(184,143,255, .3), #fff);
    &-back-btn {
        width: 45px;
        height: 20px;
        line-height: 20px;
        text-align: center;
        // padding: 5px;
        border-radius: 5px;
        border: 1px solid #fff;
        font-size: 10px;
        color: #fff;
        margin: 8px 26px;
        cursor: pointer;
    }
}
.dashboard-chat .el-textarea__inner {
    background: #3a3a3c !important;
    font-size: 13px;
    height: 100px;
    resize: none !important;
    color: #fff !important;
}
.dashboard-chat .el-textarea__inner::placeholder{
    color: rgba(235, 235, 245, 0.30) !important;
    font-size: 13px;
}
.dashboard-chat .el-textarea__inner:focus,
.dashboard-chat .el-textarea__inner,
.dashboard-chat .el-textarea__inner:hover{
    box-shadow: none !important;
}

.dashboard-chat-container-wrap::-webkit-scrollbar{
    display: block;
    width: 3px;
    height: 3px;
    // background: #000;
}
.dashboard-chat-container-wrap::-webkit-scrollbar-thumb {
    display: block;
    width: 3px;
    height: 3px;
    // background: #aaa;
}

.dashboard-chat-scrollToBottom{
    position: absolute;
    bottom: 80px;
    right: 20px;
    width: 30px;
    height: 30px;
    background: #3a3a3c;
    border-radius: 50%;
    text-align: center;
    line-height: 30px;
    transform: rotate(90deg);
    cursor: pointer;
}

// 小喇叭样式
.voice{ 
  padding-top: 12px;
  padding-left: 10px;
  margin: 100px auto;
  height: 35px;
  width: 150px;
  background: #1bbc9b;
  border-radius: 0 7px 7px;
}

.bg {
    position: absolute;
    top: 50%;
    transform: translateY(-50%);
    background:url(data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAGAAAAAYCAYAAAAF6fiUAAAAGXRFWHRTb2Z0d2FyZQBBZG9iZSBJbWFnZVJlYWR5ccllPAAAAyZpVFh0WE1MOmNvbS5hZG9iZS54bXAAAAAAADw/eHBhY2tldCBiZWdpbj0i77u/IiBpZD0iVzVNME1wQ2VoaUh6cmVTek5UY3prYzlkIj8+IDx4OnhtcG1ldGEgeG1sbnM6eD0iYWRvYmU6bnM6bWV0YS8iIHg6eG1wdGs9IkFkb2JlIFhNUCBDb3JlIDUuNi1jMDY3IDc5LjE1Nzc0NywgMjAxNS8wMy8zMC0yMzo0MDo0MiAgICAgICAgIj4gPHJkZjpSREYgeG1sbnM6cmRmPSJodHRwOi8vd3d3LnczLm9yZy8xOTk5LzAyLzIyLXJkZi1zeW50YXgtbnMjIj4gPHJkZjpEZXNjcmlwdGlvbiByZGY6YWJvdXQ9IiIgeG1sbnM6eG1wTU09Imh0dHA6Ly9ucy5hZG9iZS5jb20veGFwLzEuMC9tbS8iIHhtbG5zOnN0UmVmPSJodHRwOi8vbnMuYWRvYmUuY29tL3hhcC8xLjAvc1R5cGUvUmVzb3VyY2VSZWYjIiB4bWxuczp4bXA9Imh0dHA6Ly9ucy5hZG9iZS5jb20veGFwLzEuMC8iIHhtcE1NOkRvY3VtZW50SUQ9InhtcC5kaWQ6NzlFRDZDRDNENzlFMTFFNkJDN0NFMjA2QTFFRTRDQkIiIHhtcE1NOkluc3RhbmNlSUQ9InhtcC5paWQ6NzlFRDZDRDJENzlFMTFFNkJDN0NFMjA2QTFFRTRDQkIiIHhtcDpDcmVhdG9yVG9vbD0iQWRvYmUgUGhvdG9zaG9wIENDIDIwMTcgKFdpbmRvd3MpIj4gPHhtcE1NOkRlcml2ZWRGcm9tIHN0UmVmOmluc3RhbmNlSUQ9InhtcC5paWQ6MTAxQkEzQ0RENzM2MTFFNjgyMEI5MTNDRkQ0OTM5QUEiIHN0UmVmOmRvY3VtZW50SUQ9InhtcC5kaWQ6MTAxQkEzQ0VENzM2MTFFNjgyMEI5MTNDRkQ0OTM5QUEiLz4gPC9yZGY6RGVzY3JpcHRpb24+IDwvcmRmOlJERj4gPC94OnhtcG1ldGE+IDw/eHBhY2tldCBlbmQ9InIiPz4K4iKVAAACUUlEQVR42uSazytEURTHvTHjR4kaU8xsSDZSdmbjx4oSK8XGQrJlpSwYTSmxEWWhUIpsZK3kD7DRNBuSBZFCNjZ+JPKcV6ecXu/d3sy7595bc+vbfXPue5/749z77o83lm3bZYYFC8RZqAbQAigP2tXNj5aZF7gdkAZNk9+7WvnOCCgxRUCb9n/o1sk3pUH6QDHF/GNsoM+QeYfiy6qkFeLZDBb0GlTB4AAR/xXT9nXxZVa0WCekQd9Y0HOJjg3CHySviiZmfjO3AyIhnu0gBc0wjAIR/wLtW8z87aAOWAI9gqaYRoAff4ZUoi7EKCiUP462j4CdSCrfK4N1Ahpi6I0i/hPa50M4oFB+Dbm/SzXfL5MD4rUogxP8+Itozynm59E+q5ovyuQdHxphWh568XvR5kxq1SEn40L4e0XMA1L4EcEe7RTjLqYdqRf/gezQUwr5LxjXq+aLHPCFcTmTA7z4tutIQhXfLiJPKXyRA/oxzgW8v9DgxU+S62eF/ATGr6r5fg26Corj9RHD4Z0fvwfjS9CbQn4bxrfK+R6TyzxZNk260solTL4i/g3al10TsMXIryA72T7VfK8MnJO8X9CKy14lafXjxx8jFUsSeyUzfxhtPwHPoqTy/TJJMJzJiPgNpJdsuNJizPwztB/q4JtwHN2KW3sn3HuMOouR30l6bbsOvgkOyGIBnaPbRldalJl/h2knuvgmOKAWNAFKMUz4Iv4O6Z1xXXxTPxtazHy6khnVyS/Fb8IDpHGyuvmWgX9L4Q4toDnQFWhNN/9PgAEAR4w1ULjdCbEAAAAASUVORK5CYII=) right 0 no-repeat;
    width: 13px;
    height: 13px;
    background-size: 400%;
}
.bg-loading{
    position: absolute;
    top: 50%;
    transform: translateY(-70%);
    width: 13px;
    height: 13px;
    background-size: 400%;
}

.voicePlay {
  animation-name: voicePlay;
  animation-duration: 1s;
  animation-direction: normal;
  animation-iteration-count: infinite;
  animation-timing-function: steps(3);
}

@keyframes voicePlay {
  0% {
    background-position: 0;
  }
  100% {
    background-position: 100%;
  }
}


html{
    overflow-x: hidden !important;
}


.flex{
    display: flex;
}
.center{
    justify-content: center;
    align-items: center;
}
.fr{
    float: right;
}
.fl{
    float: left;
}
.mr-12{
    margin-right: 12px;
}

.flex-default{
    align-items: center;
    justify-content: space-between;
}
.dashboard-chat-message-tip{
    display: flex;
    width: 261px;
    justify-content: center;
    align-items: center;
    gap: 10px;
    color: rgba(235, 235, 245, 0.30);
    text-align: center;
    font-size: 12px;
    line-height: 16px;
    margin: 20px auto 0;
}

.dashboard-layout-open{
    border-radius: 0 12px 12px 0 !important;
}
.dashboard-layout-chat{

}
.dashboard-chat{
    display: flex;
    flex-direction: column;
    width: 100%;
    /* padding: 0 16px; */
    box-sizing: border-box;
}
.dashboard-chat-header{
    position: relative;
    height: 44px;
    padding: 10px;
    justify-content: space-between;
    align-items: center;
    box-sizing: border-box;
}
.dashboard-chat-header-icon{
    width: 24px;
    height: 24px;
    cursor: pointer;
}
.dashboard-chat-header-record-other{
    display: flex;
    align-items: center;
}
.dashboard-chat-header-logo{
    width: 20px;
    height: 20px;
    margin: 0 8px 0 0;
}
.dashboard-chat-header-ts-icon{
    height: 9px;
}
.dashboard-chat-header-record{
    width: 100px;
    height: 40px;
    flex-shrink: 0;
    fill: #3A3A3C;
    color: #FFF;
    text-align: center;
    font-feature-settings: 'clig' off, 'liga' off;
    /* 中/脚注/标准 */
    font-size: 13px;
    line-height: 18px;
    padding: 5px 6px 5px 14px;
    box-sizing: border-box;
    background: #3A3A3C;
    border-radius: 20px;
    align-items: center;
}
.dashboard-chat-header-record-left-ing{
    color: rgba(235, 235, 245, 0.60);
    text-align: center;
    font-size: 9px;
    font-style: normal;
    line-height: 10px;
}
.dashboard-chat-header-record-close{

}
.dashboard-chat-header-operate{
    position: relative;
}
.dashboard-chat-problems{
    position: relative;
    /* width: 375px; */
    /* height: 644px; */
    box-sizing: border-box;
    border-radius: 12px;
    background: #1C1C1E;
    backdrop-filter: blur(27.5px);
}
.dashboard-chat-problems-wrapper{
    padding: 12px;
    box-sizing: border-box;
}
.dashboard-chat-problems-wrapper-tips{
    color: rgba(235, 235, 245, 0.60);
    font-size: 12px;
    line-height: 20px;
}
.dashboard-chat-problems-tips{
    position: relative;
    display: flex;
    width: 261px;
    height: 24px;
    padding: 4px 52px;
    justify-content: center;
    align-items: center;
    gap: 10px;
    margin: 20px auto 20px;
    box-sizing: border-box;
    background: #1C1C1E;

    color: rgba(235, 235, 245, 0.30);
    text-align: center;
    font-size: 12px;
    line-height: 16px;
}

.dashboard-chat-problems-tips-text{
    padding: 0 22px;
    background: #1C1C1E;
    position: relative;
    z-index: 2;
    left: 42% !important;
}
.dashboard-chat-problems-tips-line{
    position: absolute;
    width: 204px;
    height: 1px;
    background: rgba(235, 235, 245, 0.30);
}
.dashboard-chat-problems-welcome{
    color: rgba(235, 235, 245, 0.60);
    font-feature-settings: 'clig' off, 'liga' off;
    font-family: PingFang SC;
    font-size: 14px;
    font-style: normal;
    font-weight: 400;
    line-height: 22px;
    letter-spacing: -0.4px;
}
.dashboard-chat-problems-welcome-ts{
    color: #fff;
}

.dashboard-chat-problems-item{
    display: flex;
    align-items: center;
    width: 319px;
    height: 40px;
    flex-shrink: 0;
    border-radius: 8px;
    background: #2C2C2E;
    margin: 8px auto 0;
    cursor: pointer;
    border: 1px solid transparent;
}
.dashboard-chat-problems-item-active{
    border-color: rgba(129, 255, 0, 0.50);
    background: #2C2C2E;
}
.dashboard-chat-problems-item-icon{
    width: 24px;
    height: 24px;
    margin: 0 4px;
}
.dashboard-chat-problems-item-icon-other{
    box-sizing: border-box;
    padding: 0 5px;

}
.dashboard-chat-problems-item-text{
    color: #fff;
    font-family: PingFang SC;
    font-size: 14px;
    letter-spacing: -0.4px;
}
.dashboard-chat-container-wrap{
    /* height: 600px; */
    height: calc(100% - 60px);
    flex: 1;
    overflow-y: scroll;
}
.dashboard-chat-container{
    padding: 0 16px;
    box-sizing: border-box;
}
.dashboard-chat-container-message{
    /* position: relative; */
    overflow: hidden;
    // margin: 0 0 20px;
}
.dashboard-chat-container-message-item{
    color: rgba(255, 255, 255, 0.90);
    font-feature-settings: 'clig' off, 'liga' off;
    font-size: 14px;
    line-height: 22px;
}
.dashboard-chat-container-message-item-self{
    /* position: absolute;
    top: 0;
    right: 0; */
    display: inline-flex;
    padding: 12px;
    justify-content: flex-end;
    align-items: flex-start;
    gap: 10px;
    border-radius: 8px;
    // background: #E8FE93;
    color: #000;
    /* margin: 0 0 20px 0; */
}
.dashboard-chat-container-message-item-reply{
    display: inline-flex;
    gap: 10px;
    color: rgba(255, 255, 255, 0.90);
    font-size: 14px;
    line-height: 22px;
}
.dashboard-chat-container-message-item-loading{
    width: 100%;
    text-align: center;
    color: rgba(235, 235, 245, 0.30);
}
.dashboard-chat-footer{
    // position: absolute;
    // bottom: 0;
    // left: 50%;
    // transform: translateX(-50%);
    position: relative;
    z-index: 10;
    bottom: 60px;
    display: flex;
    width: 343px;
    justify-content: center;
    align-items: center;
    flex-shrink: 0;
    color: rgba(235, 235, 245, 0.30);
    font-feature-settings: 'clig' off, 'liga' off;
    font-size: 14px;
    line-height: 20px;
    letter-spacing: -0.4px;
    padding: 12px;
    border-radius: 8px;
    background: #3A3A3C;
    box-sizing: border-box;
    margin: 0 auto 16px;
    color: #fff;
}


.dashboard-home{
    width: 100%;
    position: relative;
}
.dashboard-home-header{
    justify-content: center;
    align-items: center;
    gap: 18px;
    margin: 70px auto 0;
    flex-direction: column;
}
.dashboard-home-header-logo{
    width: 90px;
    height: 90px;
}
.dashboard-home-header-icon{
    height: 18px;
}
.dashboard-home-header-name{
    color: rgba(235, 235, 245, 0.60);
    font-feature-settings: 'clig' off, 'liga' off;
    font-family: PingFang SC;
    font-size: 15px;
    line-height: 20px;
}
.dashboard-home-container{
    margin: 80px auto 0;
}
.dashboard-home-container-item{
    width: 327px;
    height: 64px;
    flex-shrink: 0;
    border-radius: 8px;
    background: #3A3A3C;

    align-items: center;
    justify-content: space-between;
    gap: 10px;
    cursor: pointer;

    color: #FFF;
    font-feature-settings: 'case' on;
    /* 中/内容/标准 */
    font-family: PingFang SC;
    font-size: 17px;
    font-style: normal;
    font-weight: 400;
    line-height: 22px;
    padding: 0 16px;
    box-sizing: border-box;
    margin: 0 auto 12px;
}
.dashboard-home-container-item-icon{
    width: 24px;
height: 24px;
flex-shrink: 0;
}
.dashboard-home-container-item-label{
    flex: 1;
}

.dashboard-library{
    position: absolute;
    right: 375px;
    top: 0;
    width: 874px;
    height: 644px;
    overflow-y: scroll;
    background: #000;
    border-radius: 12px 0 0 12px;
}
.dashboard-library-container-scroll{
    height: 600px;
    overflow-y: scroll;
}
.dashboard-library-header{
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    display: flex;
    align-items: center;
    justify-content: space-between;
    height: 44px;
    padding: 0 12px;
    box-sizing: border-box;
    color: #fff;
    background: #000;
    font-feature-settings: 'clig' off, 'liga' off;
    /* 中/内容标题/加粗 */
    font-family: PingFang SC;
    font-size: 17px;
    font-style: normal;
    font-weight: 600;
    line-height: 22px;
    letter-spacing: -0.4px;
}
.dashboard-library-header-icon{
    width: 24px;
    height: 24px;
    cursor: pointer;
}
.dashboard-library-container{
    margin: 44px 0 0 0;
}
.dashboard-library-container-list{
    display: flex;
    flex-wrap: wrap;
    gap: 20px 12px;
    margin: 0 0 0 12px;
}
.dashboard-library-container-item{
    display: flex;
    width: 275px;
    height: 225px;
    padding-right: 0.996px;
    flex-direction: column;
    justify-content: center;
    align-items: flex-start;
    gap: 8px;
    flex-shrink: 0;
    border-radius: 12px;
    overflow: hidden;
    cursor: pointer;
    img{
        width: 100%;
        height: 100%;
    }
}

.dashboard-gallery-container-image{
    float: left;
    background-size: cover;
    background-repeat: no-repeat;
    background-position: center center;
    border: 1px solid #ebebeb;
    margin: 5px;
}

.dashboard-gallery{
    position: fixed;
    /* top: 50%;
    left: 50%;
    transform: translate(-50%, -50%); */
    z-index: 10;
    top: 0;
    left: -233%;
    /* width: 1686px; */
    width: 1280px;
    height: 866px;
    flex-shrink: 0;
    border-radius: 12px;
    border: 0.5px solid #636366;
    background: #2C2C2E;
    box-shadow: 0px 4px 38px 4px rgba(0, 0, 0, 0.28);
}
.dashboard-gallery-panel{
    display: flex;
}
.dashboard-gallery-panel-list{
    width: 140px;
    height: 866px;
    /* height: 752px; */
    flex-shrink: 0;
    opacity: 0.7;
    background: #000;
    overflow-y: scroll;
    padding: 0 18px 40px;
    box-sizing: border-box;
}
.dashboard-gallery-panel-item{
    border-style: solid;
    border-width: 6px;
    border-color: transparent;
    border-radius: 4px;
    margin: 40px 0 0 0;
    overflow: hidden;
}
.dashboard-gallery-panel-item-active {
    border-color: #81FF00;
}
.dashboard-gallery-panel-item-img{
    width: 104px;
    height: 58px;
    border-radius: 4px;
    border: 1px solid #48484A;
}
.dashboard-gallery-panel-preview{
    flex: 1;
    overflow-y: scroll;
}
.dashboard-gallery-panel-preview-header{
    display: flex;
    align-items: center;
    justify-content: space-between;
    /* width: 1546px; */
    height: 42px;
    flex-shrink: 0;
    opacity: 0.7;
    background: #1C1C1E;
    padding: 0 16px;
    box-sizing: border-box;
}
.dashboard-gallery-panel-preview-header-icons{
    display: flex;
    align-items: center;
}
.dashboard-gallery-panel-preview-header-logo{
    width: 20px;
    height: 20px;
    flex-shrink: 0;
    border-radius: 4px;
    margin: 0 8px 0 0;
    cursor: pointer;
}
.dashboard-gallery-panel-preview-header-tutor{
    height: 9px;
    flex-shrink: 0;
}
.dashboard-gallery-panel-preview-header-close{
    width: 20px;
    height: 20px;
    flex-shrink: 0;
    cursor: pointer;
}
.dashboard-gallery-panel-preview-container{
    height: 824px;
    display: flex;
    justify-content: center;
    align-items: center;
    overflow-y: scroll;
    img{
        width: 100%;
        border-radius: 12px;
    }
}
.dashboard-gallery-panel-preview-header-right{
    width: 218px;
    display: flex;
    align-items: center;
}
.dashboard-gallery-panel-preview-header-right-line{
    width: 1px;
    height: 18px;
    margin: 0 16px 0 8px;
    background: #3A3A3C;
}
.dashboard-gallery-panel-preview-header-scale{
    margin: 0 16px 0 8px;
    color: #FFF;

    text-align: center;
    font-feature-settings: 'clig' off, 'liga' off;
    /* 中/脚注/标准 */
    font-family: PingFang SC;
    font-size: 13px;
    font-style: normal;
    font-weight: 400;
    line-height: 18px; /* 138.462% */
    letter-spacing: -0.4px;
}
</style>