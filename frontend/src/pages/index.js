import clsx from 'clsx';
import Link from '@docusaurus/Link';
import useDocusaurusContext from '@docusaurus/useDocusaurusContext';
import Layout from '@theme/Layout';
import HomepageFeatures from '@site/src/components/HomepageFeatures';

import Heading from '@theme/Heading';
import styles from './index.module.css';

function HomepageHeader() {
  const {siteConfig} = useDocusaurusContext();
  return (
    <header className={clsx('hero hero--primary', styles.heroBanner)}>
      <div className="container">
        <Heading as="h1" className="hero__title">
          {siteConfig.title}
        </Heading>
        <p className="hero__subtitle">{siteConfig.tagline}</p>
        <div className={styles.buttons}>
          <Link
            className="button button--primary button--lg"
            to="/book-content">
            Start Reading
          </Link>
          <Link
            className="button button--secondary button--lg"
            to="/login"
            style={{ marginLeft: '1rem' }}>
            Login
          </Link>
          <Link
            className="button button--outline button--lg"
            to="/signup"
            style={{ marginLeft: '1rem' }}>
            Sign Up
          </Link>
        </div>
      </div>
    </header>
  );
}

export default function Home() {
  const {siteConfig} = useDocusaurusContext();
  return (
    <Layout
      title={`Hello from ${siteConfig.title}`}
      description="Physical AI & Humanoid Robotics: Bridging the Digital Brain and the Physical Body">
      <HomepageHeader />
      <main>
        <section style={{
          padding: '4rem 0',
          textAlign: 'center',
          backgroundColor: '#f9fafb'
        }}>
          <div className="container">
            <div className="row">
              <div className="col col--8 col--offset-2">
                <h2 style={{ fontSize: '2rem', marginBottom: '1.5rem' }}>AI-Powered Book Assistant</h2>
                <p style={{ fontSize: '1.2rem', lineHeight: '1.6' }}>
                  Interact with the Physical AI & Humanoid Robotics book using our intelligent chatbot.
                  Read and understand content in your preferred language.
                </p>
              </div>
            </div>
          </div>
        </section>

        <section style={{
          padding: '3rem 0',
          textAlign: 'center',
          backgroundColor: '#e5e7eb'
        }}>
          <div className="container">
            <div className="row">
              <div className="col col--10 col--offset-1">
                <h2 style={{ fontSize: '1.8rem', marginBottom: '2rem' }}>Read in Your Preferred Language</h2>
                <div style={{ display: 'flex', justifyContent: 'center', gap: '1rem', flexWrap: 'wrap' }}>
                  <Link
                    className="button button--primary button--lg"
                    to="/book-content"
                    style={{ minWidth: '250px', margin: '0.5rem' }}>
                    Read in English
                  </Link>
                  <Link
                    className="button button--secondary button--lg"
                    to="/book-content"
                    style={{ minWidth: '250px', margin: '0.5rem' }}>
                    Read in Urdu
                  </Link>
                </div>
                <p style={{ marginTop: '1.5rem', color: '#6b7280' }}>
                  Switch between English and Urdu to read the entire book content in your preferred language
                </p>
              </div>
            </div>
          </div>
        </section>

        <HomepageFeatures />
      </main>
    </Layout>
  );
}