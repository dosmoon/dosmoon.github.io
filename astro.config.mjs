import { defineConfig } from 'astro/config';
import starlight from '@astrojs/starlight';

export default defineConfig({
  site: 'https://dosmoon.com',
  integrations: [
    starlight({
      title: 'dosmoon',
      defaultLocale: 'root',
      locales: {
        root: { label: 'English', lang: 'en' },
        'zh-cn': { label: '简体中文', lang: 'zh-CN' },
      },
      social: [
        { icon: 'github', label: 'GitHub', href: 'https://github.com/dosmoon' },
      ],
      sidebar: [
        {
          label: 'Projects',
          translations: { 'zh-CN': '项目' },
          link: '/projects/',
        },
        {
          label: 'News',
          translations: { 'zh-CN': '行业动态' },
          items: [{ autogenerate: { directory: 'news' } }],
        },
      ],
    }),
  ],
});
