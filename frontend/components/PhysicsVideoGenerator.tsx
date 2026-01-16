import React, { useState } from 'react';

interface PhysicsVideoGeneratorProps {
  onGenerate: (request: {
    text: string;
    enable_physics: boolean;
    enable_fluid: boolean;
    enable_particles: boolean;
    duration: number;
    fps: number;
  }) => void;
  isGenerating: boolean;
}

export default function PhysicsVideoGenerator({ onGenerate, isGenerating }: PhysicsVideoGeneratorProps) {
  const [text, setText] = useState('');
  const [enablePhysics, setEnablePhysics] = useState(true);
  const [enableFluid, setEnableFluid] = useState(true);
  const [enableParticles, setEnableParticles] = useState(true);
  const [duration, setDuration] = useState(5.0);
  const [fps, setFps] = useState(30);

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (text.trim()) {
      onGenerate({
        text,
        enable_physics: enablePhysics,
        enable_fluid: enableFluid,
        enable_particles: enableParticles,
        duration,
        fps,
      });
    }
  };

  const examplePrompts = [
    "A close-up, slow-motion shot of a transparent glass falling onto a wooden table. As the glass hits the wood, it doesn't break, but orange juice inside splashes out in intricate, realistic droplets that catch the warm sunlight. The camera follows a single drop as it rolls across the grain of the wood.",
    "Water droplets falling on a leaf, realistic physics, slow motion",
    "Fire particles rising and swirling in the wind, cinematic",
    "Smoke and steam rising from a hot cup of coffee, atmospheric",
    "Explosion of colorful particles in slow motion, dramatic"
  ];

  return (
    <div className="w-full max-w-4xl mx-auto p-6 bg-gradient-to-br from-purple-50 to-blue-50 dark:from-gray-800 dark:to-gray-900 rounded-2xl shadow-2xl">
      <div className="text-center mb-8">
        <h2 className="text-4xl font-bold bg-gradient-to-r from-purple-600 to-blue-600 bg-clip-text text-transparent mb-2">
          Physics-Based AI Video Generator
        </h2>
        <p className="text-gray-600 dark:text-gray-300">
          Generate realistic physics simulations with fluid dynamics, particles, and more
        </p>
      </div>

      <form onSubmit={handleSubmit} className="space-y-6">
        <div>
          <label className="block text-sm font-semibold text-gray-700 dark:text-gray-300 mb-2">
            Scene Description
          </label>
          <textarea
            value={text}
            onChange={(e) => setText(e.target.value)}
            placeholder="Describe your scene with physics elements..."
            rows={4}
            className="w-full px-4 py-3 border-2 border-gray-200 dark:border-gray-600 rounded-xl focus:border-purple-500 dark:focus:border-purple-400 focus:ring-2 focus:ring-purple-200 dark:focus:ring-purple-800 transition-all duration-300 bg-white dark:bg-gray-700 text-gray-900 dark:text-white"
            disabled={isGenerating}
          />
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          <div>
            <label className="block text-sm font-semibold text-gray-700 dark:text-gray-300 mb-2">
              Duration (seconds): {duration}s
            </label>
            <input
              type="range"
              min="3"
              max="10"
              step="0.5"
              value={duration}
              onChange={(e) => setDuration(parseFloat(e.target.value))}
              className="w-full h-2 bg-gray-200 dark:bg-gray-600 rounded-lg appearance-none cursor-pointer accent-purple-600"
              disabled={isGenerating}
              title="Duration in seconds"
            />
          </div>

          <div>
            <label className="block text-sm font-semibold text-gray-700 dark:text-gray-300 mb-2">
              Frame Rate (FPS): {fps}
            </label>
            <input
              type="range"
              min="15"
              max="60"
              step="5"
              value={fps}
              onChange={(e) => setFps(parseInt(e.target.value))}
              className="w-full h-2 bg-gray-200 dark:bg-gray-600 rounded-lg appearance-none cursor-pointer accent-purple-600"
              disabled={isGenerating}
              title="Frame rate in frames per second"
            />
          </div>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          <label className="flex items-center space-x-3 p-4 bg-white dark:bg-gray-700 rounded-xl shadow-md hover:shadow-lg transition-all duration-300 cursor-pointer">
            <input
              type="checkbox"
              checked={enablePhysics}
              onChange={(e) => setEnablePhysics(e.target.checked)}
              className="w-5 h-5 text-purple-600 rounded focus:ring-purple-500"
              disabled={isGenerating}
            />
            <div>
              <span className="block font-semibold text-gray-900 dark:text-white">Physics</span>
              <span className="text-sm text-gray-500 dark:text-gray-400">Gravity, collisions</span>
            </div>
          </label>

          <label className="flex items-center space-x-3 p-4 bg-white dark:bg-gray-700 rounded-xl shadow-md hover:shadow-lg transition-all duration-300 cursor-pointer">
            <input
              type="checkbox"
              checked={enableFluid}
              onChange={(e) => setEnableFluid(e.target.checked)}
              className="w-5 h-5 text-blue-600 rounded focus:ring-blue-500"
              disabled={isGenerating}
            />
            <div>
              <span className="block font-semibold text-gray-900 dark:text-white">Fluid</span>
              <span className="text-sm text-gray-500 dark:text-gray-400">Water, liquids</span>
            </div>
          </label>

          <label className="flex items-center space-x-3 p-4 bg-white dark:bg-gray-700 rounded-xl shadow-md hover:shadow-lg transition-all duration-300 cursor-pointer">
            <input
              type="checkbox"
              checked={enableParticles}
              onChange={(e) => setEnableParticles(e.target.checked)}
              className="w-5 h-5 text-green-600 rounded focus:ring-green-500"
              disabled={isGenerating}
            />
            <div>
              <span className="block font-semibold text-gray-900 dark:text-white">Particles</span>
              <span className="text-sm text-gray-500 dark:text-gray-400">Fire, smoke, dust</span>
            </div>
          </label>
        </div>

        <div>
          <label className="block text-sm font-semibold text-gray-700 dark:text-gray-300 mb-2">
            Example Prompts
          </label>
          <div className="space-y-2">
            {examplePrompts.map((prompt, index) => (
              <button
                key={index}
                type="button"
                onClick={() => setText(prompt)}
                className="w-full text-left p-3 bg-white dark:bg-gray-700 rounded-lg border border-gray-200 dark:border-gray-600 hover:border-purple-400 dark:hover:border-purple-500 hover:bg-purple-50 dark:hover:bg-purple-900/20 transition-all duration-300 text-sm text-gray-700 dark:text-gray-300"
                disabled={isGenerating}
              >
                {prompt.substring(0, 100)}...
              </button>
            ))}
          </div>
        </div>

        <button
          type="submit"
          disabled={isGenerating || !text.trim()}
          className="w-full py-4 bg-gradient-to-r from-purple-600 to-blue-600 hover:from-purple-700 hover:to-blue-700 text-white font-bold rounded-xl shadow-lg hover:shadow-xl transform hover:-translate-y-1 transition-all duration-300 disabled:opacity-50 disabled:cursor-not-allowed disabled:transform-none"
        >
          {isGenerating ? (
            <span className="flex items-center justify-center space-x-2">
              <svg className="animate-spin h-5 w-5 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
              </svg>
              <span>Generating Physics Video...</span>
            </span>
          ) : (
            'Generate Physics Video'
          )}
        </button>
      </form>

      <div className="mt-8 p-4 bg-blue-50 dark:bg-blue-900/20 border border-blue-200 dark:border-blue-800 rounded-xl">
        <h3 className="font-semibold text-blue-900 dark:text-blue-300 mb-2">How it works:</h3>
        <ul className="text-sm text-blue-800 dark:text-blue-400 space-y-1">
          <li>• AI generates multiple keyframe images based on your scene description</li>
          <li>• Optical flow interpolation creates smooth transitions between frames</li>
          <li>• Physics engine simulates realistic particle behavior</li>
          <li>• Fluid dynamics create water/liquid effects with proper physics</li>
          <li>• Post-processing adds motion blur, color grading, and lens effects</li>
        </ul>
      </div>
    </div>
  );
}