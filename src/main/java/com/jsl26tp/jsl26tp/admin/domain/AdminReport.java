package com.jsl26tp.jsl26tp.admin.domain;

import lombok.Data;
import java.time.LocalDateTime;
import java.util.List;

/**
 * 申告管理ドメイン (FR-SCR004-3)
 *
 * 용도: 관리자 페이지에서 신고 목록 / 상세 조회 시 사용
 * 매핑: reports 테이블 + users(신고자) + reviews or toilets(대상) JOIN
 *
 * target_type에 따라 대상 정보가 달라짐:
 *   - "REVIEW" → targetName = 리뷰 내용 앞 50자, targetWriter = 리뷰 작성자
 *   - "TOILET" → targetName = 화장실 이름, targetWriter = null
 *
 * ※ reports 테이블은 deleted_at 없음
 * ※ DB 설계서 기준 status 값: PENDING / PROCESSED / DISMISSED
 */
@Data
public class AdminReport {
    private Long id;                    // 신고 고유 ID (PK)
    private Long reporterId;            // 신고자 ID (FK → users.id)
    private String reporterNickname;    // 신고자 닉네임 (JOIN: users.nickname)
    private String targetType;          // 신고 대상 타입 ("REVIEW" / "TOILET")
    private Long targetId;              // 신고 대상 ID (review.id or toilet.id)
    private String targetName;          // 대상 요약 (JOIN: 리뷰내용 앞 50자 or 화장실이름)
    private String targetFullContent;   // 리뷰 전체 내용 (REVIEW인 경우만, 상세 페이지용)
    private List<String> targetImageUrls; // 리뷰 이미지 URL 목록 (REVIEW인 경우만, 상세 페이지용)
    private String targetWriter;        // 대상 작성자 닉네임 (JOIN: REVIEW인 경우만)
    private String reason;              // 신고 사유
    private String status;              // 처리 상태 ("PENDING" / "PROCESSED" / "DISMISSED")
    private String adminNote;           // 관리자 처리 메모
    private LocalDateTime createdAt;    // 신고일
    private LocalDateTime processedAt;  // 처리일
}