package com.jsl26tp.jsl26tp.admin.service;

import com.jsl26tp.jsl26tp.common.BusinessException;
import com.jsl26tp.jsl26tp.common.ErrorCode;
import com.jsl26tp.jsl26tp.admin.domain.*;
import com.jsl26tp.jsl26tp.admin.mapper.AdminMapper;
import com.jsl26tp.jsl26tp.toilet.domain.ToiletEditRequest;
import com.jsl26tp.jsl26tp.toilet.mapper.ToiletEditRequestMapper;
import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.time.LocalDateTime;
import java.util.List;

/**
 * 管理者 Service
 *
 * 관리자 페이지의 모든 비즈니스 로직 처리
 * - 예외는 BusinessException으로 던짐 → GlobalExceptionHandler가 ApiResponse.error()로 변환
 * - Mapper 호출은 Service에서만 (Controller에서 Mapper 직접 호출 금지)
 * - 상태 변경 메서드는 @Transactional 적용 (실패 시 롤백)
 */
@Service
@RequiredArgsConstructor
public class AdminService {

    private final AdminMapper adminMapper;

    // ToiletEditRequestMapper: 다른 팀원 파일 수정 없이 주입만 해서 사용
    private final ToiletEditRequestMapper editRequestMapper;


    /** 페이지당 표시 건수 (모든 목록 공통) */
    private static final int PAGE_SIZE = 10;

    // =====================================================================
    // 1. 회원 관리 (FR-SCR004-1: 회원 정지, FR-SCR004-2: 계정 삭제)
    // =====================================================================

    /**
     * 회원 목록 조회 (페이징)
     * @param keyword 검색어 (username/nickname/email LIKE)
     * @param status  상태 필터 (ACTIVE/SUSPENDED/DELETED, 빈 문자열이면 전체)
     * @param page    현재 페이지 번호 (0-based)
     * @return AdminPageResponse — dashboard.html JS 필드명(content, number)에 맞춘 admin 전용 응답
     */
    public AdminPageResponse<AdminUser> getUserList(String keyword, String status, int page) {
        int offset = page * PAGE_SIZE;
        List<AdminUser> items = adminMapper.findUserList(keyword, status, offset, PAGE_SIZE);
        int totalCount = adminMapper.countUsers(keyword, status);
        int totalPages = (int) Math.ceil((double) totalCount / PAGE_SIZE);
        // AdminPageResponse: content(=items), number(=page), totalPages → HTML의 res.data.* 와 일치
        return new AdminPageResponse<>(items, page, PAGE_SIZE, totalCount, totalPages);
    }

    /**
     * 회원 상세 조회
     * @throws BusinessException USER_NOT_FOUND — 회원이 존재하지 않을 때
     */
    public AdminUser getUserById(Long id) {
        AdminUser user = adminMapper.findUserById(id);
        if (user == null) {
            throw new BusinessException(ErrorCode.USER_NOT_FOUND);
        }
        return user;
    }

    /**
     * 회원 정지 (FR-SCR004-1)
     * @param id   대상 회원 ID
     * @param days 정지 일수 (0이면 영구 정지, 양수면 기간 정지)
     * @throws BusinessException ACCESS_DENIED — 관리자 계정 정지 시도 시
     */
    @Transactional
    public void suspendUser(Long id, int days) {
        AdminUser user = getUserById(id);

        // 관리자 계정은 정지 불가
        if ("ROLE_ADMIN".equals(user.getRole())) {
            throw new BusinessException(ErrorCode.ACCESS_DENIED);
        }

        // days=0 → 영구 정지 (suspendUntil=null), days>0 → 기간 정지
        String suspendUntil = (days > 0)
                ? LocalDateTime.now().plusDays(days).toString()
                : null;

        adminMapper.updateUserStatus(id, "SUSPENDED", suspendUntil);
    }

    /**
     * 회원 정지 해제
     * → status="ACTIVE", suspend_until=NULL
     */
    @Transactional
    public void unsuspendUser(Long id) {
        getUserById(id); // 존재 확인 (없으면 USER_NOT_FOUND)
        adminMapper.updateUserStatus(id, "ACTIVE", null);
    }

    /**
     * 회원 삭제 (FR-SCR004-2)
     * ※ users 테이블은 deleted_at 없음 → status="DELETED"로 소프트 삭제
     */
    @Transactional
    public void deleteUser(Long id) {
        getUserById(id); // 존재 확인
        adminMapper.updateUserStatus(id, "DELETED", null);
    }

    // =====================================================================
    // 2. 신고 관리 (FR-SCR004-3)
    // =====================================================================

    /** 신고 목록 조회 (페이징) */
    public AdminPageResponse<AdminReport> getReportList(String status, String targetType, int page) {
        int offset = page * PAGE_SIZE;
        List<AdminReport> items = adminMapper.findReportList(status, targetType, offset, PAGE_SIZE);
        int totalCount = adminMapper.countReports(status, targetType);
        int totalPages = (int) Math.ceil((double) totalCount / PAGE_SIZE);
        return new AdminPageResponse<>(items, page, PAGE_SIZE, totalCount, totalPages);
    }

