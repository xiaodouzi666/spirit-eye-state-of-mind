import { createApp } from 'vue';
import { createPinia } from 'pinia';
import * as ElementPlusIconsVue from '@element-plus/icons-vue';
import App from './App.vue';
import router from './router';
import { usePermissStore } from './store/permiss';
import 'element-plus/dist/index.css';
import ElementPlus from 'element-plus'
import './assets/css/icon.css';
import 'amfe-flexible';
import 'aplayer/dist/APlayer.min.css';
import 'vant/lib/index.css';
import * as Vant from 'vant';

import NoData from '@/components/table-nodata.vue'

const app = createApp(App);
app.use(ElementPlus)
app.use(createPinia());
app.use(router);
app.use(Vant);

// 注册elementplus图标
for (const [key, component] of Object.entries(ElementPlusIconsVue)) {
    app.component(key, component);
}
app.component('no-data', NoData)

// 自定义权限指令
const permiss = usePermissStore();
app.directive('permiss', {
    mounted(el, binding) {
        if (!permiss.key.includes(String(binding.value))) {
            el['hidden'] = true;
        }
    },
});

app.mount('#app');
