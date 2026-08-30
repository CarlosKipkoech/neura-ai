import {
  createContext,
  useCallback,
  useContext,
  useState,
  type ReactNode,
} from 'react'
import type { ChatMessage, Conversation, SourceDocument } from '@/types'
import { generateId } from '@/lib/utils'
import { sendChatMessage } from '@/lib/api'
import { useAuth } from '@/context/AuthContext'

interface ChatContextType {
  conversations: Conversation[]
  activeConversation: Conversation | null
  activeConversationId: string | null
  isStreaming: boolean
  sourcesPanelOpen: boolean
  activeSources: SourceDocument[]
  sidebarCollapsed: boolean
  setSidebarCollapsed: (v: boolean) => void
  setSourcesPanelOpen: (v: boolean) => void
  setActiveSources: (sources: SourceDocument[]) => void
  selectConversation: (id: string) => void
  createConversation: () => string
  sendMessage: (content: string) => Promise<void>
  toggleSourcesPanel: () => void
}

const ChatContext = createContext<ChatContextType | null>(null)

export function ChatProvider({ children }: { children: ReactNode }) {
  const { token } = useAuth()
  const [conversations, setConversations] = useState<Conversation[]>([])
  const [activeConversationId, setActiveConversationId] = useState<string | null>(null)
  const [isStreaming, setIsStreaming] = useState(false)
  const [sourcesPanelOpen, setSourcesPanelOpen] = useState(true)
  const [activeSources, setActiveSources] = useState<SourceDocument[]>([])
  const [sidebarCollapsed, setSidebarCollapsed] = useState(false)

  const activeConversation =
    conversations.find((c) => c.id === activeConversationId) ?? null

  const selectConversation = useCallback((id: string) => {
    setActiveConversationId(id)
    const conv = conversations.find((c) => c.id === id)
    const lastAssistant = [...(conv?.messages ?? [])]
      .reverse()
      .find((m) => m.role === 'assistant')
    setActiveSources(lastAssistant?.sources ?? [])
  }, [conversations])

  const createConversation = useCallback(() => {
    const id = generateId()
    const newConv: Conversation = {
      id,
      title: 'New Conversation',
      messages: [],
      createdAt: new Date(),
      updatedAt: new Date(),
    }
    setConversations((prev) => [newConv, ...prev])
    setActiveConversationId(id)
    setActiveSources([])
    return id
  }, [])

  const normalizeSources = useCallback((sources: unknown[]): SourceDocument[] => {
    if (!Array.isArray(sources)) return []

    return sources.map((item, index) => {
      if (typeof item === 'object' && item !== null) {
        const source = item as Record<string, unknown>
        return {
          id: typeof source.id === 'string' ? source.id : `source-${index + 1}`,
          title: typeof source.title === 'string' ? source.title : `Source ${index + 1}`,
          department: typeof source.department === 'string' ? source.department : 'Knowledge Base',
          content: typeof source.content === 'string' ? source.content : JSON.stringify(source),
          confidence: typeof source.confidence === 'number' ? source.confidence : 0.85,
          page: typeof source.page === 'number' ? source.page : undefined,
          lastUpdated: typeof source.lastUpdated === 'string' ? source.lastUpdated : undefined,
          source: typeof source.source === 'string' ? source.source : undefined,
          classification: typeof source.classification === 'string' ? source.classification : undefined,
          allowedRoles: Array.isArray(source.allowedRoles)
            ? source.allowedRoles.filter((role): role is string => typeof role === 'string')
            : undefined,
        }
      }

      return {
        id: `source-${index + 1}`,
        title: `Source ${index + 1}`,
        department: 'Knowledge Base',
        content: String(item),
        confidence: 0.8,
      }
    })
  }, [])

  const sendMessage = useCallback(
    async (content: string) => {
      if (!content.trim() || isStreaming) return

      let convId = activeConversationId
      if (!convId) {
        convId = createConversation()
      }

      const userMsg: ChatMessage = {
        id: generateId(),
        role: 'user',
        content: content.trim(),
        timestamp: new Date(),
      }

      const assistantMsgId = generateId()
      const assistantMsg: ChatMessage = {
        id: assistantMsgId,
        role: 'assistant',
        content: '',
        timestamp: new Date(),
        isStreaming: true,
      }

      setConversations((prev) =>
        prev.map((c) =>
          c.id === convId
            ? {
                ...c,
                title: c.messages.length === 0 ? content.trim().slice(0, 40) : c.title,
                messages: [...c.messages, userMsg, assistantMsg],
                updatedAt: new Date(),
              }
            : c,
        ),
      )

      setIsStreaming(true)

      try {
        if (!token) {
          throw new Error('Missing auth token')
        }

        const data = await sendChatMessage(token, content.trim())
        const answer = typeof data?.answer === 'string' ? data.answer : 'I could not generate a response right now.'
        const sources = normalizeSources(Array.isArray(data?.sources) ? data.sources : [])

        setConversations((prev) =>
          prev.map((c) =>
            c.id === convId
              ? {
                  ...c,
                  messages: c.messages.map((m) =>
                    m.id === assistantMsgId
                      ? { ...m, content: answer, isStreaming: false, sources }
                      : m,
                  ),
                }
              : c,
          ),
        )
        setActiveSources(sources)
      } catch (error) {
        const fallback = 'I hit an issue while contacting the enterprise knowledge service. Please try again in a moment.'
        setConversations((prev) =>
          prev.map((c) =>
            c.id === convId
              ? {
                  ...c,
                  messages: c.messages.map((m) =>
                    m.id === assistantMsgId ? { ...m, content: fallback, isStreaming: false } : m,
                  ),
                }
              : c,
          ),
        )
        console.error('Chat request failed', error)
      } finally {
        setIsStreaming(false)
      }
    },
    [activeConversationId, createConversation, isStreaming, normalizeSources, token],
  )

  const toggleSourcesPanel = () => setSourcesPanelOpen((v) => !v)

  return (
    <ChatContext.Provider
      value={{
        conversations,
        activeConversation,
        activeConversationId,
        isStreaming,
        sourcesPanelOpen,
        activeSources,
        sidebarCollapsed,
        setSidebarCollapsed,
        setSourcesPanelOpen,
        setActiveSources,
        selectConversation,
        createConversation,
        sendMessage,
        toggleSourcesPanel,
      }}
    >
      {children}
    </ChatContext.Provider>
  )
}

export function useChat() {
  const ctx = useContext(ChatContext)
  if (!ctx) throw new Error('useChat must be used within ChatProvider')
  return ctx
}
