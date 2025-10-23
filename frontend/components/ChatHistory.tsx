import React from 'react';
import { Conversation } from '../types';
import { GlobeIcon, PlusIcon } from './Icons';

interface ChatHistoryProps {
  conversations: Conversation[];
  activeConversationId: string | null;
  onSelectConversation: (id: string) => void;
  onNewConversation: () => void;
}

const ChatHistory: React.FC<ChatHistoryProps> = ({
  conversations,
  activeConversationId,
  onSelectConversation,
  onNewConversation,
}) => {
  return (
    <div className="w-80 bg-slate-800 text-slate-100 flex flex-col p-4 border-r border-slate-700">
      <div className="flex items-center mb-6">
        <div className="flex-shrink-0 h-10 w-10 rounded-lg bg-teal-600 flex items-center justify-center text-white">
          <GlobeIcon />
        </div>
        <h1 className="text-2xl font-bold ml-3">Geospatial World</h1>
      </div>
      <button
        onClick={onNewConversation}
        className="flex items-center justify-center w-full p-2 mb-4 text-left bg-blue-600 hover:bg-blue-700 rounded-lg transition-colors"
      >
        <PlusIcon />
        <span className="ml-2">New Chat</span>
      </button>
      <div className="flex-grow overflow-y-auto hide-scrollbar">
        <h2 className="text-sm font-semibold text-slate-400 mb-2 uppercase tracking-wider">Recent</h2>
        <ul>
          {conversations.map((convo) => (
            <li key={convo.id} className="mb-2">
              <button
                onClick={() => onSelectConversation(convo.id)}
                className={`w-full text-left p-2 rounded-lg truncate transition-colors ${
                  activeConversationId === convo.id
                    ? 'bg-slate-700 border-l-4 border-blue-500 pl-3'
                    : 'border-l-4 border-transparent hover:bg-slate-600'
                }`}
              >
                {convo.title}
              </button>
            </li>
          ))}
        </ul>
      </div>
    </div>
  );
};

export default ChatHistory;