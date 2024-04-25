import { defineStore } from 'pinia';

export const useAudioStore = defineStore('audioModel', {
	state: () => ({
        isPlay: false,
        audioEle: null,
        audioUrl: '',
        loaded: false,
    }),
	actions: {
        setAudioEle(elm) {
            this.audioEle = elm;
        },
        setAudioUrl(url) {
            this.audioUrl = url;
        },
        setIsPlay(bool) {
            this.isPlay = bool;
        },
        setLoaded(bool) {
            this.loaded = bool
        }
	}
});
