import React from 'react';
import Layout from '@theme/Layout';
import ChatBot from '@site/src/components/ChatBot';

export default function ChatPage() {
  return (
    <Layout title="Book Assistant" description="RAG Chatbot for Physical AI & Humanoid Robotics Book">
      <div style={{ padding: '2rem' }}>
        <div className="container">
          <div className="row">
            <div className="col col--12">
              <h1>Book Assistant</h1>
              <p>Ask questions about the Physical AI & Humanoid Robotics book. The assistant will provide answers based on the book content.</p>
              <ChatBot />
            </div>
          </div>
        </div>
      </div>
    </Layout>
  );
}