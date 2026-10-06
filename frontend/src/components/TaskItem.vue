<script setup>
/**
 * 单个任务条目：勾选完成 + 删除。
 * 纯展示组件：不碰 store，只通过 emit 向上抛事件。
 */
defineProps({
  /** @type {{ id: number, title: string, done: boolean }} */
  task: { type: Object, required: true },
})

const emit = defineEmits(['toggle', 'remove'])
</script>

<template>
  <li
    class="flex items-center gap-3 rounded-lg border border-slate-200 bg-white px-4 py-3 shadow-sm"
  >
    <input
      type="checkbox"
      :checked="task.done"
      class="h-5 w-5 accent-emerald-600"
      :aria-label="`切换完成：${task.title}`"
      @change="emit('toggle', task)"
    />
    <span
      class="flex-1 text-slate-800"
      :class="{ 'text-slate-400 line-through': task.done }"
    >
      {{ task.title }}
    </span>
    <button
      type="button"
      class="text-sm text-slate-400 transition hover:text-red-600"
      :aria-label="`删除：${task.title}`"
      @click="emit('remove', task.id)"
    >
      删除
    </button>
  </li>
</template>
