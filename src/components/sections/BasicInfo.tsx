import React from 'react';

const BasicInfo: React.FC = () => {
  return (
    <section className="py-8 px-4 sm:px-6 lg:px-8 bg-white">
      <div className="max-w-7xl mx-auto">
        <h2 className="text-3xl font-bold text-gray-900 mb-6">1. 기본 정보</h2>
        <div className="bg-gray-50 rounded-lg p-6 shadow-sm">
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div className="flex items-start">
              <span className="font-semibold text-gray-700 w-32">회사명:</span>
              <span className="text-gray-900">팔란티어 테크놀로지스(Palantir Technologies Inc.)</span>
            </div>
            <div className="flex items-start">
              <span className="font-semibold text-gray-700 w-32">종목 코드:</span>
              <span className="text-gray-900">PLTR</span>
            </div>
            <div className="flex items-start">
              <span className="font-semibold text-gray-700 w-32">거래소:</span>
              <span className="text-gray-900">NasdaqGS</span>
            </div>
            <div className="flex items-start">
              <span className="font-semibold text-gray-700 w-32">통화:</span>
              <span className="text-gray-900">USD</span>
            </div>
            <div className="flex items-start">
              <span className="font-semibold text-gray-700 w-32">분석 일자:</span>
              <span className="text-gray-900">2025년 5월 25일</span>
            </div>
            <div className="flex items-start">
              <span className="font-semibold text-gray-700 w-32">데이터 출처:</span>
              <span className="text-gray-900">Yahoo Finance</span>
            </div>
          </div>
        </div>
      </div>
    </section>
  );
};

export default BasicInfo;
