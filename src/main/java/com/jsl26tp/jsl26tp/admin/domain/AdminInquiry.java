package com.jsl26tp.jsl26tp.admin.domain;

import lombok.Data;
import java.time.LocalDateTime;

/**
 * お問い合わせ管理ドメイン (FR-SCR004-5)
 *
 * 용도: 관리자 페이지에서 문의 목록 / 상세 / 답변 등록 시 사용
 * 매핑: inquiries 테이블 + users(작성자) + users(답변 관리자) JOIN
 *
 * 처리 흐름:
 *   1. 사용자가 문의 작성 → status = "WAITING", admin_id = null
 *   2. 관리자가 답변 등록 → status = "ANSWERED", admin_id = 관리자ID, answered_at = NOW()
 *
 * ※ inquiries 테이블은 deleted_at 있음 → 조회 시 deleted_at IS NULL 필수
 */
@Data
public class AdminInquiry {
    private Long id;                    // 문의 고유 ID (PK)
    private Long writerId;              // 작성자 ID (FK → users.id) (DB: writer_id)
    private String writerNickname;      // 작성자 닉네임 (JOIN: users.nickname)
    private String writerEmail;         // 작성자 이메일 (JOIN: users.email)
    private Long adminId;               // 답변 관리자 ID (FK → users.id, NULL 허용) (DB: admin_id)
    private String adminNickname;       // 답변 관리자 닉네임 (JOIN: users.nickname)
    private String title;               // 문의 제목
    private String content;             // 문의 내용
    private String status;              // 처리 상태 ("WAITING" / "ANSWERED")
    private String answer;              // 관리자 답변 (미답변 시 null)
    private LocalDateTime answeredAt;   // 답변 일시 (미답변 시 null)
    private LocalDateTime createdAt;    // 문의 등록일
}