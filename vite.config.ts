import { defineConfig } from 'vite';
import path from "path";
import vue from '@vitejs/plugin-vue';
import VueSetupExtend from 'vite-plugin-vue-setup-extend';
import AutoImport from 'unplugin-auto-import/vite';
import Components from 'unplugin-vue-components/vite';
import { ElementPlusResolver } from 'unplugin-vue-components/resolvers';

import postcssPxtorem from 'postcss-pxtorem';  

export default defineConfig({
	base: './',
	plugins: [
		vue(),
		VueSetupExtend(),
		AutoImport({
			resolvers: [ElementPlusResolver()]
		}),
		Components({
			resolvers: [ElementPlusResolver()]
		})
	],
	resolve: {
		alias: {
		  "@": path.resolve(__dirname, "./src"),
		},
	  },
	// server: {
	// 	host: 'localhost',
	// },
	// optimizeDeps: {
	// 	include: ['schart.js']
	// },
	css: {  
		// postcss: {  
		//   plugins: [  
		// 	postcssPxtorem({  
		// 	  rootValue: 37.5, // 设计稿宽度 / 10，例如 1920 / 10 = 192，但通常使用37.5作为基准字体大小  
		// 	  propList: ['*'], // 需要转换的属性，'*' 表示所有属性  
		// 	  minPixelValue: 2, // 小于指定值的像素单位将不被转换
		// 	  exclude: /node_modules/i
		// 	})  
		//   ]  
		// }  
	  }  
});
