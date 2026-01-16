'use client'

import { Video as VideoIcon, Play } from 'lucide-react'

interface VideoPreviewProps {
  videoUrl: string | null
}

export default function VideoPreview({ videoUrl }: VideoPreviewProps) {
  return (
    <div className="space-y-6">
      <h2 className="text-2xl font-bold text-white">Video Preview</h2>
      
      <div className="relative aspect-[9/16] bg-slate-900/50 rounded-2xl overflow-hidden border-2 border-white/10 flex items-center justify-center">
        {videoUrl ? (
          <video
            src={videoUrl}
            controls
            className="w-full h-full object-cover"
            autoPlay
            loop
          />
        ) : (
          <div className="absolute inset-0 flex flex-col items-center justify-center text-gray-500 space-y-6 bg-gradient-to-br from-slate-900/80 to-slate-800/80">
            <div className="w-24 h-24 rounded-full bg-white/5 flex items-center justify-center">
              <Play className="w-12 h-12 text-gray-400 ml-1" />
            </div>
            <div className="text-center space-y-2">
              <p className="text-2xl font-semibold text-white">Your video will appear here</p>
              <p className="text-base text-gray-400">Enter a topic to generate your video</p>
            </div>
          </div>
        )}
      </div>
    </div>
  )
}
