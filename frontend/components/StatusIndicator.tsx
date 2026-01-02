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
    <div className="glass rounded-2xl p-6 space-y-4">
      <h3 className="text-lg font-semibold text-white flex items-center gap-2">
        <Loader2 className={`w-5 h-5 ${status !== 'idle' && status !== 'complete' && status !== 'error' ? 'animate-spin' : ''} text-primary`} />
        Processing Status
      </h3>

      <div className="space-y-3">
        {steps.map((step, index) => {
          const stepStatus = getStepStatus(step.key)
          const Icon = step.icon

          return (
            <div
              key={step.key}
              className={`flex items-center gap-3 p-3 rounded-lg transition-all ${
                stepStatus === 'current' 
                  ? 'bg-primary/10 border border-primary/30' 
                  : stepStatus === 'complete' 
                    ? 'bg-green-500/10 border border-green-500/30' 
                    : stepStatus === 'error'
                      ? 'bg-red-500/10 border border-red-500/30'
                      : 'bg-surface/30 border border-white/10'
              }`}
            >
              <div className="flex-shrink-0">
                {stepStatus === 'complete' ? (
                  <CheckCircle2 className="w-6 h-6 text-green-500" />
                ) : stepStatus === 'error' ? (
                  <XCircle className="w-6 h-6 text-red-500" />
                ) : stepStatus === 'current' ? (
                  <div className="w-6 h-6 rounded-full border-2 border-primary border-t-transparent animate-spin" />
                ) : (
                  <div className="w-6 h-6 rounded-full border-2 border-white/20" />
                )}
              </div>

              <div className="flex items-center gap-2 flex-1">
                <Icon className={`w-5 h-5 ${
                  stepStatus === 'complete' 
                    ? 'text-green-500' 
                    : stepStatus === 'error'
                      ? 'text-red-500'
                      : stepStatus === 'current'
                        ? 'text-primary'
                        : 'text-gray-500'
                }`} />
                <span className={`font-medium ${
                  stepStatus === 'complete' 
                    ? 'text-green-400' 
                    : stepStatus === 'error'
                      ? 'text-red-400'
                      : stepStatus === 'current'
                        ? 'text-white'
                        : 'text-gray-500'
                }`}>
                  {step.label}
                </span>
              </div>

              {stepStatus === 'current' && (
                <div className="flex gap-1">
                  <div className="w-2 h-2 rounded-full bg-primary animate-pulse" />
                  <div className="w-2 h-2 rounded-full bg-primary animate-pulse delay-100" />
                  <div className="w-2 h-2 rounded-full bg-primary animate-pulse delay-200" />
                </div>
              )}
            </div>
          )
        })}
      </div>

      {error && (
        <div className="mt-4 p-4 bg-red-500/10 border border-red-500/30 rounded-lg">
          <p className="text-red-400 text-sm">{error}</p>
        </div>
      )}
    </div>
  )
}
