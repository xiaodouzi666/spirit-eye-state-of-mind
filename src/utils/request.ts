import axios from 'axios';
import { ElMessage } from 'element-plus';
import storageUtils from '@/utils/localStorage';

const baseUrl = import.meta.env.VITE_BASE_URL;
// 创建一个axios实例
const service = axios.create({
  baseURL: baseUrl, // url =基本url +请求url
  // 凭据:true，当跨域请求时发送cookie
  timeout: 10000 // 对超时
})

// 请求拦截器
service.interceptors.request.use(
  config => {
    return config
  },
  error => {
    // 处理请求错误
    ElMessage.error(error.message);
    return Promise.reject(error)
  }
)

// 响应拦截器
service.interceptors.response.use(
  response => {
    const { status, data } = response;
    if (![200, 201].includes(status)) {
      ElMessage.error(status + '');
      return response.data;
    }

    return response.data
  },
)

export default service

