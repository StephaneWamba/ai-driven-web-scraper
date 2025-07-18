import React from 'react';

interface Job {
  job_id: string;
  status: string;
  message: string;
  progress?: number;
  products_scraped?: number;
}

interface JobStatusProps {
  job: Job;
}

const JobStatus: React.FC<JobStatusProps> = ({ job }) => {
  const getStatusColor = (status: string) => {
    switch (status) {
      case 'running':
        return 'bg-blue-500';
      case 'completed':
        return 'bg-green-500';
      case 'failed':
        return 'bg-red-500';
      default:
        return 'bg-gray-500';
    }
  };

  const getStatusText = (status: string) => {
    switch (status) {
      case 'running':
        return 'Running';
      case 'completed':
        return 'Completed';
      case 'failed':
        return 'Failed';
      default:
        return 'Unknown';
    }
  };

  return (
    <div className="bg-white rounded-lg shadow p-6">
      <div className="flex items-center justify-between mb-4">
        <h3 className="text-lg font-semibold text-gray-900">
          Scraping Job Status
        </h3>
        <div className="flex items-center space-x-2">
          <div className={`w-3 h-3 rounded-full ${getStatusColor(job.status)}`}></div>
          <span className="text-sm font-medium text-gray-600">
            {getStatusText(job.status)}
          </span>
        </div>
      </div>

      <div className="space-y-4">
        <div>
          <p className="text-sm text-gray-600 mb-1">Job ID</p>
          <p className="text-sm font-mono bg-gray-100 px-2 py-1 rounded">
            {job.job_id}
          </p>
        </div>

        <div>
          <p className="text-sm text-gray-600 mb-1">Message</p>
          <p className="text-sm text-gray-900">{job.message}</p>
        </div>

        {job.progress !== undefined && (
          <div>
            <div className="flex justify-between text-sm text-gray-600 mb-1">
              <span>Progress</span>
              <span>{Math.round((job.progress || 0) * 100)}%</span>
            </div>
            <div className="w-full bg-gray-200 rounded-full h-2">
              <div
                className="bg-primary-600 h-2 rounded-full transition-all duration-300"
                style={{ width: `${(job.progress || 0) * 100}%` }}
              ></div>
            </div>
          </div>
        )}

        {job.products_scraped !== undefined && (
          <div>
            <p className="text-sm text-gray-600 mb-1">Products Scraped</p>
            <p className="text-lg font-semibold text-primary-600">
              {job.products_scraped}
            </p>
          </div>
        )}
      </div>
    </div>
  );
};

export default JobStatus; 