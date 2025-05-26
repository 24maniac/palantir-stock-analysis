import React, { useState } from 'react';
import { Input } from './input'; // Assuming this is a ShadCN/ui component
import { Button } from './button'; // Assuming this is a ShadCN/ui component

interface TickerInputProps {
  onTickerSubmit: (ticker: string) => void;
  isLoading: boolean;
}

const TickerInput: React.FC<TickerInputProps> = ({ onTickerSubmit, isLoading }) => {
  const [ticker, setTicker] = useState<string>('');

  const handleSubmit = (event: React.FormEvent) => {
    event.preventDefault();
    if (ticker.trim()) {
      onTickerSubmit(ticker.trim().toUpperCase());
    }
  };

  return (
    <section className="py-6 px-4 sm:px-6 lg:px-8 bg-gray-100">
      <div className="max-w-xl mx-auto">
        <form onSubmit={handleSubmit} className="flex items-center space-x-2">
          <Input
            type="text"
            placeholder="Enter stock ticker (e.g., PLTR, AAPL)"
            value={ticker}
            onChange={(e) => setTicker(e.target.value)}
            className="flex-grow"
            disabled={isLoading}
          />
          <Button type="submit" disabled={isLoading}>
            {isLoading ? 'Analyzing...' : 'Analyze'}
          </Button>
        </form>
        {/* We can add error messages here later if needed */}
      </div>
    </section>
  );
};

export default TickerInput;
