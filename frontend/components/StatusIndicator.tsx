'use client'

import { LucideIcon, CheckCircle2, XCircle, Loader2 } from 'lucide-react'

interface StatusStep {
  key: string
  label: string
  icon: LucideIcon
}

interface StatusIndicatorProps {
  status: string
  steps: StatusStep[]
  error: string | null
}

export default function StatusIndicator({ status, steps, error }: StatusIndicatorProps) {
  const getStepStatus = (stepKey: string) => {
    const currentIndex = steps.findIndex(s => s.key === status)
    const stepIndex = steps.findIndex(s => s.key === stepKey)

    if (error && status === 'error') {
      return currentIndex >= stepIndex ? 'error' : 'pending'
    }

    if (status === 'complete') return 'complete'
    if (currentIndex === -1) return 'pending'
    if (currentIndex >= stepIndex) return 'current'
    return 'pending'
  }

  return (
    <div className="bg-white/5 backdrop-blur-xl border border-white/10 rounded-2xl p-6 shadow-2xl">
      <div className="flex items-center gap-3 mb-6">
        <div className={`p-2 rounded-lg ${status !== 'idle' && status !== 'complete' && status !== 'error' ? 'bg-violet-500' : 'bg-white/10'}`}>
          <Loader2 className={`w-5 h-5 ${status !== 'idle' && status !== 'complete' && status !== 'error' ? 'animate-spin text-white' : 'text-gray-400'}`} />
        </div>
        <div>
          <h3 className="text-lg font-semibold text-white">Processing Status</h3>
          <p className="text-sm text-gray-400">
            {status === 'complete' ? 'Video created successfully!' : status === 'error' ? 'An error occurred' : 'Creating your video...'}
          </p>
        </div>
      </div>

      <div className="space-y-4">
        {steps.map((step, index) => {
          const stepStatus = getStepStatus(step.key)
          const Icon = step.icon

          return (
            <div
              key={step.key}
              className={`flex items-center gap-4 p-4 rounded-xl transition-all ${
                stepStatus === 'current' 
                  ? 'bg-violet-500/10 border-2 border-violet-500' 
                  : stepStatus === 'complete' 
                    ? 'bg-green-500/10 border-2 border-green-500' 
                    : stepStatus === 'error'
                      ? 'bg-red-500/10 border-2 border-red-500'
                      : 'bg-white/5 border-2 border-white/10'
              }`}
            >
              <div className="flex-shrink-0">
                {stepStatus === 'complete' ? (
                  <div className="w-8 h-8 rounded-full bg-green-500 flex items-center justify-center">
                    <CheckCircle2 className="w-5 h-5 text-white" />
                  </div>
                ) : stepStatus === 'error' ? (
                  <div className="w-8 h-8 rounded-full bg-red-500 flex items-center justify-center">
                    <XCircle className="w-5 h-5 text-white" />
                  </div>
                ) : stepStatus === 'current' ? (
                  <div className="w-8 h-8 rounded-full bg-violet-500 flex items-center justify-center">
                    <div className="w-5 h-5 border-2 border-white/30 border-t-white rounded-full animate-spin" />
                  </div>
                ) : (
                  <div className="w-8 h-8 rounded-full border-2 border-white/20 flex items-center justify-center">
                    <Icon className="w-4 h-4 text-gray-500" />
                  </div>
                )}
              </div>

              <div className="flex items-center gap-3 flex-1">
                <div className={`p-2 rounded-lg ${
                  stepStatus === 'complete' 
                    ? 'bg-green-500/20' 
                    : stepStatus === 'error'
                      ? 'bg-red-500/20'
                      : stepStatus === 'current'
                        ? 'bg-violet-500/20'
                        : 'bg-white/10'
                }`}>
                  <Icon className={`w-5 h-5 ${
                    stepStatus === 'complete' 
                      ? 'text-green-500' 
                      : stepStatus === 'error'
                        ? 'text-red-500'
                        : stepStatus === 'current'
                          ? 'text-violet-500'
                          : 'text-gray-500'
                  }`} />
                </div>
                <div>
                  <span className={`font-medium block ${
                    stepStatus === 'complete' 
                      ? 'text-white' 
                      : stepStatus === 'error'
                        ? 'text-white'
                        : stepStatus === 'current'
                          ? 'text-white'
                          : 'text-gray-500'
                  }`}>
                    {step.label}
                  </span>
                  {stepStatus === 'current' && (
                    <span className="text-xs text-violet-400">Processing...</span>
                  )}
                </div>
              </div>

              {stepStatus === 'current' && (
                <div className="flex gap-1">
                  <div className="w-2 h-2 rounded-full bg-violet-500 animate-pulse" />
                  <div className="w-2 h-2 rounded-full bg-violet-500 animate-pulse delay-100" />
                  <div className="w-2 h-2 rounded-full bg-violet-500 animate-pulse delay-200" />
                </div>
              )}
            </div>
          )
        })}
      </div>

      {error && (
        <div className="mt-4 p-4 bg-red-500/10 border-2 border-red-500/30 rounded-xl">
          <p className="text-red-400 text-sm font-medium">{error}</p>
        </div>
      )}
    </div>
  )
}
