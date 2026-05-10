# Drafts

把想发布的文章放到这里,Claude 负责搬运到正式目录、补 frontmatter、构建发布。

## 目录约定

- `drafts/en/` — 英文文章
- `drafts/zh-cn/` — 中文文章

## 文件命名

任意 `.md` 文件名都行,建议用 slug 风格(短横线分隔、英文小写),例如:

- `claude-4-7-launch-notes.md`
- `agent-sdk-first-look.md`

文件名最终会成为 URL 的一部分(`dosmoon.com/news/<slug>/`)。

## 最简文章模板

```markdown
---
title: 文章标题
description: 一句话摘要,会出现在站点 SEO 和卡片预览。
---

正文从这里开始。
```

只要 `title` + `description` 即可,其它 frontmatter(发布日期、作者、标签)Starlight 当前模板都不内置渲染,先省略。

## 发布流程

1. 你把文章 `.md` 文件丢进对应语言子目录
2. 告诉 Claude "发布草稿"(或直接说哪一篇)
3. Claude 把文件搬到 `src/content/docs/news/` 或 `src/content/docs/zh-cn/news/`、commit、push,GitHub Actions 自动部署到 `dosmoon.com/news/<slug>/`

## 注意

- 此目录在 `src/content/docs/` 之外,Astro **不会**自动发布草稿
- 但目录会被 git 追踪,草稿历史保留在 repo 里
