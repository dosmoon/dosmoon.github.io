# dosmoon 多项目文档体系方案

## 架构

```
dosmoon/                                  GitHub 组织
├── .github                  组织名片仓库  → 渲染在 github.com/dosmoon
├── dosmoon.github.io        组织门户站   → https://dosmoon.com/
├── project-a                项目 A      → https://dosmoon.com/project-a/
├── project-b                项目 B      → https://dosmoon.com/project-b/
└── ...
```

**两套系统,各管一摊**:

- **`.github` 仓库**:GitHub 站内展示。访问 `github.com/dosmoon` 时看到的组织名片
- **`dosmoon.github.io` 仓库**:对外门户站。承载首页、项目列表、研究笔记
- **项目仓库**:每个项目独立的文档站,通过仓库内的 `site/` 目录构建发布

`.github` 的唯一职责是**把 GitHub 站内访问者引流到门户站**。

## 技术栈

- **框架**:Astro 6 + Starlight 0.39+
- **包管理**:pnpm 9(**不用 10**,见"已知陷阱"章节)
- **部署**:GitHub Actions(`withastro/action@v6`)
- **Node**:22
- **域名**:`dosmoon.com`(已绑定到 `dosmoon.github.io`,DNS 在 Cloudflare)

## 一、`.github` 仓库

仓库名必须是 `.github`(带点),Public。

### 目录结构

```
.github/
└── profile/
    └── README.md          会渲染在 github.com/dosmoon 主页顶部
```

路径必须是 `profile/README.md`,GitHub 约定。

### profile/README.md 模板

```markdown
# dosmoon

> AI Coding 工作室

[![Portal](https://img.shields.io/badge/🏠_工作室门户-访问-blue?style=for-the-badge)](https://dosmoon.com/)
[![Research](https://img.shields.io/badge/🔬_研究笔记-阅读-green?style=for-the-badge)](https://dosmoon.com/research/)

简短介绍(2-3 行)。

## 🚀 项目

- [project-a](https://github.com/dosmoon/project-a) — 一句话描述 · [📖 文档](https://dosmoon.com/project-a/)
- [project-b](https://github.com/dosmoon/project-b) — 一句话描述 · [📖 文档](https://dosmoon.com/project-b/)

## 📚 资源

- 🌐 [工作室门户](https://dosmoon.com/)
- 🔬 [研究笔记](https://dosmoon.com/research/)
```

> 措辞注意:dosmoon 同时托管开源与闭源项目,文案避免"开源集合"这类表述。

### 组织 Settings 配套配置

`Settings → Profile`:
- **URL** 填 `https://dosmoon.com/`(组织主页右上角会出现 🔗 链接)
- 头像、Display name、Description 按需填

组织主页 → **Customize your pins**:
- Pin `dosmoon.github.io` 仓库
- Pin 5 个核心项目仓库(组织 pin 上限 6 个)

## 二、`dosmoon.github.io` 仓库(门户站)

> 当前仓库已存在临时 landing page(commit 33a9730),Starlight 骨架将整体替换之。

### astro.config.mjs

```javascript
import { defineConfig } from 'astro/config';
import starlight from '@astrojs/starlight';

export default defineConfig({
  site: 'https://dosmoon.com',
  // 不设 base
  integrations: [
    starlight({
      title: 'dosmoon',
      social: [
        { icon: 'github', label: 'GitHub', href: 'https://github.com/dosmoon' },
      ],
    }),
  ],
});
```

### .github/workflows/deploy.yml

```yaml
name: Deploy

on:
  push:
    branches: [main]
  workflow_dispatch:

permissions:
  contents: read
  pages: write
  id-token: write

concurrency:
  group: pages
  cancel-in-progress: false

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v6
        with:
          fetch-depth: 0
      - uses: withastro/action@v6
        with:
          node-version: 22
          package-manager: pnpm@9    # 钉 v9,详见"已知陷阱"

  deploy:
    needs: build
    runs-on: ubuntu-latest
    environment:
      name: github-pages
      url: ${{ steps.deployment.outputs.page_url }}
    steps:
      - uses: actions/deploy-pages@v4
        id: deployment
```

仓库 Settings → Pages → Source 选 **GitHub Actions**。

## 三、项目仓库

### 目录结构

