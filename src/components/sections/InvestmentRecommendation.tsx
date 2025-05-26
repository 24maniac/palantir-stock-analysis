import React from 'react';

const InvestmentRecommendation: React.FC = () => {
  return (
    <section className="py-8 px-4 sm:px-6 lg:px-8 bg-gray-50">
      <div className="max-w-7xl mx-auto">
        <h2 className="text-3xl font-bold text-gray-900 mb-6">4. 투자 추천</h2>
        <div className="bg-white rounded-lg p-6 shadow-sm">
          <p className="text-gray-700 mb-6">
            Yahoo Finance에서 제공하는 투자 분석가들의 의견을 종합했습니다:
          </p>
          
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            <div className="bg-indigo-50 p-5 rounded-lg border border-indigo-100">
              <div className="flex items-center justify-center h-12 w-12 rounded-md bg-indigo-500 text-white mb-4">
                <svg xmlns="http://www.w3.org/2000/svg" className="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 7h8m0 0v8m0-8l-8 8-4-4-6 6" />
                </svg>
              </div>
              <h3 className="text-lg font-medium text-gray-900">목표가</h3>
              <p className="mt-2 text-gray-600">별도 제시 없음</p>
            </div>
            
            <div className="bg-indigo-50 p-5 rounded-lg border border-indigo-100">
              <div className="flex items-center justify-center h-12 w-12 rounded-md bg-indigo-500 text-white mb-4">
                <svg xmlns="http://www.w3.org/2000/svg" className="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
                </svg>
              </div>
              <h3 className="text-lg font-medium text-gray-900">등급</h3>
              <p className="mt-2 text-gray-600">HOLD (보유)</p>
            </div>
            
            <div className="bg-indigo-50 p-5 rounded-lg border border-indigo-100">
              <div className="flex items-center justify-center h-12 w-12 rounded-md bg-indigo-500 text-white mb-4">
                <svg xmlns="http://www.w3.org/2000/svg" className="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 21V5a2 2 0 00-2-2H7a2 2 0 00-2 2v16m14 0h2m-2 0h-5m-9 0H3m2 0h5M9 7h1m-1 4h1m4-4h1m-1 4h1m-5 10v-5a1 1 0 011-1h2a1 1 0 011 1v5m-4 0h4" />
                </svg>
              </div>
              <h3 className="text-lg font-medium text-gray-900">제공자</h3>
              <p className="mt-2 text-gray-600">Argus Research</p>
            </div>
          </div>
          
          <div className="mt-8 bg-gray-50 p-5 rounded-lg border border-gray-200">
            <h3 className="text-lg font-medium text-gray-900 mb-3">투자 의견 해석</h3>
            <p className="text-gray-700">
              투자 분석가들은 팔란티어에 대해 <span className="font-bold">중립</span> 의견을 제시하고 있습니다. 
              이는 현재 주가가 이미 상당한 상승을 기록한 상태에서, 추가 상승 여력과 하락 위험이 균형을 이루고 있다는 
              판단으로 해석됩니다.
            </p>
          </div>
        </div>
      </div>
    </section>
  );
};

export default InvestmentRecommendation;
