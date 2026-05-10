# Drafts

`drafts/` 是**发件箱**,只放还没发布的文章。已发布的从这里删掉,历史去 git 里查。

## 工作流

1. **你写中文** → 放进 `drafts/zh-cn/<slug>.md`(只要 frontmatter 不写也行,Claude 会补)
2. **Claude 翻译英文** → 生成 `drafts/en/<slug>.md`,等你审稿
3. **你审完点头** → Claude 把两边 publish 到 `src/content/docs/news/` 和 `src/content/docs/zh-cn/news/`,删掉 `drafts/` 里的两份副本,commit & push,GitHub Actions 自动部署到 `dosmoon.com/news/<slug>/`

## 文件命名

`.md` 文件名是 URL 的一部分(`dosmoon.com/news/<slug>/`),用短横线分隔的英文小写 slug:

- `claude-4-7-launch-notes.md`
- `agent-sdk-first-look.md`

中英文用同一个 slug,这样两边 URL 对齐。

## 最简文章模板(可选)

```markdown
---
title: 文章标题
description: 一句话摘要,出现在 SEO 与卡片预览中。
---

正文从这里开始。
```

只要 `title` + `description`。Starlight 当前模板不渲染发布日期、作者、标签,这些字段先省。
原稿写不写 frontmatter 都行——publish 时 Claude 会去掉源 H1、补上正确的 frontmatter。

## 注意

- `drafts/` 在 `src/content/docs/` 之外,Astro **不会**自动发布
- 已发布即删除——`drafts/` 里能看到的就是"还在路上的"
- 想看作者原稿,`git log` / `git show` 永远在
