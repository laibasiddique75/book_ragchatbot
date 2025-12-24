// // @ts-nocheck

// /** @type {import('@docusaurus/plugin-content-docs').SidebarsConfig} */
// const sidebars = {
//   tutorialSidebar: [
//     'intro',
//     {
//       type: 'category',
//       label: '1: Introduction to Physical AI',
//       items: [
//         '1-introduction/why-physical-ai',
//       ],
//     },
//     {
//       type: 'category',
//       label: '2: ROS 2 Fundamentals (Weeks 3-5)',
//       items: [
//         '2-ros2-fundamentals/week-3-5',
//       ],
//     },
//     {
//       type: 'category',
//       label: '5: Lab Setup',
//       items: [
//         '5-lab-setup/digital-twin-workstation',
//       ],
//     },
//     {
//       type: 'category',
//       label: 'Weeks 1-2: Fundamentals of Robotics',
//       items: [
//         'weeks/week-1/intro-to-physical-ai',
//         'weeks/week-1/learning-outcomes',
//         'weeks/week-1/setup-environment',
//         'weeks/week-1/hardware-overview',
//         'weeks/week-2/physics-of-robotics',
//         'weeks/week-2/kinematics-basics',
//         'weeks/week-2/sensors-overview'
//       ],
//     },
//     {
//       type: 'category',
//       label: 'Weeks 6-8: Digital Twin (Gazebo & Unity)',
//       items: [
//         'weeks/week-6-8/digital-twin-concepts',
//         'weeks/week-6-8/gazebo-simulation',
//         'weeks/week-6-8/unity-integration',
//         'weeks/week-6-8/robot-modeling',
//         'weeks/week-6-8/physics-simulation',
//         'weeks/week-6-8/twin-exercises'
//       ],
//     },
//     {
//       type: 'category',
//       label: 'Weeks 9-11: AI-Robot Brain (NVIDIA Isaac™)',
//       items: [
//         'weeks/week-9-11/isaac-ecosystem',
//         'weeks/week-9-11/perception-systems',
//         'weeks/week-9-11/planning-control',
//         'weeks/week-9-11/reinforcement-learning',
//         'weeks/week-9-11/isaac-exercises'
//       ],
//     },
//     {
//       type: 'category',
//       label: 'Weeks 12-15: Vision-Language-Action (VLA & LLMs)',
//       items: [
//         'weeks/week-12-15/vla-concepts',
//         'weeks/week-12-15/llm-integration',
//         'weeks/week-12-15/multimodal-learning',
//         'weeks/week-12-15/human-robot-interaction',
//         'weeks/week-12-15/capstone-prep'
//       ],
//     },
//     {
//       type: 'category',
//       label: 'Projects',
//       items: [
//         'projects/week-3-5-project',
//         'projects/week-6-8-project',
//         'projects/week-9-11-project',
//         'projects/capstone-project'
//       ],
//     },
//     {
//       type: 'category',
//       label: 'Hardware & Lab Requirements',
//       items: [
//         'hardware/digital-twin-workstation',
//         'hardware/economy-jetson-kit',
//         'hardware/setup-guide'
//       ],
//     },
//     {
//       type: 'category',
//       label: 'Assessment',
//       items: [
//         'assessment/weekly-assignments',
//         'assessment/project-rubrics',
//         'assessment/capstone-assessment'
//       ],
//     }
//   ],
// };

// export default sidebars;

// @ts-nocheck

/** @type {import('@docusaurus/plugin-content-docs').SidebarsConfig} */
const sidebars = {
  tutorialSidebar: [
    'intro',
    {
      type: 'category',
      label: '1: Introduction to Physical AI',
      items: [
        'introduction/why-physical-ai',
      ],
    },
    {
      type: 'category',
      label: '2: ROS 2 Fundamentals (Weeks 3-5)',
      items: [
        'ros2-fundamentals/week-3-5',
      ],
    },
    {
      type: 'category',
      label: '5: Lab Setup',
      items: [
        'lab-setup/digital-twin-workstation',
      ],
    },
  ],
};

export default sidebars;
