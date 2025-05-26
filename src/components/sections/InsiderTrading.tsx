import React from 'react';

const InsiderTrading: React.FC = () => {
  return (
    <section className="py-8 px-4 sm:px-6 lg:px-8 bg-gray-50">
      <div className="max-w-7xl mx-auto">
        <h2 className="text-3xl font-bold text-gray-900 mb-6">6. 내부자 거래 정보</h2>
        <div className="bg-white rounded-lg p-6 shadow-sm">
          <p className="text-gray-700 mb-6">
            회사 내부자들의 주식 거래 정보를 분석했습니다:
          </p>
          
          <div className="space-y-6">
            <div className="bg-white p-5 rounded-lg border border-gray-200">
              <div className="flex items-center mb-3">
                <div className="flex-shrink-0">
                  <div className="flex items-center justify-center h-10 w-10 rounded-full bg-purple-500 text-white">
                    <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" />
                    </svg>
                  </div>
                </div>
                <div className="ml-4">
                  <h3 className="text-lg font-medium text-gray-900">BUCKLEY JEFFREY JOHANSING</h3>
                  <p className="text-sm text-gray-500">임원 (Officer)</p>
                </div>
              </div>
              <div className="ml-14">
                <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                  <div>
                    <span className="text-sm text-gray-500">최근 거래:</span>
                    <p className="font-medium text-gray-900">매도 (Sale)</p>
                  </div>
                  <div>
                    <span className="text-sm text-gray-500">거래일:</span>
                    <p className="font-medium text-gray-900">2025-05-21</p>
                  </div>
                  <div>
                    <span className="text-sm text-gray-500">보유 수량:</span>
                    <p className="font-medium text-gray-900">34,280주</p>
                  </div>
                </div>
              </div>
            </div>
            
            <div className="bg-white p-5 rounded-lg border border-gray-200">
              <div className="flex items-center mb-3">
                <div className="flex-shrink-0">
                  <div className="flex items-center justify-center h-10 w-10 rounded-full bg-purple-500 text-white">
                    <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" />
                    </svg>
                  </div>
                </div>
                <div className="ml-4">
                  <h3 className="text-lg font-medium text-gray-900">COHEN STEPHEN ANDREW</h3>
                  <p className="text-sm text-gray-500">사장 (President)</p>
                </div>
              </div>
              <div className="ml-14">
                <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                  <div>
                    <span className="text-sm text-gray-500">최근 거래:</span>
                    <p className="font-medium text-gray-900">파생상품 행사/전환</p>
                  </div>
                  <div>
                    <span className="text-sm text-gray-500">거래일:</span>
                    <p className="font-medium text-gray-900">2025-05-21</p>
                  </div>
                  <div>
                    <span className="text-sm text-gray-500">보유 수량:</span>
                    <p className="font-medium text-gray-900">592주</p>
                  </div>
                </div>
              </div>
            </div>
            
            <div className="bg-white p-5 rounded-lg border border-gray-200">
              <div className="flex items-center mb-3">
                <div className="flex-shrink-0">
                  <div className="flex items-center justify-center h-10 w-10 rounded-full bg-purple-500 text-white">
                    <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" />
                    </svg>
                  </div>
                </div>
                <div className="ml-4">
                  <h3 className="text-lg font-medium text-gray-900">GLAZER DAVID ALAN</h3>
                  <p className="text-sm text-gray-500">최고재무책임자 (CFO)</p>
                </div>
              </div>
              <div className="ml-14">
                <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                  <div>
                    <span className="text-sm text-gray-500">최근 거래:</span>
                    <p className="font-medium text-gray-900">매도 (Sale)</p>
                  </div>
                  <div>
                    <span className="text-sm text-gray-500">거래일:</span>
                    <p className="font-medium text-gray-900">2025-05-21</p>
                  </div>
                  <div>
                    <span className="text-sm text-gray-500">보유 수량:</span>
                    <p className="font-medium text-gray-900">492,080주</p>
                  </div>
                </div>
              </div>
            </div>
          </div>
          
          <div className="mt-6 bg-yellow-50 p-4 rounded-md border border-yellow-100">
            <p className="text-gray-700">
              최근 내부자들의 거래 패턴을 보면, 주요 임원들이 주식을 매도하는 경향이 관찰됩니다. 
              이는 현재 주가 수준에서 일부 내부자들이 이익 실현을 선택하고 있음을 시사할 수 있습니다.
            </p>
          </div>
        </div>
      </div>
    </section>
  );
};

export default InsiderTrading;
