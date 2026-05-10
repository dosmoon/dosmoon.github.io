# dosmoon.github.io

Source for the dosmoon studio portal — published at [dosmoon.com](https://dosmoon.com/).

Built with [Astro](https://astro.build/) + [Starlight](https://starlight.astro.build/), bilingual (English root + 简体中文 at `/zh-cn/`), deployed via GitHub Actions to GitHub Pages.

## Local development

```sh
pnpm install
pnpm dev
```

## Project layout

```
src/content/docs/         English content (root locale)
src/content/docs/zh-cn/   Chinese content
public/                   Static assets (CNAME, favicons, …)
docs/                     Internal planning notes — not published
drafts/                   Article inbox (zh-cn/, en/) — see drafts/README.md
```

## Deployment

Pushing to `main` triggers `.github/workflows/deploy.yml`. Pages serves from the GitHub Actions artifact; the custom domain `dosmoon.com` is configured at the repo level (Settings → Pages).