```
project-a/
├── src/                         项目源码
├── docs/                        项目文档源(分公开与内部两区)
│   ├── public/                  对外发布:API、架构、用户指南、CHANGELOG
│   └── private/                 仅内部:开发草案、设计讨论、TODO
├── site/                        文档站构建产物源(本方案管辖)
│   ├── astro.config.mjs
│   ├── package.json
│   ├── scripts/
│   │   └── sync-docs.mjs        构建前把 docs/public/** 同步进 content/docs/
│   └── src/content/docs/        Starlight 内容(自动生成,纳入 .gitignore)
└── .github/workflows/
    └── deploy-site.yml          文档站部署
```

### docs/ 公开/内部双区设计

**为什么分两区**:开发期的草稿、设计讨论(像本文档自身)不适合对外,但需要随项目代码一起版本化。物理目录隔离比 frontmatter 标记更安全 —— 不会因为漏写一个 `draft: true` 就误发布。

**约定**:
- `docs/public/` 树结构 = 站点导航结构(Starlight 按目录自动生成 sidebar)
- `docs/private/` 不进入构建,但跟随仓库提交,GitHub 网页上可读
- `site/src/content/docs/` 是**构建产物**,纳入 `.gitignore`,只由 `sync-docs.mjs` 写入

**sync-docs.mjs 行为**:
1. 清空 `site/src/content/docs/`
2. 把 `docs/public/**` 复制进去(保留目录结构)
3. 在 `site` 的 `package.json` 里 `"prebuild": "node scripts/sync-docs.mjs"`,自动在 `astro build` 前执行

### site/astro.config.mjs

```javascript
import { defineConfig } from 'astro/config';
import starlight from '@astrojs/starlight';

export default defineConfig({
  site: 'https://dosmoon.com',
  base: '/<REPO>',                    // 必填,与仓库名一致
  integrations: [
    starlight({
      title: '<PROJECT_NAME>',
      social: [
        { icon: 'github', label: 'GitHub', href: 'https://github.com/dosmoon/<REPO>' },
      ],
      editLink: {
        // 注意指向 docs/public/ 而非 site/,因为编辑者改的是源
        baseUrl: 'https://github.com/dosmoon/<REPO>/edit/main/docs/public/',
      },
      lastUpdated: true,
    }),
  ],
});
```

### .github/workflows/deploy-site.yml

```yaml
name: Deploy Site

on:
  push:
    branches: [main]
    paths:
      - 'docs/public/**'
      - 'site/**'
      - '.github/workflows/deploy-site.yml'
  workflow_dispatch:

permissions:
  contents: read
  pages: write
  id-token: write

concurrency:
  group: pages
  cancel-in-progress: false

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v6
        with:
          fetch-depth: 0
      - uses: withastro/action@v6
        with:
          path: ./site
          node-version: 22
          package-manager: pnpm@9    # 钉 v9,详见"已知陷阱"

  deploy:
    needs: build
    runs-on: ubuntu-latest
    environment:
      name: github-pages
      url: ${{ steps.deployment.outputs.page_url }}
    steps:
      - uses: actions/deploy-pages@v4
        id: deployment
```

注意 `paths` 触发条件包含 `docs/public/**`,确保只改文档也能触发部署。

### 仓库 About 配置

仓库主页右上角 About → ⚙️:
- **Website** 填 `https://dosmoon.com/<REPO>/`
- ☑️ 勾选 **Use your GitHub Pages website**

### 内容编写指南(项目仓的 Claude Code 看这一节就够)

> 本节是面向**任何要往项目仓 `docs/public/` 里加内容的人**(包括 aistack 自己仓里的 Claude Code session)的操作手册。规范层面的"为什么这么设计"已经在前面章节讲过,本节只讲怎么用。

#### 发布机制(必须先理解的一条)

`docs/public/` 是**唯一的发布源**。任何想出现在 `https://dosmoon.com/<REPO>/` 的内容,必须放在这里。`docs/public/` 之外的所有路径(包括项目仓里现存的 `docs/api/`、`docs/design/`、`docs/research-note/` 等)**不会被发布**,但跟随仓库提交,GitHub 网页可读。

要把现有内容发出去:`git mv docs/api docs/public/api`,git 会识别为重命名,blame 历史保留。一次搬一个目录或一个文件,每次 commit 单独评审,避免一锅端把不该公开的内容也带进去。

