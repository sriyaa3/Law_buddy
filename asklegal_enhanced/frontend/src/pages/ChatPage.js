import React, { useState, useEffect, useRef } from 'react';
import styled from 'styled-components';
import { FaPaperPlane, FaRobot, FaUser, FaLightbulb } from 'react-icons/fa';
import ReactMarkdown from 'react-markdown';
import rehypeHighlight from 'rehype-highlight';
import 'highlight.js/styles/github.css';
import { chatApi } from '../services/api';

const PageContainer = styled.div`
  max-width: 1200px;
  margin: 0 auto;
`;

const PageTitle = styled.h1`
  color: #2c3e50;
  margin-bottom: 20px;
`;

const ChatContainer = styled.div`
  display: flex;
  flex-direction: column;
  height: calc(100vh - 150px);
  background: white;
  border-radius: 8px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
  overflow: hidden;
`;

const ChatMessages = styled.div`
  flex: 1;
  overflow-y: auto;
  padding: 20px;
  display: flex;
  flex-direction: column;
  gap: 15px;
`;

const Message = styled.div`
  display: flex;
  gap: 10px;
  max-width: 80%;
  
  ${props => props.isUser && `
    align-self: flex-end;
  `}
`;

const MessageAvatar = styled.div`
  font-size: 20px;
  color: #3498db;
  min-width: 30px;
`;

const MessageContent = styled.div`
  background: ${props => props.isUser ? '#3498db' : '#f1f2f6'};
  color: ${props => props.isUser ? 'white' : '#2c3e50'};
  padding: 12px 15px;
  border-radius: 18px;
  line-height: 1.6;
  
  h1, h2, h3 {
    margin-top: 15px;
    margin-bottom: 10px;
    color: ${props => props.isUser ? 'white' : '#2c3e50'};
  }
  
  h1 { font-size: 1.5em; }
  h2 { font-size: 1.3em; }
  h3 { font-size: 1.1em; }
  
  p {
    margin: 10px 0;
  }
  
  ul, ol {
    margin: 10px 0;
    padding-left: 25px;
  }
  
  li {
    margin: 5px 0;
  }
  
  strong {
    font-weight: 600;
  }
  
  code {
    background: ${props => props.isUser ? 'rgba(255, 255, 255, 0.2)' : 'rgba(0, 0, 0, 0.1)'};
    padding: 2px 6px;
    border-radius: 3px;
    font-family: 'Courier New', monospace;
    font-size: 0.9em;
  }
  
  pre {
    background: ${props => props.isUser ? 'rgba(255, 255, 255, 0.2)' : 'rgba(0, 0, 0, 0.05)'};
    padding: 10px;
    border-radius: 5px;
    overflow-x: auto;
    margin: 10px 0;
  }
  
  pre code {
    background: none;
    padding: 0;
  }
  
  table {
    border-collapse: collapse;
    width: 100%;
    margin: 10px 0;
  }
  
  th, td {
    border: 1px solid ${props => props.isUser ? 'rgba(255, 255, 255, 0.3)' : '#ddd'};
    padding: 8px;
    text-align: left;
  }
  
  th {
    background: ${props => props.isUser ? 'rgba(255, 255, 255, 0.2)' : 'rgba(0, 0, 0, 0.05)'};
    font-weight: 600;
  }
`;

const SuggestionContainer = styled.div`
  background: #e8f4fc;
  border-radius: 8px;
  padding: 15px;
  margin-top: 10px;
`;

const SuggestionTitle = styled.div`
  font-weight: 600;
  margin-bottom: 10px;
  display: flex;
  align-items: center;
  gap: 8px;
`;

const SuggestionList = styled.div`
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
`;

const SuggestionItem = styled.div`
  background: #3498db;
  color: white;
  padding: 8px 12px;
  border-radius: 20px;
  font-size: 13px;
  cursor: pointer;
  transition: background-color 0.2s;
  
  &:hover {
    background: #2980b9;
  }
`;

const InputContainer = styled.div`
  display: flex;
  padding: 20px;
  border-top: 1px solid #eee;
  background: white;
`;

const MessageInput = styled.input`
  flex: 1;
  padding: 12px 15px;
  border: 1px solid #ddd;
  border-radius: 25px;
  font-size: 14px;
  outline: none;
  
  &:focus {
    border-color: #3498db;
  }
`;

const SendButton = styled.button`
  background: #3498db;
  color: white;
  border: none;
  border-radius: 50%;
  width: 45px;
  height: 45px;
  margin-left: 10px;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: background-color 0.2s;
  
  &:hover {
    background: #2980b9;
  }
`;

const QuickActions = styled.div`
  display: flex;
  padding: 10px 20px;
  border-top: 1px solid #eee;
  background: #f8f9fa;
  gap: 10px;
`;

const ActionButton = styled.button`
  background: #ecf0f1;
  color: #2c3e50;
  border: none;
  border-radius: 20px;
  padding: 8px 15px;
  font-size: 13px;
  cursor: pointer;
  transition: background-color 0.2s;
  
  &:hover {
    background: #d5dbdb;
  }
`;

