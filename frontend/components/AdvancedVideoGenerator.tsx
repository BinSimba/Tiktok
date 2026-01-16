'use client'

import { useState } from 'react'
import { Send, Film, Zap, Sparkles, Settings, ChevronDown, ChevronUp } from 'lucide-react'

interface AdvancedVideoGeneratorProps {
  onGenerate: (params: any) => void
  isProcessing: boolean
}

export default function AdvancedVideoGenerator({ onGenerate, isProcessing }: AdvancedVideoGeneratorProps) {
  const [text, setText] = useState('')
  const [showSettings, setShowSettings] = useState(false)
  const [videoType, setVideoType] = useState('cinematic')
  const [style, setStyle] = useState('cinematic')
  const [characterType, setCharacterType] = useState('person')
  const [emotion, setEmotion] = useState('neutral')
  const [quality, setQuality] = useState('low')
  const [cameraMovement, setCameraMovement] = useState('static')
  const [duration, setDuration] = useState(5.0)

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault()
    if (text.trim()) {
      onGenerate({
        text: text.trim(),
        is_custom: true,
        video_type: videoType,
        style,
        character_type: characterType,
        emotion,
        quality,
        camera_movement: cameraMovement,
        duration
      })
    }
  }

  return (
    <div className="space-y-6">
      <h1 className="text-4xl font-bold text-white">Advanced AI Video</h1>
      
      <form onSubmit={handleSubmit} className="space-y-4">
        <div className="space-y-2">
          <label htmlFor="text" className="text-lg font-semibold text-gray-200">
            Describe your video
          </label>
          <textarea
            id="text"
            value={text}
            onChange={(e) => setText(e.target.value)}
            placeholder="Describe the scene, action, or story you want to create..."
            className="w-full h-48 px-5 py-4 bg-white/5 border-2 border-white/10 rounded-2xl text-white text-lg placeholder-gray-500 focus:outline-none focus:ring-2 focus:ring-violet-500/50 focus:border-violet-500 transition-all resize-none"
            disabled={isProcessing}
          />
        </div>

        <button
          type="button"
          onClick={() => setShowSettings(!showSettings)}
          className="w-full py-3 px-6 bg-white/5 border-2 border-white/10 rounded-xl font-medium text-white flex items-center justify-center gap-2 hover:bg-white/10 transition-all"
        >
          <Settings className="w-5 h-5" />
          {showSettings ? 'Hide' : 'Show'} Advanced Settings
          {showSettings ? <ChevronUp className="w-5 h-5" /> : <ChevronDown className="w-5 h-5" />}
        </button>

        {showSettings && (
          <div className="space-y-4 p-6 bg-white/5 border-2 border-white/10 rounded-2xl">
            <div className="grid md:grid-cols-2 gap-4">
              <div className="space-y-2">
                <label className="text-sm font-semibold text-gray-300">Video Type</label>
                <select
                  value={videoType}
                  onChange={(e) => setVideoType(e.target.value)}
                  className="w-full px-4 py-3 bg-white/5 border-2 border-white/10 rounded-xl text-white focus:outline-none focus:ring-2 focus:ring-violet-500/50 focus:border-violet-500"
                  disabled={isProcessing}
                  aria-label="Video Type"
                >
                  <option value="cinematic">Cinematic</option>
                  <option value="character">Character Animation</option>
                  <option value="hybrid">Hybrid (Character + Background)</option>
                </select>
              </div>

              <div className="space-y-2">
                <label className="text-sm font-semibold text-gray-300">Style</label>
                <select
                  value={style}
                  onChange={(e) => setStyle(e.target.value)}
                  className="w-full px-4 py-3 bg-white/5 border-2 border-white/10 rounded-xl text-white focus:outline-none focus:ring-2 focus:ring-violet-500/50 focus:border-violet-500"
                  disabled={isProcessing}
                  aria-label="Style"
                >
                  <option value="cinematic">Cinematic</option>
                  <option value="anime">Anime</option>
                  <option value="realistic">Realistic</option>
                  <option value="abstract">Abstract</option>
                  <option value="vintage">Vintage</option>
                  <option value="neon">Neon</option>
                  <option value="noir">Noir</option>
                  <option value="watercolor">Watercolor</option>
                </select>
              </div>

              {videoType === 'character' || videoType === 'hybrid' ? (
                <>
                  <div className="space-y-2">
                    <label className="text-sm font-semibold text-gray-300">Character</label>
                    <select
                      value={characterType}
                      onChange={(e) => setCharacterType(e.target.value)}
                      className="w-full px-4 py-3 bg-white/5 border-2 border-white/10 rounded-xl text-white focus:outline-none focus:ring-2 focus:ring-violet-500/50 focus:border-violet-500"
                      disabled={isProcessing}
                      aria-label="Character"
                    >
                      <option value="person">Person</option>
                      <option value="animal">Animal</option>
                      <option value="cartoon">Cartoon</option>
                      <option value="robot">Robot</option>
                      <option value="fantasy">Fantasy</option>
                    </select>
                  </div>

                  <div className="space-y-2">
                    <label className="text-sm font-semibold text-gray-300">Emotion</label>
                    <select
                      value={emotion}
                      onChange={(e) => setEmotion(e.target.value)}
                      className="w-full px-4 py-3 bg-white/5 border-2 border-white/10 rounded-xl text-white focus:outline-none focus:ring-2 focus:ring-violet-500/50 focus:border-violet-500"
                      disabled={isProcessing}
                      aria-label="Emotion"
                    >
                      <option value="neutral">Neutral</option>
                      <option value="happy">Happy</option>
                      <option value="sad">Sad</option>
                      <option value="angry">Angry</option>
                      <option value="surprised">Surprised</option>
                      <option value="excited">Excited</option>
                      <option value="calm">Calm</option>
                      <option value="confident">Confident</option>
                    </select>
                  </div>
                </>
              ) : null}

              <div className="space-y-2">
                <label className="text-sm font-semibold text-gray-300">Quality</label>
                <select
                  value={quality}
                  onChange={(e) => setQuality(e.target.value)}
                  className="w-full px-4 py-3 bg-white/5 border-2 border-white/10 rounded-xl text-white focus:outline-none focus:ring-2 focus:ring-violet-500/50 focus:border-violet-500"
                  disabled={isProcessing}
                  aria-label="Quality"
                >
                  <option value="speed">Speed (720p, 15fps)</option>
                  <option value="balanced">Balanced (1080p, 30fps)</option>
                  <option value="quality">Quality (1080p, 30fps)</option>
                  <option value="high">High (1440p, 30fps)</option>
                  <option value="ultra">Ultra (4K, 60fps)</option>
                </select>
              </div>

              <div className="space-y-2">
                <label className="text-sm font-semibold text-gray-300">Camera Movement</label>
                <select
                  value={cameraMovement}
                  onChange={(e) => setCameraMovement(e.target.value)}
                  className="w-full px-4 py-3 bg-white/5 border-2 border-white/10 rounded-xl text-white focus:outline-none focus:ring-2 focus:ring-violet-500/50 focus:border-violet-500"
                  disabled={isProcessing}
                  aria-label="Camera Movement"
                >
                  <option value="static">Static</option>
                  <option value="slow_zoom_in">Slow Zoom In</option>
                  <option value="slow_zoom_out">Slow Zoom Out</option>
                  <option value="pan_left">Pan Left</option>
                  <option value="pan_right">Pan Right</option>
                  <option value="tilt_up">Tilt Up</option>
                  <option value="tilt_down">Tilt Down</option>
                  <option value="orbit_left">Orbit Left</option>
                  <option value="orbit_right">Orbit Right</option>
                </select>
              </div>

              <div className="space-y-2 md:col-span-2">
                <label htmlFor="duration-slider" className="text-sm font-semibold text-gray-300">Duration: {duration}s</label>
                <input
                  id="duration-slider"
                  type="range"
                  min="3"
                  max="60"
                  step="0.5"
                  value={duration}
                  onChange={(e) => setDuration(parseFloat(e.target.value))}
                  className="w-full h-2 bg-white/10 rounded-lg appearance-none cursor-pointer accent-violet-500"
                  disabled={isProcessing}
                  aria-label="Duration"
                />
              </div>
            </div>
          </div>
        )}

        <button
          type="submit"
          disabled={isProcessing || !text.trim()}
          className="w-full py-4 px-8 bg-gradient-to-r from-violet-600 to-purple-600 rounded-2xl font-semibold text-white text-lg shadow-lg hover:shadow-xl transform hover:scale-[1.02] transition-all duration-300 disabled:opacity-50 disabled:cursor-not-allowed disabled:transform-none flex items-center justify-center gap-3"
        >
          {isProcessing ? (
            <>
              <div className="w-6 h-6 border-3 border-white/30 border-t-white rounded-full animate-spin" />
              Generating Advanced Video...
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
            <div className="text-xl font-bold text-white">{duration}s</div>
          </div>
          <div className="text-sm text-gray-400 font-medium">Duration</div>
        </div>
        <div className="text-center space-y-2">
          <div className="flex items-center justify-center gap-2 mb-2">
            <Zap className="w-5 h-5 text-violet-400" />
            <div className="text-xl font-bold text-white capitalize">{style}</div>
          </div>
          <div className="text-sm text-gray-400 font-medium">Style</div>
        </div>
        <div className="text-center space-y-2">
          <div className="flex items-center justify-center gap-2 mb-2">
            <Sparkles className="w-5 h-5 text-violet-400" />
            <div className="text-xl font-bold text-white capitalize">{quality}</div>
          </div>
          <div className="text-sm text-gray-400 font-medium">Quality</div>
        </div>
      </div>
    </div>
  )
}