#### 文件结构与 URL 映射

```
docs/public/index.md              → /<REPO>/
docs/public/configuration.md      → /<REPO>/configuration/
docs/public/api/index.md          → /<REPO>/api/
docs/public/api/asr.md            → /<REPO>/api/asr/
```

文件路径 = URL 路径(去掉 `.md`)。`index.md` 渲染为目录首页。

#### Frontmatter 模板

每个 `.md` 文件顶部必须有 frontmatter:

```yaml
---
title: 页面标题
description: 一句话描述,出现在 sidebar tooltip、搜索摘要、HTML <meta> 中
---
```

只要 `title` 在 sidebar 显示;`description` 不显示但对 SEO 关键。可选字段(按需加):

```yaml
---
title: ...
description: ...
sidebar:
  order: 1                    # 控制在 sidebar 中的排序
  badge: { text: New }        # 标题旁加一个徽章
draft: true                   # 临时下线已发布的页(不出现在生产构建)
---
```

#### 双语放置规则

- **英文版**直接放在 `docs/public/` 根下:`docs/public/api/asr.md`
- **中文版**整体放在 `docs/public/zh-cn/` 下,**镜像同样的目录结构和文件名**:`docs/public/zh-cn/api/asr.md`
- **文件名保持英文**(包括中文版),Starlight 靠文件名配对中英版本来驱动语言切换器
- 翻译的是 frontmatter 的 `title`/`description` 和正文,文件名永远不动
- 中文版可以漏译某些页,Starlight 会自动 fallback 到英文版,并在页顶显示"此内容尚不支持你的语言"提示

**对应关系示例**:

| 英文路径 | 中文路径 | URL(英文) | URL(中文) |
|---|---|---|---|
| `docs/public/api/asr.md` | `docs/public/zh-cn/api/asr.md` | `/<REPO>/api/asr/` | `/<REPO>/zh-cn/api/asr/` |

**❌ 不要这样写**:`docs/public/api/zh-cn/asr.md`(语言前缀必须是 `docs/public/` 的最外层目录,不能嵌进子模块里)

#### 草稿与下线

- **写到一半 commit**:文件名前加 `_`,如 `_wip-new-feature.md`。`sync-docs.mjs` 会跳过 `_` 开头的文件,Astro/Starlight 默认也忽略它们。改完去掉前缀就发出去
- **临时下线已发布页**:在 frontmatter 加 `draft: true`,Astro 会跳过它。比 mv 进 `docs/private/` 更轻量,但要记得删

#### 本地开发

```sh
cd site
npx pnpm@9 install
npx pnpm@9 dev      # http://localhost:4321/<REPO>/
```

构建本地预览(模拟生产):

```sh
npx pnpm@9 build
npx pnpm@9 preview
```

注意:
- 本地必须用 **pnpm 9**(原因见"已知陷阱"第 2 条)。直接安装的 pnpm 通常是 v10,会报 `ERR_PNPM_IGNORED_BUILDS`。`npx pnpm@9` 是最方便的解
- `dev`/`build` 通过 `prebuild` hook 自动跑 `sync-docs.mjs`,把 `docs/public/` 复制到 `site/src/content/docs/`
- **不要直接编辑 `site/src/content/docs/`**:它是构建产物,gitignored,每次构建都会被 `sync-docs.mjs` 覆盖。要改内容只改 `docs/public/` 下的源文件
- 文档站每页右上角有"Edit on GitHub"链接,点了直接跳到 `github.com/<ORG>/<REPO>/edit/main/docs/public/<file>`

#### 部署触发

- push 到 `main` 时,只在改了 `docs/public/**`、`site/**`、`.github/workflows/deploy-site.yml` 时才触发部署 workflow
- 改项目仓的源码(如 aistack 的 `aistack/` Python 包)**不会**触发文档站重新部署
- 想强制重跑:GitHub Actions 页面 → 选 `Deploy Site` workflow → 点 **Run workflow**(workflow_dispatch 已配置)

#### 排查清单

文档没出现在站上时按顺序检查:

1. 文件是否在 `docs/public/` 下?(不在 → 不会发布)
2. 文件名是否以 `_` 开头?(是 → 被 sync 脚本跳过)
3. frontmatter 是否有 `draft: true`?(有 → 被 Astro 跳过)
4. 最近一次 push 是否触发了 `Deploy Site` workflow?(`gh run list --repo <ORG>/<REPO> --workflow=deploy-site.yml`)
5. workflow 是否成功?失败的话看日志

