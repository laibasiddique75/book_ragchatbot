import React, { useState, useEffect, useRef } from 'react';
import { useThemeConfig } from '@docusaurus/theme-common';
import useDocusaurusContext from '@docusaurus/useDocusaurusContext';
import BrowserOnly from '@docusaurus/BrowserOnly';

const BACKEND_URL = 'http://localhost:8000'; // Replace with your backend URL in production

const ChatBot = () => {
  const [messages, setMessages] = useState([]);
  const [inputText, setInputText] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [selectedText, setSelectedText] = useState(''); // To store selected text
  const [isExpanded, setIsExpanded] = useState(false);
  const messagesEndRef = useRef(null);
  const inputRef = useRef(null);

  // Function to get selected text from the page
  useEffect(() => {
    const handleSelection = () => {
      const selectedText = window.getSelection().toString().trim();
      if (selectedText) {
        setSelectedText(selectedText);
      }
    };

    document.addEventListener('mouseup', handleSelection);
    return () => {
      document.removeEventListener('mouseup', handleSelection);
    };
  }, []);

  // Scroll to bottom of messages
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!inputText.trim() || isLoading) return;

    // Add user message to chat
    const userMessage = { role: 'user', content: inputText, timestamp: new Date() };
    setMessages(prev => [...prev, userMessage]);
    setIsLoading(true);

    try {
      // Get response from backend
      const response = await fetch(`${BACKEND_URL}/chat`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          message: inputText,
          selected_text: selectedText,
        }),
      });

      if (!response.ok) {
        throw new Error(`Server error: ${response.status}`);
      }

      const data = await response.json();

      // Add assistant message to chat
      const assistantMessage = {
        role: 'assistant',
        content: data.response,
        sources: data.sources || [],
        timestamp: new Date(),
      };
      setMessages(prev => [...prev, assistantMessage]);

      // Clear selected text after using it
      setSelectedText('');
    } catch (error) {
      console.error('Error getting chat response:', error);
      const errorMessage = {
        role: 'assistant',
        content: 'Sorry, I encountered an error. Please try again.',
        timestamp: new Date(),
      };
      setMessages(prev => [...prev, errorMessage]);
    } finally {
      setIsLoading(false);
      setInputText('');
    }
  };

  const clearChat = () => {
    setMessages([]);
    setSelectedText('');
  };

  const toggleExpand = () => {
    setIsExpanded(!isExpanded);
  };

  return (
    <div className="chatbot-container" style={{
      fontFamily: 'Inter, -apple-system, BlinkMacSystemFont, Segoe UI, Roboto, Oxygen, Ubuntu, Cantarell, Open Sans, Helvetica Neue, sans-serif',
      border: 'none',
      borderRadius: '16px',
      padding: '0',
      margin: '1rem 0',
      backgroundColor: 'white',
      boxShadow: '0 10px 30px rgba(0, 0, 0, 0.1)',
      minHeight: '500px',
      display: 'flex',
      flexDirection: 'column',
      overflow: 'hidden'
    }}>
      {/* Header */}
      <div style={{
        backgroundColor: '#2563eb',
        color: 'white',
        padding: '16px 20px',
        display: 'flex',
        justifyContent: 'space-between',
        alignItems: 'center',
        position: 'relative'
      }}>
        <div style={{ display: 'flex', alignItems: 'center' }}>
          <div style={{
            width: '40px',
            height: '40px',
            borderRadius: '50%',
            backgroundColor: 'rgba(255, 255, 255, 0.2)',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            marginRight: '12px'
          }}>
            <svg width="20" height="20" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
              <path d="M12 2C6.48 2 2 6.48 2 12C2 17.52 6.48 22 12 22C13.96 22 15.8 21.49 17.4 20.6L21 22L19.6 18.4C20.49 16.8 21 14.96 21 13C21 7.48 16.52 3 12 3ZM8 15.5C7.17 15.5 6.5 14.83 6.5 14C6.5 13.17 7.17 12.5 8 12.5C8.83 12.5 9.5 13.17 9.5 14C9.5 14.83 8.83 15.5 8 15.5ZM12 15.5C11.17 15.5 10.5 14.83 10.5 14C10.5 13.17 11.17 12.5 12 12.5C12.83 12.5 13.5 13.17 13.5 14C13.5 14.83 12.83 15.5 12 15.5ZM16 15.5C15.17 15.5 14.5 14.83 14.5 14C14.5 13.17 15.17 12.5 16 12.5C16.83 12.5 17.5 13.17 17.5 14C17.5 14.83 16.83 15.5 16 15.5Z" fill="white"/>
            </svg>
          </div>
          <div>
            <h3 style={{ margin: 0, fontSize: '1.2rem', fontWeight: '600' }}>Book Assistant</h3>
            <div style={{ fontSize: '0.8rem', opacity: 0.8 }}>Powered by Qwen & RAG</div>
          </div>
        </div>
        <div style={{ display: 'flex', gap: '8px' }}>
          <button
            onClick={clearChat}
            style={{
              backgroundColor: 'rgba(255, 255, 255, 0.2)',
              border: 'none',
              borderRadius: '8px',
              padding: '6px 12px',
              color: 'white',
              cursor: 'pointer',
              fontSize: '0.9rem',
              transition: 'background-color 0.2s'
            }}
            onMouseOver={(e) => e.target.style.backgroundColor = 'rgba(255, 255, 255, 0.3)'}
            onMouseOut={(e) => e.target.style.backgroundColor = 'rgba(255, 255, 255, 0.2)'}
          >
            Clear
          </button>
        </div>
      </div>

      {/* Selected text indicator */}
      {selectedText && (
        <div style={{
          backgroundColor: '#fef3c7',
          border: '1px solid #f59e0b',
          padding: '12px',
          margin: '12px',
          borderRadius: '8px',
          fontSize: '0.85rem',
          display: 'flex',
          alignItems: 'flex-start'
        }}>
          <div style={{
            color: '#d97706',
            fontWeight: 'bold',
            marginRight: '8px',
            fontSize: '1.2rem'
          }}>
            📍
          </div>
          <div>
            <div style={{ fontWeight: '600', marginBottom: '4px' }}>Context from selected text:</div>
            <div style={{ fontStyle: 'italic', lineHeight: '1.4' }}>
              "{selectedText.substring(0, 150)}{selectedText.length > 150 ? '...' : ''}"
            </div>
          </div>
        </div>
      )}

      {/* Messages container */}
      <div style={{
        flex: 1,
        overflowY: 'auto',
        padding: '20px',
        backgroundColor: '#f9fafb',
        maxHeight: isExpanded ? 'none' : '300px'
      }}>
        {messages.length === 0 ? (
          <div style={{
            textAlign: 'center',
            padding: '40px 20px',
            color: '#6b7280'
          }}>
            <div style={{
              width: '80px',
              height: '80px',
              borderRadius: '50%',
              backgroundColor: '#dbeafe',
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
              margin: '0 auto 16px'
            }}>
              <svg width="40" height="40" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                <path d="M20 2H4C2.9 2 2.01 2.9 2.01 4L2 22L6 18H20C21.1 18 22 17.1 22 16V4C22 2.9 21.1 2 20 2ZM9 12H7V10H9V12ZM17 12H15V10H17V12ZM13 12H11V10H13V12Z" fill="#3b82f6"/>
              </svg>
            </div>
            <h4 style={{ margin: '0 0 8px 0', fontSize: '1.25rem', color: '#1f2937' }}>Ask about the Book</h4>
            <p style={{ margin: 0, lineHeight: '1.6' }}>
              I can help answer questions about Physical AI & Humanoid Robotics.<br />
              Select text on the page to ask questions about specific content.
            </p>
          </div>
        ) : (
          <div>
            {messages.map((msg, index) => (
              <div key={index} style={{
                marginBottom: '20px',
                display: 'flex',
                justifyContent: msg.role === 'user' ? 'flex-end' : 'flex-start'
              }}>
                <div className={msg.role === 'user' ? 'chat-message-user' : 'chat-message-assistant'} style={{
                  position: 'relative',
                  wordWrap: 'break-word',
                  wordBreak: 'break-word'
                }}>
                  <div style={{ whiteSpace: 'pre-wrap', lineHeight: '1.5' }}>
                    {msg.content}
                  </div>

                  {msg.sources && msg.sources.length > 0 && (
                    <div style={{
                      marginTop: '12px',
                      paddingTop: '12px',
                      borderTop: '1px solid rgba(0,0,0,0.1)',
                      fontSize: '0.85rem'
                    }}>
                      <details style={{
                        border: '1px solid #e5e7eb',
                        borderRadius: '8px',
                        padding: '12px',
                        backgroundColor: msg.role === 'user' ? '#1d4ed8' : '#f9fafb'
                      }}>
                        <summary style={{
                          cursor: 'pointer',
                          fontWeight: '600',
                          color: msg.role === 'user' ? 'white' : '#4f46e5',
                          outline: 'none',
                          marginBottom: '8px'
                        }}>
                          📚 Sources
                        </summary>
                        <ul style={{
                          margin: '8px 0 0 0',
                          padding: '0 0 0 20px',
                          textAlign: 'left',
                          color: msg.role === 'user' ? 'rgba(255,255,255,0.9)' : '#6b7280'
                        }}>
                          {msg.sources.map((source, idx) => (
                            <li key={idx} style={{ marginBottom: '8px' }}>
                              {source.text?.substring(0, 100)}...
                            </li>
                          ))}
                        </ul>
                      </details>
                    </div>
                  )}
                </div>
              </div>
            ))}
            {isLoading && (
              <div style={{
                display: 'flex',
                justifyContent: 'flex-start',
                marginBottom: '20px'
              }}>
                <div className="chat-message-assistant">
                  <div style={{ display: 'flex', alignItems: 'center' }}>
                    <div style={{
                      width: '12px',
                      height: '12px',
                      borderRadius: '50%',
                      backgroundColor: '#9ca3af',
                      marginRight: '6px',
                      animation: 'pulse 1.4s ease-in-out infinite both'
                    }} style={{
                      width: '12px',
                      height: '12px',
                      borderRadius: '50%',
                      backgroundColor: '#9ca3af',
                      marginRight: '6px',
                      animation: 'pulse 1.4s ease-in-out infinite both',
                      animationDelay: '0ms'
                    }}></div>
                    <div style={{
                      width: '12px',
                      height: '12px',
                      borderRadius: '50%',
                      backgroundColor: '#9ca3af',
                      marginRight: '6px',
                      animation: 'pulse 1.4s ease-in-out infinite both',
                      animationDelay: '0.2s'
                    }}></div>
                    <div style={{
                      width: '12px',
                      height: '12px',
                      borderRadius: '50%',
                      backgroundColor: '#9ca3af',
                      animation: 'pulse 1.4s ease-in-out infinite both',
                      animationDelay: '0.4s'
                    }}></div>
                    <span style={{ marginLeft: '10px', color: '#9ca3af' }}>Thinking...</span>
                  </div>
                </div>
              </div>
            )}
            <div ref={messagesEndRef} />
          </div>
        )}
      </div>

      {/* Input area */}
      <div style={{
        padding: '16px 20px',
        backgroundColor: 'white',
        borderTop: '1px solid #e5e7eb'
      }}>
        <form onSubmit={handleSubmit} style={{ display: 'flex', gap: '12px' }}>
          <div style={{
            flex: 1,
            position: 'relative',
            display: 'flex',
            alignItems: 'center'
          }}>
            <input
              ref={inputRef}
              type="text"
              value={inputText}
              onChange={(e) => setInputText(e.target.value)}
              placeholder="Ask a question about the book..."
              style={{
                width: '100%',
                padding: '14px 50px 14px 16px',
                border: '1px solid #d1d5db',
                borderRadius: '50px',
                fontSize: '1rem',
                outline: 'none',
                transition: 'border-color 0.2s',
                backgroundColor: '#f9fafb'
              }}
              onFocus={(e) => {
                e.target.style.borderColor = '#93c5fd';
                e.target.style.boxShadow = '0 0 0 3px rgba(59, 130, 246, 0.1)';
              }}
              onBlur={(e) => {
                e.target.style.borderColor = '#d1d5db';
                e.target.style.boxShadow = 'none';
              }}
              disabled={isLoading}
            />
            <button
              type="submit"
              disabled={isLoading || !inputText.trim()}
              style={{
                position: 'absolute',
                right: '6px',
                width: '36px',
                height: '36px',
                borderRadius: '50%',
                backgroundColor: '#2563eb',
                color: 'white',
                border: 'none',
                cursor: (isLoading || !inputText.trim()) ? 'not-allowed' : 'pointer',
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center',
                transition: 'background-color 0.2s',
                opacity: (isLoading || !inputText.trim()) ? 0.6 : 1
              }}
              onMouseOver={(e) => {
                if (!(isLoading || !inputText.trim())) {
                  e.target.style.backgroundColor = '#1d4ed8';
                }
              }}
              onMouseOut={(e) => {
                e.target.style.backgroundColor = '#2563eb';
              }}
            >
              <svg width="18" height="18" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                <path d="M2.01 21L23 12L2.01 3L2 10L17 12L2 14L2.01 21Z" fill="white"/>
              </svg>
            </button>
          </div>
        </form>
        <div style={{
          fontSize: '0.75rem',
          color: '#9ca3af',
          textAlign: 'center',
          marginTop: '10px'
        }}>
          Powered by Qwen AI & RAG Technology
        </div>
      </div>

      <style jsx>{`
        @keyframes pulse {
          0%, 100% { transform: scale(1); }
          50% { transform: scale(1.2); }
        }
      `}</style>
    </div>
  );
};

const ChatBotWrapper = () => {
  return (
    <BrowserOnly>
      {() => <ChatBot />}
    </BrowserOnly>
  );
};

export default ChatBotWrapper;