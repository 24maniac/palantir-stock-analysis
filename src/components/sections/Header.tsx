import React from 'react';

const Header: React.FC = () => {
  return (
    <header className="bg-gradient-to-r from-blue-900 to-indigo-800 text-white py-12 px-4 sm:px-6 lg:px-8">
      <div className="max-w-7xl mx-auto">
        <h1 className="text-4xl font-bold tracking-tight sm:text-5xl md:text-6xl">
          팔란티어(PLTR) 주가 분석 보고서
        </h1>
        <p className="mt-3 text-xl">
          최신 데이터 기반 종합 주가 분석 및 투자 인사이트
        </p>
        <div className="mt-4 flex flex-wrap items-center gap-2">
          <span className="bg-blue-800 px-3 py-1 rounded-full text-sm font-medium">
            현재 주가: $123.31
          </span>
          <span className="bg-green-700 px-3 py-1 rounded-full text-sm font-medium">
            전일 대비: +$1.02 (+0.83%)
          </span>
          <span className="bg-blue-800 px-3 py-1 rounded-full text-sm font-medium">
            분석 일자: 2025년 5월 25일
          </span>
        </div>
      </div>
    </header>
  );
};

export default Header;
