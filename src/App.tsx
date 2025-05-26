import React, { useState, useEffect } from 'react'; // Added useState, useEffect
import Header from './components/sections/Header';
import BasicInfo from './components/sections/BasicInfo';
import CurrentStockSituation from './components/sections/CurrentStockSituation';
import TechnicalAnalysis from './components/sections/TechnicalAnalysis';
import InvestmentRecommendation from './components/sections/InvestmentRecommendation';
import KeyDevelopments from './components/sections/KeyDevelopments';
import InsiderTrading from './components/sections/InsiderTrading';
import Analysis from './components/sections/Analysis';
import DataSource from './components/sections/DataSource';
import Footer from './components/sections/Footer';
import TickerInput from './components/ui/TickerInput'; // Import TickerInput
// We will define AnalysisData type later
// import { AnalysisData } from './types'; // Placeholder for data type

function App() {
  const [currentTicker, setCurrentTicker] = useState<string>('PLTR'); // Default to PLTR
  const [analysisData, setAnalysisData] = useState<any | null>(null); // Using 'any' for now
  const [isLoading, setIsLoading] = useState<boolean>(false);
  const [error, setError] = useState<string | null>(null);

  const handleTickerSubmit = async (ticker: string) => {
    setCurrentTicker(ticker);
    setIsLoading(true);
    setError(null);
    setAnalysisData(null); // Clear previous data

    // **Conceptual Trigger for Python Script**
    // In a real backend setup, this would be an API call that runs the script.
    // For now, we'll simulate a delay and then try to fetch the files.
    // This part will be more fleshed out in the data fetching logic step.
    console.log(`Frontend: Requesting analysis for ${ticker}`);

    // Simulate backend processing time
    await new Promise(resolve => setTimeout(resolve, 2000)); // Simulate 2s delay

    try {
      // Paths are relative to the 'public' directory
      const response = await fetch(`/analysis_outputs/${ticker}_analysis_result.json`);
      if (!response.ok) {
        // Try to get a more specific error from the response if possible
        let errorText = `Failed to fetch analysis data: ${response.statusText}`;
        if (response.status === 404) {
            errorText = `Analysis data not found for ticker ${ticker}. Please ensure the ticker is correct and the analysis has been run.`;
        } else {
            try {
                const errorData = await response.json();
                errorText = errorData.message || errorText;
            } catch (e) {
                // Ignore if response is not JSON
            }
        }
        throw new Error(errorText);
      }
      const data = await response.json();
      setAnalysisData(data);
      console.log(`Frontend: Analysis data for ${ticker} loaded.`);
    } catch (err: any) {
      console.error("Frontend: Error fetching analysis data:", err);
      setError(err.message || 'An unexpected error occurred.');
      setAnalysisData(null);
    } finally {
      setIsLoading(false);
    }
  };
  
  // Fetch initial data for PLTR on component mount for demonstration
  useEffect(() => {
    handleTickerSubmit('PLTR');
  }, []);


  return (
    <div className="min-h-screen bg-gray-50">
      <Header />
      <TickerInput onTickerSubmit={handleTickerSubmit} isLoading={isLoading} />
      {/* Display loading and error states */}
      {isLoading && (
        <div className="text-center py-4">
          <p className="text-lg text-blue-600">Loading analysis for {currentTicker}...</p>
        </div>
      )}
      {error && (
        <div className="text-center py-4">
          <p className="text-lg text-red-600">Error: {error}</p>
        </div>
      )}

      {/* Pass analysisData and currentTicker to relevant components */}
      {analysisData && !isLoading && !error && (
        <main>
          <BasicInfo analysisData={analysisData.basic_info} stockSymbol={currentTicker} />
          <CurrentStockSituation analysisData={analysisData.current_price} stockSymbol={currentTicker} />
          <TechnicalAnalysis 
            analysisData={analysisData.technical_analysis} 
            stockSymbol={currentTicker} 
            chartPath={`/analysis_outputs/${currentTicker}_stock_chart.png`} 
          />
          <InvestmentRecommendation analysisData={analysisData.investment_recommendation} stockSymbol={currentTicker} />
          <KeyDevelopments analysisData={analysisData.key_developments} stockSymbol={currentTicker} />
          <InsiderTrading analysisData={analysisData.insider_trading} stockSymbol={currentTicker} />
          <Analysis analysisData={analysisData.conclusion} stockSymbol={currentTicker} />
          <DataSource stockSymbol={currentTicker} />
        </main>
      )}
      <Footer />
    </div>
  );
}

export default App;
