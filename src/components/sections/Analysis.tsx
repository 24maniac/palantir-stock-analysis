import React from 'react';

const Analysis: React.FC = () => {
  return (
    <section className="py-8 px-4 sm:px-6 lg:px-8 bg-white">
      <div className="max-w-7xl mx-auto">
        <h2 className="text-3xl font-bold text-gray-900 mb-6">7. 종합 분석 및 결론</h2>
        
        <div className="mb-8">
          <h3 className="text-2xl font-semibold text-gray-800 mb-4">7.1 주가 추세</h3>
          <div className="bg-white rounded-lg p-6 shadow-sm border border-gray-200">
            <div className="flex items-center mb-4">
              <div className="h-10 w-2 bg-green-500 rounded-full mr-3"></div>
              <h4 className="text-xl font-medium text-gray-900">강한 상승 추세</h4>
            </div>
            <p className="text-gray-700">
              팔란티어의 주가는 현재 <span className="font-bold text-green-600">강한 상승</span> 추세를 보이고 있습니다. 
              최근 종가($123.31)가 20일 이동평균선($121.08) 위에 위치하고 있어 단기적으로 상승 모멘텀이 유지되고 있습니다. 
              또한 모든 주요 이동평균선(20일, 50일, 200일)이 상승 배열을 형성하고 있어, 중장기적으로도 상승 추세가 지속될 가능성이 높습니다.
            </p>
          </div>
        </div>
        
        <div className="mb-8">
          <h3 className="text-2xl font-semibold text-gray-800 mb-4">7.2 거래량 분석</h3>
          <div className="bg-white rounded-lg p-6 shadow-sm border border-gray-200">
            <p className="text-gray-700">
              최근 거래량(65,765,700주)은 20일 평균 거래량(97,740,115주)과 유사한 수준을 유지하고 있어, 
              시장 참여도는 안정적인 상태입니다. 이는 현재의 주가 움직임이 충분한 시장 참여 하에 이루어지고 있음을 의미하며, 
              추세의 신뢰성을 뒷받침합니다.
            </p>
            <div className="mt-4 flex items-center">
              <div className="w-full bg-gray-200 rounded-full h-2.5">
                <div className="bg-blue-600 h-2.5 rounded-full" style={{ width: '67%' }}></div>
              </div>
              <span className="ml-3 text-sm font-medium text-gray-700">67% 수준</span>
            </div>
          </div>
        </div>
        
        <div className="mb-8">
          <h3 className="text-2xl font-semibold text-gray-800 mb-4">7.3 투자 의견</h3>
          <div className="bg-white rounded-lg p-6 shadow-sm border border-gray-200">
            <p className="text-gray-700">
              투자 분석가들은 팔란티어에 대해 <span className="font-bold">중립</span> 의견을 제시하고 있습니다. 
              이는 현재 주가가 이미 상당한 상승을 기록한 상태에서, 추가 상승 여력과 하락 위험이 균형을 이루고 있다는 
              판단으로 해석됩니다.
            </p>
            <p className="mt-4 text-gray-700">
              기술적 분석 관점에서는 강한 상승 추세가 유지되고 있으나, 현재 주가가 저항선($124.62)에 근접해 있어 
              단기적인 조정 가능성도 존재합니다. 투자자들은 손절매 수준($93.15)을 참고하여 리스크 관리를 할 필요가 있습니다.
            </p>
          </div>
        </div>
        
        <div>
          <h3 className="text-2xl font-semibold text-gray-800 mb-4">7.4 주의사항</h3>
          <div className="bg-yellow-50 rounded-lg p-6 shadow-sm border border-yellow-200">
            <div className="flex">
              <div className="flex-shrink-0">
                <svg className="h-6 w-6 text-yellow-600" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
                </svg>
              </div>
              <div className="ml-3">
                <h3 className="text-lg font-medium text-yellow-800">투자 주의사항</h3>
                <div className="mt-2 text-yellow-700">
                  <p>
                    본 보고서는 정보 제공 목적으로만 작성되었으며, 투자 권유를 위한 것이 아닙니다. 
                    투자 결정은 개인의 책임하에 이루어져야 하며, 본 보고서의 정보만으로 투자 결정을 내리지 마십시오. 
                    항상 다양한 정보 소스를 참고하고, 필요시 전문가의 조언을 구하시기 바랍니다.
                  </p>
                  <p className="mt-2">
                    특히 팔란티어 주식은 최근 1년간 약 547%의 급격한 상승을 기록했으므로, 투자 시 높은 변동성에 대비해야 합니다.
                  </p>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>
  );
};

export default Analysis;
