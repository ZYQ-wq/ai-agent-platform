export interface ProjectFile {
  path: string
  language: string
  content: string
}

export interface CodingProject {
  id: string
  name: string
  files: ProjectFile[]
}

export interface ChatMessage {
  role: 'user' | 'assistant'
  content: string
}