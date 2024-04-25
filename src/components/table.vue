<template>  
    <el-table  
      :data="paginatedData"  
      style="width: 100%"  
    >  
      <el-table-column  
        prop="name"  
        label="Name"  
      ></el-table-column>  
      <el-table-column  
        prop="age"  
        label="Age"  
      ></el-table-column>  
      <!-- 添加更多列根据需要 -->  
    </el-table>  
    
    <el-pagination  
      @size-change="handleSizeChange"  
      @current-change="handleCurrentChange"  
      :current-page="currentPage"  
      :page-sizes="[10, 20, 30, 40]"  
      :page-size="pageSize"  
      layout="total, sizes, prev, pager, next, jumper"  
      :total="totalItems">  
    </el-pagination>  
  </template>  
    
<script setup> 
import { defineProps } from 'vue'

const props = defineProps({
    items: {  
        type: Array,  
        required: true  
    },  
    perPage: {  
        type: Number,  
        default: 10  
    }
})

const data = reactive({
    currentPage: 1,  
    pageSize: props.perPage,  
    totalItems: props.items.length  
})

const paginatedData = computed(() => {  
    const start = (data.currentPage - 1) * data.pageSize;  
    const end = data.currentPage * data.pageSize;  
    return props.items.slice(start, end);  
})

const handleSizeChange = (val) => {  
    data.pageSize = val;  
    data.currentPage = 1;  
}  

const handleCurrentChange = (val) => {  
    data.currentPage = val;  
}
  </script>