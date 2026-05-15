import { useState, useRef, useEffect } from 'react';
import { Send, Bot, User, Loader2, Sparkles, AlertCircle } from 'lucide-react';
import './AIAssistant.css';

export default function AIAssistant() {
  const [messages, setMessages] = useState([
    {
      id: 1,
      type: 'ai',
      content: 'Hello! I am your AI Health Assistant. How can I help you analyze your symptoms or understand your medical reports today?',
      timestamp: new Date().toISOString(),
    }
  ]);
  const [input, setInput] = useState('');
  const [isTyping, setIsTyping] = useState(false);
  const messagesEndRef = useRef(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const handleSend = (e) => {
    e.preventDefault();
    if (!input.trim()) return;

    const userMessage = {
      id: Date.now(),
      type: 'user',
      content: input,
      timestamp: new Date().toISOString(),
    };

    setMessages(prev => [...prev, userMessage]);
    setInput('');
    setIsTyping(true);

    // Simulate AI response
    setTimeout(() => {
      const aiResponse = {
        id: Date.now() + 1,
        type: 'ai',
        content: 'I am analyzing your query based on our medical database. This is a simulated response since the backend is currently not connected, but when live, this will stream insights from the HealthCare AI engine.',
        timestamp: new Date().toISOString(),
      };
      setMessages(prev => [...prev, aiResponse]);
      setIsTyping(false);
    }, 1500);
  };

  return (
    <div className="assistant-container animate-enter">
      <div className="page-header">
        <div>
          <h1 className="text-gradient">AI Health Assistant</h1>
          <p>Get instant insights on your health and medical queries</p>
        </div>
        <div className="badge badge-primary animate-pulse-glow">
          <Sparkles size={14} className="mr-2" />
          Powered by AI
        </div>
      </div>

      <div className="chat-interface glass-card">
        <div className="chat-messages">
          {messages.map((msg) => (
            <div key={msg.id} className={`message-wrapper ${msg.type}`}>
              <div className="message-avatar">
                {msg.type === 'ai' ? <Bot size={20} /> : <User size={20} />}
              </div>
              <div className={`message-bubble ${msg.type}`}>
                <p>{msg.content}</p>
                <span className="message-time">
                  {new Date(msg.timestamp).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
                </span>
              </div>
            </div>
          ))}
          {isTyping && (
            <div className="message-wrapper ai">
              <div className="message-avatar">
                <Bot size={20} />
              </div>
              <div className="message-bubble ai typing">
                <div className="typing-dot"></div>
                <div className="typing-dot"></div>
                <div className="typing-dot"></div>
              </div>
            </div>
          )}
          <div ref={messagesEndRef} />
        </div>

        <div className="disclaimer">
          <AlertCircle size={14} />
          <span>This AI is for informational purposes only. Do not use for medical emergencies.</span>
        </div>

        <form className="chat-input-area" onSubmit={handleSend}>
          <input
            type="text"
            className="form-control chat-input"
            placeholder="Ask about symptoms, reports, or general health..."
            value={input}
            onChange={(e) => setInput(e.target.value)}
          />
          <button type="submit" className="btn btn-primary send-btn" disabled={!input.trim() || isTyping}>
            {isTyping ? <Loader2 size={20} className="spinner" /> : <Send size={20} />}
          </button>
        </form>
      </div>
    </div>
  );
}
