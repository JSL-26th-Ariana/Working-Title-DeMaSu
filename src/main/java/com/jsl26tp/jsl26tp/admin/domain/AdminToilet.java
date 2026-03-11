package com.jsl26tp.jsl26tp.admin.domain;

import lombok.Data;
import java.math.BigDecimal;
import java.time.LocalDateTime;

/**
 * トイレ承認ドメイン (FR-SCR004-4)
 *
 * 용도: 관리자 페이지에서 사용자 제보 화장실 승인/반려 처리
 * 매핑: toilets 테이블 + users(제보자) LEFT JOIN
 *
 * 승인 대기 조건: source = 'USER' AND status = 'PENDING'
 * 공공데이터 조건: source = 'PUBLIC_API' AND status = 'APPROVED'
 *
 * ※ toilets 테이블은 deleted_at 있음 → 조회 시 deleted_at IS NULL 필수
 */
@Data
public class AdminToilet {
    private Long id;                    // 화장실 고유 ID (PK)
    private String name;                // 화장실 이름
    private String address;             // 주소
    private BigDecimal latitude;        // 위도 (DECIMAL(10,7))
    private BigDecimal longitude;       // 경도 (DECIMAL(10,7))
    private String openHours;           // 운영 시간 (DB: open_hours)
    private Boolean is24hours;          // 24시간 여부 (DB: is_24hours, TINYINT)
    private Boolean isWheelchair;       // 휠체어 이용 가능 (DB: is_wheelchair)
    private Boolean hasPaper;           // 화장지 비치 (DB: has_paper)
    private Boolean hasSoap;            // 비누 비치 (DB: has_soap)
    private Boolean hasSanitary;        // 생리대 자판기 (DB: has_sanitary)
    private Boolean hasDiaper;          // 기저귀 교환대 (DB: has_diaper)
    private String toiletType;          // 변기 종류 ("WESTERN" / "SQUAT") (DB: toilet_type)
    private Boolean hasEmergency;       // 비상벨 (DB: has_emergency)
    private String source;              // 등록 출처 ("PUBLIC_API" / "USER")
    private String status;              // 승인 상태 ("PENDING" / "APPROVED" / "REJECTED")
    private Long byUserId;              // 제보자 ID (FK → users.id) (DB: by_user_id)
    private String byUserNickname;      // 제보자 닉네임 (JOIN: users.nickname)
    private LocalDateTime createdAt;    // 등록일
}