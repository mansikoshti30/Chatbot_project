import React, { useState, useEffect, useRef } from 'react';
import ChatHistory from './components/ChatHistory';
import ChatWindow from './components/ChatWindow';
import ChatInput from './components/ChatInput';
import { Conversation, Message, Role } from './types';

const App: React.FC = () => {
  const [conversations, setConversations] = useState<Conversation[]>([]);
  const [activeConversationId, setActiveConversationId] = useState<string | null>(null);
  const [isLoading, setIsLoading] = useState(false);
  const timeoutRef = useRef<number | null>(null);

  useEffect(() => {
    // Start with a new, empty conversation on initial load
    handleNewConversation();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  const activeConversation = conversations.find(c => c.id === activeConversationId);
  
  const conversationStarted = activeConversation ? activeConversation.messages.length > 0 : false;

  useEffect(() => {
    return () => {
      if (timeoutRef.current) {
        clearTimeout(timeoutRef.current);
      }
    };
  }, []);

  const handleSendMessage = async (text: string) => {
    if (!activeConversationId) return;

    const newMessage: Message = { role: Role.USER, text };
    
    // Update the conversation with the user's message
    const updatedConversations = conversations.map(convo => {
        if (convo.id === activeConversationId) {
            // If it's the first message, create a title
            const title = convo.messages.length === 0 ? text.substring(0, 30) : convo.title;
            return { ...convo, title: title, messages: [...convo.messages, newMessage] };
        }
        return convo;
    });
    setConversations(updatedConversations);
    setIsLoading(true);

    // Simulate a bot response
    timeoutRef.current = window.setTimeout(() => {
        const botMessage: Message = {
            role: Role.MODEL,
            text: `This is a simulated response to: "${text}". The backend service is not connected.`,
            sources: [
                { title: 'Simulated Location 1', uri: '#' },
                { title: 'Simulated Location 2', uri: '#' }
            ]
        };
        const finalConversations = conversations.map(convo => {
            if (convo.id === activeConversationId) {
                return { ...convo, messages: [...convo.messages, newMessage, botMessage] };
            }
            return convo;
        });
        setConversations(finalConversations);
        setIsLoading(false);
    }, 1500);
  };

  const handleNewConversation = () => {
    const newId = `convo-${Date.now()}`;
    const newConversation: Conversation = {
      id: newId,
      title: 'New Chat',
      messages: [],
    };
    setConversations(prev => [newConversation, ...prev]);
    setActiveConversationId(newId);
  };

  const handleSelectConversation = (id: string) => {
    setActiveConversationId(id);
  };
  
  const handleStopGenerating = () => {
      if (timeoutRef.current) {
          clearTimeout(timeoutRef.current);
      }
      setIsLoading(false);
  };

  return (
    <div className="flex h-screen bg-slate-900 text-slate-100">
      <ChatHistory
        conversations={conversations}
        activeConversationId={activeConversationId}
        onSelectConversation={handleSelectConversation}
        onNewConversation={handleNewConversation}
      />
      <div className="flex-1 flex flex-col">
        {conversationStarted ? (
          <>
            <ChatWindow messages={activeConversation?.messages || []} isLoading={isLoading} />
            <ChatInput 
                onSendMessage={handleSendMessage} 
                isLoading={isLoading} 
                conversationStarted={conversationStarted}
                onStopGenerating={handleStopGenerating}
            />
          </>
        ) : (
          <div className="flex-1 flex flex-col items-center justify-center p-4">
             <div className="w-full max-w-3xl text-center">
                <h1 className="text-4xl font-bold text-slate-300 mb-8">Hello! How can I Help you ?</h1>
                <ChatInput 
                    onSendMessage={handleSendMessage} 
                    isLoading={isLoading} 
                    conversationStarted={conversationStarted}
                    onStopGenerating={handleStopGenerating}
                />
             </div>
          </div>
        )}
      </div>
    </div>
  );
};

export default App;
