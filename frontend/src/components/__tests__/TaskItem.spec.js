import { mount } from '@vue/test-utils'
import { describe, expect, it } from 'vitest'

import TaskItem from '@/components/TaskItem.vue'

const task = { id: 1, title: '写交付报告', done: false }

describe('TaskItem', () => {
  it('渲染任务标题', () => {
    const wrapper = mount(TaskItem, { props: { task } })
    expect(wrapper.text()).toContain('写交付报告')
  })

  it('勾选时向上抛 toggle 事件并携带任务', async () => {
    const wrapper = mount(TaskItem, { props: { task } })
    await wrapper.find('input[type="checkbox"]').setValue(true)
    expect(wrapper.emitted('toggle')).toHaveLength(1)
    expect(wrapper.emitted('toggle')[0]).toEqual([task])
  })

  it('点删除时向上抛 remove 事件并携带 id', async () => {
    const wrapper = mount(TaskItem, { props: { task } })
    await wrapper.find('button').trigger('click')
    expect(wrapper.emitted('remove')).toEqual([[1]])
  })
})
