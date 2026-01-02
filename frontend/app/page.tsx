'use client'

import { useState } from 'react'
import ScriptGenerator from '@/components/ScriptGenerator'
import VideoPreview from '@/components/VideoPreview'
import StatusIndicator from '@/components/StatusIndicator'
import { Wand2, Video, Zap } from 'lucide-react'

type ProcessingStatus = 'idle' | 'generating-script' | 'generating-audio' | 'assembling-video' | 'complete' | 'error'

export default function Home() {
  const [status, setStatus] = useState<ProcessingStatus>('idle')
  const [videoUrl, setVideoUrl] = useState<string | null>(null)
  const [script, setScript] = useState<string | null>(null)
  const [error, setError] = useState<string | null>(null)

  const handleGenerate = async (text: string, isCustom: boolean) => {
    setStatus('generating-script')
    setError(null)

    const isMobile = typeof window !== 'undefined' && /iPhone|iPad|iPod|Android/i.test(window.navigator.userAgent)
    const baseUrl = process.env.NEXT_PUBLIC_API_URL || (isMobile ? 'http://192.168.1.169:8000' : 'http://localhost:8000')

    try {
      const response = await fetch(`${baseUrl}/generate-video`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ 
          text,
          is_custom: isCustom 
        }),
      })

      if (!response.ok) {
        throw new Error('Failed to generate video')
      }

      const data = await response.json()
      setScript(data.script)
      const mobileVideoUrl = data.video_url.replace('http://localhost:8000', baseUrl)
      setVideoUrl(mobileVideoUrl)
      setStatus('complete')
    } catch (err) {
      setError(err instanceof Error ? err.message : 'An error occurred')
      setStatus('error')
    }
  }

  const statusSteps = [
    { key: 'generating-script', label: 'Preparing Script', icon: Wand2 },
    { key: 'generating-audio', label: 'Creating Voiceover', icon: Zap },
    { key: 'assembling-video', label: 'Assembling Video', icon: Video },
  ]

  return (
    <main className="container mx-auto px-4 py-8 max-w-6xl">
      <header className="text-center mb-12">
        <div className="inline-flex items-center gap-2 mb-4">
          <div className="p-3 rounded-2xl bg-gradient-to-br from-primary/20 to-secondary/20 border border-primary/30">
            <Video className="w-8 h-8 text-primary" />
          </div>
          <h1 className="text-5xl font-bold neon-text">
            Text-to-TikTok
          </h1>
        </div>
        <p className="text-gray-400 text-lg max-w-2xl mx-auto">
          Transform your text into viral TikTok videos. Write your own script or let AI generate one from your topic.
        </p>
      </header>

      <div className="grid lg:grid-cols-2 gap-8">
        <div className="space-y-6">
          <ScriptGenerator 
            onGenerate={handleGenerate} 
            isProcessing={status !== 'idle' && status !== 'complete' && status !== 'error'}
          />
          
          {status !== 'idle' && (
            <StatusIndicator 
              status={status} 
              steps={statusSteps}
              error={error}
            />
          )}
          
          {script && (
            <div className="glass rounded-2xl p-6 space-y-4">
              <h3 className="text-xl font-semibold text-white flex items-center gap-2">
                <Wand2 className="w-5 h-5 text-secondary" />
                Script
              </h3>
              <div className="bg-surface/50 rounded-xl p-4 border border-white/10">
                <p className="text-gray-300 whitespace-pre-wrap leading-relaxed">
                  {script}
                </p>
              </div>
            </div>
          )}
        </div>

        <div className="space-y-6">
          <VideoPreview videoUrl={videoUrl} />
        </div>
      </div>
    </main>
  )
}
