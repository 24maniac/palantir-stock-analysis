import React from 'react';

const DataSource: React.FC = () => {
  return (
    <section className="py-8 px-4 sm:px-6 lg:px-8 bg-gray-50">
      <div className="max-w-7xl mx-auto">
        <h2 className="text-3xl font-bold text-gray-900 mb-6">8. 데이터 출처 및 분석 방법론</h2>
        <div className="bg-white rounded-lg p-6 shadow-sm">
          <ul className="space-y-4">
            <li className="flex items-start">
              <div className="flex-shrink-0">
                <svg className="h-6 w-6 text-green-500" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
                </svg>
              </div>
              <p className="ml-3 text-gray-700">
                <span className="font-medium text-gray-900">데이터 출처:</span> Yahoo Finance API
              </p>
            </li>
            <li className="flex items-start">
              <div className="flex-shrink-0">
                <svg className="h-6 w-6 text-green-500" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
                </svg>
              </div>
              <p className="ml-3 text-gray-700">
                <span className="font-medium text-gray-900">분석 기간:</span> 최근 1년 (2024년 5월 ~ 2025년 5월)
              </p>
            </li>
            <li className="flex items-start">
              <div className="flex-shrink-0">
                <svg className="h-6 w-6 text-green-500" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
                </svg>
              </div>
              <p className="ml-3 text-gray-700">
                <span className="font-medium text-gray-900">분석 방법:</span> 기술적 분석(이동평균선, 거래량 분석), 전문가 의견 종합
              </p>
            </li>
            <li className="flex items-start">
              <div className="flex-shrink-0">
                <svg className="h-6 w-6 text-green-500" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
                </svg>
              </div>
              <p className="ml-3 text-gray-700">
                <span className="font-medium text-gray-900">분석 일자:</span> 2025년 5월 25일
              </p>
            </li>
          </ul>
          
          <div className="mt-6 bg-blue-50 p-4 rounded-md border border-blue-100">
            <h3 className="font-medium text-blue-800 mb-2">분석 데이터 신뢰성</h3>
            <p className="text-gray-700">
              본 분석에 사용된 데이터는 Yahoo Finance API를 통해 수집된 공개 정보를 기반으로 합니다. 
              이동평균선, 거래량, 기술적 지표 등은 수집된 주가 데이터를 기반으로 계산되었으며, 
              투자 추천 및 목표가는 전문 분석가들의 의견을 종합한 것입니다.
            </p>
          </div>
        </div>
      </div>
    </section>
  );
};

export default DataSource;
