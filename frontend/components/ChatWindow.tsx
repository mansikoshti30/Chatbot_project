import React, { useEffect, useRef } from 'react';
import { Message } from '../types';
import ChatMessage from './ChatMessage';
import { GlobeIcon } from './Icons';

interface ChatWindowProps {
  messages: Message[];
  isLoading: boolean;
}

const ChatWindow: React.FC<ChatWindowProps> = ({ messages, isLoading }) => {
  const messagesEndRef = useRef<HTMLDivElement>(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages, isLoading]);

  return (
    <div className="flex-1 overflow-y-auto p-4">
      <div className="max-w-4xl mx-auto">
        {messages.map((msg, index) => (
          <ChatMessage key={index} message={msg} />
        ))}
        {isLoading && (
          <div className="flex items-start gap-4 p-4 animate-fade-in-up">
            <div className="flex-shrink-0 h-8 w-8 rounded-full bg-slate-800 flex items-center justify-center text-white">
                <div className="animate-spin text-teal-500">
                    <GlobeIcon />
                </div>
            </div>
            <div className="max-w-xl md:max-w-2xl px-5 py-3 rounded-2xl bg-slate-700 text-slate-200 rounded-bl-none">
                <p className="text-slate-400">Thinking...</p>
            </div>
          </div>
        )}
        <div ref={messagesEndRef} />
      </div>
    </div>
  );
};

export default ChatWindow;