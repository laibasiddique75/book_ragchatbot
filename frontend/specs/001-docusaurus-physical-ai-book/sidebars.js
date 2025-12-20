// @ts-check

/** @type {import('@docusaurus/plugin-content-docs').SidebarsConfig} */
const sidebars = {
  tutorialSidebar: [
    'intro',
    {
      type: 'category',
      label: 'Week 1: Introduction to Physical AI',
      items: [
        'weeks/week-1/intro-to-physical-ai',
        'weeks/week-1/learning-outcomes',
        'weeks/week-1/setup-environment',
        'weeks/week-1/hardware-overview'
      ],
    },
    {
      type: 'category',
      label: 'Week 2: Fundamentals of Robotics',
      items: [
        'weeks/week-2/physics-of-robotics',
        'weeks/week-2/kinematics-basics',
        'weeks/week-2/sensors-overview'
      ],
    },
    {
      type: 'category',
      label: 'Weeks 3-5: The Robotic Nervous System (ROS 2)',
      items: [
        'weeks/week-3-5/ros2-intro',
        'weeks/week-3-5/ros2-architecture',
        'weeks/week-3-5/ros2-nodes-topics',
        'weeks/week-3-5/ros2-workspaces',
        'weeks/week-3-5/ros2-launch-files',
        'weeks/week-3-5/ros2-exercises',
        'weeks/week-3-5/ros2-project'
      ],
    },
    {
      type: 'category',
      label: 'Weeks 6-8: The Digital Twin (Gazebo & Unity)',
      items: [
        'weeks/week-6-8/digital-twin-concepts',
        'weeks/week-6-8/gazebo-simulation',
        'weeks/week-6-8/unity-integration',
        'weeks/week-6-8/robot-modeling',
        'weeks/week-6-8/physics-simulation',
        'weeks/week-6-8/twin-exercises'
      ],
    },
    {
      type: 'category',
      label: 'Weeks 9-11: The AI-Robot Brain (NVIDIA Isaac™)',
      items: [
        'weeks/week-9-11/isaac-ecosystem',
        'weeks/week-9-11/perception-systems',
        'weeks/week-9-11/planning-control',
        'weeks/week-9-11/reinforcement-learning',
        'weeks/week-9-11/isaac-exercises'
      ],
    },
    {
      type: 'category',
      label: 'Weeks 12-15: Vision-Language-Action (VLA & LLMs)',
      items: [
        'weeks/week-12-15/vla-concepts',
        'weeks/week-12-15/llm-integration',
        'weeks/week-12-15/multimodal-learning',
        'weeks/week-12-15/human-robot-interaction',
        'weeks/week-12-15/capstone-prep'
      ],
    },
    {
      type: 'category',
      label: 'Projects',
      items: [
        'projects/week-3-5-project',
        'projects/week-6-8-project',
        'projects/week-9-11-project',
        'projects/capstone-project'
      ],
    },
    {
      type: 'category',
      label: 'Hardware & Lab Requirements',
      items: [
        'hardware/digital-twin-workstation',
        'hardware/economy-jetson-kit',
        'hardware/setup-guide'
      ],
    },
    {
      type: 'category',
      label: 'Assessment',
      items: [
        'assessment/weekly-assignments',
        'assessment/project-rubrics',
        'assessment/capstone-assessment'
      ],
    }
  ],
};

export default sidebars;