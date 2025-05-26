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

function App() {
  return (
    <div className="min-h-screen bg-gray-50">
      <Header />
      <main>
        <BasicInfo />
        <CurrentStockSituation />
        <TechnicalAnalysis />
        <InvestmentRecommendation />
        <KeyDevelopments />
        <InsiderTrading />
        <Analysis />
        <DataSource />
      </main>
      <Footer />
    </div>
  );
}

export default App;
