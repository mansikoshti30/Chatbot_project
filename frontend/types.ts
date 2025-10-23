
export enum Role {
  USER = 'user',
  MODEL = 'model',
}

export interface Message {
  role: Role;
  text: string;
  sources?: { uri: string; title: string }[];
}

export interface Conversation {
  id: string;
  title: string;
  messages: Message[];
}
