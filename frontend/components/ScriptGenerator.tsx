'use client'

import { useState } from 'react'
import { Send, Sparkles, Type } from 'lucide-react'

interface ScriptGeneratorProps {
  onGenerate: (text: string, isCustom: boolean) => void
  isProcessing: boolean
}

export default function ScriptGenerator({ onGenerate, isProcessing }: ScriptGeneratorProps) {
  const [text, setText] = useState('')
  const [mode, setMode] = useState<'topic' | 'custom'>('custom')

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault()
    if (text.trim()) {
      onGenerate(text.trim(), mode === 'custom')
    }
  }

  return (
    <div className="glass rounded-2xl p-6 space-y-6 neon-border">
      <div className="flex items-center justify-between">
        <div className="flex items-center gap-3">
          <div className="p-2 rounded-lg bg-gradient-to-br from-primary/20 to-secondary/20">
            <Sparkles className="w-6 h-6 text-primary" />
          </div>
          <h2 className="text-2xl font-bold text-white">Create TikTok Video</h2>
        </div>
        
        <div className="flex gap-3">
          <button
            type="button"
            onClick={() => setMode('topic')}
            className={`px-5 py-2.5 rounded-xl text-sm font-semibold transition-all ${
              mode === 'topic'
                ? 'bg-primary text-white shadow-lg shadow-primary/30 border-2 border-primary'
                : 'bg-surface/30 text-gray-500 border border-white/10 hover:border-white/30'
            }`}
          >
            AI Generate
          </button>
          <button
            type="button"
            onClick={() => setMode('custom')}
            className={`px-5 py-2.5 rounded-xl text-sm font-semibold transition-all flex items-center gap-2 ${
              mode === 'custom'
                ? 'bg-secondary text-white shadow-lg shadow-secondary/30 border-2 border-secondary'
                : 'bg-surface/30 text-gray-500 border border-white/10 hover:border-white/30'
            }`}
          >
            <Type className="w-4 h-4" />
            Write Your Own
          </button>
        </div>
      </div>

      <form onSubmit={handleSubmit} className="space-y-4">
        <div className="space-y-2">
          <label htmlFor="text" className="text-sm font-medium text-gray-300">
            {mode === 'topic' ? 'Enter your topic' : 'Write your custom script'}
          </label>
          <textarea
            id="text"
            value={text}
            onChange={(e) => setText(e.target.value)}
            placeholder={
              mode === 'topic'
                ? "e.g., 'How to become a morning person', '5 productivity hacks', 'The science of happiness'..."
                : "Write your own script here. This will be converted to speech and displayed as subtitles in your video..."
            }
            className="w-full h-32 px-4 py-3 bg-surface/50 border border-white/20 rounded-xl text-white placeholder-gray-500 focus:outline-none focus:ring-2 focus:ring-primary/50 focus:border-primary transition-all resize-none"
            disabled={isProcessing}
          />
        </div>

        <button
          type="submit"
          disabled={isProcessing || !text.trim()}
          className="w-full py-4 px-6 bg-gradient-to-r from-primary via-secondary to-accent rounded-xl font-semibold text-white shadow-neon hover:shadow-neon-strong transform hover:scale-[1.02] transition-all duration-300 disabled:opacity-50 disabled:cursor-not-allowed disabled:transform-none flex items-center justify-center gap-2"
        >
          {isProcessing ? (
            <>
              <div className="w-5 h-5 border-2 border-white/30 border-t-white rounded-full animate-spin" />
              Creating Video...
            </>
          ) : (
            <>
              <Send className="w-5 h-5" />
              {mode === 'topic' ? 'Generate with AI' : 'Create Video'}
            </>
          )}
        </button>
      </form>

      <div className="grid grid-cols-3 gap-3 text-center">
        <div className="glass-strong rounded-lg p-3">
          <div className="text-2xl font-bold text-primary">15s</div>
          <div className="text-xs text-gray-400">Duration</div>
        </div>
        <div className="glass-strong rounded-lg p-3">
          <div className="text-2xl font-bold text-secondary">{mode === 'topic' ? 'AI' : 'Custom'}</div>
          <div className="text-xs text-gray-400">Script</div>
        </div>
        <div className="glass-strong rounded-lg p-3">
          <div className="text-2xl font-bold text-accent">HD</div>
          <div className="text-xs text-gray-400">Quality</div>
        </div>
      </div>
    </div>
  )
}