    /**
     * 신고 상세 조회
     * @throws BusinessException BAD_REQUEST — 신고가 존재하지 않을 때
     */
    public AdminReport getReportById(Long id) {
        AdminReport report = adminMapper.findReportById(id);
        if (report == null) {
            throw new BusinessException(ErrorCode.BAD_REQUEST);
        }
        // REVIEW 타입이면 review_images 테이블에서 이미지 URL 목록 조회
        if ("REVIEW".equals(report.getTargetType()) && report.getTargetId() != null) {
            List<String> imageUrls = adminMapper.findReviewImageUrls(report.getTargetId());
            report.setTargetImageUrls(imageUrls);
        }
        return report;
    }

    /**
     * 신고 승인 — 대상 콘텐츠에 조치 후 PROCESSED 처리
     *
     * 처리 흐름:
     * 1. 신고 조회 → PENDING 상태인지 확인
     * 2. target_type에 따라 대상 조치:
     *    - "REVIEW" → reviews.status = "HIDDEN" (비표시)
     *    - "TOILET" → toilets.status = "REJECTED" (반려)
     * 3. reports.status = "PROCESSED", processed_at = NOW()
     *
     * @Transactional: 대상 조치 + 신고 상태 변경을 하나의 트랜잭션으로 (실패 시 전체 롤백)
     */
    @Transactional
    public void resolveReport(Long id, String adminNote) {
        AdminReport report = getReportById(id);

        // 이미 처리된 신고는 재처리 불가
        if (!"PENDING".equals(report.getStatus())) {
            throw new BusinessException(ErrorCode.BAD_REQUEST);
        }

        // 대상 콘텐츠에 조치
        if ("REVIEW".equals(report.getTargetType())) {
            adminMapper.hideReview(report.getTargetId());        // 리뷰 비표시
        } else if ("TOILET".equals(report.getTargetType())) {
            adminMapper.rejectToiletByReport(report.getTargetId()); // 화장실 반려
        }

        // 신고를 PROCESSED로 변경 (DB 설계서 기준)
        adminMapper.updateReportStatus(id, "PROCESSED", adminNote);
    }

    /**
     * 신고 기각 — 대상 콘텐츠는 변경하지 않고 DISMISSED 처리
     */
    @Transactional
    public void dismissReport(Long id, String adminNote) {
        AdminReport report = getReportById(id);

        if (!"PENDING".equals(report.getStatus())) {
            throw new BusinessException(ErrorCode.BAD_REQUEST);
        }

        // 대상 콘텐츠 변경 없이 신고만 기각
        adminMapper.updateReportStatus(id, "DISMISSED", adminNote);
    }

    // =====================================================================
    // 3. 화장실 승인 (FR-SCR004-4)
    // =====================================================================

    /** 화장실 목록 조회 (페이징) */
    public AdminPageResponse<AdminToilet> getToiletList(String status, int page) {
        int offset = page * PAGE_SIZE;
        List<AdminToilet> items = adminMapper.findToiletList(status, offset, PAGE_SIZE);
        int totalCount = adminMapper.countToilets(status);
        int totalPages = (int) Math.ceil((double) totalCount / PAGE_SIZE);
        return new AdminPageResponse<>(items, page, PAGE_SIZE, totalCount, totalPages);
    }

    /**
     * 화장실 상세 조회
     * @throws BusinessException TOILET_NOT_FOUND — 화장실이 존재하지 않을 때
     */
    public AdminToilet getToiletById(Long id) {
        AdminToilet toilet = adminMapper.findToiletById(id);
        if (toilet == null) {
            throw new BusinessException(ErrorCode.TOILET_NOT_FOUND);
        }
        return toilet;
    }

    /**
     * 화장실 승인 (PENDING → APPROVED)
     * - SQL에 AND status='PENDING' 조건이 있어서 이미 처리된 건은 영향행 0
     * - 영향행 0이면 BAD_REQUEST 예외
     */
    @Transactional
    public void approveToilet(Long id) {
        if (adminMapper.approveToilet(id) == 0) {
            throw new BusinessException(ErrorCode.BAD_REQUEST);
        }
    }

    /**
     * 화장실 반려 (PENDING → REJECTED)
     */
    @Transactional
    public void rejectToilet(Long id) {
        if (adminMapper.rejectToilet(id) == 0) {
            throw new BusinessException(ErrorCode.BAD_REQUEST);
        }
    }

    // =====================================================================
    // 4. 문의 관리 (FR-SCR004-5)
    // =====================================================================

    /** 문의 목록 조회 (페이징) */
    public AdminPageResponse<AdminInquiry> getInquiryList(String status, String keyword, int page) {
        int offset = page * PAGE_SIZE;
        List<AdminInquiry> items = adminMapper.findInquiryList(status, keyword, offset, PAGE_SIZE);
        int totalCount = adminMapper.countInquiries(status, keyword);
        int totalPages = (int) Math.ceil((double) totalCount / PAGE_SIZE);
        return new AdminPageResponse<>(items, page, PAGE_SIZE, totalCount, totalPages);
    }

