import React, { useState, useEffect, useCallback } from 'react';
import axios from 'axios';
import ScrapingControls from './ScrapingControls';
import ProductTable from './ProductTable';
import Analytics from './Analytics';
import JobStatus from './JobStatus';

interface DashboardProps {
  apiBaseUrl: string;
}

interface Job {
  job_id: string;
  status: string;
  message: string;
  progress?: number;
  products_scraped?: number;
}

interface Product {
  id: number;
  name: string;
  price: number;
  competitor: string;
  url: string;
  rating?: number;
  review_count?: number;
  scraped_at: string;
  confidence_score: number;
}

const Dashboard: React.FC<DashboardProps> = ({ apiBaseUrl }) => {
  const [products, setProducts] = useState<Product[]>([]);
  const [currentJob, setCurrentJob] = useState<Job | null>(null);
  const [analytics, setAnalytics] = useState<any>(null);
  const [loading, setLoading] = useState(false);

  const loadProducts = useCallback(async () => {
    try {
      const response = await axios.get(`${apiBaseUrl}/api/products`);
      setProducts(response.data);
    } catch (error) {
      console.error('Failed to load products:', error);
    }
  }, [apiBaseUrl]);

  const loadAnalytics = useCallback(async () => {
    try {
      const response = await axios.get(`${apiBaseUrl}/api/analysis/competitive`);
      setAnalytics(response.data.analysis);
    } catch (error) {
      console.error('Failed to load analytics:', error);
    }
  }, [apiBaseUrl]);

  useEffect(() => {
    loadProducts();
    loadAnalytics();
  }, [loadProducts, loadAnalytics]);

  const startDemoScraping = async () => {
    setLoading(true);
    try {
      const response = await axios.get(`${apiBaseUrl}/api/demo/start`);
      setCurrentJob({
        job_id: response.data.job_id,
        status: 'started',
        message: 'Demo scraping started'
      });
      
      // Poll for job status
      pollJobStatus(response.data.job_id);
    } catch (error) {
      console.error('Failed to start demo scraping:', error);
      setLoading(false);
    }
  };

  const pollJobStatus = async (jobId: string) => {
    const interval = setInterval(async () => {
      try {
        const response = await axios.get(`${apiBaseUrl}/api/scrape/status/${jobId}`);
        setCurrentJob(response.data);
        
        if (response.data.status === 'completed' || response.data.status === 'failed') {
          clearInterval(interval);
          setLoading(false);
          loadProducts(); // Refresh products
          loadAnalytics(); // Refresh analytics
        }
      } catch (error) {
        console.error('Failed to get job status:', error);
        clearInterval(interval);
        setLoading(false);
      }
    }, 2000); // Poll every 2 seconds
  };

  return (
    <div className="space-y-8">
      {/* Hero Section */}
      <div className="bg-gradient-to-r from-primary-600 to-primary-700 rounded-lg p-8 text-white">
        <h2 className="text-3xl font-bold mb-4">
          Competitive Price Intelligence Dashboard
        </h2>
        <p className="text-primary-100 text-lg mb-6">
          Monitor prices across Amazon, Best Buy, and Walmart in real-time with AI-powered data extraction.
        </p>
        <div className="flex items-center space-x-4">
          <button
            onClick={startDemoScraping}
            disabled={loading}
            className="bg-white text-primary-600 px-6 py-3 rounded-lg font-semibold hover:bg-gray-100 transition-colors disabled:opacity-50"
          >
            {loading ? 'Starting Demo...' : 'Start Live Demo'}
          </button>
          <div className="text-sm text-primary-200">
            Click to start a live scraping demonstration
          </div>
        </div>
      </div>

      {/* Job Status */}
      {currentJob && (
        <JobStatus job={currentJob} />
      )}

      {/* Analytics */}
      {analytics && (
        <Analytics data={analytics} />
      )}

      {/* Products Table */}
      <div className="bg-white rounded-lg shadow">
        <div className="px-6 py-4 border-b border-gray-200">
          <h3 className="text-lg font-semibold text-gray-900">
            Scraped Products ({products.length})
          </h3>
        </div>
        <ProductTable products={products} />
      </div>

      {/* Scraping Controls */}
      <ScrapingControls 
        apiBaseUrl={apiBaseUrl} 
        onScrapingComplete={() => {
          loadProducts();
          loadAnalytics();
        }}
      />
    </div>
  );
};

export default Dashboard; 