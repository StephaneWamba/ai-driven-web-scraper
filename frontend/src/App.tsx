import React, { useState, useEffect } from 'react';
import axios from 'axios';
import Dashboard from './components/Dashboard';
import Header from './components/Header';
import './App.css';

// API base URL
const API_BASE_URL = 'http://54.165.182.47:8000';

function App() {
  const [isConnected, setIsConnected] = useState(false);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    // Check API connection on startup
    checkApiConnection();
  }, []);

  const checkApiConnection = async () => {
    try {
      const response = await axios.get(`${API_BASE_URL}/health`);
      setIsConnected(response.data.status === 'healthy');
    } catch (error) {
      console.error('API connection failed:', error);
      setIsConnected(false);
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600 mx-auto"></div>
          <p className="mt-4 text-gray-600">Connecting to AI Scraper API...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50">
      <Header isConnected={isConnected} />
      <main className="container mx-auto px-4 py-8">
        {isConnected ? (
          <Dashboard apiBaseUrl={API_BASE_URL} />
        ) : (
          <div className="text-center py-12">
            <div className="bg-red-50 border border-red-200 rounded-lg p-6 max-w-md mx-auto">
              <h3 className="text-lg font-medium text-red-800 mb-2">
                Connection Failed
              </h3>
              <p className="text-red-600 mb-4">
                Unable to connect to the AI Scraper API. Please check if the server is running.
              </p>
              <button
                onClick={checkApiConnection}
                className="bg-red-600 text-white px-4 py-2 rounded hover:bg-red-700 transition-colors"
              >
                Retry Connection
              </button>
            </div>
          </div>
        )}
      </main>
    </div>
  );
}

export default App;
