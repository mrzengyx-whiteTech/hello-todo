import { defineStore } from 'pinia'
import { ref } from 'vue'

import { createTask, deleteTask, fetchTasks, updateTask } from '@/api/tasks'

/**
 * 任务列表 store：视图的单一数据源，所有 API 调用收口在这里。
 */
export const useTasksStore = defineStore('tasks', () => {
  /** @type {import('vue').Ref<Array<import('@/api/tasks').Task>>} */
  const tasks = ref([])
  const loading = ref(false)
  /** @type {import('vue').Ref<string | null>} 最近一次操作失败信息，供页面 toast 展示 */
  const lastError = ref(null)

  /** 拉取全部任务。 */
  async function loadAll() {
    loading.value = true
    lastError.value = null
    try {
      tasks.value = await fetchTasks()
    } catch (err) {
      lastError.value = err.message
    } finally {
      loading.value = false
    }
  }

  /**
   * 新增任务（成功后头插，避免整表刷新）。
   * @param {string} title - 任务标题
   */
  async function add(title) {
    lastError.value = null
    try {
      const created = await createTask(title)
      tasks.value.unshift(created)
    } catch (err) {
      lastError.value = err.message
    }
  }

  /**
   * 勾选/取消完成（乐观更新失败则回滚：本地状态必须与服务端一致）。
   * @param {import('@/api/tasks').Task} task - 目标任务
   */
  async function toggle(task) {
    const prev = task.done
    task.done = !prev
    lastError.value = null
    try {
      await updateTask(task.id, { done: task.done })
    } catch (err) {
      task.done = prev
      lastError.value = err.message
    }
  }

  /**
   * 删除任务。
   * @param {number} id - 任务 ID
   */
  async function remove(id) {
    lastError.value = null
    try {
      await deleteTask(id)
      tasks.value = tasks.value.filter((t) => t.id !== id)
    } catch (err) {
      lastError.value = err.message
    }
  }

  return { tasks, loading, lastError, loadAll, add, toggle, remove }
})
