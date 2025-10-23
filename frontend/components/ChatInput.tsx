import React, { useState, useRef, useEffect } from 'react';
import { SendIcon, StopIcon } from './Icons';

interface ChatInputProps {
  onSendMessage: (message: string) => void;
  isLoading: boolean;
  conversationStarted: boolean;
  onStopGenerating: () => void;
}

const ChatInput: React.FC<ChatInputProps> = ({ onSendMessage, isLoading, conversationStarted, onStopGenerating }) => {
  const [input, setInput] = useState('');
  const textareaRef = useRef<HTMLTextAreaElement>(null);

  useEffect(() => {
    if (textareaRef.current) {
      textareaRef.current.style.height = 'auto';
      textareaRef.current.style.height = `${textareaRef.current.scrollHeight}px`;
    }
  }, [input]);

  const handleSend = () => {
    if (input.trim() && !isLoading) {
      onSendMessage(input.trim());
      setInput('');
    }
  };

  const handleKeyPress = (e: React.KeyboardEvent<HTMLTextAreaElement>) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSend();
    }
  };

  if (!conversationStarted) {
    // Welcome screen input style
    return (
      <div className="w-full max-w-3xl mx-auto">
        <div className="relative">
          <textarea
            ref={textareaRef}
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyPress={handleKeyPress}
            placeholder="Ask anything"
            disabled={isLoading}
            rows={1}
            className="w-full bg-slate-800 text-slate-100 p-4 pr-14 rounded-lg resize-none border border-slate-700 focus:outline-none focus:ring-2 focus:ring-blue-500 transition-shadow text-lg hide-scrollbar"
            style={{ maxHeight: '200px', overflowY: 'auto' }}
          />
          <button
            onClick={handleSend}
            disabled={isLoading || !input.trim()}
            className="absolute right-3 top-1/2 -translate-y-1/2 p-2 rounded-full text-slate-300 hover:bg-slate-700 disabled:text-slate-500 disabled:hover:bg-transparent transition-colors"
            aria-label="Send message"
          >
            <SendIcon />
          </button>
        </div>
      </div>
    );
  }

  // Default chat input style
  return (
    <div className="p-4 bg-slate-900 border-t border-slate-700">
      <div className="relative max-w-4xl mx-auto flex items-end gap-2">
        <textarea
          ref={textareaRef}
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyPress={handleKeyPress}
          placeholder="Ask me about anywhere in the world..."
          disabled={isLoading}
          rows={1}
          className="w-full bg-slate-800 text-slate-100 p-3 pr-12 rounded-lg resize-none border border-slate-700 focus:outline-none focus:ring-2 focus:ring-blue-500 transition-shadow hide-scrollbar"
          style={{ maxHeight: '200px', overflowY: 'auto' }}
        />
        {isLoading ? (
            <button
                onClick={onStopGenerating}
                className="p-2 rounded-full text-slate-300 bg-slate-700 hover:bg-slate-600 transition-colors"
                aria-label="Stop generating"
            >
                <StopIcon />
            </button>
        ) : (
            <button
                onClick={handleSend}
                disabled={!input.trim()}
                className="absolute right-3 top-1/2 -translate-y-1/2 p-2 rounded-full text-slate-300 hover:bg-slate-700 disabled:text-slate-500 disabled:hover:bg-transparent transition-colors"
                aria-label="Send message"
            >
                <SendIcon />
            </button>
        )}
      </div>
    </div>
  );
};

export default ChatInput;