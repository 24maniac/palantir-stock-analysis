import React from 'react';

const Footer: React.FC = () => {
  return (
    <footer className="bg-gray-800 text-white py-8 px-4 sm:px-6 lg:px-8">
      <div className="max-w-7xl mx-auto">
        <div className="flex flex-col md:flex-row justify-between items-center">
          <div className="mb-4 md:mb-0">
            <h3 className="text-xl font-bold">팔란티어(PLTR) 주가 분석</h3>
            <p className="text-gray-300 mt-1">© 2025 주가 분석 보고서</p>
          </div>
          <div className="flex flex-col md:flex-row md:space-x-6 space-y-2 md:space-y-0">
            <a href="#" className="text-gray-300 hover:text-white transition-colors">
              데이터 출처
            </a>
            <a href="#" className="text-gray-300 hover:text-white transition-colors">
              면책 조항
            </a>
            <a href="#" className="text-gray-300 hover:text-white transition-colors">
              연락처
            </a>
          </div>
        </div>
        <div className="mt-8 border-t border-gray-700 pt-4 text-sm text-gray-400 text-center">
          이 웹사이트는 정보 제공 목적으로만 제작되었으며, 투자 권유를 위한 것이 아닙니다.
        </div>
      </div>
    </footer>
  );
};

export default Footer;
