package com.jsl26tp.jsl26tp.admin.domain;

import lombok.Data;
import java.math.BigDecimal;

/**
 * 수정 제안 승인 시 화장실 정보 수정 요청 DTO
 *
 * 용도: PUT /api/admin/toilets/{id} 요청 바디
 * - 관리자가 수정 제안 상세 페이지에서 직접 편집한 값을 담아서 전송
 * - AdminMapper.updateToilet()에 전달되어 toilets 테이블 UPDATE
 *
 * ※ Boolean 필드는 null 허용 (체크박스 미전송 시 false로 처리)
 */
@Data
public class ToiletUpdateRequest {

    private String name;            // 화장실 이름 (DB: name)
    private String address;         // 주소 (DB: address)
    private BigDecimal latitude;    // 위도 (DB: latitude, DECIMAL(10,7))
    private BigDecimal longitude;   // 경도 (DB: longitude, DECIMAL(10,7))
    private String openHours;       // 운영 시간 (DB: open_hours)
    private Boolean is24hours;      // 24시간 여부 (DB: is_24hours)
    private String toiletType;      // 변기 종류 WESTERN/SQUAT (DB: toilet_type)
    private Boolean isWheelchair;   // 휠체어 이용 가능 (DB: is_wheelchair)
    private Boolean hasPaper;       // 화장지 비치 (DB: has_paper)
    private Boolean hasSoap;        // 비누 비치 (DB: has_soap)
    private Boolean hasSanitary;    // 생리대 자판기 (DB: has_sanitary)
    private Boolean hasDiaper;      // 기저귀 교환대 (DB: has_diaper)
    private Boolean hasEmergency;   // 비상벨 (DB: has_emergency)
}
