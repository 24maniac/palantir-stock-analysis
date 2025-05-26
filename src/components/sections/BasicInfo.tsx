import React from 'react';
// Assuming ShadCN UI components are available. If not, these would be standard HTML or other UI library components.
// import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'; 

// Mock Card components if actual ones are not available for this step
const Card: React.FC<{ children: React.ReactNode, className?: string }> = ({ children, className }) => <div className={`bg-white shadow rounded-lg ${className}`}>{children}</div>;
const CardHeader: React.FC<{ children: React.ReactNode, className?: string }> = ({ children, className }) => <div className={`p-4 sm:p-6 border-b border-gray-200 ${className}`}>{children}</div>;
const CardTitle: React.FC<{ children: React.ReactNode, className?: string }> = ({ children, className }) => <h2 className={`text-xl sm:text-2xl font-semibold text-gray-800 ${className}`}>{children}</h2>;
const CardContent: React.FC<{ children: React.ReactNode, className?: string }> = ({ children, className }) => <div className={`p-4 sm:p-6 ${className}`}>{children}</div>;


interface BasicInfoProps {
  analysisData?: {
    company_name?: string;
    symbol?: string;
    exchange?: string;
    currency?: string;
    // These fields were in the original hardcoded version, might not be in analysisData.basic_info
    // analysis_date?: string; 
    // data_source?: string;
  };
  stockSymbol: string;
}

const BasicInfo: React.FC<BasicInfoProps> = ({ analysisData, stockSymbol }) => {
  const sectionTitle = "1. Basic Information"; // English title

  if (!analysisData) {
    return (
      <section id="basic-info" className="py-8 px-4 sm:px-6 lg:px-8 bg-white">
        <div className="max-w-7xl mx-auto">
          <Card>
            <CardHeader>
              <CardTitle>{sectionTitle} for {stockSymbol.toUpperCase()}</CardTitle>
            </CardHeader>
            <CardContent>
              <p className="text-gray-600">Loading basic information...</p>
            </CardContent>
          </Card>
        </div>
      </section>
    );
  }

  // Use actual data or fallbacks
  const companyName = analysisData.company_name || `${stockSymbol.toUpperCase()} Company`;
  const symbol = analysisData.symbol || stockSymbol.toUpperCase();
  const exchange = analysisData.exchange || 'N/A';
  const currency = analysisData.currency || 'N/A';
  // const analysisDate = analysisData.analysis_date || new Date().toLocaleDateString(); // Example, if needed
  // const dataSource = analysisData.data_source || 'API'; // Example, if needed

  return (
    <section id="basic-info" className="py-8 px-4 sm:px-6 lg:px-8 bg-white">
      <div className="max-w-7xl mx-auto">
        <Card>
          <CardHeader>
            <CardTitle className="text-2xl md:text-3xl">
              {companyName} ({symbol})
            </CardTitle>
            <p className="text-lg md:text-xl text-gray-600 mt-1">{sectionTitle}</p>
          </CardHeader>
          <CardContent>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-x-6 gap-y-4">
              <div>
                <h3 className="text-sm font-medium text-gray-500">Company Name</h3>
                <p className="mt-1 text-lg text-gray-900">{companyName}</p>
              </div>
              <div>
                <h3 className="text-sm font-medium text-gray-500">Ticker Symbol</h3>
                <p className="mt-1 text-lg text-gray-900">{symbol}</p>
              </div>
              <div>
                <h3 className="text-sm font-medium text-gray-500">Exchange</h3>
                <p className="mt-1 text-lg text-gray-900">{exchange}</p>
              </div>
              <div>
                <h3 className="text-sm font-medium text-gray-500">Currency</h3>
                <p className="mt-1 text-lg text-gray-900">{currency}</p>
              </div>
              {/* 
              These fields were in the original hardcoded version. 
              If they are not part of analysisData.basic_info, they should be removed or handled.
              For now, I'm commenting them out as they are not in the provided JSON structure for basic_info.
              <div>
                <h3 className="text-sm font-medium text-gray-500">Analysis Date</h3>
                <p className="mt-1 text-lg text-gray-900">{analysisDate}</p>
              </div>
              <div>
                <h3 className="text-sm font-medium text-gray-500">Data Source</h3>
                <p className="mt-1 text-lg text-gray-900">{dataSource}</p>
              </div>
              */}
            </div>
          </CardContent>
        </Card>
      </div>
    </section>
  );
};

export default BasicInfo;
