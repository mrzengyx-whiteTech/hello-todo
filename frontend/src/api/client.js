import axios from 'axios'

/**
 * 全局 axios 实例：统一 baseURL 与错误处理入口。
 * 生产环境由 Caddy 同源反代 /api；开发环境由 Vite proxy 转发，故恒用相对路径。
 */
const client = axios.create({
  baseURL: '/',
  timeout: 10000,
})

client.interceptors.response.use(
  (response) => response,
  /**
   * 统一错误出口：把后端 detail 拍平成 Error.message，调用方只用 catch 一句。
   * @param {import('axios').AxiosError} error - axios 错误对象
   * @returns {Promise<never>} 永远 reject
   */
  (error) => {
    const message = error.response?.data?.detail ?? error.message ?? '网络异常'
    return Promise.reject(new Error(message))
  },
)

export default client
