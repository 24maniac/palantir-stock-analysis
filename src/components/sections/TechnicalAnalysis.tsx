import React from 'react';

const TechnicalAnalysis: React.FC = () => {
  return (
    <section className="py-8 px-4 sm:px-6 lg:px-8 bg-white">
      <div className="max-w-7xl mx-auto">
        <h2 className="text-3xl font-bold text-gray-900 mb-6">3. 기술적 분석</h2>
        
        <div className="mb-8">
          <h3 className="text-2xl font-semibold text-gray-800 mb-4">3.1 이동평균선 분석</h3>
          <div className="bg-white rounded-lg p-6 shadow-sm border border-gray-200">
            <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-6">
              <div className="bg-blue-50 p-4 rounded-md">
                <div className="flex items-center justify-between mb-2">
                  <span className="font-medium text-blue-800">20일 이동평균선</span>
                  <span className="bg-blue-100 text-blue-800 px-2 py-1 rounded text-sm font-medium">$121.08</span>
                </div>
                <p className="text-sm text-gray-600">단기 추세 지표</p>
              </div>
              
              <div className="bg-indigo-50 p-4 rounded-md">
                <div className="flex items-center justify-between mb-2">
                  <span className="font-medium text-indigo-800">50일 이동평균선</span>
                  <span className="bg-indigo-100 text-indigo-800 px-2 py-1 rounded text-sm font-medium">$102.54</span>
                </div>
                <p className="text-sm text-gray-600">중기 추세 지표</p>
              </div>
              
              <div className="bg-purple-50 p-4 rounded-md">
                <div className="flex items-center justify-between mb-2">
                  <span className="font-medium text-purple-800">200일 이동평균선</span>
                  <span className="bg-purple-100 text-purple-800 px-2 py-1 rounded text-sm font-medium">$71.57</span>
                </div>
                <p className="text-sm text-gray-600">장기 추세 지표</p>
              </div>
            </div>
            
            <div className="bg-green-50 p-4 rounded-md border border-green-100 mb-4">
              <h4 className="font-medium text-green-800 mb-2">현재 추세: <span className="font-bold">강한 상승</span></h4>
              <p className="text-gray-700">
                현재 주가($123.31)는 모든 주요 이동평균선 위에 위치하고 있으며, 20일 이동평균선이 50일 이동평균선보다 높고, 
                50일 이동평균선이 200일 이동평균선보다 높은 상태로, 전형적인 강세 구도를 형성하고 있습니다.
              </p>
            </div>
            
            <p className="text-gray-700">
              이동평균선 간의 관계를 통해 골든크로스(상승 신호)와 데드크로스(하락 신호)를 분석했습니다. 
              현재는 모든 이동평균선이 상승 배열을 형성하고 있어, 중장기적으로도 상승 추세가 지속될 가능성이 높습니다.
            </p>
          </div>
        </div>
        
        <div>
          <h3 className="text-2xl font-semibold text-gray-800 mb-4">3.2 주요 기술적 지표</h3>
          <div className="bg-white rounded-lg p-6 shadow-sm border border-gray-200">
            <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-6">
              <div className="flex flex-col">
                <div className="flex items-center">
                  <span className="inline-flex items-center justify-center h-8 w-8 rounded-full bg-green-100 text-green-800 mr-3">
                    <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 7h8m0 0v8m0-8l-8 8-4-4-6 6" />
                    </svg>
                  </span>
                  <span className="font-medium text-gray-900">지지선</span>
                </div>
                <div className="mt-2 ml-11">
                  <span className="text-2xl font-bold text-gray-900">$16.49</span>
                  <p className="mt-1 text-sm text-gray-500">주가가 하락할 때 반등이 일어날 가능성이 높은 가격대</p>
                </div>
              </div>
              
              <div className="flex flex-col">
                <div className="flex items-center">
                  <span className="inline-flex items-center justify-center h-8 w-8 rounded-full bg-red-100 text-red-800 mr-3">
                    <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 17h8m0 0v-8m0 8l-8-8-4 4-6-6" />
                    </svg>
                  </span>
                  <span className="font-medium text-gray-900">저항선</span>
                </div>
                <div className="mt-2 ml-11">
                  <span className="text-2xl font-bold text-gray-900">$124.62</span>
                  <p className="mt-1 text-sm text-gray-500">주가가 상승할 때 상승이 멈출 가능성이 높은 가격대</p>
                </div>
              </div>
              
              <div className="flex flex-col">
                <div className="flex items-center">
                  <span className="inline-flex items-center justify-center h-8 w-8 rounded-full bg-yellow-100 text-yellow-800 mr-3">
                    <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
                    </svg>
                  </span>
                  <span className="font-medium text-gray-900">손절매 수준</span>
                </div>
                <div className="mt-2 ml-11">
                  <span className="text-2xl font-bold text-gray-900">$93.15</span>
                  <p className="mt-1 text-sm text-gray-500">투자 손실을 제한하기 위한 권장 매도 가격</p>
                </div>
              </div>
            </div>
            
            <div className="bg-yellow-50 p-4 rounded-md border border-yellow-100">
              <p className="text-gray-700">
                현재 주가는 저항선($124.62)에 근접해 있어, 이 수준에서 단기적인 조정 가능성이 있습니다. 
                그러나 전체적인 추세는 여전히 강한 상승세를 유지하고 있습니다.
              </p>
            </div>
          </div>
        </div>
      </div>
    </section>
  );
};

export default TechnicalAnalysis;