function ChatPage() {
  const [messages, setMessages] = useState([
    {
      id: 1,
      text: "Hello! I'm your AI Legal Assistant for MSMEs. I can help you with legal queries, compliance requirements, document generation, and more. How can I assist you today?",
      isUser: false,
      timestamp: new Date()
    }
  ]);
  const [inputMessage, setInputMessage] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const messagesEndRef = useRef(null);
  
  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };
  
  useEffect(() => {
    scrollToBottom();
  }, [messages]);
  
  const handleSendMessage = async () => {
    if (!inputMessage.trim() || isLoading) return;
    
    // Add user message
    const userMessage = {
      id: Date.now(),
      text: inputMessage,
      isUser: true,
      timestamp: new Date()
    };
    
    setMessages(prev => [...prev, userMessage]);
    setInputMessage('');
    setIsLoading(true);
    
    try {
      // Send to backend API
      const response = await chatApi.sendMessage(inputMessage, 'default_chat');
      
      // Add AI response
      const aiMessage = {
        id: Date.now() + 1,
        text: response.data.response,
        isUser: false,
        timestamp: new Date()
      };
      
      setMessages(prev => [...prev, aiMessage]);
    } catch (error) {
      console.error('Error sending message:', error);
      
      // Add error message
      const errorMessage = {
        id: Date.now() + 1,
        text: "Sorry, I encountered an error. Please try again.",
        isUser: false,
        timestamp: new Date()
      };
      
      setMessages(prev => [...prev, errorMessage]);
    } finally {
      setIsLoading(false);
    }
  };
  
  const handleKeyPress = (e) => {
    if (e.key === 'Enter') {
      handleSendMessage();
    }
  };
  
  const handleQuickAction = (action) => {
    setInputMessage(action);
  };
  
  const handleSuggestionClick = (suggestion) => {
    setInputMessage(suggestion);
  };
  
  return (
    <PageContainer>
      <PageTitle>Legal Chat Assistant</PageTitle>
      
      <ChatContainer>
        <ChatMessages>
          {messages.map((message) => (
            <div key={message.id}>
              <Message key={message.id} isUser={message.isUser}>
                <MessageAvatar>
                  {message.isUser ? <FaUser /> : <FaRobot />}
                </MessageAvatar>
                <MessageContent isUser={message.isUser}>
                  {message.isUser ? (
                    message.text
                  ) : (
                    <ReactMarkdown rehypePlugins={[rehypeHighlight]}>
                      {message.text}
                    </ReactMarkdown>
                  )}
                </MessageContent>
              </Message>
              
              {/* Show suggestions for the initial welcome message */}
              {!message.isUser && messages.length === 1 && (
                <SuggestionContainer>
                  <SuggestionTitle>
                    <FaLightbulb /> Quick Questions You Can Ask:
                  </SuggestionTitle>
                  <SuggestionList>
                    <SuggestionItem onClick={() => handleSuggestionClick("What are the GST requirements for small businesses?")}>
                      GST Requirements
                    </SuggestionItem>
                    <SuggestionItem onClick={() => handleSuggestionClick("How to register a trademark for my business?")}>
                      Trademark Registration
                    </SuggestionItem>
                    <SuggestionItem onClick={() => handleSuggestionClick("What employment laws apply to my business?")}>
                      Employment Laws
                    </SuggestionItem>
                    <SuggestionItem onClick={() => handleSuggestionClick("How to create a vendor agreement?")}>
                      Vendor Agreement
                    </SuggestionItem>
                  </SuggestionList>
                </SuggestionContainer>
              )}
            </div>
          ))}
          {isLoading && (
            <Message isUser={false}>
              <MessageAvatar>
                <FaRobot />
              </MessageAvatar>
              <MessageContent isUser={false}>
                Thinking...
              </MessageContent>
            </Message>
          )}
          <div ref={messagesEndRef} />
        </ChatMessages>
        
        <QuickActions>
          <ActionButton onClick={() => handleQuickAction("Generate an NDA")}>
            Generate NDA
          </ActionButton>
          <ActionButton onClick={() => handleQuickAction("Check compliance requirements")}>
            Check Compliance
          </ActionButton>
          <ActionButton onClick={() => handleQuickAction("Analyze this contract")}>
            Analyze Contract
          </ActionButton>
        </QuickActions>
        
        <InputContainer>
          <MessageInput
            value={inputMessage}
            onChange={(e) => setInputMessage(e.target.value)}
            onKeyPress={handleKeyPress}
            placeholder="Ask a legal question or request document generation..."
            disabled={isLoading}
          />
          <SendButton onClick={handleSendMessage} disabled={isLoading}>
            <FaPaperPlane />
          </SendButton>
        </InputContainer>
      </ChatContainer>
    </PageContainer>
  );
}

export default ChatPage;