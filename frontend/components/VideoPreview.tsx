'use client'

import { Video as VideoIcon, Download, Share2 } from 'lucide-react'

interface VideoPreviewProps {
  videoUrl: string | null
}

export default function VideoPreview({ videoUrl }: VideoPreviewProps) {
  const handleDownload = () => {
    if (videoUrl) {
      const a = document.createElement('a')
      a.href = videoUrl
      a.download = 'tiktok-video.mp4'
      document.body.appendChild(a)
      a.click()
      document.body.removeChild(a)
    }
  }

  const handleShare = async () => {
    if (videoUrl && navigator.share) {
      try {
        await navigator.share({
          title: 'My AI-Generated TikTok',
          text: 'Check out this video I made with AI!',
          url: videoUrl,
        })
      } catch (err) {
        console.error('Share failed:', err)
      }
    }
  }

  return (
    <div className="glass rounded-2xl p-6 space-y-6 neon-border">
      <div className="flex items-center gap-3">
        <div className="p-2 rounded-lg bg-gradient-to-br from-primary/20 to-secondary/20">
          <VideoIcon className="w-6 h-6 text-primary" />
        </div>
        <h2 className="text-2xl font-bold text-white">Video Preview</h2>
      </div>

      <div className="relative aspect-[9/16] bg-surface/50 rounded-xl overflow-hidden border border-white/10">
        {videoUrl ? (
          <video
            src={videoUrl}
            controls
            className="w-full h-full object-cover"
            autoPlay
            loop
          />
        ) : (
          <div className="absolute inset-0 flex flex-col items-center justify-center text-gray-500 space-y-4">
            <VideoIcon className="w-16 h-16 opacity-50" />
            <p className="text-lg">Your video will appear here</p>
            <p className="text-sm">Enter a topic and generate your video</p>
          </div>
        )}
      </div>

      {videoUrl && (
        <div className="flex gap-3">
          <button
            onClick={handleDownload}
            className="flex-1 py-3 px-4 bg-surface/80 border border-primary/50 rounded-xl font-medium text-white hover:bg-primary/20 transition-all flex items-center justify-center gap-2"
          >
            <Download className="w-5 h-5" />
            Download
          </button>
          <button
            onClick={handleShare}
            className="flex-1 py-3 px-4 bg-surface/80 border border-secondary/50 rounded-xl font-medium text-white hover:bg-secondary/20 transition-all flex items-center justify-center gap-2"
          >
            <Share2 className="w-5 h-5" />
            Share
          </button>
        </div>
      )}
    </div>
  )
}
