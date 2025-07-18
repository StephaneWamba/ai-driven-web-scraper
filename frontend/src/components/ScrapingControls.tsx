import React, { useState } from 'react';
import axios from 'axios';

interface ScrapingControlsProps {
  apiBaseUrl: string;
  onScrapingComplete: () => void;
}

const ScrapingControls: React.FC<ScrapingControlsProps> = ({ apiBaseUrl, onScrapingComplete }) => {
  const [urls, setUrls] = useState<string>('');
  const [sites, setSites] = useState<string[]>(['amazon', 'bestbuy', 'walmart']);
  const [maxProducts, setMaxProducts] = useState<number>(50);
  const [loading, setLoading] = useState(false);
  const [message, setMessage] = useState('');

  const handleStartScraping = async () => {
    if (!urls.trim()) {
      setMessage('Please enter at least one URL');
      return;
    }

    setLoading(true);
    setMessage('');

    try {
      const urlList = urls.split('\n').filter(url => url.trim());
      
      const response = await axios.post(`${apiBaseUrl}/api/scrape/start`, {
        urls: urlList,
        target_sites: sites,
        max_products: maxProducts,
        use_ai_parsing: true,
        include_images: true,
        include_reviews: false
      });

      setMessage(`Scraping job started! Job ID: ${response.data.job_id}`);
      onScrapingComplete();
    } catch (error: any) {
      setMessage(`Error: ${error.response?.data?.detail || error.message}`);
    } finally {
      setLoading(false);
    }
  };

  const handleSiteToggle = (site: string) => {
    if (sites.includes(site)) {
      setSites(sites.filter(s => s !== site));
    } else {
      setSites([...sites, site]);
    }
  };

  return (
    <div className="bg-white rounded-lg shadow p-6">
      <h3 className="text-lg font-semibold text-gray-900 mb-6">
        Advanced Scraping Controls
      </h3>

      <div className="space-y-6">
        {/* URLs Input */}
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">
            Target URLs (one per line)
          </label>
          <textarea
            value={urls}
            onChange={(e) => setUrls(e.target.value)}
            placeholder="https://www.amazon.com/s?k=iphone+15&#10;https://www.bestbuy.com/site/searchpage.jsp?st=iphone+15"
            className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-primary-500 focus:border-transparent"
            rows={4}
          />
        </div>

        {/* Site Selection */}
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">
            Target Sites
          </label>
          <div className="flex space-x-4">
            {['amazon', 'bestbuy', 'walmart'].map((site) => (
              <label key={site} className="flex items-center">
                <input
                  type="checkbox"
                  checked={sites.includes(site)}
                  onChange={() => handleSiteToggle(site)}
                  className="rounded border-gray-300 text-primary-600 focus:ring-primary-500"
                />
                <span className="ml-2 text-sm text-gray-700 capitalize">{site}</span>
              </label>
            ))}
          </div>
        </div>

        {/* Max Products */}
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">
            Maximum Products per Site
          </label>
          <input
            type="number"
            value={maxProducts}
            onChange={(e) => setMaxProducts(Number(e.target.value))}
            min="1"
            max="1000"
            className="w-32 px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-primary-500 focus:border-transparent"
          />
        </div>

        {/* Message Display */}
        {message && (
          <div className={`p-4 rounded-md ${
            message.includes('Error') 
              ? 'bg-red-50 border border-red-200 text-red-700' 
              : 'bg-green-50 border border-green-200 text-green-700'
          }`}>
            {message}
          </div>
        )}

        {/* Start Button */}
        <button
          onClick={handleStartScraping}
          disabled={loading || sites.length === 0}
          className="w-full bg-primary-600 text-white py-3 px-4 rounded-md font-medium hover:bg-primary-700 focus:outline-none focus:ring-2 focus:ring-primary-500 focus:ring-offset-2 disabled:opacity-50 disabled:cursor-not-allowed"
        >
          {loading ? 'Starting Scraping...' : 'Start Scraping Job'}
        </button>

        {/* Info */}
        <div className="text-sm text-gray-500 bg-gray-50 p-4 rounded-md">
          <h4 className="font-medium text-gray-700 mb-2">How it works:</h4>
          <ul className="space-y-1">
            <li>• Enter URLs from Amazon, Best Buy, or Walmart</li>
            <li>• Select which sites to scrape</li>
            <li>• Set maximum products to extract per site</li>
            <li>• AI-powered parsing ensures accurate data extraction</li>
            <li>• Real-time progress tracking and results</li>
          </ul>
        </div>
      </div>
    </div>
  );
};

export default ScrapingControls; 