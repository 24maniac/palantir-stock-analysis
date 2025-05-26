import React from 'react';

const KeyDevelopments: React.FC = () => {
  return (
    <section className="py-8 px-4 sm:px-6 lg:px-8 bg-white">
      <div className="max-w-7xl mx-auto">
        <h2 className="text-3xl font-bold text-gray-900 mb-6">5. 주요 개발 사항</h2>
        <div className="bg-white rounded-lg p-6 shadow-sm border border-gray-200">
          <p className="text-gray-700 mb-6">
            팔란티어와 관련된 최근 주요 뉴스와 개발 사항을 정리했습니다:
          </p>
          
          <div className="space-y-6">
            <div className="flex">
              <div className="flex-shrink-0">
                <div className="flex items-center justify-center h-12 w-12 rounded-md bg-blue-500 text-white">
                  <svg xmlns="http://www.w3.org/2000/svg" className="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" />
                  </svg>
                </div>
              </div>
              <div className="ml-4">
                <h3 className="text-lg font-medium text-gray-900">2025년 매출 전망 상향 조정</h3>
                <p className="mt-2 text-gray-600">
                  <span className="text-sm text-blue-600 font-medium">2025-05-05</span>
                </p>
                <p className="mt-1 text-gray-600">
                  팔란티어가 2025년 매출 전망을 $38.9억-$39.0억으로 발표했으며, 이는 시장 예상치인 $37.5억을 상회하는 수준입니다. 
                  이러한 긍정적인 전망은 주가 상승에 호재로 작용할 수 있습니다.
                </p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>
  );
};

export default KeyDevelopments;
