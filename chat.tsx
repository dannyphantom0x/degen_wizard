'use client';

import { useState, useRef, useEffect } from 'react';
import axios from 'axios';

const ChatComponent = () => {
  const [messages, setMessages] = useState<{ text: string; sender: 'user' | 'bot' }[]>([]);
  const [currentMessage, setCurrentMessage] = useState('');
  const [loading, setLoading] = useState(false);
  const chatEndRef = useRef<HTMLDivElement>(null);

  const scrollToBottom = () => {
    chatEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  const sendMessage = async () => {
    if (currentMessage.trim() === '') return;

    const userMessage = { text: currentMessage, sender: 'user' as const };
    setMessages([...messages, userMessage]);
    setCurrentMessage('');
    setLoading(true);

    try {
      const response = await axios.post(
        '',
        {
          model: 'gpt-3.5-turbo',
          messages: [
            { role: 'user', content: currentMessage },
            {
              role: 'system',
              content:
                '""',
            },
          ],
          max_tokens: 150,
        }
      );

      const botMessage = response.data.choices[0].message.content.trim();
      const botResponse = { text: botMessage, sender: 'bot' as const };
      setMessages((prevMessages) => [...prevMessages, botResponse]);
    } catch (error) {
      console.error('Error communicating with OpenAI:', error);
      setMessages((prevMessages) => [
        ...prevMessages,
        { text: 'Sorry, I couldn’t generate a response.', sender: 'bot' as const },
      ]);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  return (
    <div style={{ border: '1px solid #ccc', borderRadius: '8px', padding: '16px', width: '800px', margin: '0 auto', backgroundColor: 'white' }}>
      <div
        style={{
          height: '400px',
          overflowY: 'auto',
          marginBottom: '16px',
          padding: '8px',
          border: '1px solid #ddd',
          borderRadius: '4px',
          backgroundColor: '#f9f9f9',
        }}
      >
        {messages.map((message, index) => (
          <div
            key={index}
            style={{
              display: 'flex',
              alignItems: 'center',
              margin: '8px 0',
              textAlign: message.sender === 'user' ? 'right' : 'left',
              flexDirection: message.sender === 'user' ? 'row-reverse' : 'row',
            }}
          >
            <div
              style={{
                display: 'flex',
                alignItems: 'center',
                margin: message.sender === 'user' ? '0 0 0 8px' : '0 8px 0 0',
              }}
            >
              {message.sender === 'user' ? (
                <img
                  src="/user-icon.jpg"
                  alt="User"
                  style={{ width: '32px', height: '32px', borderRadius: '50%' }}
                />
              ) : (
                <img
                  src="/bot-icon.jpg"
                  alt="Wizard"
                  style={{ width: '32px', height: '32px', borderRadius: '100%' }}
                />
              )}
            </div>
            <span
              style={{
                display: 'inline-block',
                padding: '8px 12px',
                borderRadius: '16px',
                backgroundColor: message.sender === 'user' ? '#007bff' : '#e0e0e0',
                color: message.sender === 'user' ? '#fff' : '#000',
                maxWidth: '70%',
                wordWrap: 'break-word',
              }}
            >
              {message.text}
            </span>
          </div>
        ))}
        <div ref={chatEndRef} />
        {loading && (
          <div style={{ textAlign: 'left', margin: '8px 0' }}>
            <span
              style={{
                display: 'inline-block',
                padding: '8px 12px',
                borderRadius: '16px',
                backgroundColor: '#e0e0e0',
                color: '#000',
              }}
            >
              Bot is typing...
            </span>
          </div>
        )}
      </div>
      <div style={{ display: 'flex', gap: '8px' }}>
        <input
          type="text"
          value={currentMessage}
          onChange={(e) => setCurrentMessage(e.target.value)}
          onKeyDown={(e) => e.key === 'Enter' && sendMessage()}
          style={{ flex: 1, padding: '8px', borderRadius: '4px', border: '1px solid #ccc' }}
          placeholder="Type your message..."
          disabled={loading}
        />
        <button
          onClick={sendMessage}
          style={{ padding: '8px 16px', borderRadius: '4px', border: 'none', backgroundColor: '#007bff', color: '#fff' }}
          disabled={loading}
        >
          Send
        </button>
      </div>
    </div>
  );
};

export default ChatComponent;
