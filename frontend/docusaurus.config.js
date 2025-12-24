
// // @ts-nocheck
// import {themes as prismThemes} from 'prism-react-renderer';

// /** @type {import('@docusaurus/types').Config} */
// const config = {
//   title: 'Physical AI & Humanoid Robotics: Bridging the Digital Brain and the Physical Body',
//   tagline: 'A comprehensive course on embodied artificial intelligence',
//   favicon: 'img/favicon.ico',

//   // Set the production url of your site here
//   url: 'https://your-organization.github.io',
//   // Set the /<baseUrl>/ pathname under which your site is served
//   // For GitHub pages deployment, it is often '/<projectName>/'
//   baseUrl: '/physical-ai-humanoid-robotics',

//   // GitHub pages deployment config.
//   // If you aren't using GitHub pages, you don't need these.
//   organizationName: 'your-organization', // Usually your GitHub org/user name.
//   projectName: 'physical-ai-humanoid-robotics', // Usually your repo name.

//   onBrokenLinks: 'throw',
//   onBrokenMarkdownLinks: 'warn',

//   // Even if you don't use internationalization, you can use this field to set
//   // useful metadata like html lang. For example, if your site is Chinese, you
//   // may want to replace "en" with "zh-Hans".
//   i18n: {
//     defaultLocale: 'en',
//     locales: ['en'],
//   },

//   presets: [
//     [
//       'classic',
//       /** @type {import('@docusaurus/preset-classic').Options} */
//       ({
//         docs: {
//           sidebarPath: './sidebars.js',
//           // Please change this to your repo.
//           // Remove this to remove the "edit this page" links.
//           editUrl:
//             'https://github.com/your-organization/physical-ai-humanoid-robotics/tree/main/',
//         },
//         blog: false, // Disable blog if not needed
//         theme: {
//           customCss: './src/css/custom.css',
//         },
//       }),
//     ],
//   ],

//   themeConfig:
//     /** @type {import('@docusaurus/preset-classic').ThemeConfig} */
//     ({
//       // Replace with your project's social card
//       image: 'img/docusaurus-social-card.jpg',
//       navbar: {
//         title: 'Physical AI & Humanoid Robotics',
//         logo: {
//           alt: 'Physical AI Logo',
//           src: 'img/robot-icon.svg',
//         },
//         items: [
//           {
//             type: 'docSidebar',
//             sidebarId: 'tutorialSidebar',
//             position: 'left',
//             label: 'Course Content',
//           },
//           {
//             href: 'https://github.com/your-organization/physical-ai-humanoid-robotics',
//             label: 'GitHub',
//             position: 'right',
//           },
//         ],
//       },
//       footer: {
//         style: 'dark',
//         links: [
//           {
//             title: 'Course Sections',
//             items: [
//               {
//                 label: 'Week 1: Introduction',
//                 to: '/docs/1-introduction/why-physical-ai',
//               },
//               {
//                 label: 'Weeks 3-5: ROS 2 Fundamentals',
//                 to: '/docs/2-ros2-fundamentals/week-3-5',
//               },
//               {
//                 label: 'Lab Setup',
//                 to: '/docs/5-lab-setup/digital-twin-workstation',
//               },
//             ],
//           },
//           {
//             title: 'Community',
//             items: [
//               {
//                 label: 'Stack Overflow',
//                 href: 'https://stackoverflow.com/questions/tagged/docusaurus',
//               },
//               {
//                 label: 'Discord',
//                 href: 'https://discordapp.com/invite/docusaurus',
//               },
//             ],
//           },
//           {
//             title: 'More',
//             items: [
//               {
//                 label: 'GitHub',
//                 href: 'https://github.com/facebook/docusaurus',
//               },
//             ],
//           },
//         ],
//         copyright: `Copyright © ${new Date().getFullYear()} Physical AI & Humanoid Robotics Course. Built with Docusaurus.`,
//       },
//       prism: {
//         theme: prismThemes.github,
//         darkTheme: prismThemes.dracula,
//         additionalLanguages: ['python', 'bash', 'json', 'docker', 'robotframework'],
//       },
//       // Enable math support
//       markdown: {
//         mermaid: true,
//       },
//     }),

