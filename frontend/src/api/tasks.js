import client from './client'

/**
 * @typedef {Object} Task
 * @property {number} id - 任务 ID
 * @property {string} title - 任务标题（后端已去首尾空白）
 * @property {boolean} done - 完成状态
 * @property {string} created_at - 创建时间（ISO 字符串）
 */

/**
 * 获取全部任务（创建时间倒序）。
 * @returns {Promise<Array<Task>>} 任务列表
 */
export function fetchTasks() {
  return client.get('/api/tasks').then((res) => res.data)
}

/**
 * 新增任务。
 * @param {string} title - 任务标题
 * @returns {Promise<Task>} 创建后的任务
 */
export function createTask(title) {
  return client.post('/api/tasks', { title }).then((res) => res.data)
}

/**
 * 部分更新任务。
 * @param {number} id - 任务 ID
 * @param {{ title?: string, done?: boolean }} payload - 待更新字段
 * @returns {Promise<Task>} 更新后的任务
 */
export function updateTask(id, payload) {
  return client.patch(`/api/tasks/${id}`, payload).then((res) => res.data)
}

/**
 * 删除任务。
 * @param {number} id - 任务 ID
 * @returns {Promise<void>}
 */
export function deleteTask(id) {
  return client.delete(`/api/tasks/${id}`).then(() => undefined)
}
