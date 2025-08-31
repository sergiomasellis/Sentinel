import { useState, useEffect } from 'react'
import './App.css'

function App() {
  const [activeTab, setActiveTab] = useState('dashboard')
  const [manualTrigger, setManualTrigger] = useState({
    repositoryUrl: '',
    branch: '',
    commitId: '',
    jiraTicketId: '',
    testTypes: ['e2e', 'integration']
  })
  const [isSubmitting, setIsSubmitting] = useState(false)
  const [submitMessage, setSubmitMessage] = useState('')
  const [testRuns, setTestRuns] = useState([])
  const [isLoadingTestRuns, setIsLoadingTestRuns] = useState(false)

  const fetchTestRuns = async () => {
    setIsLoadingTestRuns(true)
    try {
      const response = await fetch('http://localhost:8000/api/v1/test-runs')
      if (response.ok) {
        const data = await response.json()
        setTestRuns(data.test_runs || [])
      } else {
        console.error('Failed to fetch test runs')
        setTestRuns([])
      }
    } catch (error) {
      console.error('Error fetching test runs:', error)
      setTestRuns([])
    } finally {
      setIsLoadingTestRuns(false)
    }
  }

  // Fetch test runs when the component mounts or when switching to test-runs tab
  useEffect(() => {
    if (activeTab === 'test-runs') {
      fetchTestRuns()
    }
  }, [activeTab])

  const handleManualTrigger = async (e: React.FormEvent) => {
    e.preventDefault()
    setIsSubmitting(true)
    setSubmitMessage('')

    try {
      const response = await fetch('http://localhost:8000/api/v1/test-runs', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          repository_url: manualTrigger.repositoryUrl,
          branch: manualTrigger.branch,
          commit_id: manualTrigger.commitId,
          jira_ticket_id: manualTrigger.jiraTicketId || null,
          test_types: manualTrigger.testTypes
        })
      })

      if (response.ok) {
        const data = await response.json()
        setSubmitMessage(`Test run ${data.run_id} triggered successfully!`)
        // Reset form
        setManualTrigger({
          repositoryUrl: '',
          branch: '',
          commitId: '',
          jiraTicketId: '',
          testTypes: ['e2e', 'integration']
        })
      } else {
        const error = await response.json()
        setSubmitMessage(`Error: ${error.detail || 'Failed to trigger test run'}`)
      }
    } catch (error) {
      setSubmitMessage('Error: Failed to connect to server')
    } finally {
      setIsSubmitting(false)
    }
  }

  return (
    <div className="min-h-screen bg-gray-50">
      <header className="bg-white shadow-sm border-b">
        <div className="container mx-auto px-4 py-4">
          <h1 className="text-2xl font-bold text-gray-900">Sentinel - AI-Driven Testing Platform</h1>
        </div>
      </header>

      <nav className="bg-white border-b">
        <div className="container mx-auto px-4">
          <div className="flex space-x-8">
            <button
              onClick={() => setActiveTab('dashboard')}
              className={`py-4 px-2 border-b-2 transition-colors ${
                activeTab === 'dashboard' 
                  ? 'border-blue-500 text-blue-600' 
                  : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
              }`}
            >
              Dashboard
            </button>
            <button
              onClick={() => setActiveTab('test-runs')}
              className={`py-4 px-2 border-b-2 transition-colors ${
                activeTab === 'test-runs' 
                  ? 'border-blue-500 text-blue-600' 
                  : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
              }`}
            >
              Test Runs
            </button>
            <button
              onClick={() => setActiveTab('reports')}
              className={`py-4 px-2 border-b-2 transition-colors ${
                activeTab === 'reports' 
                  ? 'border-blue-500 text-blue-600' 
                  : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
              }`}
            >
              Reports
            </button>
            <button
              onClick={() => setActiveTab('settings')}
              className={`py-4 px-2 border-b-2 transition-colors ${
                activeTab === 'settings' 
                  ? 'border-blue-500 text-blue-600' 
                  : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
              }`}
            >
              Settings
            </button>
          </div>
        </div>
      </nav>

      <main className="container mx-auto px-4 py-8">
        {activeTab === 'dashboard' && (
          <div>
            <h2 className="text-xl font-semibold text-gray-900 mb-6">Dashboard</h2>

            {/* Manual Test Trigger Form */}
            <div className="bg-white p-6 rounded-lg shadow mb-8">
              <h3 className="text-lg font-medium text-gray-900 mb-4">Trigger Test Run</h3>
              <form onSubmit={handleManualTrigger} className="space-y-4">
                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-1">
                      Repository URL *
                    </label>
                    <input
                      type="url"
                      required
                      value={manualTrigger.repositoryUrl}
                      onChange={(e) => setManualTrigger(prev => ({ ...prev, repositoryUrl: e.target.value }))}
                      placeholder="https://bitbucket.org/workspace/repo.git"
                      className="w-full p-2 border border-gray-300 rounded focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                    />
                  </div>
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-1">
                      Branch *
                    </label>
                    <input
                      type="text"
                      required
                      value={manualTrigger.branch}
                      onChange={(e) => setManualTrigger(prev => ({ ...prev, branch: e.target.value }))}
                      placeholder="main"
                      className="w-full p-2 border border-gray-300 rounded focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                    />
                  </div>
                </div>
                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-1">
                      Commit ID *
                    </label>
                    <input
                      type="text"
                      required
                      value={manualTrigger.commitId}
                      onChange={(e) => setManualTrigger(prev => ({ ...prev, commitId: e.target.value }))}
                      placeholder="abc123456789"
                      className="w-full p-2 border border-gray-300 rounded focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                    />
                  </div>
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-1">
                      Jira Ticket ID
                    </label>
                    <input
                      type="text"
                      value={manualTrigger.jiraTicketId}
                      onChange={(e) => setManualTrigger(prev => ({ ...prev, jiraTicketId: e.target.value }))}
                      placeholder="PROJ-123"
                      className="w-full p-2 border border-gray-300 rounded focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                    />
                  </div>
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    Test Types
                  </label>
                  <div className="flex space-x-4">
                    <label className="flex items-center">
                      <input
                        type="checkbox"
                        checked={manualTrigger.testTypes.includes('e2e')}
                        onChange={(e) => {
                          const types = e.target.checked
                            ? [...manualTrigger.testTypes, 'e2e']
                            : manualTrigger.testTypes.filter(t => t !== 'e2e')
                          setManualTrigger(prev => ({ ...prev, testTypes: types }))
                        }}
                        className="mr-2"
                      />
                      E2E Tests
                    </label>
                    <label className="flex items-center">
                      <input
                        type="checkbox"
                        checked={manualTrigger.testTypes.includes('integration')}
                        onChange={(e) => {
                          const types = e.target.checked
                            ? [...manualTrigger.testTypes, 'integration']
                            : manualTrigger.testTypes.filter(t => t !== 'integration')
                          setManualTrigger(prev => ({ ...prev, testTypes: types }))
                        }}
                        className="mr-2"
                      />
                      Integration Tests
                    </label>
                  </div>
                </div>
                <div className="flex items-center space-x-4">
                  <button
                    type="submit"
                    disabled={isSubmitting}
                    className="bg-blue-600 text-white px-6 py-2 rounded hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed"
                  >
                    {isSubmitting ? 'Triggering...' : 'Trigger Test Run'}
                  </button>
                  {submitMessage && (
                    <span className={`text-sm ${submitMessage.includes('Error') ? 'text-red-600' : 'text-green-600'}`}>
                      {submitMessage}
                    </span>
                  )}
                </div>
              </form>
            </div>

            {/* Metrics Cards */}
            <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
              <div className="bg-white p-6 rounded-lg shadow">
                <h3 className="text-lg font-medium text-gray-900 mb-2">Total Test Runs</h3>
                <p className="text-3xl font-bold text-gray-900">0</p>
              </div>
              <div className="bg-white p-6 rounded-lg shadow">
                <h3 className="text-lg font-medium text-gray-900 mb-2">Success Rate</h3>
                <p className="text-3xl font-bold text-gray-900">-</p>
              </div>
              <div className="bg-white p-6 rounded-lg shadow">
                <h3 className="text-lg font-medium text-gray-900 mb-2">Auto-Healed Tests</h3>
                <p className="text-3xl font-bold text-gray-900">0</p>
              </div>
            </div>
          </div>
        )}

        {activeTab === 'test-runs' && (
           <div>
             <h2 className="text-xl font-semibold text-gray-900 mb-6">Test Runs</h2>
             <div className="bg-white p-6 rounded-lg shadow">
               {isLoadingTestRuns ? (
                 <p className="text-gray-500">Loading test runs...</p>
               ) : testRuns.length > 0 ? (
                 <div className="space-y-4">
                   {testRuns.map((testRun) => (
                     <div key={testRun.run_id} className="border border-gray-200 rounded-lg p-4">
                       <div className="flex justify-between items-start">
                         <div>
                           <h3 className="font-medium text-gray-900">Run ID: {testRun.run_id}</h3>
                           <p className="text-sm text-gray-600 mt-1">{testRun.message}</p>
                         </div>
                         <span className={`px-2 py-1 text-xs font-medium rounded-full ${
                           testRun.status === 'completed' ? 'bg-green-100 text-green-800' :
                           testRun.status === 'in_progress' ? 'bg-blue-100 text-blue-800' :
                           testRun.status === 'failed' ? 'bg-red-100 text-red-800' :
                           'bg-gray-100 text-gray-800'
                         }`}>
                           {testRun.status}
                         </span>
                       </div>
                     </div>
                   ))}
                 </div>
               ) : (
                 <p className="text-gray-500">No test runs yet. Connect your CI/CD pipeline to get started.</p>
               )}
             </div>
           </div>
         )}

        {activeTab === 'reports' && (
          <div>
            <h2 className="text-xl font-semibold text-gray-900 mb-6">Reports</h2>
            <div className="bg-white p-6 rounded-lg shadow">
              <p className="text-gray-500">No reports available.</p>
            </div>
          </div>
        )}

        {activeTab === 'settings' && (
          <div>
            <h2 className="text-xl font-semibold text-gray-900 mb-6">Settings</h2>
            <div className="bg-white p-6 rounded-lg shadow">
              <h3 className="text-lg font-medium text-gray-900 mb-4">Integration Settings</h3>
              <div className="space-y-4">
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">Bitbucket Webhook URL</label>
                  <input 
                    type="text" 
                    readOnly 
                    value="http://localhost:8000/api/v1/webhooks/bitbucket"
                    className="w-full p-2 border border-gray-300 rounded bg-gray-50"
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">Harness Webhook URL</label>
                  <input 
                    type="text" 
                    readOnly 
                    value="http://localhost:8000/api/v1/webhooks/harness"
                    className="w-full p-2 border border-gray-300 rounded bg-gray-50"
                  />
                </div>
              </div>
            </div>
          </div>
        )}
      </main>
    </div>
  )
}

export default App
