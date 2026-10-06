<script setup>
import { onMounted, ref } from 'vue'

import TaskItem from '@/components/TaskItem.vue'
import { useTasksStore } from '@/stores/tasks'

const store = useTasksStore()
const newTitle = ref('')

/** 提交新增：空标题直接忽略（后端还有一道清洗兜底，双保险）。 */
async function submit() {
  const title = newTitle.value.trim()
  if (!title) return
  await store.add(title)
  // 只有成功（无错误）才清空输入，失败时保留用户输入避免重敲
  if (!store.lastError) newTitle.value = ''
}

onMounted(store.loadAll)
</script>

<template>
  <main class="mx-auto max-w-xl px-4 py-10">
    <h1 class="text-2xl font-bold text-slate-900">hello-todo</h1>
    <p class="mt-1 text-sm text-slate-500">一人公司演练项目 · 由数字员工 Linus 交付</p>

    <form class="mt-6 flex gap-2" @submit.prevent="submit">
      <input
        v-model="newTitle"
        type="text"
        maxlength="200"
        placeholder="要做点什么？"
        class="flex-1 rounded-lg border border-slate-300 px-4 py-2 outline-none focus:border-emerald-500"
      />
      <button
        type="submit"
        class="rounded-lg bg-emerald-600 px-5 py-2 font-medium text-white transition hover:bg-emerald-700"
      >
        添加
      </button>
    </form>

    <p v-if="store.lastError" class="mt-3 text-sm text-red-600">{{ store.lastError }}</p>

    <p v-if="store.loading" class="mt-8 text-center text-slate-400">加载中…</p>
    <p v-else-if="store.tasks.length === 0" class="mt-8 text-center text-slate-400">
      暂无任务，加一条试试
    </p>
    <ul v-else class="mt-6 space-y-2">
      <TaskItem
        v-for="task in store.tasks"
        :key="task.id"
        :task="task"
        @toggle="store.toggle"
        @remove="store.remove"
      />
    </ul>
  </main>
</template>