## 四、自定义域名(已完成,记录为参考)

`dosmoon.com` 已绑定到 `dosmoon.github.io`,所有项目仓库的 Pages 自动跟上,使用同一个根域名:

```
https://dosmoon.com/         → 门户站
https://dosmoon.com/repo-a/  → 项目 A
https://dosmoon.com/repo-b/  → 项目 B
```

### Cloudflare 配置要点(已完成)

DNS 在 Cloudflare,需保持以下设置:

- DNS 记录:`CNAME  @  dosmoon.github.io.`(或 4 条 A 记录指向 GitHub IP)
- **代理状态必须为 DNS only(灰云)**,不能开橙云代理
  - 原因:橙云代理会拦截 GitHub 的 Let's Encrypt HTTP-01 证书续签验证,导致证书过期
- SSL/TLS 加密模式建议 **Full**,不要用 Flexible
  - 原因:Flexible 会让浏览器→CF 是 HTTPS 但 CF→GitHub 是 HTTP,GitHub 会 301 回 HTTPS 形成重定向循环

### GitHub 端配置(已完成)

- `dosmoon.github.io` 仓库 → Settings → Pages → Custom domain 已填 `dosmoon.com`
- Enforce HTTPS 已勾选
- **项目仓库的 Custom domain 字段保持空白**,继承组织 Pages 的域名

### 关键陷阱(防止后续踩坑)

❌ 不要在项目仓库 Settings → Pages 填 Custom domain。只在 `dosmoon.github.io` 填一次,各项目继承。

❌ 不要在代码或文档中硬编码 `dosmoon.github.io`。GitHub 会 301 重定向到 `dosmoon.com`,但每次访问多一跳,且对 SEO 不利。

❌ 不要在 Cloudflare 上开橙云代理(见上)。

### 验证清单(可重复执行)

