<template>
    <div class="radar" id="radar"></div>
</template>

<script setup>
import { onMounted, nextTick } from 'vue';
import * as echarts from 'echarts';

const dataBJ = [

  [234, 185, 230, 4.09, 123, 69, 27],
  
];
const lineStyle = {
  width: 1,
  opacity: 0.5
};
const option = {
  backgroundColor: '#44546A',
  radar: {
    indicator: [
      { name: 'Tonality', max: 300 },
      { name: 'Loudness', max: 350 },
      { name: 'Roughess', max: 300 },
      { name: 'Fluctuation strength', max: 5 },
      { name: 'Articulation Index', max: 200 },
      { name: 'Sharphess', max: 100 }
    ],
    shape: 'circle',
    splitNumber: 5,
    axisName: {
      color: '#fff'
    },
    splitLine: {
      lineStyle: {
        color: [
          '#fff',
          '#fff',
          '#fff',
          '#fff',
          '#fff',
          '#fff'
        ].reverse()
      }
    },
    splitArea: {
      show: false
    },
    axisLine: {
      lineStyle: {
        color: '#fff'
      }
    }
  },
  series: [
    {
      name: 'Beijing',
      type: 'radar',
      lineStyle: lineStyle,
      data: dataBJ,
      symbol: 'none',
      itemStyle: {
        color: '#fff'
      },
      areaStyle: {
        opacity: 0.5,
        color: '#4472C4'
      }
    }
  ]
};

onMounted(() => {
    nextTick(() => {
      var chartDom = document.querySelector('#radar');
      var myChart = echarts.init(chartDom);

      option && myChart.setOption(option);
    })
})


</script>

<style scoped lang="less">
#radar{
    width: 580px;
    height: 360px;
}
</style>