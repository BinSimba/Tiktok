const API_BASE_URL = 'https://tiktok-backend-onpd.onrender.com'

export interface GenerateVideoRequest {
  topic: string
}

export interface GenerateVideoResponse {
  script: string
  video_url: string
}

export async function generateVideo(topic: string): Promise<GenerateVideoResponse> {
  const response = await fetch(`${API_BASE_URL}/generate-video`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({ topic }),
  })

  if (!response.ok) {
    throw new Error('Failed to generate video')
  }

  return response.json()
}
