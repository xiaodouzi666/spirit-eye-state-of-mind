<template>
    <div class="sidebar">
        <div class="sidebar-header">
            <div class="sidebar-header-title">
                技能认定考试生成系统
                <div class="sidebar-header-title-en">
                    Professional Technical Level Recognition
                </div>
            </div>

            <div class="sidebar-header-user">
                <img class="sidebar-header-avatar" src="@/assets/img/img.jpg" />
                <div class="sidebar-header-name">系统管理员</div>
                <div class="sidebar-header-nickname">Mortimer</div>
            </div>
            
        </div>
        <el-menu
            class="sidebar-el-menu"
            :default-active="onRoutes"
            :collapse="sidebar.collapse"
            background-color="#2570FF"
            text-color="#bfcbd9"
            active-text-color="#2570FF"
            unique-opened
            router
        >
            <template v-for="item in items">
                <template v-if="item.subs">
                    <el-sub-menu :index="item.index" :key="item.index" v-permiss="item.permiss">
                        <template #title>
                            <el-icon>
                                <component :is="item.icon"></component>
                            </el-icon>
                            <span>{{ item.title }}</span>
                        </template>
                        <template v-for="subItem in item.subs">
                            <el-sub-menu
                                v-if="subItem.subs"
                                :index="subItem.index"
                                :key="subItem.index"
                                v-permiss="item.permiss"
                            >
                                <template #title>
                                    <div class="">{{ subItem.title }}</div>
                                </template>
                                <el-menu-item v-for="(threeItem, i) in subItem.subs" :key="i" :index="threeItem.index">
                                    {{ threeItem.title }}
                                </el-menu-item>
                            </el-sub-menu>
                            <el-menu-item v-else :index="subItem.index" v-permiss="item.permiss">
                                {{ subItem.title }}
                            </el-menu-item>
                        </template>
                    </el-sub-menu>
                </template>
                <template v-else>
                    <el-menu-item :index="item.index" :key="item.index" v-permiss="item.permiss">
                        <el-icon>
                            <component :is="item.icon"></component>
                        </el-icon>
                        <template #title>{{ item.title }}</template>
                    </el-menu-item>
                </template>
            </template>
        </el-menu>
    </div>
</template>

<script setup lang="ts">
import { computed } from 'vue';
import { useSidebarStore } from '../store/sidebar';
import { useRoute } from 'vue-router';

const items = [
    {
        icon: 'Calendar',
        index: '1',
        title: '待考信息',
        permiss: '2',
        subs: [
            {
                index: '/examine',
                title: '待考列表',
                permiss: '2',
            },
            {
                index: '/studentInfo',
                title: '考生信息',
                permiss: '2',
            },
        ],
    },
    {
        icon: 'Edit',
        index: '3',
        title: '考试管理',
        permiss: '4',
        subs: [
            {
                index: '/subject',
                title: '题库管理',
                permiss: '5',
            },
            {
                index: '/paper',
                title: '试卷管理',
                permiss: '6',
            },
            // {
            //     index: '4',
            //     title: '三级菜单',
            //     permiss: '7',
            //     subs: [
            //         {
            //             index: '/editor',
            //             title: '富文本编辑器',
            //             permiss: '8',
            //         },
            //         {
            //             index: '/markdown',
            //             title: 'markdown编辑器',
            //             permiss: '9',
            //         },
            //     ],
            // },
        ],
    },
    // {
    //     icon: 'Setting',
    //     index: '/icon',
    //     title: '自定义图标',
    //     permiss: '10',
    // },
    // {
    //     icon: 'PieChart',
    //     index: '/charts',
    //     title: 'schart图表',
    //     permiss: '11',
    // },
    // {
    //     icon: 'Warning',
    //     index: '/permission',
    //     title: '权限管理',
    //     permiss: '13',
    // },
    // {
    //     icon: 'CoffeeCup',
    //     index: '/donate',
    //     title: '支持作者',
    //     permiss: '14',
    // },
];

const route = useRoute();
const onRoutes = computed(() => {
    return route.path;
});

const sidebar = useSidebarStore();
</script>

<style scoped>
.sidebar {
    display: block;
    /* position: absolute; */
    /* left: 0;
    top: 70px;
    bottom: 0; */
    height: 100vh;
    overflow-y: scroll;
    width: 260px;
    /* height: 1080px; */
    background: #2570FF;
}
.sidebar::-webkit-scrollbar {
    width: 0;
}
.sidebar-el-menu:not(.el-menu--collapse) {
    width: 261px;
}
.sidebar > ul {
    /* height: 100%; */
}

.sidebar-header-title{
    margin: 5px;
    background: rgba(255,255,255,0.2);
    text-align: center;
    font-size: 20px;
    color: #fff;
    padding: 10px 0;
}
.sidebar-header-title-en{
    font-size: 12px;
}
.sidebar-header-user{
    margin: 0 90px;
    text-align: center;
}
.sidebar-header-avatar{
    width: 80px;
    height: 80px;
    border-radius: 50%;
    border: 1px solid #FFFFFF;
    margin: 60px 0 0 0;
}
.sidebar-header-name{
    /* width: 82px; */
    white-space: nowrap;
    height: 22px;
    font-size: 16px;
    font-family: PingFang SC, PingFang SC;
    font-weight: bold;
    color: #FFFFFF;
    line-height: 19px;
    -webkit-background-clip: text;
    margin: 10px auto;
    /* -webkit-text-fill-color: transparent; */
}
.sidebar-header-nickname{
    /* width: 70px; */
    height: 22px;
    font-size: 16px;
    font-family: PingFang SC, PingFang SC;
    font-weight: 500;
    color: rgba(255,255,255,0.5);
    line-height: 19px;
    -webkit-background-clip: text;
    /* -webkit-text-fill-color: transparent; */
}
</style>
