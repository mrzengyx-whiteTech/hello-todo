# 代码注释规范

> 适用范围：本项目全部源码。执行者：Linus 及所有 AI/人类协作者。

## 总则

- 注释解释「为什么」，不复述「是什么」；好命名优于好注释
- 魔法数字一律提取为常量，常量名自解释
- 删除代码好过注释代码：禁止保留注释掉的死代码（Git 有历史）

## JavaScript（前端，无 TypeScript）

- 导出函数、API 响应、非平凡逻辑**必须**写 JSDoc（`@param` / `@returns` / `@throws` 带类型），让 IDE 提供类型提示

```javascript
/**
 * 按状态筛选任务列表。
 * @param {Array<{id: number, title: string, done: boolean}>} tasks - 原始任务列表
 * @param {'all' | 'active' | 'done'} filter - 筛选条件
 * @returns {Array<{id: number, title: string, done: boolean}>} 筛选后的新数组，不改原列表
 */
export function filterTasks(tasks, filter) { /* ... */ }
```

## Python（后端）

- 公共函数 / 类**必须**有类型注解 + Google 风格 docstring（`Args` / `Returns` / `Raises`）

```python
def normalize_title(raw: str) -> str:
    """清洗任务标题。

    Args:
        raw: 用户原始输入。

    Returns:
        去除首尾空白后的标题。

    Raises:
        ValueError: 清洗后为空字符串时。
    """
```

## TODO / FIXME

- 必须带日期与责任方：`# TODO(2026-10-07, Linus): 接入鉴权后改为按用户过滤`
- 交付前清零：要么完成，要么转为 ADR / 交付报告的「遗留与建议」条目

## 什么时候必须写注释

- 违反直觉的写法（为什么不按常规做）
- 外部约束（第三方 API 的怪癖、浏览器兼容 hack）
- 业务规则（为什么是这个阈值/顺序/限制）
