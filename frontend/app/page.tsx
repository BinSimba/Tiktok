'use client'

import { useState } from 'react'
import ScriptGenerator from '@/components/ScriptGenerator'
import AdvancedVideoGenerator from '@/components/AdvancedVideoGenerator'
import PhysicsVideoGenerator from '@/components/PhysicsVideoGenerator'
import VideoPreview from '@/components/VideoPreview'
import { Zap, Sparkles, Waves } from 'lucide-react'

export default function Home() {
  const [videoUrl, setVideoUrl] = useState<string | null>(null)
  const [isProcessing, setIsProcessing] = useState(false)
  const [mode, setMode] = useState<'script' | 'advanced' | 'physics'>('script')

  const handleScriptGenerate = async (text: string) => {
    setIsProcessing(true)
    setVideoUrl(null)

    const baseUrl = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'

    try {
      const response = await fetch(`${baseUrl}/generate-advanced-video`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ 
          text,
          is_custom: true,
          video_type: 'cinematic',
          style: 'cinematic',
          quality: 'high',
          camera_movement: 'slow_zoom_in',
          duration: 10.0
        }),
      })

      if (!response.ok) {
        throw new Error('Failed to generate video')
      }

      const data = await response.json()
      setVideoUrl(data.video_url)
    } catch (err) {
      console.error('Error generating video:', err)
      alert('Failed to generate video. Please try again.')
    } finally {
      setIsProcessing(false)
    }
  }

  const handleAdvancedGenerate = async (params: any) => {
    setIsProcessing(true)
    setVideoUrl(null)

    const baseUrl = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'

    try {
      const response = await fetch(`${baseUrl}/generate-advanced-video`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(params),
      })

      if (!response.ok) {
        throw new Error('Failed to generate advanced video')
      }

      const data = await response.json()
      setVideoUrl(data.video_url)
    } catch (err) {
      console.error('Error generating advanced video:', err)
      alert('Failed to generate advanced video. Please try again.')
    } finally {
      setIsProcessing(false)
    }
  }

  const handlePhysicsGenerate = async (params: any) => {
    setIsProcessing(true)
    setVideoUrl(null)

    const baseUrl = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'

    try {
      const response = await fetch(`${baseUrl}/generate-physics-video`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(params),
      })

      if (!response.ok) {
        throw new Error('Failed to generate physics video')
      }

      const data = await response.json()
      setVideoUrl(data.video_url)
    } catch (err) {
      console.error('Error generating physics video:', err)
      alert('Failed to generate physics video. Please try again.')
    } finally {
      setIsProcessing(false)
    }
  }

  return (
    <main className="min-h-screen bg-gradient-to-br from-slate-950 via-slate-900 to-slate-950">
      <div className="container mx-auto px-6 py-12 max-w-7xl">
        <div className="mb-8 flex justify-center gap-4">
          <button
            onClick={() => setMode('script')}
            className={`px-6 py-3 rounded-xl font-semibold flex items-center gap-2 transition-all ${
              mode === 'script'
                ? 'bg-violet-600 text-white shadow-lg'
                : 'bg-white/5 text-gray-400 hover:bg-white/10'
            }`}
          >
            <Zap className="w-5 h-5" />
            Script to Video
          </button>
          <button
            onClick={() => setMode('advanced')}
            className={`px-6 py-3 rounded-xl font-semibold flex items-center gap-2 transition-all ${
              mode === 'advanced'
                ? 'bg-violet-600 text-white shadow-lg'
                : 'bg-white/5 text-gray-400 hover:bg-white/10'
            }`}
          >
            <Sparkles className="w-5 h-5" />
            Advanced AI
          </button>
          <button
            onClick={() => setMode('physics')}
            className={`px-6 py-3 rounded-xl font-semibold flex items-center gap-2 transition-all ${
              mode === 'physics'
                ? 'bg-blue-600 text-white shadow-lg'
                : 'bg-white/5 text-gray-400 hover:bg-white/10'
            }`}
          >
            <Waves className="w-5 h-5" />
            Physics
          </button>
        </div>

        <div className="grid lg:grid-cols-2 gap-12">
          <div className="flex flex-col justify-center">
            {mode === 'script' ? (
              <ScriptGenerator 
                onGenerate={handleScriptGenerate} 
                isProcessing={isProcessing}
              />
            ) : mode === 'advanced' ? (
              <AdvancedVideoGenerator
                onGenerate={handleAdvancedGenerate}
                isProcessing={isProcessing}
              />
            ) : (
              <PhysicsVideoGenerator
                onGenerate={handlePhysicsGenerate}
                isGenerating={isProcessing}
              />
            )}
          </div>

          <div className="flex flex-col justify-center">
            <VideoPreview videoUrl={videoUrl} />
          </div>
        </div>
      </div>
    </main>
  )
}
