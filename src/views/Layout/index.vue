<template>
	<div class="layout">
		<Header />
		<div class="container">
			<router-view />
		</div>

		<!--播放器-->
		<audio class="audio"ref="audioElement" :src="audioUrl" @loadeddata="onAudioLoaded" controls></audio>
		<!-- <audio controls src="https://cn-south-17-aplayer-46154810.oss.dogecdn.com/hikarunara.mp3" ref="mmPlayer"></audio> -->
	</div>
	
</template>
<script setup lang="ts">
import { ref, onMounted, watch } from 'vue';
import { useAudioStore } from '@/store/audio';
import Header from './header.vue';

const store = useAudioStore()

const audioElement = ref()
const audioUrl = ref()
const mediaRecorder = ref()

watch(store, (newVal) => {
	if(newVal.audioUrl) {
		audioUrl.value = newVal.audioUrl
	}

	if(newVal.isPlay) {
		playRecording()
	} else {
		const audio = store.audioEle;
		if (audio && audio.paused === false) {  
			audio.pause();  
     	}
	}
}, { deep: true})

const playRecording = () => {  

    const audio = store.audioEle;
    // audio.currentTime = 0; // 重置播放位置到开头  
    audio.play();  
};  

const onAudioLoaded = (...event) => {
    // playRecording()
	store.setLoaded(true)
}

onMounted(() => {
	store.setAudioEle(document.querySelector('audio'))
})
</script>

<style lang="less" scoped>
.layout {
	width: 1920px;
	background: #000;
	height: 100vh;
	overflow-y: scroll;
	padding: 20px 50px;
}
.container{
	height: 100%;
	background: #000;
	border: none;
	padding: 80px 0 0 0;
	// overflow-y: scroll;
}

.audio{
	position: fixed;
	left: 0;
	bottom: -1000%;

}
</style>
