import clsx from 'clsx';
import Heading from '@theme/Heading';
import styles from './styles.module.css';

const FeatureList = [
  {
    title: 'Physical AI & Robotics',
    Svg: require('@site/static/img/robot-icon.svg').default,
    description: (
      <>
        Learn about the intersection of artificial intelligence and physical systems,
        exploring how AI can interact with and control robotic platforms.
      </>
    ),
  },
  {
    title: 'ROS 2 Fundamentals',
    Svg: require('@site/static/img/robot-icon.svg').default, // Using same SVG for now
    description: (
      <>
        Master Robot Operating System 2 (ROS 2) fundamentals for building robust
        robotic applications and systems.
      </>
    ),
  },
  {
    title: 'Digital Twins & Simulation',
    Svg: require('@site/static/img/robot-icon.svg').default, // Using same SVG for now
    description: (
      <>
        Explore digital twin environments and simulation platforms for testing
        and developing robotic systems safely.
      </>
    ),
  },
];

function Feature({Svg, title, description}) {
  return (
    <div className={clsx('col col--4')}>
      <div className={clsx('feature-card', 'text--center', 'padding-vert--md', 'padding-horiz--lg')}>
        <div className="text--center">
          <Svg className={styles.featureSvg} role="img" />
        </div>
        <div className="text--center padding-horiz--md">
          <Heading as="h3">{title}</Heading>
          <p>{description}</p>
        </div>
      </div>
    </div>
  );
}

export default function HomepageFeatures() {
  return (
    <section className={styles.features}>
      <div className="container">
        <div className="row">
          {FeatureList.map((props, idx) => (
            <Feature key={idx} {...props} />
          ))}
        </div>
      </div>
    </section>
  );
}