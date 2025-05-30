import { useState } from 'react'

interface WorkflowData {
  execution_id: string
  status: string
  result: any
}

interface N8NWorkflowProps {
  workflowId: string
  title: string
  description: string
}

export default function N8NWorkflow({ workflowId, title, description }: N8NWorkflowProps) {
  const [isLoading, setIsLoading] = useState(false)
  const [workflowData, setWorkflowData] = useState<WorkflowData | null>(null)
  const [error, setError] = useState<string | null>(null)

  const triggerWorkflow = async () => {
    setIsLoading(true)
    setError(null)

    try {
      const response = await fetch('/api/n8n/trigger', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          workflow_id: workflowId,
          data: {} // Add any required data here
        })
      })

      const data = await response.json()
      
      if (data.error) {
        throw new Error(data.error)
      }

      setWorkflowData(data)
      
      // Poll for status updates
      const pollInterval = setInterval(async () => {
        const statusResponse = await fetch(`/api/n8n/status/${data.execution_id}`)
        const statusData = await statusResponse.json()
        
        setWorkflowData(statusData)
        
        if (statusData.status === 'completed' || statusData.status === 'failed') {
          clearInterval(pollInterval)
          setIsLoading(false)
        }
      }, 2000)

    } catch (error) {
      console.error('Error triggering workflow:', error)
      setError(error instanceof Error ? error.message : 'Failed to trigger workflow')
      setIsLoading(false)
    }
  }

  return (
    <div className="bg-white rounded-lg shadow p-6">
      <h3 className="text-lg font-semibold text-gray-900">{title}</h3>
      <p className="mt-2 text-sm text-gray-600">{description}</p>
      
      <div className="mt-4">
        <button
          onClick={triggerWorkflow}
          disabled={isLoading}
          className="rounded-lg bg-primary-600 px-4 py-2 text-white hover:bg-primary-700 focus:outline-none focus:ring-2 focus:ring-primary-500 focus:ring-offset-2 disabled:opacity-50"
        >
          {isLoading ? 'Running...' : 'Run Workflow'}
        </button>
      </div>

      {error && (
        <div className="mt-4 p-4 bg-red-50 rounded-lg">
          <p className="text-sm text-red-600">{error}</p>
        </div>
      )}

      {workflowData && (
        <div className="mt-4">
          <div className="bg-gray-50 rounded-lg p-4">
            <h4 className="text-sm font-medium text-gray-900">Workflow Status</h4>
            <div className="mt-2">
              <p className="text-sm text-gray-600">
                Status: <span className="font-medium">{workflowData.status}</span>
              </p>
              {workflowData.result && (
                <div className="mt-2">
                  <p className="text-sm font-medium text-gray-900">Result:</p>
                  <pre className="mt-1 text-xs text-gray-600 bg-gray-100 p-2 rounded">
                    {JSON.stringify(workflowData.result, null, 2)}
                  </pre>
                </div>
              )}
            </div>
          </div>
        </div>
      )}
    </div>
  )
} 