    /**
     * 문의 상세 조회
     * @throws BusinessException BAD_REQUEST — 문의가 존재하지 않을 때
     */
    public AdminInquiry getInquiryById(Long id) {
        AdminInquiry inquiry = adminMapper.findInquiryById(id);
        if (inquiry == null) {
            throw new BusinessException(ErrorCode.BAD_REQUEST);
        }
        return inquiry;
    }

    /**
     * 문의 답변 등록
     * → SET answer=답변, admin_id=관리자ID, status="ANSWERED", answered_at=NOW()
     */
    @Transactional
    public void answerInquiry(Long id, String answer, Long adminId) {
        getInquiryById(id); // 존재 확인
        adminMapper.answerInquiry(id, answer, adminId);
    }

    /**
     * 화장실 정보 수정 (수정 제안 승인 시 관리자가 직접 편집한 값 저장)
     *
     * 처리 흐름:
     * 1. 화장실 존재 확인 (없으면 TOILET_NOT_FOUND)
     * 2. toilets 테이블 UPDATE (name, address, 좌표, 운영시간, 설비 등)
     * 3. 영향행 0이면 이미 삭제된 화장실 → BAD_REQUEST
     *
     * @param id  수정 대상 화장실 ID
     * @param req 관리자가 편집한 수정 내용 DTO
     */
    @Transactional
    public void updateToilet(Long id, ToiletUpdateRequest req) {
        getToiletById(id); // 존재 확인 (없으면 TOILET_NOT_FOUND)
        if (adminMapper.updateToilet(id, req) == 0) {
            throw new BusinessException(ErrorCode.BAD_REQUEST);
        }
    }

    // =====================================================================
    // 5. 수정 제안 관리
    // ToiletEditRequestMapper를 주입해서 사용 (해당 파일 수정 없음)
    // =====================================================================

    /**
     * 수정 제안 목록 조회 (페이징 + 상태 필터)
     * - ToiletEditRequestMapper.findAllRequests() 전체 목록을 가져온 뒤 페이징 처리
     * - status가 비어있으면 전체, 값이 있으면 해당 상태만 필터링
     *
     * @param status 필터 상태 (PENDING/APPROVED/REJECTED/빈 문자열=전체)
     * @param page   현재 페이지 번호 (0-based)
     * @return AdminPageResponse — content/number/totalPages 필드로 dashboard.html JS와 매핑
     */
    public AdminPageResponse<ToiletEditRequest> getEditRequestList(String status, int page) {
        // 전체 목록 조회 후 상태 필터링
        List<ToiletEditRequest> all = editRequestMapper.findAllRequests();

        // status가 비어있지 않으면 해당 상태만 필터링
        if (status != null && !status.isBlank()) {
            all = all.stream()
                    .filter(r -> status.equals(r.getStatus()))
                    .collect(java.util.stream.Collectors.toList());
        }

        int totalCount = all.size();
        int totalPages = (int) Math.ceil((double) totalCount / PAGE_SIZE);

        // 페이지에 해당하는 범위만 잘라서 반환
        int from = page * PAGE_SIZE;
        int to = Math.min(from + PAGE_SIZE, totalCount);
        List<ToiletEditRequest> content = (from >= totalCount)
                ? List.of()
                : all.subList(from, to);

        return new AdminPageResponse<>(content, page, PAGE_SIZE, totalCount, totalPages);
    }

    /**
     * 수정 제안 상세 조회
     * @throws BusinessException BAD_REQUEST — 존재하지 않는 수정 제안 ID
     */
    public ToiletEditRequest getEditRequestById(Long id) {
        ToiletEditRequest req = editRequestMapper.findById(id);
        if (req == null) {
            throw new BusinessException(ErrorCode.BAD_REQUEST);
        }
        return req;
    }

    /**
     * 수정 제안 승인 (PENDING → APPROVED)
     * - 수정 제안 상태만 변경 (화장실 데이터 자동 반영 없음 — 관리자가 직접 확인 후 처리)
     */
    @Transactional
    public void approveEditRequest(Long id) {
        getEditRequestById(id); // 존재 확인
        editRequestMapper.updateStatus(id, "APPROVED");
    }

    /**
     * 수정 제안 거절 (PENDING → REJECTED)
     */
    @Transactional
    public void rejectEditRequest(Long id) {
        getEditRequestById(id); // 존재 확인
        editRequestMapper.updateStatus(id, "REJECTED");
    }

    // =====================================================================
    // 6. 화장실 강제 삭제 (관리자 전용)
    // =====================================================================

    /**
     * 화장실 소프트 삭제
     * → toilets.deleted_at = NOW()
     * - 이후 deleted_at IS NULL 조건이 붙는 모든 조회(지도, 목록 등)에서 자동 제외
     *
     * @throws BusinessException BAD_REQUEST — 이미 삭제됐거나 존재하지 않는 화장실
     */
    @Transactional
    public void deleteToilet(Long id) {
        if (adminMapper.deleteToilet(id) == 0) {
            throw new BusinessException(ErrorCode.BAD_REQUEST);
        }
    }
}