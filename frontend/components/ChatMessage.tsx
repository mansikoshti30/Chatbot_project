import React from 'react';
import { Message, Role } from '../types';
import { UserIcon, GlobeIcon, MapPinIcon } from './Icons';

interface ChatMessageProps {
  message: Message;
}

const ChatMessage: React.FC<ChatMessageProps> = ({ message }) => {
  const isUser = message.role === Role.USER;

  return (
    <div className={`flex items-start gap-4 p-4 animate-fade-in-up ${isUser ? 'justify-end' : ''}`}>
      {!isUser && (
        <div className="flex-shrink-0 h-8 w-8 rounded-full bg-teal-600 flex items-center justify-center text-white">
          <GlobeIcon />
        </div>
      )}
      <div className={`max-w-xl md:max-w-2xl px-5 py-3 rounded-2xl ${isUser ? 'bg-blue-700 text-white rounded-br-none' : 'bg-slate-700 text-slate-200 rounded-bl-none'}`}>
        <p className="whitespace-pre-wrap">{message.text}</p>
        {message.sources && message.sources.length > 0 && (
          <div className="mt-3 pt-3 border-t border-slate-600">
            <h3 className="text-xs font-semibold text-slate-400 mb-1">Sources:</h3>
            <ul className="space-y-1">
              {message.sources.map((source, index) => (
                <li key={index}>
                  <a
                    href={source.uri}
                    target="_blank"
                    rel="noopener noreferrer"
                    className="text-blue-400 hover:text-blue-300 text-sm flex items-center"
                  >
                    <MapPinIcon />
                    <span className="truncate">{source.title}</span>
                  </a>
                </li>
              ))}
            </ul>
          </div>
        )}
      </div>
      {isUser && (
        <div className="flex-shrink-0 h-8 w-8 rounded-full bg-slate-600 flex items-center justify-center text-white">
          <UserIcon />
        </div>
      )}
    </div>
  );
};

export default ChatMessage;