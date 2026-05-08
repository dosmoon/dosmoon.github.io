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

- **框架**:Astro 5 + Starlight
- **包管理**:pnpm
- **部署**:GitHub Actions(`withastro/action@v6`)
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
          package-manager: pnpm@latest

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
          package-manager: pnpm@latest

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

1. ✅ **域名绑定**(已完成):`dosmoon.com` → `dosmoon.github.io`,HTTPS 生效
2. **创建 `.github` 仓库**:加 `profile/README.md`,组织主页生效
3. **改造 `dosmoon.github.io`**:用 Astro + Starlight 替换当前临时 landing page,部署上线
4. **配置组织 Settings**:URL、Pinned repos
5. **试点一个项目**:加 `docs/public/` + `docs/private/` + `site/` + `sync-docs.mjs` + `deploy-site.yml`,验证 `https://dosmoon.com/<REPO>/` 正常
6. **推广到其他项目**:复制试点结构

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
