import React from 'react';

const CurrentStockSituation: React.FC = () => {
  return (
    <section className="py-8 px-4 sm:px-6 lg:px-8 bg-gray-50">
      <div className="max-w-7xl mx-auto">
        <h2 className="text-3xl font-bold text-gray-900 mb-6">2. 현재 주가 상황</h2>
        <div className="bg-white rounded-lg p-6 shadow-sm">
          <p className="text-gray-700 mb-4">
            팔란티어의 주가 데이터를 분석한 결과, 다음과 같은 주요 정보를 확인했습니다:
          </p>
          
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mb-6">
            <div className="bg-white p-4 rounded-md border border-gray-200">
              <h3 className="font-semibold text-gray-800 mb-3">현재 주가 정보</h3>
              <ul className="space-y-2">
                <li className="flex justify-between">
                  <span className="text-gray-600">현재 주가:</span>
                  <span className="font-medium text-gray-900">$123.31</span>
                </li>
                <li className="flex justify-between">
                  <span className="text-gray-600">전일 대비 변동:</span>
                  <span className="font-medium text-green-600">+$1.02 (+0.83%)</span>
                </li>
                <li className="flex justify-between">
                  <span className="text-gray-600">일일 최고가:</span>
                  <span className="font-medium text-gray-900">$125.54</span>
                </li>
                <li className="flex justify-between">
                  <span className="text-gray-600">일일 최저가:</span>
                  <span className="font-medium text-gray-900">$120.69</span>
                </li>
                <li className="flex justify-between">
                  <span className="text-gray-600">거래량:</span>
                  <span className="font-medium text-gray-900">65,437,595주</span>
                </li>
              </ul>
            </div>
            
            <div className="bg-white p-4 rounded-md border border-gray-200">
              <h3 className="font-semibold text-gray-800 mb-3">52주 최고가/최저가</h3>
              <ul className="space-y-2">
                <li className="flex justify-between">
                  <span className="text-gray-600">52주 최고가:</span>
                  <span className="font-medium text-gray-900">$133.49</span>
                </li>
                <li className="flex justify-between">
                  <span className="text-gray-600">52주 최저가:</span>
                  <span className="font-medium text-gray-900">$20.64</span>
                </li>
                <li className="flex justify-between">
                  <span className="text-gray-600">1년간 상승률:</span>
                  <span className="font-medium text-green-600">약 547%</span>
                </li>
                <li className="flex justify-between">
                  <span className="text-gray-600">전일 종가:</span>
                  <span className="font-medium text-gray-900">$20.72</span>
                </li>
              </ul>
            </div>
          </div>
          
          <div className="bg-blue-50 p-5 rounded-lg border border-blue-100">
            <h3 className="text-lg font-medium text-blue-800 mb-2">거래량 추이</h3>
            <ul className="space-y-2">
              <li className="flex justify-between">
                <span className="text-gray-600">최근 거래량:</span>
                <span className="font-medium text-gray-900">65,765,700주</span>
              </li>
              <li className="flex justify-between">
                <span className="text-gray-600">20일 평균 거래량:</span>
                <span className="font-medium text-gray-900">97,740,115주</span>
              </li>
              <li className="flex justify-between">
                <span className="text-gray-600">평균 대비 거래량 변화:</span>
                <span className="font-medium text-red-600">-32.71%</span>
              </li>
            </ul>
            <p className="mt-3 text-gray-700">
              최근 거래량은 20일 평균과 유사한 수준을 유지하고 있어, 시장 참여도는 안정적인 상태입니다.
            </p>
          </div>
        </div>
      </div>
    </section>
  );
};

export default CurrentStockSituation;