//   // Add plugins
//   plugins: [
//     // Plugin for math formulas (KaTeX)
//     [
//       '@docusaurus/plugin-content-docs',
//       {
//         id: 'math',
//         path: 'docs/math',
//         routeBasePath: 'math',
//         sidebarPath: false,
//       },
//     ],
//     // Plugin for client-side search
//     [
//       '@docusaurus/plugin-client-redirects',
//       {
//         redirects: [
//           {
//             to: '/docs/1-introduction/why-physical-ai',
//             from: ['/docs/intro', '/docs/getting-started'],
//           },
//         ],
//       },
//     ],
//   ],

//   // Add themes
//   themes: [
//     // Add @docusaurus/theme-mermaid for Mermaid diagrams
//     '@docusaurus/theme-mermaid',
//     // Add @docusaurus/theme-live-codeblock for live code editing
//     '@docusaurus/theme-live-codeblock',
//   ],
// };

// export default config;

// @ts-nocheck
import { themes as prismThemes } from 'prism-react-renderer';

/** @type {import('@docusaurus/types').Config} */
const config = {
  title: 'Physical AI & Humanoid Robotics',
  tagline: 'Bridging the Digital Brain and the Physical Body',
  favicon: 'img/favicon.ico',

  url: 'https://book-ragchatbot-nwww.vercel.app',
  baseUrl: '/',

  organizationName: 'your-organization',
  projectName: 'physical-ai-humanoid-robotics',

  onBrokenLinks: 'warn',
  onBrokenMarkdownLinks: 'warn',

  i18n: {
    defaultLocale: 'en',
    locales: ['en'],
  },

  presets: [
    [
      'classic',
      {
        docs: {
          sidebarPath: './sidebars.js',
          editUrl:
            'https://github.com/your-organization/physical-ai-humanoid-robotics/tree/main/',
          showLastUpdateTime: true,
        },
        blog: false,
        theme: {
          customCss: './src/css/custom.css',
        },
      },
    ],
  ],

  themeConfig: {
    image: 'img/docusaurus-social-card.jpg',

    navbar: {
      title: 'Physical AI & Humanoid Robotics',
      logo: {
        alt: 'Physical AI Logo',
        src: 'img/robot-icon.svg',
      },
      items: [
        {
          type: 'docSidebar',
          sidebarId: 'tutorialSidebar',
          position: 'left',
          label: 'Course Content',
        },
        {
          to: '/chat',
          label: 'Chat with Book',
          position: 'left',
        },
        {
          href: 'https://github.com/your-organization/physical-ai-humanoid-robotics',
          label: 'GitHub',
          position: 'right',
        },
      ],
    },

    footer: {
      style: 'dark',
      links: [
        {
          title: 'Course Sections',
          items: [
            {
              label: 'Introduction',
              to: '/docs/introduction/why-physical-ai',
            },
            {
              label: 'ROS 2 Fundamentals',
              to: '/docs/ros2-fundamentals/week-3-5',
            },
            {
              label: 'Lab Setup',
              to: '/docs/lab-setup/digital-twin-workstation',
            },
          ],
        },
        {
          title: 'Community',
          items: [
            {
              label: 'Discord',
              href: 'https://discordapp.com/invite/docusaurus',
            },
            {
              label: 'Stack Overflow',
              href: 'https://stackoverflow.com/questions/tagged/docusaurus',
            },
          ],
        },
        {
          title: 'More',
          items: [
            {
              label: 'GitHub',
              href: 'https://github.com/facebook/docusaurus',
            },
            {
              label: 'Chat with Book',
              to: '/chat',
            },
          ],
        },
      ],
      copyright: `Copyright © ${new Date().getFullYear()} Physical AI & Humanoid Robotics`,
    },

    prism: {
      theme: prismThemes.github,
      darkTheme: prismThemes.dracula,
      additionalLanguages: ['python', 'bash', 'json', 'docker'],
    },

    markdown: {
      mermaid: true,
      onBrokenMarkdownLinks: 'warn',
    },
  },

  themes: [
    '@docusaurus/theme-mermaid',
    '@docusaurus/theme-live-codeblock',
  ],
};

export default config;
