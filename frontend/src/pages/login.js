import React from 'react';
import Layout from '@theme/Layout';
import AuthForm from '@site/src/components/Auth/AuthForm';

export default function LoginPage() {
  return (
    <Layout title="Login" description="Login to access the book assistant">
      <div style={{ padding: '2rem', minHeight: '80vh', display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
        <div className="container">
          <div className="row">
            <div className="col col--6 col--offset-3">
              <AuthForm isSignupMode={false} />
            </div>
          </div>
        </div>
      </div>
    </Layout>
  );
}