'use client'

import { useState } from 'react'
import { Send, Film, Zap, Sparkles } from 'lucide-react'

interface ScriptGeneratorProps {
  onGenerate: (text: string) => void
  isProcessing: boolean
}

export default function ScriptGenerator({ onGenerate, isProcessing }: ScriptGeneratorProps) {
  const [text, setText] = useState('')

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault()
    if (text.trim()) {
      onGenerate(text.trim())
    }
  }

  return (
    <div className="space-y-6">
      <h1 className="text-4xl font-bold text-white">Script to Video</h1>
      
      <form onSubmit={handleSubmit} className="space-y-4">
        <div className="space-y-2">
          <label htmlFor="text" className="text-lg font-semibold text-gray-200">
            Write your custom script
          </label>
          <textarea
            id="text"
            value={text}
            onChange={(e) => setText(e.target.value)}
            placeholder="Enter a topic and generate your video..."
            className="w-full h-48 px-5 py-4 bg-white/5 border-2 border-white/10 rounded-2xl text-white text-lg placeholder-gray-500 focus:outline-none focus:ring-2 focus:ring-violet-500/50 focus:border-violet-500 transition-all resize-none"
            disabled={isProcessing}
          />
        </div>

        <button
          type="submit"
          disabled={isProcessing || !text.trim()}
          className="w-full py-4 px-8 bg-gradient-to-r from-violet-600 to-purple-600 rounded-2xl font-semibold text-white text-lg shadow-lg hover:shadow-xl transform hover:scale-[1.02] transition-all duration-300 disabled:opacity-50 disabled:cursor-not-allowed disabled:transform-none flex items-center justify-center gap-3"
        >
          {isProcessing ? (
            <>
              <div className="w-6 h-6 border-3 border-white/30 border-t-white rounded-full animate-spin" />
              Generating...
            </>
          ) : (
            <>
              <Send className="w-6 h-6" />
              Generate Video
            </>
          )}
        </button>
      </form>

      <div className="grid grid-cols-3 gap-6 pt-6 border-t border-white/10">
        <div className="text-center space-y-2">
          <div className="flex items-center justify-center gap-2 mb-2">
            <Film className="w-5 h-5 text-violet-400" />
            <div className="text-xl font-bold text-white">15s</div>
          </div>
          <div className="text-sm text-gray-400 font-medium">Duration</div>
        </div>
        <div className="text-center space-y-2">
          <div className="flex items-center justify-center gap-2 mb-2">
            <Zap className="w-5 h-5 text-violet-400" />
            <div className="text-xl font-bold text-white">Custom</div>
          </div>
          <div className="text-sm text-gray-400 font-medium">Script</div>
        </div>
        <div className="text-center space-y-2">
          <div className="flex items-center justify-center gap-2 mb-2">
            <Sparkles className="w-5 h-5 text-violet-400" />
            <div className="text-xl font-bold text-white">HD</div>
          </div>
          <div className="text-sm text-gray-400 font-medium">Quality</div>
        </div>
      </div>
    </div>
  )
}