- [ ] `https://dosmoon.com/` 打开门户
- [ ] `https://dosmoon.com/<REPO>/` 打开项目站
- [ ] `https://dosmoon.github.io/` 自动 301 到 `https://dosmoon.com/`
- [ ] HTTPS 证书有效(Let's Encrypt,90 天自动续)
- [ ] 各站内部链接、CSS、图片正常
- [ ] 页面源码 `<link rel="canonical">` 是 `dosmoon.com`
- [ ] sitemap.xml 里链接是 `dosmoon.com`

## 实施顺序

1. ✅ **域名绑定**:`dosmoon.com` → `dosmoon.github.io`,HTTPS 生效
2. ✅ **创建 `.github` 仓库**:`profile/README.md` 双语(英文默认 + `README.zh-CN.md`),组织主页生效
3. ✅ **改造 `dosmoon.github.io`**:Astro 6 + Starlight 0.39 替换临时 landing page,双语部署上线
4. **配置组织 Settings**:URL、Pinned repos(浏览器 UI 操作)
5. **试点一个项目**:加 `docs/public/` + `docs/private/` + `site/` + `sync-docs.mjs` + `deploy-site.yml`,验证 `https://dosmoon.com/<REPO>/` 正常
6. **推广到其他项目**:复制试点结构

## 已知陷阱与 CI 配置经验

下面三条都是 `dosmoon.github.io` 门户站首次部署时踩过的真坑,验证有效后写进规范。给项目仓搭 `site/` 时,直接照本节的结论配,不要自行尝试"更新版本/更激进默认值"。

### 1. `packageManager` 字段与 workflow `package-manager` 输入二选一

**症状**:CI 报 `Multiple versions of pnpm specified ... ERR_PNPM_BAD_PM_VERSION`。

**原因**:`pnpm/action-setup`(被 `withastro/action@v6` 内部调用)读到了两个不一致的 pnpm 版本来源——`package.json` 里的 `"packageManager": "pnpm@x.y.z"` 与 workflow 的 `package-manager: pnpm@xxx`。

**结论**:
- 项目 `package.json` **不要写 `packageManager` 字段**
- workflow 里固定写 `package-manager: pnpm@9`
- 单一来源:workflow 是 CI pnpm 版本的唯一权威
- 本地开发用什么 pnpm 都行(corepack/全局安装/包管理器都可以)

### 2. CI 必须钉 pnpm@9,不要用 pnpm@10 或 pnpm@latest

**症状**:CI 报 `[ERR_PNPM_IGNORED_BUILDS] Ignored build scripts: esbuild@..., sharp@...`。

**原因**:pnpm 10 默认拒绝执行 dependency 的 postinstall 脚本(供应链安全考虑)。`esbuild` 和 `sharp` 都依赖原生二进制的 install hook,被拒绝后 build 直接失败。pnpm 10 的官方解法是在 `package.json` 加 `pnpm.onlyBuiltDependencies: ["esbuild", "sharp"]` 白名单,但**实测在 `withastro/action@v6` 调起的环境里这个字段不生效**(原因尚未深究)。

**结论**:
- workflow 写 `package-manager: pnpm@9`,绕开整个 strict 模式
- 不要写 `pnpm@latest`(latest 现在 = pnpm 10,且会持续漂移)
- 等 pnpm 10 在 `withastro/action` 里的支持稳定再考虑升级

### 3. Starlight 0.39+ 的 `social` 是数组,旧版是对象;且强制 Astro 6

**症状**:Astro 5 + Starlight 0.32 + 数组 `social` 配置 → `Expected type "object", received "array"`;升级到 Starlight 0.39 但 Astro 还是 5 → `astro/zod does not provide an export named 'locales'`。

**原因**:Starlight `social` 字段在 0.39 版本从对象语法切到了数组语法,且 0.39 把 peer dep 升到 `astro@^6.0.0`。

**结论**(给项目仓 `site/` 用):
```json
// package.json
{
  "dependencies": {
    "@astrojs/starlight": "^0.39.0",
    "astro": "^6.0.0",
    "sharp": "^0.33.5"
  }
}
```
```js
// astro.config.mjs
starlight({
  social: [
    { icon: 'github', label: 'GitHub', href: 'https://github.com/dosmoon/<REPO>' },
  ],
})
```
不要照抄 Starlight 旧文档里的 `social: { github: '...' }` 写法。

### 4. `public/CNAME` 不要省

**结论**:每个用 GitHub Actions 部署到 Pages + 自定义域名的仓库,`public/CNAME` 文件都必须存在,内容是 `dosmoon.com`(单行)。Astro 会把它复制到 `dist/`,Pages 用它确认自定义域名归属。省掉这一步,自定义域名设置可能在某次重新部署后丢失。

### 5. Pages Source 切到 GitHub Actions 是手动 UI 步骤,且必须**先切再 push**

**症状**:如果保持 `Deploy from a branch` 模式直接 push Astro 源码,Pages 会把 `package.json`、`src/` 当成静态文件发布,网站立刻坏掉。

**结论**:
1. 先在浏览器里 Settings → Pages → Source 改为 **GitHub Actions**
2. 再 push 代码
3. 等 workflow 跑完 artifact 上传,Pages 自动接管

新建项目仓时,这一步绝不能颠倒。门户已经踩过、不会再踩,但项目仓试点时仍要遵守此顺序。

## 不变约束

- 项目文档目录统一:`docs/public/`(对外)+ `docs/private/`(内部)
- 项目站源目录统一叫 `site/`,内容来自 `sync-docs.mjs` 自动同步
- workflow 文件统一叫 `deploy-site.yml`,触发 paths 包含 `docs/public/**` 和 `site/**`
- 仓库 Settings → Pages → Source 必须设为 **GitHub Actions**(需在 Web UI 手动操作)
- 项目仓库 About 的 Website 字段必须配置
- 自定义域名只在 `dosmoon.github.io` 仓库配置,所有项目仓库的 Custom domain 必须保持空白
- 所有 `astro.config.mjs` 的 `site` 字段统一为 `https://dosmoon.com`
- Cloudflare 必须保持 DNS only(灰云),SSL/TLS 模式 Full

## 本文档自身的归宿

本草案随实施而演化。当 dosmoon 的某个项目仓库率先建起 `docs/public/` + `docs/private/` 结构后,本文档应当迁入"工作室基础设施"项目的 `docs/private/` 下(它属于内部建设记录,不必对外)。在那之前,暂存于 `dosmoon-github-io/docs/` 是合理的过渡。
