package com.jsl26tp.jsl26tp.admin.domain;

import lombok.Data;
import java.time.LocalDate;
import java.time.LocalDateTime;

/**
 * 会員管理ドメイン (FR-SCR004-1, FR-SCR004-2)
 *
 * 용도: 관리자 페이지에서 회원 목록 조회 / 상세 조회 시 사용
 * 매핑: users 테이블 + reviews(리뷰수) + reports(신고받은수) 서브쿼리 JOIN
 *
 * ※ users 테이블은 deleted_at 없음 → status 필드로 소프트 삭제 관리
 */
@Data
public class AdminUser {
    private Long id;                    // 회원 고유 ID (PK)
    private String username;            // 아이디 (UNIQUE)
    private String nickname;            // 닉네임 (UNIQUE)
    private String email;               // 이메일 (UNIQUE)
    private String phone;               // 연락처 (선택)
    private String gender;              // 성별 (MALE / FEMALE / OTHER)
    private LocalDate birthdate;        // 생년월일 (선택)
    private String iconUrl;             // 프로필 이미지 경로 (DB: icon_url)
    private String role;                // 권한 ("ROLE_USER" / "ROLE_ADMIN")
    private String socialType;          // 소셜 로그인 구분 ("LOCAL" / "GOOGLE")
    private String status;              // 계정 상태 ("ACTIVE" / "SUSPENDED" / "DELETED")
    private LocalDateTime suspendUntil; // 정지 해제 일시 (null이면 영구정지 or 미정지)
    private LocalDateTime createdAt;    // 가입일
    private int reviewCount;            // 작성 리뷰 수 (SQL 서브쿼리로 JOIN)
    private int reportCount;            // 신고 받은 수 (SQL 서브쿼리로 JOIN)
}