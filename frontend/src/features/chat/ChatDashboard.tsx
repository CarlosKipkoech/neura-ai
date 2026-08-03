import { useChat } from '@/context/ChatContext'
import { Sidebar } from './Sidebar'
import { ChatInterface } from './ChatInterface'
import { SourcePanel } from './SourcePanel'

export function ChatDashboard() {
  const { sourcesPanelOpen, activeSources, setSourcesPanelOpen } = useChat()

  return (
    <div className="h-screen flex bg-[var(--bg-primary)] gradient-mesh">
      <Sidebar />
      <main className="flex-1 flex min-w-0">
        <ChatInterface />
        <SourcePanel
          sources={activeSources}
          isOpen={sourcesPanelOpen}
          onClose={() => setSourcesPanelOpen(false)}
        />
      </main>
    </div>
  )
}
